#!/usr/bin/env python3
"""Unrestricted four-flip closure of the demo (round-2 block 2), sharded.

The demo is the only certified worked example of the block-77 format. Its answer is not
reachable at k<=3 anywhere on either join (285,129,390 documents each, all derived, zero),
and word-edge k=4 is closed too, so unrestricted k=4 is the first unexplored level:
C(1197,4) = 85,111,122,915 documents. The md5 prefix 3c6 screens to 1 in 4096, so only
about 20.8M documents ever need a full PBKDF2 derivation.

Scanning is done by ci/k4global (C, incremental midstate MD5, ~200k docs/s per core);
this driver shards it by ordinal range, derives every 3c6 survivor against the demo and
the two block-77 escrows, and gates on the certified stage-one pair before running.
"""
import hashlib, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import btc
from coincurve import PrivateKey

DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
T = {DEMO: "DEMO", LIVE: "LIVE", OLD: "OLD"}
BASE = os.path.join(HERE, "base_demo.txt")
CERT_MD5 = "7759227d7406d8230d7e3a8f7b9846d7"
CERT_STAGE1 = "9dd2efb9bc976c2095bd534d7b8d431c"


def _pub(k):
    x, y = PrivateKey(k.to_bytes(32, "big")).public_key.point()
    return (x, y)


btc.pubkey = _pub


def addr(d, ix):
    m = btc.entropy_to_mnemonic(bytes.fromhex(d))
    k = btc.derive_path(btc.mnemonic_seed(m, ""),
                        (44 + 0x80000000, 0x80000000, 0x80000000, 0, ix))
    return btc.p2pkh(_pub(k))


def gate():
    got = hashlib.md5(open(BASE, "rb").read()).hexdigest()
    assert got == CERT_MD5, "demo base drift %s" % got
    a = addr(CERT_STAGE1, 0)
    assert a == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN", a
    print("gate OK: demo base 7759227d, stage-one calibration 19TbyN5", flush=True)


def run(start, end, join, idxs):
    if join != "lf":
        print("skip join=%s under K4D (LF demo substrate only)" % join, flush=True)
        return
    gate()
    binp = os.path.join(HERE, "k4global")
    if not os.path.exists(binp):
        subprocess.run(["gcc", "-O2", "-o", binp, os.path.join(HERE, "k4global.c")],
                       check=True)
    out = os.path.join(HERE, "k4d_hits_%d_%d.txt" % (start, end))
    if os.path.exists(out):
        os.remove(out)
    print("scan ordinals %d..%d" % (start, end), flush=True)
    subprocess.run([binp, BASE, str(start), str(end), out, "19800"], check=True)
    if not os.path.exists(out):
        print("no survivors in range", flush=True)
        return
    seen = set()
    hits = 0
    n = 0
    for line in open(out):
        parts = line.split()
        if len(parts) != 5:
            continue
        h = parts[4]
        if h in seen:
            continue
        seen.add(h)
        n += 1
        for ix in idxs:
            a = addr(h, ix)
            if a in T:
                hits += 1
                rec = "***HIT %s md5=%s pos=%s idx=%d addr=%s" % (
                    T[a], h, ",".join(parts[:4]), ix, a)
                print(rec, flush=True)
                open(os.path.join(HERE, "K4D_SOLUTION.txt"), "a").write(rec + "\n")
        if n % 20000 == 0:
            print("  derived %d/%d" % (n, len(seen)), flush=True)
    print("DONE range %d..%d survivors=%d hits=%d" % (start, end, n, hits), flush=True)
