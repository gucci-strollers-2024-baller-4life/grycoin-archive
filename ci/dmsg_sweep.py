"""Demo, letter level: the marks spell a short message from the demo's own vocabulary.

The demo (round-2 block 2) is the only instance in the family with a certified base
(md5 7759227d, published in its own thread) and a known-funded escrow (1tzieUf...), so it is
the calibration for the device.  Its author says the letter choice "is obvious if you know the
solution to Satoshi's bitcointalk puzzle", i.e. the marks are letters spelling a signature, not
a paragraph selection.  This lane takes every word of the demo's own vocabulary of length 2..4
and, for every in-order placement of its letters anywhere in the text, uppercases exactly those
positions, hashes, and derives candidates whose md5 begins 3c (the published prefix is 3c6, and
the wider two-nibble filter guards a Block-59 style typo on the third digit).

Sharded by contiguous ordinal over the whole (word, placement) space.
"""
import hashlib, itertools, os, time

import rtl_ci as R

P = R.load()
BASE = {}
RAW = None
RAW = open("prior/demo_base.txt", "rb").read()
LOW = RAW.lower()
L = len(RAW)
DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
JOINS = (("lf", RAW), ("crlf", RAW.replace(b"\n\n", b"\r\n\r\n")))


def emb_count(msg):
    m = msg.lower().encode()
    nxt = None
    for i in range(len(m) - 1, -1, -1):
        arr = [0] * (L + 2)
        for p in range(L - 1, -1, -1):
            c = (1 if i == len(m) - 1 else nxt[p + 1]) if LOW[p:p + 1] == m[i:i + 1] else 0
            arr[p] = c + arr[p + 1]
        nxt = arr
    return nxt[0]


import re
vocab = {w.upper() for w in re.findall(r"[A-Za-z]+", RAW.decode()) if 2 <= len(w) <= 4}
WORDS = sorted(vocab, key=lambda w: (len(w), w))
COUNT = [emb_count(w) for w in WORDS]
CUM = []
acc = 0
for c in COUNT:
    acc += c
    CUM.append(acc)
TOTAL = acc
POS = {}


def positions(ch):
    if ch not in POS:
        POS[ch] = [i for i in range(L) if LOW[i:i + 1] == ch.encode().lower()]
    return POS[ch]


def gate():
    for sep, want in R.CERT.items():
        assert hashlib.md5(sep.join(x.encode() for x in P)).hexdigest() == want, "base drift"
    assert hashlib.md5(RAW).hexdigest() == "7759227d7406d8230d7e3a8f7b9846d7", "demo base drift"
    assert TOTAL > 0
    print("gate OK [DMSG]: chapter bases reproduced; demo base 7759227d reproduced; %d words len 2..4; "
          "%d in-order placements; filter 3c (pfx3c6 counted separately); target %s"
          % (len(WORDS), TOTAL, DEMO), flush=True)


gate()


def run(start, end, idxs):
    hi = min(end, TOTAL)
    if start >= TOTAL:
        print("DONE dmsg %d..%d n=0 (space is %d)" % (start, end, TOTAL), flush=True)
        return
    print("axes DMSG total=%d shard=%d..%d indices=%s joins=LF+CRLF2 filter=3c" % (TOTAL, start, hi, idxs), flush=True)
    t0 = time.time()
    n = 0
    p3 = p36 = 0
    deriv = 0
    hits = 0
    for wi, w in enumerate(WORDS):
        lo = 0 if wi == 0 else CUM[wi - 1]
        wend = CUM[wi]
        if wend <= start or lo >= hi:
            continue
        msg = w.lower()
        plists = [positions(c) for c in msg]
        base_pos = max(start, lo)
        for ordinal, sel in enumerate(itertools.product(*plists)):
            g = lo + ordinal
            if g < base_pos:
                continue
            if g >= hi or g >= wend:
                break
            if any(sel[i] >= sel[i + 1] for i in range(len(sel) - 1)):
                continue
            buf = bytearray(RAW)
            for p in sel:
                c = buf[p]
                if 97 <= c <= 122:
                    buf[p] = c - 32
            body = bytes(buf)
            for tag, text in (("lf", body), ("crlf", body.replace(b"\n\n", b"\r\n\r\n"))):
                d = hashlib.md5(text).hexdigest()
                n += 1
                if d[:2] != "3c":
                    continue
                p3 += 1
                if d[:3] == "3c6":
                    p36 += 1
                for ix in idxs:
                    deriv += 1
                    if R.addr(d, ix) == DEMO:
                        hits += 1
                        print("***HIT word=%s sel=%s join=%s idx=%d md5=%s escrow=%s"
                              % (w, sel, tag, ix, d, DEMO), flush=True)
                        open("HIT_DMSG_%s_%s_%d.txt" % (w, tag, ix), "wb").write(text)
        if n and n % 500000 < 2:
            print("n=%d word=%s rate=%.0f docs/s" % (n, w, n / (time.time() - t0)), flush=True)
    print("DONE dmsg %d..%d n=%d pfx3c=%d pfx3c6=%d derivations=%d hits=%d in %ds"
          % (start, hi, n, p3, p36, deriv, hits, time.time() - t0), flush=True)
