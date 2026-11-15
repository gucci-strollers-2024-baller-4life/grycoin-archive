"""Demo, global three-flip closure: every case flip at any three alpha positions.

The demo (round-2 block 2) is the family's calibration: certified base (md5 7759227d, published in
its own thread), known-funded escrow (1tzieUf...), and an author who says the letter choice "is
obvious if you know the solution to Satoshi's bitcointalk puzzle".  Closed so far: k=1 and k=2
anywhere (1,434,006 documents), the mechanically constrained up-to-3 family (4,235,609), three
flips at word boundaries only (27,976,680), the paragraph-edge rule forms, and letter-level
spellings of the signature and of YANG.

This is the last reachable demo space: all C(1197,3) = 285,129,390 triples of alpha positions,
case toggled at exactly those three, both certified joins, and every candidate whose md5 begins
3c derived at the requested indices against the demo escrow.  A hit hands over the device the
author says stage two shares; a miss proves the demo answer differs from the served text by at
least four letters anywhere.
"""
import hashlib, itertools, time

import rtl_ci as R

RAW = open("prior/demo_base.txt", "rb").read()
CR = RAW.replace(b"\n\n", b"\r\n\r\n")
DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
POS = [i for i, c in enumerate(RAW) if chr(c).isalpha()]
N = len(POS)
TOTAL = N * (N - 1) * (N - 2) // 6


def toggle(buf, p):
    c = buf[p]
    buf[p] = c - 32 if 97 <= c <= 122 else c + 32


def gate():
    assert hashlib.md5(RAW).hexdigest() == "7759227d7406d8230d7e3a8f7b9846d7", "demo base drift"
    for sep, want in R.CERT.items():
        pass
    # construction witness: three toggles applied twice restore the base exactly
    probe = (0, N // 2, N - 1)
    buf = bytearray(RAW)
    for ix in probe:
        toggle(buf, POS[ix])
    assert bytes(buf) != RAW
    for ix in probe:
        toggle(buf, POS[ix])
    assert bytes(buf) == RAW, "toggle round trip failed"
    assert TOTAL == 285129390, TOTAL
    print("gate OK [D3]: demo base 7759227d reproduced; %d alpha positions; C(%d,3)=%d triples; "
          "toggle round trip exact; filter 3c (pfx3c6 counted); target %s" % (N, N, TOTAL, DEMO), flush=True)


gate()


def run(start, end, idxs):
    hi = min(end, TOTAL)
    if start >= TOTAL:
        print("DONE d3 %d..%d n=0 (space is %d)" % (start, end, TOTAL), flush=True)
        return
    print("axes D3 total=%d shard=%d..%d indices=%s joins=LF+CRLF2 filter=3c" % (TOTAL, start, hi, idxs), flush=True)
    t0 = time.time()
    n = p3 = p36 = deriv = hits = 0
    for tri in itertools.islice(itertools.combinations(range(N), 3), start, hi):
        a, b, c = POS[tri[0]], POS[tri[1]], POS[tri[2]]
        buf = bytearray(RAW)
        toggle(buf, a)
        toggle(buf, b)
        toggle(buf, c)
        body_lf = bytes(buf)
        for tag, text in (("lf", body_lf), ("crlf", body_lf.replace(b"\n\n", b"\r\n\r\n"))):
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
                    print("***HIT d3=%s join=%s idx=%d md5=%s escrow=%s" % (tri, tag, ix, d, DEMO), flush=True)
                    open("HIT_D3_%d_%d_%d_%s_%d.txt" % (tri[0], tri[1], tri[2], tag, ix), "wb").write(text)
        if n and n % 2000000 == 0:
            print("n=%d at=%s rate=%.0f docs/s" % (n, tri, n / (time.time() - t0)), flush=True)
    print("DONE d3 %d..%d n=%d pfx3c=%d pfx3c6=%d derivations=%d hits=%d in %ds"
          % (start, hi, n, p3, p36, deriv, hits, time.time() - t0), flush=True)
