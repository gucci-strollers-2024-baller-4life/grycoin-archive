#!/usr/bin/env python3
"""Real Big Block, exhaustive two-case-flip space on the ONE-line-break substrate (e7f3720c).

Why this substrate. The author added the extra line breaks on 2019-07-25 ("I added extra line
breaks between paragraphs. This information is needed to solve the block") and re-funded on
2019-07-31, "hashing with a slightly different solution". The earlier escrow 1EFojcAo was funded
2019-07-22, before that change, so it pairs with the single-break serialisation: the same 273
paragraphs joined by ONE line break, md5 e7f3720c, 45,456 bytes, 35,825 letter positions.

A two-flip document on this base is not a document on any other base, so this is new coverage
rather than a re-run. Both escrows are tested: the live 14zMk and the earlier 1EFojcAo.

Enumeration, sharding and the gate mirror ci/pairs_sweep.py: the ordinal space is
C(35,825,2) = 641,697,400 unordered pairs, and the dispatch workflow passes START/END.

Usage: python3 ci/pairs_sb.py START END join idxs
"""
import hashlib, os, sys, time
from bisect import bisect_right

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import btc
from coincurve import PrivateKey

ESC = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
V1T = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
TARGETS = {ESC: "LIVE(14zMk)", V1T: "V1(1EFojcAo)"}
CERT_SINGLE = "e7f3720c6f9c95afe37efb0b78ebc8ac"


def _pub(k):
    x, y = PrivateKey(k.to_bytes(32, "big")).public_key.point()
    return (x, y)


btc.pubkey = _pub


def addr(d, ix):
    m = btc.entropy_to_mnemonic(bytes.fromhex(d))
    k = btc.derive_path(btc.mnemonic_seed(m, ""), (44 + 0x80000000, 0x80000000, 0x80000000, 0, ix))
    return btc.p2pkh(_pub(k))


def load():
    base = open(os.path.join(HERE, "base_chapter_singlecrlf.txt"), "rb").read()
    got = hashlib.md5(base).hexdigest()
    assert got == CERT_SINGLE, "base drift %s != %s" % (got, CERT_SINGLE)
    pos = [i for i, c in enumerate(base) if 65 <= c <= 90 or 97 <= c <= 122]
    assert len(pos) == 35825, len(pos)
    return base, pos


def gate(base, pos):
    a = addr("9dd2efb9bc976c2095bd534d7b8d431c", 0)
    assert a == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN", a
    b = bytearray(base)
    b[pos[0]] ^= 0x20
    b[pos[1]] ^= 0x20
    s = bytearray(base)
    s[pos[0]] ^= 0x20
    s[pos[1]] ^= 0x20
    assert bytes(b) == bytes(s)
    print("gate OK [PAIRSB]: one-line-break substrate e7f3720c, 35825 letter positions, "
          "stage-one calibration 19TbyN5, pair space %d, targets %s"
          % (len(pos) * (len(pos) - 1) // 2, "+".join(TARGETS.values())), flush=True)


def cum_table(n):
    return [i * (2 * n - i - 1) // 2 for i in range(n + 1)]


def _doc(base, p, q):
    b = bytearray(base)
    b[p] ^= 0x20
    b[q] ^= 0x20
    return bytes(b)


def run(start, end, join, idxs):
    if join != "lf":
        print("skip join=%s under PAIRSB (single substrate, one pass)" % join, flush=True)
        return
    base, pos = load()
    gate(base, pos)
    n = len(pos)
    cum = cum_table(n)
    total = cum[n]
    end = min(end, total)
    if start >= end:
        print("empty range %d..%d of %d" % (start, end, total), flush=True)
        return
    B = bytearray(base)
    t0 = time.time(); cnt = 0; hits = 0
    i = bisect_right(cum, start) - 1
    j = i + 1 + (start - cum[i])
    print("PAIRSB range %d..%d of %d, first pair (%d,%d)" % (start, end, total, i, j), flush=True)
    while True:
        p, q = pos[i], pos[j]
        B[p] ^= 0x20
        B[q] ^= 0x20
        d = hashlib.md5(bytes(B)).hexdigest()
        B[p] ^= 0x20
        B[q] ^= 0x20
        cnt += 1
        for ix in idxs:
            a = addr(d, ix)
            if a in TARGETS:
                hits += 1
                print("***HIT pair=(%d,%d) idx=%d md5=%s escrow=%s" % (p, q, ix, d, TARGETS[a]),
                      flush=True)
                open("HIT_pairsb_%d_%d_%d.txt" % (p, q, ix), "wb").write(_doc(base, p, q))
        if cnt % 50000 == 0:
            el = time.time() - t0
            print("n=%d pair=(%d,%d) rate=%.0f/s eta=%.0fs"
                  % (cnt, p, q, cnt / el, el * (end - start - cnt) / cnt), flush=True)
        if start + cnt >= end:
            break
        j += 1
        if j >= n:
            i += 1
            if i >= n - 1:
                break
            j = i + 1
    print("DONE pairsb %d..%d n=%d hits=%d in %ds" % (start, end, cnt, hits, time.time() - t0),
          flush=True)


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], [int(x) for x in sys.argv[4].split(",")])
