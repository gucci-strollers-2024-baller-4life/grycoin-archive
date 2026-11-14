"""Minimal, dependency-free Bitcoin key pipeline for the RBB hunt.

Pipeline (certified in the hunt docs):
    text -> MD5 (16 bytes) -> BIP39 12 words -> PBKDF2-SHA512(pass="") ->
    BIP32 m/44'/0'/0'/0/i -> P2PKH address

Self-test targets (must pass):
    md5 9dd2efb9bc976c2095bd534d7b8d431c  @ m/44'/0'/0'/0/0 -> 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN
    chapter (\\n\\n) md5 48d31820...        @ m/44'/0'/0'/0/0 -> 14isnRimk9qAzpm85qwiFgLjzxL1387TXL
"""
import hashlib, hmac, struct, os

# ---------- secp256k1 (fixed-base comb, private-key->pubkey only) ----------
P  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def _inv(a, m=P):
    return pow(a, m - 2, m)


def _add(p, q):
    if p is None:
        return q
    if q is None:
        return p
    if p[0] == q[0]:
        if (p[1] + q[1]) % P == 0:
            return None
        lam = 3 * p[0] * p[0] % P * _inv(2 * p[1]) % P
    else:
        lam = (q[1] - p[1]) % P * _inv((q[0] - p[0]) % P) % P
    x = (lam * lam - p[0] - q[0]) % P
    return (x, (lam * (p[0] - x) - p[1]) % P)


def _build_table():
    """T[j][i] = i * 16^j * G, j = 0..63, i = 0..15."""
    table = []
    base = (Gx, Gy)
    for _ in range(64):
        row = [None]
        cur = None
        for _i in range(1, 16):
            cur = _add(cur, base)
            row.append(cur)
        table.append(row)
        # base *= 16
        b = base
        for _i in range(4):
            b = _add(b, b)
        base = b
    return table


_TABLE = _build_table()


def pubkey(k):
    k %= N
    if k == 0:
        raise ValueError("zero key")
    acc = None
    j = 0
    while k:
        nib = k & 0xF
        if nib:
            acc = _add(acc, _TABLE[j][nib])
        k >>= 4
        j += 1
    return acc


# ---------- base58 ----------
_B58 = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58check(payload: bytes) -> str:
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    num = int.from_bytes(payload + chk, "big")
    out = bytearray()
    while num:
        num, rem = divmod(num, 58)
        out.append(_B58[rem])
    for b in payload:
        if b == 0:
            out.append(_B58[0])
        else:
            break
    return (out[::-1]).decode()


def _compressed(pub) -> bytes:
    x, y = pub
    return bytes([2 + (y & 1)]) + x.to_bytes(32, "big")


def p2pkh(pub) -> str:
    raw = _compressed(pub)
    h = hashlib.new("ripemd160", hashlib.sha256(raw).digest()).digest()
    return b58check(b"\x00" + h)


def hash160(k: int) -> bytes:
    raw = _compressed(pubkey(k))
    return hashlib.new("ripemd160", hashlib.sha256(raw).digest()).digest()


# ---------- BIP39 ----------
_WORDS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bip39_english.txt")).read().split()


def entropy_to_mnemonic(ent: bytes) -> str:
    cs = hashlib.sha256(ent).digest()[0] >> 4
    n = int.from_bytes(ent, "big") << 4 | cs
    total = len(ent) * 8 // 11 + 1
    return " ".join(_WORDS[(n >> (11 * (total - 1 - i))) & 0x7FF] for i in range(total))


def mnemonic_seed(mnemonic: str, passphrase: str = "") -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha512", mnemonic.encode("utf-8"), ("mnemonic" + passphrase).encode("utf-8"), 2048, 64
    )


# ---------- BIP32 (private-only derivation) ----------
def master_key(seed: bytes):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return int.from_bytes(I[:32], "big"), I[32:]


def ckd_priv(k: int, c: bytes, i: int):
    if i >= 0x80000000:
        data = b"\x00" + k.to_bytes(32, "big") + struct.pack(">I", i)
    else:
        x, y = pubkey(k)
        data = b"\x02" if y % 2 == 0 else b"\x03"
        data += x.to_bytes(32, "big") + struct.pack(">I", i)
    I = hmac.new(c, data, hashlib.sha512).digest()
    ki = (int.from_bytes(I[:32], "big") + k) % N
    return ki, I[32:]


def derive_path(seed: bytes, path):
    k, c = master_key(seed)
    for i in path:
        k, c = ckd_priv(k, c, i)
    return k


H = 0x80000000
DEFAULT_PATH = (44 + H, 0 + H, 0 + H, 0, 0)  # m/44'/0'/0'/0/0


# ---------- text pipeline ----------
def md5_hex(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def addr_from_md5hex(h: str, path=DEFAULT_PATH) -> str:
    m = entropy_to_mnemonic(bytes.fromhex(h))
    return p2pkh(pubkey(derive_path(mnemonic_seed(m), path)))


def addr_from_text(text: str, path=DEFAULT_PATH) -> str:
    return addr_from_md5hex(md5_hex(text), path)


def wif_from_md5hex(h: str, path=DEFAULT_PATH) -> str:
    m = entropy_to_mnemonic(bytes.fromhex(h))
    k = derive_path(mnemonic_seed(m), path)
    return b58check(b"\x80" + k.to_bytes(32, "big") + b"\x01")


if __name__ == "__main__":
    # --- self tests ---
    a = addr_from_md5hex("9dd2efb9bc976c2095bd534d7b8d431c")
    print("stage1 addr:", a, "OK" if a == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN" else "FAIL")
    print("stage1 WIF :", wif_from_md5hex("9dd2efb9bc976c2095bd534d7b8d431c"))
    m = entropy_to_mnemonic(bytes.fromhex("9dd2efb9bc976c2095bd534d7b8d431c"))
    print("stage1 mnem:", m)
