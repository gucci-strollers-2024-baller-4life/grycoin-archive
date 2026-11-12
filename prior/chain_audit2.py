import json,hashlib
import demo_oracle as D
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1 as K
WL=D.WL; ALPH="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58(b):
    n=int.from_bytes(b,'big'); s=''
    while n: n,r=divmod(n,58); s=ALPH[r]+s
    return ALPH[0]*(len(b)-len(b.lstrip(b'\x00')))+s
def mnem(e):
    n=len(e)*8; cs=n//32
    bits=''.join(f'{x:08b}' for x in e)+''.join(f'{x:08b}' for x in hashlib.sha256(e).digest())[:cs]
    return ' '.join(WL[int(bits[i:i+11],2)] for i in range(0,len(bits),11))
def wif(ent):
    seed=Bip39SeedGenerator(mnem(ent)).Generate("")
    k=K.FromSeed(seed).DerivePath("m/44'/0'/0'/0/0").PrivateKey().Raw().ToBytes()
    v=b'\x80'+k; return b58(v+hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4])
A=json.load(open('answers_raw.json'))
keys=sorted(A,key=lambda k:(k.split(':')[0],int(k.split(':')[1])))
mins={}
for k in keys:
    alg,s=A[k]; ent=hashlib.new(alg.lower().replace('-',''),s.encode()).digest()
    mins[k]=(wif(ent),ent.hex())
ok3=ok7=okfull=0; pairs=0; misses=[]
for a,b in zip(keys,keys[1:]):
    if a.split(':')[0]!=b.split(':')[0]: continue
    pairs+=1; W=mins[a][0]; H=mins[a][1]; s=A[b][1].rstrip()
    m3 = s.endswith(W[-3:]) or s.endswith(H[-3:])
    m7 = s.endswith(W[-7:]) or s.endswith(H[-7:])
    mf = s.endswith(W) or s.endswith(H)
    ok3+=m3; ok7+=m7; okfull+=mf
    if not (m3 or m7 or mf): misses.append((a,b,s[-14:]))
print(f'consecutive pairs audited: {pairs}')
print(f'  next block ends with prev WIF/hex last3 : {ok3}')
print(f'  ... last7 : {ok7}   ... full : {okfull}')
print(f'  unexplained : {len(misses)}')
for a,b,t in misses[:10]: print('   ',a,'->',b,'tail',repr(t))
