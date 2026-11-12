#!/usr/bin/env python3
"""receipt_four_units.py - the 44-char solution string as a *receipt*, plus the composition test.

Reading the certified block-77 solution as a ledger rather than a key:

    1A1 efi2DM Hal Finney  |  TS mN ihsotaS otomakaN
    ---- forward set (4) --   ---- mirrored set (4) ----

four items encoded forward, four encoded mirrored = four head-marks and four tail-marks. The
certified stage-one answer is exactly that: 4 paragraphs, each with its first letter lowered and its
last letter raised (8 edits, net zero). The demo's answer is also 4 paragraphs. So the receipt says a
"move the capitals" answer has FOUR units, not twelve.

The chapter names twelve candidate paragraphs (those containing "recognize the signs"). Four of twelve
is 495 quads, each one deterministic text. That is the family this closes.

Second test: the string as a composition prefix/suffix on the principal zero-balance texts, since a
salt would contradict the one certified mechanism (marked text -> md5 -> BIP39 -> address).
"""
import json, re, sys, hashlib, itertools, time
sys.path.insert(0, "harness")
import fast2

LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
IDX = [0, 1, 2, 5, 6, 7, 44, 76, 77]
P = [t for _, t in json.load(open("wp_paras.json"))]
KEY = "recognize the signs"
S44 = "1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN"
WIF44 = "L4VdZUDY2BXa7VVkjuYkmaLvi8P5qNZaARwwB9wjqkDa6Sn4JLV4"


def addrs(h):
    e = bytes.fromhex(h)
    return {i: fast2.addr_from_key(fast2.key_at(fast2.seed_from(e), i)) for i in IDX}


assert addrs("9dd2efb9bc976c2095bd534d7b8d431c")[0] == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"
assert addrs("684b250ea52c1e33a6f6143ded0e62e6")[0] == "1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP"


def head(p):
    return next((j for j, c in enumerate(p) if c.isalpha()), None)


def tail(p):
    return next((len(p) - 1 - j for j, c in enumerate(reversed(p)) if c.isalpha()), None)


def transport(quads, paras):
    out = list(paras)
    for i in quads:
        t = list(out[i - 1])
        j = head(out[i - 1])
        if j is not None and t[j].isupper():
            t[j] = t[j].lower()
        k = tail(out[i - 1])
        if k is not None and t[k].islower():
            t[k] = t[k].upper()
        out[i - 1] = "".join(t)
    return out


def check(text, label, rows, hits):
    h = hashlib.md5(text.encode("utf-8")).hexdigest()
    a = addrs(h)
    hit = [k for k, v in a.items() if v in (LIVE, OLD)]
    rows.append({"label": label, "md5": h, "addr0": a[0], "hits": hit})
    if hit:
        print("  *** HIT", label, h, hit, flush=True)
        hits += 1
    return hits


def main():
    t0 = time.time()
    signs = [i for i, p in enumerate(P, 1) if KEY in p.lower()]
    print(f"sign paragraphs ({len(signs)}): {signs}")
    rows, hits = [], 0
    quads = list(itertools.combinations(signs, 4))
    print(f"4-of-{len(signs)} quads: {len(quads)}  (x2 joins = {2*len(quads)} texts)")
    for n, q in enumerate(quads, 1):
        paras = transport(q, P)
        for sep in ("\n\n", "\r\n\r\n"):
            hits = check(sep.join(paras), f"quad{list(q)}|{len(sep)}", rows, hits)
        if n % 100 == 0:
            print(f"  {n}/{len(quads)}  {time.time()-t0:.0f}s  hits {hits}", flush=True)
    print(f"quads done: {len(rows)} texts, {len(rows)*len(IDX)} derivations, {hits} hits, "
          f"{time.time()-t0:.0f}s")

    # composition test on the principal zero-balance texts
    base_rows = len(rows)
    principals = {"W1": [5, 6, 7, 8], "W2": [93, 94, 95, 96], "W3": [168, 169, 170, 171],
                  "REP": [231, 232, 233, 235], "sign12": signs}
    print("\ncomposition test (44-char string as prefix/suffix):")
    for name, q in principals.items():
        paras = transport(q, P)
        for sep, jn in (("\n\n", "LF"), ("\r\n\r\n", "CRLF")):
            body = sep.join(paras)
            for comp, cname in ((S44 + " " + body, "44+sp"),
                                (body + " " + S44, "sp+44"),
                                (S44 + body, "44"),
                                (body + S44, "44post"),
                                (S44 + " TOMI Omit TOMI " + WIF44 + " " + body, "tomitpl"),
                                (body + " TOMI Omit TOMI " + WIF44 + " " + S44, "tomitplpost")):
                hits = check(comp, f"{name}|{jn}|{cname}", rows, hits)
    print(f"  composition: {len(rows)-base_rows} texts, {hits} hits total")

    json.dump(rows, open("receipt_four_units_results.json", "w"))
    print(f"\ntotal {len(rows)} texts, {len(rows)*len(IDX)} derivations, {hits} hits, "
          f"{time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
