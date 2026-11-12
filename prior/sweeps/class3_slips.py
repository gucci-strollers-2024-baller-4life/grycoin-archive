"""Class-3 slips on the accepted sign sets (SLIP_PATTERNS.md sec.8.2) -- never enumerated before.

Her documented error class on the answer's own layer is a *wrong-direction flip* or a
*stray capital* (R2 b12: "solution was grycoin, not Grycoin ... first mistake of this round").
Applied to the stage-two object that means: take an accepted sign set, and

  tier A : invert the flip direction of exactly one paragraph in the set
  tier B : apply the set normally and add exactly one stray case toggle, kept inside the
           set's own paragraphs (her typo would land where she was working)

Every candidate is address-verified against BOTH escrows on hash160 (never on the
base58 string), plus the accepted indices. Base text is rebuilt from wp_paras_br.json and
must reproduce the certified digests before any run.

Usage:  python3 sweeps/class3_slips.py [A|B|AB] [--max-min N]
"""
import hashlib, json, sys, time, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import fast2

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)

LIVE_H = fast2.h160(fast2.LIVE)
OLD_H = fast2.h160(fast2.OLD)
IDX = (0, 1, 2, 76, 77)
CERT = {"lf": "46a308c279540a33e977ea1f660e8458", "mixed": "bd07e6ee209c5ab65d874bbbcfccda18"}

# accepted sign sets, 1-indexed paragraph numbers
SETS = {
    "W1_5-8": [5, 6, 7, 8],
    "W2_93-96": [93, 94, 95, 96],
    "W3_168-171": [168, 169, 170, 171],
    "W4_230-234": [230, 231, 232, 234],
    "W4b_231-235": [231, 232, 233, 235],
    "ALL3": [5, 6, 7, 8, 93, 94, 95, 96, 168, 169, 170, 171],
    "ALL4": [5, 6, 7, 8, 93, 94, 95, 96, 168, 169, 170, 171, 230, 231, 232, 234],
}


def build(kind):
    segs = json.load(open(os.path.join(HERE, "wp_paras_br.json")))
    join = "\r\n\r\n" if kind != "lf" else "\n\n"
    ibr = "\n"
    text = join.join(ibr.join(s) for s in segs)
    b = text.encode()
    assert hashlib.md5(b).hexdigest() == CERT[kind], kind
    # paragraph BYTE offsets (the chapter holds six U+00A0 characters, so char offsets != byte
    # offsets from char 9,084 onward; this used to return char spans against encoded bytes)
    offs, pos = [], 0
    jb = len(join.encode())
    for s in segs:
        para = ibr.join(s).encode()
        offs.append((pos, pos + len(para)))
        pos += len(para) + jb
    return b, offs


def letters(b, start, end):
    return [i for i in range(start, end) if 65 <= b[i] <= 90 or 97 <= b[i] <= 122]


def first_last(b, para_off):
    s, e = para_off
    ls = letters(b, s, e)
    return (ls[0], ls[-1]) if ls else (None, None)


def toggle(b, ps):
    a = bytearray(b)
    for p in ps:
        c = a[p]
        a[p] = c + 32 if 65 <= c <= 90 else c - 32
    return bytes(a)


def is_lower(c):
    return 97 <= c <= 122


def edges(b, para_off, mode):
    """mode A (stage-one certified): first down, last up. mode B: the inverse."""
    f, l = first_last(b, para_off)
    out = []
    if f is None:
        return out
    if mode == "A":
        if not is_lower(b[f]):
            out.append(f)
        if is_lower(b[l]):
            out.append(l)
    else:
        if is_lower(b[f]):
            out.append(f)
        if not is_lower(b[l]):
            out.append(l)
    return out


def run(tiers, max_seconds=None):
    t0 = time.time()
    cands = derivs = 0
    hits = []
    for kind in ("mixed", "lf"):
        b, offs = build(kind)
        for name, paras in SETS.items():
            base_pos = []
            per_para = {}
            for p in paras:
                e = edges(b, offs[p - 1], "A")
                per_para[p] = e
                base_pos += e
            for mode in ("A", "B"):
                if mode == "A":
                    pos, pp = base_pos, per_para
                else:
                    pos = []
                    pp = {}
                    for p in paras:
                        e = edges(b, offs[p - 1], "B")
                        pp[p] = e
                        pos += e
                if not pos:
                    continue
                # baseline + tier A (one paragraph's direction inverted)
                variants = [("plain", pos)]
                if "A" in tiers:
                    for p in paras:
                        inv = edges(b, offs[p - 1], "B" if mode == "A" else "A")
                        variants.append((f"inv{p}", [x for x in pos if x not in pp[p]] + inv))
                if "B" in tiers:
                    pool = sorted({x for p in paras for x in letters(b, *offs[p - 1])})
                    base_set = set(pos)
                    for s in pool:
                        if s in base_set:
                            continue
                        variants.append((f"stray{s}", pos + [s]))
                for tag, ps in variants:
                    h = hashlib.md5(toggle(b, ps)).digest()
                    for idx in IDX:
                        a = fast2.addr_from_key(fast2.key_at(fast2.seed_from(h), idx))
                        derivs += 1
                        ah = fast2.h160(a)
                        if ah in (LIVE_H, OLD_H):
                            which = "LIVE" if ah == LIVE_H else "OLD"
                            hits.append((kind, name, mode, tag, idx, h.hex(), a, which))
                            print("*** HIT", hits[-1], flush=True)
                    cands += 1
                    if cands % 200 == 0:
                        el = time.time() - t0
                        print(f"  {kind} {name} {mode} {tag:10s} cands={cands} "
                              f"derivs={derivs} {derivs/el:.0f}/s", flush=True)
                        if max_seconds and el > max_seconds:
                            return dict(cands=cands, derivs=derivs, hits=hits, stop="time")
    return dict(cands=cands, derivs=derivs, hits=hits,
                secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    tiers = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "ACOUNT"
    cap = None
    if "--max-min" in sys.argv:
        cap = 60 * float(sys.argv[sys.argv.index("--max-min") + 1])
    if tiers == "COUNT":
        for kind in ("mixed", "lf"):
            b, offs = build(kind)
            for name, paras in SETS.items():
                n = len({x for p in paras for x in letters(b, *offs[p - 1])})
                print(kind, name, "letters in set:", n)
        sys.exit()
    t = tiers if tiers in ("A", "B", "AB") else "AB"
    r = run(t, cap)
    print(json.dumps(r, indent=1)[:2000])
