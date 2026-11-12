#!/usr/bin/env python3
"""demo_oracle.py — Grycoin-2 / RBB candidate oracle.

Pipeline (certified on Stage One vector from e1976g): md5(text) -> 16B BIP39 entropy
-> 12 words -> seed (PBKDF2, passphrase 'mnemonic') -> BIP32 path -> P2PKH address.

Modes:
  selftest               verify against e1976g Stage One: md5 9dd2efb9... -> 19TbyN5KCg...
  hash [prefix]          read enum_md5 MATCH lines on stdin (e.g. "MATCH two flips=6,1032 md5=..."),
                         filter by prefix, derive each, compare vs escrow. Print hits.
"""
import sys, hashlib
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1

ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
WL = [l.strip() for l in open("harness/bip39_english.txt")]
ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58(b):
    n = int.from_bytes(b, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = ALPH[r] + s
    pad = 0
    for c in b:
        if c == 0:
            pad += 1
        else:
            break
    return "1" * pad + s


def rmd160(b):
    try:
        return hashlib.new("ripemd160", b).digest()
    except Exception:
        # pure-python RIPEMD-160
        def rol(x, n): return ((x << n) | (x >> (32 - n))) & 0xffffffff
        K1 = [0x00000000, 0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e]
        K2 = [0x50a28be6, 0x5c4dd124, 0x6d703ef3, 0x7a6d76e9, 0x00000000]
        R1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
              7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,
              3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,
              1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,
              4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13]
        R2 = [5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,
              6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,
              15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,
              8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,
              12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11]
        S1 = [11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,
              7,6,8,13,11,12,5,12,2,15,4,11,9,14,5,8,
              15,5,14,11,12,6,11,9,4,8,13,7,15,14,13,10,
              2,7,13,15,12,8,14,4,6,9,1,11,10,5,3,14]
        S2 = [8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,
              9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,
              9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,
              15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8]
        def f1(x,y,z): return x ^ y ^ z
        def f2(x,y,z): return (x & y) | (~x & z)
        def f3(x,y,z): return (x | ~y) ^ z
        def f4(x,y,z): return (x & z) | (y & ~z)
        def f5(x,y,z): return x ^ (y | ~z)
        F1 = [f1,f2,f3,f4,f5]; F2 = [f5,f4,f3,f2,f1]
        P = [0]*16; Q = [0]*16
        for i in range(16): P[i] = int.from_bytes(b[4*i:4*i+4], 'little')
        msg = P + P
        msg[16+5] ^= 0x80000000
        for i in (x for x in range(17,32) if x != 21): msg[i] = 0
        msg[31] = len(b) * 8
        h = [0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0]
        a,b,c,d,e = h; A,B,C,D,E = h
        for j in range(80):
            rnd = j // 16
            T = rol((a + F1[rnd](b,c,d) + e + K1[rnd] + msg[R1[j]]) & 0xffffffff, S1[j]) + b
            a,b,c,d,e = e,T,b,rol(c,10)&0xffffffff,a
            U = rol((A + F2[rnd](B,C,D) + E + K2[rnd] + msg[R2[j]]) & 0xffffffff, S2[j]) + B
            A,B,C,D,E = E,U,B,rol(C,10)&0xffffffff,A
        hh = [(h[0]+a+d)&0xffffffff,(h[1]+b+e)&0xffffffff,(h[2]+c+A)&0xffffffff,
              (h[3]+d+B)&0xffffffff,(h[4]+e+C)&0xffffffff]
        return b"".join(x.to_bytes(4, "little") for x in hh)


def entropy_to_words(d16):
    bits = "".join(f"{x:08b}" for x in d16)
    chk = hashlib.sha256(d16).digest()
    chkbits = f"{chk[0]:08b}"[:4]
    allbits = bits + chkbits
    return " ".join(WL[int(allbits[i:i+11], 2)] for i in range(0, 132, 11))


def derive(d16, path="m/44'/0'/0'/0/0"):
    words = entropy_to_words(d16)
    seed = Bip39SeedGenerator(words).Generate("")
    child = Bip32Slip10Secp256k1.FromSeed(seed).DerivePath(path)
    pub = child.PrivateKey().PublicKey().RawCompressed().ToBytes()
    h160 = rmd160(hashlib.sha256(pub).digest())
    v = b"\x00" + h160
    chk = hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4]
    return words, b58(v + chk)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "selftest":
        words, addr = derive(bytes.fromhex("9dd2efb9bc976c2095bd534d7b8d431c"))
        ok_words = words == "oven number unveil junior item aware finger price estate symbol express degree"
        ok_addr = addr == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"
        print("words:", words, "| ok:", ok_words)
        print("addr:", addr, "| ok:", ok_addr)
        print("SELFTEST", "OK" if (ok_words and ok_addr) else "FAIL")
        sys.exit(0 if (ok_words and ok_addr) else 1)
    elif mode == "hash":
        import re
        prefix = sys.argv[2] if len(sys.argv) > 2 else ""
        n = 0
        for line in sys.stdin:
            m = re.match(r"MATCH (\S+) flips=([\d,]+) md5=([0-9a-f]+)", line.strip())
            if not m:
                continue
            mode_, flips, md5hex = m.groups()
            if prefix and not md5hex.startswith(prefix):
                continue
            n += 1
            words, addr = derive(bytes.fromhex(md5hex))
            if addr == ESCROW:
                print("!!! ESCROW MATCH !!!", mode_, "flips:", flips, "md5:", md5hex, "words:", words, "addr:", addr)
            else:
                print("no", mode_, "flips:", flips, "md5:", md5hex)
        print(f"checked {n} candidates")
