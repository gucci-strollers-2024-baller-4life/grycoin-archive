#!/usr/bin/env python3
"""block29_spelling.py - Block 29 read as a spelling rule and applied to the chapter.

Block 29's answer is the block text with `voice` -> `vOIce`, and the block itself then names the
result: "How about Aoi?" / "Artificial Omnipotent Intelligence".  Read off the marked sentence,

    A pleasant female vOIce.

the rule is: the sentence's FIRST letter is the anchor and is the name's first letter (here the
one-letter word `A`); the remaining letters of the name are set as capitals at occurrences already
present inside words (here `o` and `i` inside `voice`); nothing else moves, nothing is lowered.

That is a *different* geometry from the demo's (paragraph-first DOWN + sentence-final UP): additive,
word-interior, and anchored on the sentence, not on the paragraph or the edge.

Applied to the chapter, per sentence:
  anchor   first alphabetic character of the sentence equals name[0]
  marks    name[1:] occurs in order inside that same sentence
  variant  S-int : every mark is strictly interior to its word (block 29's `vOIce` shape)
           S-any : marks at any position (superset, for completeness)
Two serialisations (LF, CRLF), indices 0,1,2,5,6,7,44,76,77, both escrows.
AOI is included only as a control: that family is already closed byte-exact by
sweeps/aoi_chapter_byte.py (53,787 candidates).
"""
import json, re, sys, time, hashlib
sys.path.insert(0, "harness")
import btc
try:
    import fast2
    def md5_hex(t):
        return hashlib.md5(t.encode("utf-8")).hexdigest()
    def addrs(h):
        ent = bytes.fromhex(h)
        return {i: fast2.addr_from_key(fast2.key_at(fast2.seed_from(ent), i)) for i in IDX}
except ImportError:
    md5_hex = btc.md5_hex
    addrs = None

LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
IDX = [0, 1, 2, 5, 6, 7, 44, 76, 77]
P = [t for _, t in json.load(open("wp_paras.json"))]
NAMES = sys.argv[1].split(",")
if addrs is not None:      # certified stage-one vector, before any chapter work
    assert addrs("9dd2efb9bc976c2095bd534d7b8d431c")[0] == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN", \
        "fast2 harness self-test failed"
    print("harness self-test: OK (stage-one @0 reproduces)")
ARM = sys.argv[2] if len(sys.argv) > 2 else "int"      # int | any


def sents(p):
    out, s = [], 0
    for m in re.finditer(r'[.!?]+["\u201d]?(?=\s|$)', p):
        out.append((s, m.end()))
        s = m.end()
    if s < len(p):
        out.append((s, len(p)))
    return out


def kinds(p):
    k = {}
    for m in re.finditer(r"[A-Za-z']+", p):
        a, b = m.span()
        for j in range(a, b):
            k[j] = 'solo' if a == b - 1 else ('init' if j == a else ('fin' if j == b - 1 else 'int'))
    return k


def embed(p, a, b, name, depth=1, start=0, acc=()):
    if depth == len(name):
        yield acc
        return
    need = name[depth]
    for j in range(start, b):
        if p[j].isalpha() and p[j].upper() == need:
            yield from embed(p, a, b, name, depth + 1, j + 1, acc + (j,))


if addrs is None:
    def addrs(h):
        k, c = btc.master_key(btc.mnemonic_seed(btc.entropy_to_mnemonic(bytes.fromhex(h))))
        for d in (44 + btc.H, 0 + btc.H, 0 + btc.H, 0):
            k, c = btc.ckd_priv(k, c, d)
        return {i: btc.p2pkh(btc.pubkey(btc.ckd_priv(k, c, i)[0])) for i in IDX}


def main():
    t0 = time.time()
    seen, cands = set(), []
    for name in NAMES:
        for i, p in enumerate(P, 1):
            k = kinds(p)
            for a, b in sents(p):
                m = re.match(r'\s*["\u201c(\[]*([A-Za-z])', p[a:b])
                if not m or m.group(1).upper() != name[0]:
                    continue
                for t in embed(p, a, b, name, 1, a):
                    if ARM == "int" and not all(k.get(j) == 'int' for j in t):
                        continue
                    edited = list(p)
                    for j in t:
                        edited[j] = edited[j].upper()
                    paras = list(P)
                    paras[i - 1] = "".join(edited)
                    for sep in ("\n\n", "\r\n\r\n"):
                        key = hash(sep.join(paras))
                        if key in seen:
                            continue
                        seen.add(key)
                        cands.append((name, i, t, sep, sep.join(paras)))
    print(f"candidates {len(cands)}  ({time.time()-t0:.0f}s)", flush=True)
    rows, hits = [], 0
    for n, (name, i, t, sep, text) in enumerate(cands, 1):
        jn = "LF" if sep == "\n\n" else "CRLF"
        h = md5_hex(text)
        a_ = addrs(h)
        hit = [j for j, v in a_.items() if v in (LIVE, OLD)]
        if hit:
            hits += 1
            print(f"*** HIT {name} P{i} {t} {jn} {h} {hit}", flush=True)
        rows.append({"name": name, "para": i, "marks": list(t), "sep": "LF" if "\n\n" == sep else "CRLF",
                     "md5": h, "addr0": a_[0], "hits": hit})
        if n % 200 == 0:
            print(f"  {n}/{len(cands)}  {time.time()-t0:.0f}s", flush=True)
    json.dump(rows, open(f"block29_spelling_{ARM}_{NAMES[0]}_results.json", "w"))
    print(f"done: {len(rows)} derivations, {len({r['md5'] for r in rows})} distinct md5, {hits} hits,"
          f" {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
