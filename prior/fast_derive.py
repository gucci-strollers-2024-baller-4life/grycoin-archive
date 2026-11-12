"""Fast certified derive: 16B md5 -> BIP39(12 words, cksum) -> PBKDF2 seed -> m/44'/0'/0'/0/0 -> P2PKH."""
import hashlib, hmac
from coincurve import PrivateKey

WL = [l.strip() for l in open("ninjaops-puzzle-lanes/bip39_english.txt")]
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def entropy_to_words(d16):
    bits = "".join(f"{x:08b}" for x in d16)
    chk = hashlib.sha256(d16).digest()
    allbits = bits + f"{chk[0]:08b}"[:4]
    return " ".join(WL[int(allbits[i:i+11], 2)] for i in range(0, 132, 11))

def b58(b):
    n = int.from_bytes(b, "big"); s = ""
    while n: n, r = divmod(n, 58); s = ALPH[r] + s
    pad = 0
    for c in b:
        if c == 0: pad += 1
        else: break
    return "1"*pad + s

def rmd160(b):
    try: return hashlib.new("ripemd160", b).digest()
    except Exception: raise

def derive_addr(d16, passphrase=""):
    words = entropy_to_words(d16)
    seed = hashlib.pbkdf2_hmac('sha512', words.encode(), ('mnemonic'+passphrase).encode(), 2048)
    I = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    k, c = I[:32], I[32:]
    for idx in (0x8000002C, 0x80000000, 0x80000000, 0, 0):
        if idx >= 0x80000000:
            data = b'\x00' + k + idx.to_bytes(4,'big')
        else:
            data = PrivateKey(k).public_key.format(compressed=True) + idx.to_bytes(4,'big')
        I2 = hmac.new(c, data, hashlib.sha512).digest()
        k = ((int.from_bytes(I2[:32],'big') + int.from_bytes(k,'big')) % N).to_bytes(32,'big')
        c = I2[32:]
    pub = PrivateKey(k).public_key.format(compressed=True)
    h160 = rmd160(hashlib.sha256(pub).digest())
    v = b'\x00' + h160
    chk = hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4]
    return words, b58(v + chk)

if __name__ == '__main__':
    words, addr = derive_addr(bytes.fromhex('9dd2efb9bc976c2095bd534d7b8d431c'))
    ok = addr == '19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN' and words == 'oven number unveil junior item aware finger price estate symbol express degree'
    print(words); print(addr, "| SELFTEST", "OK" if ok else "FAIL")
    import time
    t=time.time()
    for i in range(1000): derive_addr(bytes([i%256]*16))
    print(f"{1000/(time.time()-t):.0f} derives/s")
