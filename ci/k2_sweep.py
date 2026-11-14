"""Exhaustive two-letter case-flip sweep of the certified chapter base.

Space: every unordered pair of alphabetic positions in the LF base (md5 46a308c2).
Each candidate = the base with exactly those two letters' case toggled. md5 -> BIP39 ->
BIP32 m/44'/0'/0'/0/i -> P2PKH, compared to both escrows.

Sharded by triangular pair index: cum(i) = number of pairs whose first index < i, so
index t in [cum(i), cum(i+1)) maps to (i, j=i+1+(t-cum(i))). The mapping is a bijection
over all n*(n-1)/2 pairs; shard ranges partition the space exactly.

Usage: k2_sweep.py START END [procs]
"""
import bisect
import hashlib
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CERT = "46a308c279540a33e977ea1f660e8458"
ESC = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
V1T = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"

_G = {}


def _derive_setup():
    import btc
    from coincurve import PrivateKey

    def _pub(k):
        x, y = PrivateKey(k.to_bytes(32, "big")).public_key.point()
        return (x, y)

    btc.pubkey = _pub
    return btc


def load_base():
    b = open(os.path.join(HERE, "base_chapter_lf.txt"), "rb").read()
    got = hashlib.md5(b).hexdigest()
    assert got == CERT, "base drift: %s != %s" % (got, CERT)
    return b


def letters(b):
    return [i for i, c in enumerate(b) if 65 <= c <= 90 or 97 <= c <= 122]


def flipbyte(c):
    return c + 32 if 65 <= c <= 90 else c - 32


def cum_table(n):
    return [i * n - i * (i + 1) // 2 for i in range(n)]


def worker(args):
    lo, hi, idxs, prog = args
    btc = _derive_setup()
    def addr(d, ix):
        m = btc.entropy_to_mnemonic(bytes.fromhex(d))
        k = btc.derive_path(btc.mnemonic_seed(m, ""), (0x8000002c, 0x80000000, 0x80000000, 0, ix))
        return btc.p2pkh(btc.pubkey(k))

    base = load_base()
    pos = letters(base)
    n = len(pos)
    cum = cum_table(n)
    targets = {ESC: "ESC", V1T: "V1"}
    buf = bytearray(base)
    i = bisect.bisect_right(cum, lo) - 1
    if i < 0:
        i = 0
    t = lo
    done = 0
    t0 = time.time()
    while t < hi and i < n - 1:
        pi = pos[i]
        oi = buf[pi]
        buf[pi] = flipbyte(oi)
        j = i + 1 + (t - cum[i])
        while j < n and t < hi:
            pj = pos[j]
            oj = buf[pj]
            buf[pj] = flipbyte(oj)
            d = hashlib.md5(buf).hexdigest()
            for ix in idxs:
                if addr(d, ix) in targets:
                    body = bytes(buf)
                    fn = "HIT_k2_%d_%d_%d.txt" % (i, j, ix)
                    open(fn, "wb").write(body)
                    print("***HIT pair=(%d,%d) md5=%s idx=%d target=%s file=%s"
                          % (i, j, d, ix, targets[addr(d, ix)], fn), flush=True)
            buf[pj] = oj
            t += 1
            j += 1
            done += 1
            if done % prog == 0:
                print("pid=%d n=%d t=%d rate=%.0f/s" % (os.getpid(), done, t, done / (time.time() - t0)),
                      flush=True)
        buf[pi] = oi
        i += 1
    print("pid=%d DONE %d..%d n=%d in %ds" % (os.getpid(), lo, hi, done, time.time() - t0), flush=True)


def run(start, end, procs=4, idxs=None):
    if idxs is None:
        idxs = [int(x) for x in os.environ.get("INDICES", "0").split(",")]
    base = load_base()
    n = len(letters(base))
    total = n * (n - 1) // 2
    end = min(end, total)
    if start >= end:
        print("empty range %d..%d (total %d)" % (start, end, total), flush=True)
        return
    print("k2 base ok 46a308c2 letters=%d pairs=%d range=%d..%d procs=%d idxs=%s"
          % (n, total, start, end, procs, idxs), flush=True)
    span = end - start
    chunk = span // procs
    jobs = []
    for k in range(procs):
        lo = start + k * chunk
        hi = end if k == procs - 1 else lo + chunk
        jobs.append((lo, hi, idxs, max(1000, (hi - lo) // 10)))
    if procs == 1:
        worker(jobs[0])
    else:
        with mp.Pool(procs) as p:
            p.map(worker, jobs)
    print("SHARD COMPLETE %d..%d" % (start, end), flush=True)


def main():
    procs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    run(int(sys.argv[1]), int(sys.argv[2]), procs)


if __name__ == "__main__":
    main()
