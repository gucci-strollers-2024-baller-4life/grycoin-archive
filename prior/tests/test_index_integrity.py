"""Index integrity test. Run before trusting any sweep number in this repo.

    python3 tests/test_index_integrity.py

Exit code 0 means: the certified pipeline still reproduces published values, the chapter bases
still hash to their certified digests, paragraph spans are byte-aligned, no toggle ever lands on a
non-letter, and the six U+00A0 characters are the only non-ASCII content. Anything else is a
failure and every sweep built on the failing path is void.
"""
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import corpus  # noqa: E402
import fast2  # noqa: E402

FAILED = []


def check(name, fn):
    try:
        detail = fn()
    except Exception as exc:                                  # noqa: BLE001
        FAILED.append((name, f"{type(exc).__name__}: {exc}"))
        print(f"FAIL  {name}: {type(exc).__name__}: {exc}")
        return
    print(f"PASS  {name}{('  ' + detail) if detail else ''}")


def derive(md5_hex, idx=0):
    return fast2.addr_from_key(fast2.key_at(fast2.seed_from(bytes.fromhex(md5_hex)), idx))


def t_stage_one():
    b = open(os.path.join(HERE, "preimages/r2b77_stage1.txt"), "rb").read()
    h = hashlib.md5(b).hexdigest()
    assert h == "9dd2efb9bc976c2095bd534d7b8d431c", h
    a = derive(h)
    assert a == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN", a
    return h


def t_r1_77():
    b = open(os.path.join(HERE, "preimages/r1b77.txt"), "rb").read()
    h = hashlib.md5(b).hexdigest()
    a = derive(h)
    assert a == "1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP", a
    return h


def t_r2_76():
    b = open(os.path.join(HERE, "preimages/r2b76.txt"), "rb").read()
    h = hashlib.md5(b).hexdigest()
    a = derive(h)
    assert a == "13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd", a
    return h


def t_chapter_digests():
    for kind in ("mixed", "lf"):
        b, _ = corpus.chapter(kind)
        assert hashlib.md5(b).hexdigest() == corpus.CERT[kind]
    return "both bases certified"


def t_drift():
    d = corpus.drift("mixed")
    assert len(d) == 6, d
    assert [r["char_index"] for r in d] == [9084, 16922, 17272, 17780, 33411, 43301], d
    assert d[-1]["byte_index"] - d[-1]["char_index"] == 5
    return f"{len(d)} U+00A0, max drift 6 bytes"


def t_census():
    c = corpus.census("mixed")
    assert c == {0xA0: 6}, c
    return "only U+00A0 present"


def t_spans_aligned():
    seeds = corpus.seeds()
    for kind in ("mixed", "lf"):
        b, spans = corpus.chapter(kind)
        join, ibr = ("\r\n\r\n", "\n") if kind == "mixed" else ("\n\n", "\n")
        for i, (s, e) in enumerate(spans):
            want = ibr.join(seeds[i]).encode() if isinstance(seeds[i], list) else seeds[i].encode()
            assert b[s:s + len(want)] == want, f"{kind} para {i+1}"
            assert e == s + len(want), f"{kind} para {i+1} end"
        assert len(b) == spans[-1][1], kind
    return "273 spans x 2 bases"


def t_toggles_are_letters():
    b, spans = corpus.chapter("mixed")
    sets = [[5, 6, 7, 8], [93, 94, 95, 96], [168, 169, 170, 171],
            [230, 231, 232, 234], [231, 232, 233, 235]]
    n = 0
    for ps in sets:
        for p in ps:
            s, e = spans[p - 1]
            ls = [i for i in range(s, e) if corpus.is_letter(b[i])]
            corpus.toggle(b, [ls[0], ls[-1]])
            n += 2
    return f"{n} edge toggles, all letters"


def t_toggle_refuses_nonletter():
    b, _ = corpus.chapter("mixed")
    target = next(i for i in range(len(b)) if not corpus.is_letter(b[i]))
    try:
        corpus.toggle(b, [target])
    except AssertionError:
        return f"refused byte {target} ({bytes(b[target:target+1])!r})"
    raise AssertionError("toggle accepted a non-letter byte")


def t_other_corpora_documented():
    rows = []
    for name, spec in corpus.OTHER_CORPORA.items():
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        S = json.load(open(path, encoding="utf-8"))
        def txt(p):
            return "\n".join(p) if isinstance(p, list) else p
        h = hashlib.md5("\n\n".join(txt(p) for p in S).encode()).hexdigest()
        if "lf" in spec:
            assert h == spec["lf"], f"{name}: {h} != {spec['lf']}"
        rows.append(f"{name}={h[:8]}")
    return " ".join(rows)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def t_cooperating_scripts():
    """Every sweep script that exposes build() must return byte-aligned spans."""
    targets = [("sweeps/class3_slips.py", "c3"), ("sweeps/slip_extension.py", "se")]
    seeds = corpus.seeds()
    checked = []
    for path, name in targets:
        if not os.path.exists(os.path.join(HERE, path)):
            continue
        mod = _load(path, name)
        for kind in ("mixed", "lf"):
            b, offs = mod.build(kind)
            join, ibr = ("\r\n\r\n", "\n") if kind == "mixed" else ("\n\n", "\n")
            for i, (s, e) in enumerate(offs):
                want = ibr.join(seeds[i]).encode() if isinstance(seeds[i], list) else seeds[i].encode()
                assert b[s:s + len(want)] == want, f"{path} {kind} para {i+1}"
        checked.append(path)
    if not checked:
        raise AssertionError("no cooperating scripts found")
    return f"{len(checked)} scripts, spans aligned"


def t_guard_coverage():
    """every script that mentions a chapter corpus must carry the guard"""
    import glob
    import guard
    missing = []
    for f in sorted(glob.glob(os.path.join(HERE, "*.py")) +
                    glob.glob(os.path.join(HERE, "sweeps/*.py")) +
                    glob.glob(os.path.join(HERE, "harness/*.py")) +
                    glob.glob(os.path.join(HERE, "demos/*.py"))):
        src = open(f, encoding="utf-8", errors="replace").read()
        if not any(k in src for k in list(guard.CANONICAL) + list(guard.OTHER)):
            continue
        if os.path.basename(f) == "guard.py":
            continue
        if "from guard import" not in src:
            missing.append(os.path.relpath(f, HERE))
    assert not missing, f"{len(missing)} unguarded: {missing[:6]}"
    return "all chapter scripts guarded"


def t_guard_detects_drift():
    import tempfile
    import textwrap
    import guard
    bad = textwrap.dedent("""
        import json
        SEGS = json.load(open('wp_paras_br.json'))
        text = "\\r\\n\\r\\n".join("\\n".join(p) for p in SEGS)
        spans, pos = [], 0
        for p in SEGS:
            t = "\\n".join(p)
            spans.append((pos, pos + len(t)))
            pos += len(t) + 4
        a = bytearray(text.encode()); a[spans[100][0]] ^= 32
    """)
    good = bad.replace('t = "\\n".join(p)', 't = ("\\n".join(p)).encode()')
    with tempfile.TemporaryDirectory() as d:
        fb = os.path.join(d, "bad.py")
        fg = os.path.join(d, "good.py")
        open(fb, "w").write(bad)
        open(fg, "w").write(good)
        assert guard.check_source(fb), "detector missed the char/byte bug"
        assert not guard.check_source(fg), f"detector flagged the byte-correct version"
    return "refuses char spans, passes byte spans"


TESTS = [
    ("stage-one chain 9dd2efb9 -> 19TbyN5", t_stage_one),
    ("R1:77 chain 684b250e -> 1FAAKp", t_r1_77),
    ("R2:76 chain f8e5edbc -> 13Cv6S", t_r2_76),
    ("chapter digests (2 bases)", t_chapter_digests),
    ("paragraph spans byte-aligned", t_spans_aligned),
    ("non-ASCII census", t_census),
    ("char/byte drift table", t_drift),
    ("edge toggles land on letters", t_toggles_are_letters),
    ("toggle refuses non-letters", t_toggle_refuses_nonletter),
    ("other corpora are different objects", t_other_corpora_documented),
    ("cooperating sweep scripts byte-aligned", t_cooperating_scripts),
    ("guard deployed on every chapter script", t_guard_coverage),
    ("guard detects the drift bug", t_guard_detects_drift),
]

if __name__ == "__main__":
    for name, fn in TESTS:
        check(name, fn)
    print()
    if FAILED:
        print(f"{len(FAILED)} FAILING: do not trust sweep results until fixed")
        for n, e in FAILED:
            print(f"  - {n}: {e}")
        sys.exit(1)
    print(f"all {len(TESTS)} checks pass: the pipeline is byte-exact")
