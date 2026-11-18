#!/usr/bin/env python3
"""Exhaustive two-case-flip ("a couple of letters") sweep of the chapter, sharded.

Family: every unordered pair of alpha positions in the 45,456-byte LF base; the document
is the base with BOTH letters' case swapped.  That is exactly every text obtainable from
the chapter by changing the capitalization of two letters anywhere, C(35825,2) =
641,697,400 documents per join.

Why this family: the author's own description of the block-77 format is "keep the whole
long text and change only a couple of letters in their capitalization"; her worked example
in the demo is one lowering plus one raising.  Every structured placement (paragraph edges,
anchors, sentence edges, line units, sign windows, name at-occurrence readings, ordinal
occurrences) is closed on verified zeros, so the unconstrained pair space is the remaining
literal reading.

Sharding: the dispatch workflow passes START and END over an integer ordinal space; the
suffix input carries the block offset ("PAIRS<offset>"), which is how this lane reaches
later blocks without editing the workflow.

Gate: the certified stage-one preimage must reproduce 19TbyN5 at index 0, and the base must
hash to 46a308c2, before a single candidate is derived.
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
CERT_LF = "46a308c279540a33e977ea1f660e8458"


def _pub(k):
    x, y = PrivateKey(k.to_bytes(32, "big")).public_key.point()
    return (x, y)


btc.pubkey = _pub


def addr(d, ix):
    m = btc.entropy_to_mnemonic(bytes.fromhex(d))
    k = btc.derive_path(btc.mnemonic_seed(m, ""), (44 + 0x80000000, 0x80000000, 0x80000000, 0, ix))
    return btc.p2pkh(_pub(k))


CERT_CRLF2 = "bd07e6ee209c5ab65d874bbbcfccda18"
SUBSTRATE = os.environ.get("PAIRS_SUBSTRATE", "lf")


def load():
    if SUBSTRATE == "crlf2":
        base = open(os.path.join(HERE, "base_chapter_crlf2.txt"), "rb").read()
        want = CERT_CRLF2
    else:
        base = open(os.path.join(HERE, "base_chapter_lf.txt"), "rb").read()
        want = CERT_LF
    got = hashlib.md5(base).hexdigest()
    assert got == want, "base drift %s != %s" % (got, want)
    pos = [i for i, c in enumerate(base) if 65 <= c <= 90 or 97 <= c <= 122]
    assert len(pos) == 35825, len(pos)
    return base, pos


def gate(base, pos):
    a = addr("9dd2efb9bc976c2095bd534d7b8d431c", 0)
    assert a == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN", a
    # construction control: flipping positions 0 and 1 of the base must equal the naive build
    b = bytearray(base)
    b[pos[0]] ^= 0x20
    b[pos[1]] ^= 0x20
    s = bytearray(base)
    p0, p1 = pos[0], pos[1]
    s[p0] = s[p0] ^ 0x20
    s[p1] = s[p1] ^ 0x20
    assert bytes(b) == bytes(s)
    print("gate OK: substrate %s, 35825 alpha positions, stage-one calibration 19TbyN5, "
          "pair space C(n,2)=%d, targets %s" % (SUBSTRATE, len(pos) * (len(pos) - 1) // 2,
                                                "+".join(TARGETS.values())), flush=True)


def cum_table(n):
    """cum[i] = number of pairs whose first index is < i."""
    return [i * (2 * n - i - 1) // 2 for i in range(n + 1)]


def run(start, end, join, idxs):
    if join != "lf":
        print("skip join=%s under PAIRS (LF substrate only)" % join, flush=True)
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
    t0 = time.time()
    cnt = 0
    hits = 0
    i = bisect_right(cum, start) - 1
    j = i + 1 + (start - cum[i])
    print("PAIRS range %d..%d of %d, first pair (%d,%d)" % (start, end, total, i, j), flush=True)
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
                print("***HIT pair=(%d,%d) join=%s idx=%d md5=%s escrow=%s"
                      % (p, q, join, ix, d, TARGETS[a]), flush=True)
                open("HIT_pairs_%d_%d_%d.txt" % (p, q, ix), "wb").write(_doc(base, p, q))
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
    print("DONE join=%s range %d..%d n=%d hits=%d in %ds"
          % (join, start, end, cnt, hits, time.time() - t0), flush=True)


def _doc(base, p, q):
    b = bytearray(base)
    b[p] ^= 0x20
    b[q] ^= 0x20
    return bytes(b)
