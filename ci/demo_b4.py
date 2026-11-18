#!/usr/bin/env python3
"""Demo oracle, four case flips at WORD BOUNDARIES: C(548,4) = 3,716,599,705 documents.

Why this and not the mechanical space. The demo's worked example marks a word-initial and a
word-final, so the markable positions are the 284 word-initials and 284 word-finals of
demo_base.txt (548 distinct, 20 single-letter words counted in both). The *mechanical* four-flip
space -- only the 23 capitalised initials that can be lowered and the 273 lowercase finals that can
be raised, 296 positions -- was closed on 2026-11-17 (313,413,310 documents, zero). That leaves the
case changes the mechanical restriction forbids: raising a lowercase word-initial, lowering an
uppercase word-final, and any mix. All of those are legal marks by the same mechanic, and all of
them live in this 548-position space, whose four-flip slice is 3.72 billion documents.

At the measured md5-bound rate that is about thirteen minutes of wall time across twenty CI shards,
and the published 12-bit 3c6 prefix means only one document in 4096 needs a derivation.
"""
import hashlib, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import btc
from coincurve import PrivateKey

ESC = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
CERT_LF = "7759227d7406d8230d7e3a8f7b9846d7"


def _pub(k):
    x, y = PrivateKey(k.to_bytes(32, "big")).public_key.point()
    return (x, y)


btc.pubkey = _pub


def addr(h, ix=0):
    m = btc.entropy_to_mnemonic(bytes.fromhex(h))
    k = btc.derive_path(btc.mnemonic_seed(m, ""), (44 + 0x80000000, 0x80000000, 0x80000000, 0, ix))
    return btc.p2pkh(_pub(k))


def load():
    base = open(os.path.join(HERE, "demo_base.txt"), "rb").read()
    got = hashlib.md5(base).hexdigest()
    assert got == CERT_LF, "demo base drift %s != %s" % (got, CERT_LF)
    crlf = base.replace(b"\n\n", b"\r\n\r\n")
    text = base.decode()
    pos = set()
    for m in re.finditer(r"[A-Za-z]+", text):
        pos.add(m.start())
        pos.add(m.end() - 1)
    pos = sorted(pos)
    return base, crlf, pos


def _C(n, k):
    from math import comb
    return comb(n, k)


def gate(base, crlf, pos):
    a = addr("9dd2efb9bc976c2095bd534d7b8d431c", 0)
    assert a == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN", a
    assert len(pos) == 548, len(pos)
    print("gate OK [DEMOB4]: demo base 7759227d, %d word-boundary positions, stage-one calibration "
          "19TbyN5, C(548,4)=%d, target %s" % (len(pos), _C(len(pos), 4), ESC), flush=True)


def unrank(n, k, ordinal):
    out = []
    x = n - 1
    for j in range(k, 0, -1):
        while _C(x, j) > ordinal:
            x -= 1
        out.append(x)
        ordinal -= _C(x, j)
        x -= 1
    return out[::-1]


def run(start, end, join, idxs):
    base, crlf, pos = load()
    gate(base, crlf, pos)
    n_pos = len(pos)
    total = _C(n_pos, 4)
    end = min(end, total)
    if start >= end:
        print("empty range %d..%d of %d" % (start, end, total), flush=True)
        return
    print("DEMOB4 range %d..%d of %d" % (start, end, total), flush=True)
    t0 = time.time(); n = 0; p3 = 0; hits = 0
    for ordv in range(start, end):
        sel = unrank(n_pos, 4, ordv)
        for tag, src in (("lf", base), ("crlf", crlf)):
            b = bytearray(src)
            for si in sel:
                p = pos[si]
                b[p] ^= 0x20
            h = hashlib.md5(bytes(b)).hexdigest()
            n += 1
            if not h.startswith("3c6"):
                continue
            p3 += 1
            if addr(h, 0) == ESC:
                hits += 1
                print("***HIT DEMOB4 ord=%d sel=%s join=%s md5=%s" % (ordv, sel, tag, h), flush=True)
        if n % 2000000 == 0:
            el = time.time() - t0
            print("  %d/%d %.0fs %.0f docs/s pfx3c6=%d" % (ordv, end, el, n / el, p3), flush=True)
    print("DONE demob4 %d..%d n=%d pfx3c6=%d hits=%d in %.0fs" % (start, end, n, p3, hits, time.time() - t0),
          flush=True)


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], [int(x) for x in sys.argv[4].split(",")])
