"""Self-contained fast pipeline for the RBB hunt (coincurve + local BIP39 list).

Differences from harness/fast.py: no hardcoded foreign sandbox path, own wordlist,
p2pkh returns the address string, and hash160 is exposed for exact comparison.

Pipeline (certified): text -> MD5 (16 B entropy) -> BIP39 12 words, "" passphrase ->
PBKDF2-SHA512 2048 -> BIP32 m/44'/0'/0'/0/i -> compressed pubkey -> P2PKH.

Self-test (must pass before any run):
    md5 9dd2efb9bc976c2095bd534d7b8d431c @ i=0 -> 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN
    chapter LF2 md5 48d31820...              @ i=0 -> 14isnRimk9qAzpm85qwiFgLjzxL1387TXL
"""
import hashlib, hmac, struct, os

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
H = 0x80000000
ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

_HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = [w.strip() for w in open(os.path.join(_HERE, "bip39_english.txt")) if w.strip()]
assert len(WORDS) == 2048, len(WORDS)

from coincurve import PrivateKey
# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)

# escrows
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
STAGE1 = "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"


def h160(addr):
    """hash160 of a base58 P2PKH address (compare on this, never on strings)."""
    payload = _b58decode(addr)[:-4]
    return payload[1:]


def _b58decode(s):
    n = 0
    for ch in s:
        n = n * 58 + ALPH.index(ch)
    pad = len(s) - len(s.lstrip("1"))
    body = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\x00" * pad + body


def _b58encode(b):
    n = int.from_bytes(b, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = ALPH[r] + s
    return ALPH[0] * (len(b) - len(b.lstrip(b"\x00"))) + s


def mnemonic(ent):
    cs = hashlib.sha256(ent).digest()[0] >> 4
    n = int.from_bytes(ent, "big") << 4 | cs
    tot = len(ent) * 8 // 11 + 1
    return " ".join(WORDS[(n >> (11 * (tot - 1 - i))) & 0x7FF] for i in range(tot))


def seed_from(ent):
    return hashlib.pbkdf2_hmac("sha512", mnemonic(ent).encode(), b"mnemonic", 2048, 64)


def pub(k):
    return PrivateKey(k.to_bytes(32, "big")).public_key.format(compressed=True)


def pubhash(k):
    return hashlib.new("ripemd160", hashlib.sha256(pub(k)).digest()).digest()


def ckd(k, c, i):
    if i >= H:
        data = b"\x00" + k.to_bytes(32, "big") + struct.pack(">I", i)
    else:
        data = pub(k) + struct.pack(">I", i)
    I = hmac.new(c, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + k) % N, I[32:]


def parent(seed, account=0):
    """m/44'/0'/0'/0 -- one PBKDF2 per candidate; indices are then cheap-ish."""
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32], "big"), I[32:]
    for i in (44 | H, account | H, 0 | H, 0):
        k, c = ckd(k, c, i)
    return k, c


def key_at(seed, idx):
    k, c = parent(seed)
    k, _ = ckd(k, c, idx)
    return k


def addr_from_key(k):
    payload = b"\x00" + pubhash(k)
    return _b58encode(payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4])


def wif(k, compressed=True):
    payload = b"\x80" + k.to_bytes(32, "big") + (b"\x01" if compressed else b"")
    return _b58encode(payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4])


def addr(ent, idx=0):
    return addr_from_key(key_at(seed_from(ent), idx))


def addr_md5hex(h, idx=0):
    return addr(bytes.fromhex(h), idx)


def md5h(b):
    return hashlib.md5(b).hexdigest()


if __name__ == "__main__":
    import time
    a = addr_md5hex("9dd2efb9bc976c2095bd534d7b8d431c")
    b = addr_md5hex("48d31820" + "0" * 24)  # placeholder, see note
    print("stage1", a, a == STAGE1)
    base = open(os.path.join(_HERE, "..", "base_chapter_lf.txt"), "rb").read()
    t0 = time.time()
    n = 500
    for i in range(n):
        addr(hashlib.md5(base[:-1] + bytes([base[-1] ^ 0])).digest())
    dt = time.time() - t0
    print(f"{n/dt:.1f} derivations/s over {len(base)} bytes")
    print("live h160", h160(LIVE).hex(), "flag", h160(LIVE).hex()[:8])
