"""Fast rule-family probe for the RBB (coincurve backend), 2026-10-31.

Pipeline (certified): text -> MD5 (16 bytes = entropy) -> BIP39 12 words (empty
passphrase) -> PBKDF2-SHA512/2048 -> m/44'/0'/0'/0/i -> P2PKH compressed.

Self-tests that MUST pass before any sweep:
  stage one : md5 9dd2efb9bc976c2095bd534d7b8d431c @ idx0 -> 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN
  chapter   : LF\\n\\n join md5 48d31820...              @ idx0 -> 14isnRimk9qAzpm85qwiFgLjzxL1387TXL
"""
import hashlib, hmac, json, sys, itertools
from coincurve import PrivateKey

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

WL = [w.strip() for w in open("harness/bip39_english.txt", encoding="utf-8") if w.strip()]
assert len(WL) == 2048, len(WL)
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
STAGE1 = "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58(b):
    n = int.from_bytes(b, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = B58[r] + s
    pad = len(b) - len(b.lstrip(b"\0"))
    return "1" * pad + s


def md5b(t):
    return hashlib.md5(t.encode("utf-8")).digest()


def entropy_to_mnemonic(e):
    h = hashlib.sha256(e).digest()
    bits = bin(int.from_bytes(e + h[:1], "big"))[2:].zfill(132)
    return [WL[int(bits[i:i + 11], 2)] for i in range(0, 132, 11)]


def seed_from_mnemonic(m):
    return hashlib.pbkdf2_hmac("sha512", " ".join(m).encode(), b"mnemonic", 2048)


def master(seed):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return int.from_bytes(I[:32], "big"), I[32:]


def ckd_priv(k, c, i):
    if i >= 0x80000000:
        data = b"\0" + k.to_bytes(32, "big") + i.to_bytes(4, "big")
    else:
        pub = PrivateKey(k.to_bytes(32, "big")).public_key.format(compressed=True)
        data = pub + i.to_bytes(4, "big")
    I = hmac.new(c, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + k) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141, I[32:]


H = 0x80000000
PATH = [44 + H, 0 + H, 0 + H, 0]


def addr_at(entropy, idx):
    m = entropy_to_mnemonic(entropy)
    k, c = master(seed_from_mnemonic(m))
    for j in PATH:
        k, c = ckd_priv(k, c, j)
    k, c = ckd_priv(k, c, idx)
    pub = PrivateKey(k.to_bytes(32, "big")).public_key.format(compressed=True)
    return b58(b"\0" + hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest() +
               hashlib.sha256(hashlib.sha256(b"\0" + hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()).digest()).digest()[:4])


def check(t, idxs=(0,), label="", hits=None):
    a = md5b(t)
    for i in idxs:
        got = addr_at(a, i)
        if got in (LIVE, OLD):
            print("HIT!! %s idx%d -> %s  md5=%s" % (label, i, got, a.hex()))
            if hits is not None:
                hits.append((label, i, got, a.hex()))
            return True
    return False


if __name__ == "__main__":
    # --- self-tests ---
    a = addr_at(bytes.fromhex("9dd2efb9bc976c2095bd534d7b8d431c"), 0)
    print("stage-one selftest:", a, "PASS" if a == STAGE1 else "FAIL")
    paras = json.load(open("chapter_paras_exact.json", encoding="utf-8"))
    base = "\n\n".join(p.strip() for p in paras)
    print("lf-join md5:", md5b(base).hex(), "chars", len(base))
    print("chapter selftest:", addr_at(md5b(base), 0),
          "PASS" if addr_at(md5b(base), 0) == "14isnRimk9qAzpm85qwiFgLjzxL1387TXL" else "FAIL")
