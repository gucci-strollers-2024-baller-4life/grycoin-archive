#!/usr/bin/env python3
"""RTL-suffixed subset sweep, shardable. Usage: rtl_ci.py START END JOIN IDX,IDX
Space: integer masks over the 24 F/W sign-violating paragraphs. Certified mechanic
(head letter down, terminal letter up) applied to the selected paragraphs, join,
append the literal suffix " RTL", md5, BIP39, BIP32, P2PKH, compare to the escrow."""
import sys, os, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import btc
from coincurve import PrivateKey

def _pub(k):
    x, y = PrivateKey(k.to_bytes(32, 'big')).public_key.point()
    return (x, y)
btc.pubkey = _pub

ESC = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
V1T = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
VIOL = [4,5,6,7,69,92,93,94,95,99,101,105,119,131,138,167,168,169,170,231,232,234,235,258]
N = len(VIOL)
_RAW = os.environ.get("RTL_SUFFIX", " RTL")
V1 = (_RAW == "V1")
SUF = b"" if _RAW in ("NONE", "V1") else _RAW.encode()
Hc = 0x80000000

def flips(p):
    a = [i for i, c in enumerate(p) if c.isalpha()]
    if not a:
        return p
    c = list(p)
    c[a[0]] = c[a[0]].lower()
    c[a[-1]] = c[a[-1]].upper()
    return "".join(c)

def addr(d, ix):
    n = int(btc.entropy_to_mnemonic(bytes.fromhex(d)).replace(" ", "\x00").split("\x00")[0]) if False else None
    m = btc.entropy_to_mnemonic(bytes.fromhex(d))
    k = btc.derive_path(btc.mnemonic_seed(m, ""), (44+Hc, 0+Hc, 0+Hc, 0, ix))
    return btc.p2pkh(_pub(k))

def main():
    start = int(sys.argv[1]); end = int(sys.argv[2])
    join = sys.argv[3]; idxs = [int(x) for x in sys.argv[4].split(',')]
    sep = b"\r\n" if V1 else (b"\r\n\r\n" if join == 'crlf' else b"\n\n")
    if V1 and join == 'lf':
        print('skip duplicate join under V1'); return
    P = open(os.path.join(HERE, 'base_chapter_lf.txt'), encoding='utf-8').read().split("\n\n")
    assert len(P) == 273
    assert sum(len(p) for p in P) + 2*(len(P)-1) == 45450, "substrate drift"
    norm = [p.encode() for p in P]
    flip = [flips(p).encode() for p in P]
    t0 = time.time(); n = 0
    for mask in range(start, min(end, 1 << N)):
        full = []
        vm = 0
        for i in range(273):
            if vm < N and i == VIOL[vm]:
                full.append(flip[vm] if (mask >> vm) & 1 else norm[i]); vm += 1
            else:
                full.append(norm[i])
        body = sep.join(full) + SUF
        d = hashlib.md5(body).hexdigest()
        n += 1
        for ix in idxs:
            if addr(d, ix) == (V1T if V1 else ESC):
                print("***HIT mask=%d join=%s idx=%d md5=%s" % (mask, join, ix, d), flush=True)
        if n % 25000 == 0:
            print("n=%d mask=%d rate=%.0f/s" % (n, mask, n/(time.time()-t0)), flush=True)
    print("DONE %s %d..%d n=%d in %ds" % (join, start, end, n, time.time()-t0), flush=True)

if __name__ == '__main__':
    main()
