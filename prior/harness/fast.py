import hashlib,hmac,struct,sys
from coincurve import PrivateKey
sys.path.insert(0,'/app/conversations/6ae3ed2b707ef780407c50db/repos/grycoin-rbb-hunt/harness')
import btc as ref   # only for wordlist/mnemonic
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
H=0x80000000
def mnemonic(ent):
    cs=hashlib.sha256(ent).digest()[0]>>4
    n=int.from_bytes(ent,'big')<<4|cs
    tot=len(ent)*8//11+1
    return ' '.join(ref._WORDS[(n>>(11*(tot-1-i)))&0x7FF] for i in range(tot))
def seed_from(ent):
    return hashlib.pbkdf2_hmac('sha512',mnemonic(ent).encode(),b'mnemonic',2048,64)
def pub(k):
    return PrivateKey(k.to_bytes(32,'big')).public_key.format(compressed=True)
def ckd(k,c,i):
    if i>=H:
        data=b'\x00'+k.to_bytes(32,'big')+struct.pack('>I',i)
    else:
        data=pub(k)+struct.pack('>I',i)
    I=hmac.new(c,data,hashlib.sha512).digest()
    return (int.from_bytes(I[:32],'big')+k)%N, I[32:]
def key_at(seed,path=(44+H,0+H,0+H,0,0)):
    I=hmac.new(b'Bitcoin seed',seed,hashlib.sha512).digest()
    k,c=int.from_bytes(I[:32],'big'),I[32:]
    for i in path: k,c=ckd(k,c,i)
    return k
def b58check(payload):
    a='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    chk=hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    num=int.from_bytes(payload+chk,'big'); s=''
    while num: num,r=divmod(num,58); s=a[r]+s
    return '1'*(len(payload+chk)-len((payload+chk).lstrip(b'\x00')))+s
def p2pkh(k):
    p=pub(k)
    return b58check(b'\x00'+hashlib.new('ripemd160',hashlib.sha256(p).digest()).digest())
def addr(ent):
    return p2pkh(key_at(seed_from(ent)))
def addr_md5hex(h):
    return addr(bytes.fromhex(h))
def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()
