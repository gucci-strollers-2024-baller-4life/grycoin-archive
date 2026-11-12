#!/usr/bin/env python3
"""outing_quads.py - transport the four "outing" paragraphs instead of the phrase-matched ones.

The demo's failure localised the decoy: "recognize the signs" defines a sign (a word that outs the
author) rather than selecting paragraphs. So the selector is semantic: the paragraphs where the
narrative unmasks an identity. Pool built from the identity/outing lexicon, ranked; every 4-quad in
the pool is one deterministic transported text (head down, tail up), per the receipt's four units.
"""
import json, re, sys, hashlib, itertools, time
sys.path.insert(0, "harness")
import fast2

LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
IDX = [0, 1, 2, 5, 6, 7, 44, 76, 77]
P = [t for _, t in json.load(open("wp_paras.json"))]
POOL = [168, 169, 204, 216, 218, 222, 223, 231, 243, 246, 248, 249, 251, 253, 255, 261, 266, 271]


def addrs(h):
    e = bytes.fromhex(h)
    return {i: fast2.addr_from_key(fast2.key_at(fast2.seed_from(e), i)) for i in IDX}


assert addrs("9dd2efb9bc976c2095bd534d7b8d431c")[0] == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"


def transport(quads, paras):
    out = list(paras)
    for i in quads:
        p = out[i - 1]
        b = list(p)
        j = next((x for x, c in enumerate(p) if c.isalpha()), None)
        k = next((len(p) - 1 - x for x, c in enumerate(reversed(p)) if c.isalpha()), None)
        if j is not None and b[j].isupper():
            b[j] = b[j].lower()
        if k is not None and b[k].islower():
            b[k] = b[k].upper()
        out[i - 1] = "".join(b)
    return out


t0 = time.time()
quads = list(itertools.combinations(POOL, 4))
print(f"pool {len(POOL)} -> {len(quads)} quads, {2*len(quads)} texts")
hits, n = 0, 0
for q in quads:
    for sep, jn in (("\n\n", "LF"), ("\r\n\r\n", "CRLF")):
        h = hashlib.md5(sep.join(transport(q, P)).encode()).hexdigest()
        a = addrs(h)
        n += 1
        hit = [k for k, v in a.items() if v in (LIVE, OLD)]
        if hit:
            hits += 1
            print("  *** HIT", q, jn, h, hit, flush=True)
print(f"{n} texts, {n*len(IDX)} derivations, {hits} hits, {time.time()-t0:.0f}s")

print("\nthe four highest-signal outings, on their own:")
for q in [(255, 251, 248, 204), (168, 222, 243, 246), (248, 251, 255, 168)]:
    for sep, jn in (("\n\n", "LF"), ("\r\n\r\n", "CRLF")):
        h = hashlib.md5(sep.join(transport(q, P)).encode()).hexdigest()
        print(f"  {q} {jn:4s} {h} {addrs(h)[0]}")
