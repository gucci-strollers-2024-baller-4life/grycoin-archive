#!/usr/bin/env python3
"""Demo oracle, five mechanical flips: C(294,5) = 17,689,173,558 documents.

Why this family. The demo's worked example is the only place the author states his own marking:
`I` -> `i` lowers a WORD-INITIAL and `himself` -> `himselF` raises a WORD-FINAL. So the markable
positions are the 23 capitalised word-initials (lowerable) and the 271 lowercase word-finals
(raisable) of demo_base.txt, 294 in total, with the polarity fixed by the position type. Every
four-flip combination of those 294 was closed on 2026-11-17 (five plans, 313,413,310 documents,
zero), and the global three-flip space C(1197,3) was closed earlier, so the demo answer differs
from the served text by at least five mechanical flips if it is a case-marked demo at all.

Five flips is 17.7B documents, which is 59 minutes of wall time across twenty CI shards at the
measured md5-bound rate, and the published 12-bit `3c6` prefix means only 1 in 4096 needs a
derivation.

Ordinal -> subset uses the combinatorial number system, so a shard range is a contiguous block of
the space and the shards tile it exactly.
"""
import hashlib, os, sys, time

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
    import re
    word = re.compile(r"[A-Za-z]+")
    pos = []
    for m in word.finditer(text):
        s, e = m.start(), m.end() - 1
        if text[s].isupper():
            pos.append(("d", s))
        if text[e].islower():
            pos.append(("u", e))
    pos.sort(key=lambda x: x[1])
    return base, crlf, pos


def gate(base, crlf, pos):
    a = addr("9dd2efb9bc976c2095bd534d7b8d431c", 0)
    assert a == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN", a
    assert len(pos) == 296, len(pos)
    print("gate OK [DEMOK5]: demo base 7759227d, %d mechanical positions, stage-one calibration "
          "19TbyN5, C(296,5)=%d, target %s" % (len(pos), _C(len(pos), 5), ESC), flush=True)


def _C(n, k):
    from math import comb
    return comb(n, k)


def unrank(n, k, ordinal):
    """Combinatorial number system: ordinal -> sorted k-subset of range(n)."""
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
    total = _C(n_pos, 5)
    end = min(end, total)
    if start >= end:
        print("empty range %d..%d of %d" % (start, end, total), flush=True)
        return
    print("DEMOK5 range %d..%d of %d" % (start, end, total), flush=True)
    t0 = time.time(); n = 0; p3 = 0; hits = 0
    C = _C
    for ordv in range(start, end):
        sel = unrank(n_pos, 5, ordv)
        for tag, src in (("lf", base), ("crlf", crlf)):
            b = bytearray(src)
            for si in sel:
                kind, p = pos[si]
                c = b[p]
                if kind == "d" and 65 <= c <= 90:
                    b[p] = c + 32
                elif kind == "u" and 97 <= c <= 122:
                    b[p] = c - 32
            h = hashlib.md5(bytes(b)).hexdigest()
            n += 1
            if not h.startswith("3c6"):
                continue
            p3 += 1
            if addr(h, 0) == ESC:
                hits += 1
                print("***HIT DEMO ord=%d sel=%s join=%s md5=%s" % (ordv, sel, tag, h), flush=True)
        if n % 2000000 == 0:
            el = time.time() - t0
            print("  %d/%d %.0fs %.0f docs/s pfx3c6=%d" % (ordv, end, el, n / el, p3), flush=True)
    print("DONE demok5 %d..%d n=%d pfx3c6=%d hits=%d in %.0fs" % (start, end, n, p3, hits, time.time() - t0),
          flush=True)


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], [int(x) for x in sys.argv[4].split(",")])
