"""Fast BIP39/BIP44 derivation for the Grycoin hunt. Drop-in for demo_oracle.derive().

Speed comes from: direct hashlib.pbkdf2_hmac (C), manual BIP32 with hmac-sha512,
coincurve for the EC point, and the m/44'/0'/0'/0 parent derived once per candidate
so extra indices cost one HMAC plus one EC multiply.
"""
import hashlib, hmac, struct
from coincurve import PrivateKey

WORDLIST = [w.strip() for w in open("harness/bip39_english.txt")]
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def words_from_entropy(ent: bytes) -> str:
    bits = "".join(f"{b:08b}" for b in ent)
    chk = hashlib.sha256(ent).digest()
    nbits = len(ent) * 8 // 32
    bits += "".join(f"{b:08b}" for b in chk)[:nbits]
    return " ".join(WORDLIST[int(bits[i:i+11], 2)] for i in range(0, len(bits), 11))

def _b58(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = ALPH[r] + s
    pad = len(b) - len(b.lstrip(b"\x00"))
    return ALPH[0] * pad + s

def _child(priv: int, chain: bytes, index: int):
    data = (b"\x00" + priv.to_bytes(32, "big") if index >= 0x80000000
            else PrivateKey(priv.to_bytes(32, "big")).public_key.format(True)) + struct.pack(">I", index)
    I = hmac.new(chain, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + priv) % N, I[32:]

def parent(ent: bytes):
    """m/44'/0'/0'/0 — everything the RBB chain needs, once per entropy."""
    seed = hashlib.pbkdf2_hmac("sha512", words_from_entropy(ent).encode(), b"mnemonic", 2048)
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    priv, chain = int.from_bytes(I[:32], "big"), I[32:]
    for idx in (0x80000000 | 44, 0x80000000 | 0, 0x80000000 | 0, 0):
        priv, chain = _child(priv, chain, idx)
    return priv, chain

def address(priv: int) -> str:
    pub = PrivateKey(priv.to_bytes(32, "big")).public_key.format(True)
    h = hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()
    payload = b"\x00" + h
    return _b58(payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4])

def wif(priv: int, compressed: bool = True) -> str:
    payload = b"\x80" + priv.to_bytes(32, "big") + (b"\x01" if compressed else b"")
    return _b58(payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4])

def derive(ent: bytes, path: str = "m/44'/0'/0'/0/0"):
    """Drop-in for demo_oracle.derive: returns (mnemonic, address), same as the oracle."""
    priv, chain = parent(ent)
    i = int(path.rstrip("/").split("/")[-1])
    p, _ = _child(priv, chain, i)
    return words_from_entropy(ent), address(p)

def addresses(ent: bytes, indices):
    """All requested indices from one parent derivation — much cheaper than N derive() calls."""
    priv, chain = parent(ent)
    out = {}
    for i in indices:
        p, _ = _child(priv, chain, i)
        out[i] = address(p)
    return out


def check() -> bool:
    """Self-test against the certified stage-one pair. Print before trusting any negative."""
    ent = hashlib.md5(open("safudev_stage1.txt", "rb").read()).digest()
    assert ent.hex().startswith("9dd2efb9"), ent.hex()
    ok = addresses(ent, [0])[0] == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"
    print("fastderive self-test:", "PASS" if ok else "FAIL")
    return ok
