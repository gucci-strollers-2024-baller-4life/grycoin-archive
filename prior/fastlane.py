"""Fast certified lane: md5hex -> BIP39 -> seed -> m/44'/0'/0'/0/i -> P2PKH (coincurve)."""
import hashlib, hmac, struct, os
import coincurve
_B58=b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_WORDS=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"harness","bip39_english.txt")).read().split()
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
def b58check(p):
    c=hashlib.sha256(hashlib.sha256(p).digest()).digest()[:4]
    n=int.from_bytes(p+c,"big"); o=bytearray()
    while n: n,r=divmod(n,58); o.append(_B58[r])
    for b in p:
        if b==0: o.append(_B58[0])
        else: break
    return bytes(o[::-1]).decode()
def mnemonic(ent):
    cs=hashlib.sha256(ent).digest()[0]>>4
    n=(int.from_bytes(ent,"big")<<4)|cs
    t=len(ent)*8//11+1
    return " ".join(_WORDS[(n>>(11*(t-1-i)))&0x7FF] for i in range(t))
def seed_of(m): return hashlib.pbkdf2_hmac("sha512", m.encode(), b"mnemonic", 2048, 64)
def ckd(k,c,i):
    if i>=0x80000000: d=b"\x00"+k.to_bytes(32,"big")+struct.pack(">I",i)
    else: d=coincurve.PublicKey.from_valid_secret(k.to_bytes(32,"big")).format(compressed=True)+struct.pack(">I",i)
    I=hmac.new(c,d,hashlib.sha512).digest()
    return (int.from_bytes(I[:32],"big")+k)%N, I[32:]
H=0x80000000
def addr(md5hex, path=(44+H,0+H,0+H,0,0)):
    m=mnemonic(bytes.fromhex(md5hex)); I=hmac.new(b"Bitcoin seed", seed_of(m), hashlib.sha512).digest()
    k,c=int.from_bytes(I[:32],"big"), I[32:]
    for i in path: k,c=ckd(k,c,i)
    raw=coincurve.PublicKey.from_valid_secret(k.to_bytes(32,"big")).format(compressed=True)
    return b58check(b"\x00"+hashlib.new("ripemd160",hashlib.sha256(raw).digest()).digest())
if __name__=="__main__":
    print("stage1     :", addr("9dd2efb9bc976c2095bd534d7b8d431c"), "expect 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN")
    print("chapter24  :", addr("95f52c6d420da1c078bc381315fda562"), "expect 1KhpoRgnQSaEGbjcAn8GrXX71jv6pXkack")
