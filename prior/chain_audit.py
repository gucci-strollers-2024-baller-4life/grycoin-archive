import json,hashlib,re,os
import demo_oracle as D
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1 as K
WL=D.WL
ALPH="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
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
rows=[]
for key in sorted(A,key=lambda k:(k.split(':')[0],int(k.split(':')[1]))):
    alg,s=A[key]; ent=hashlib.new(alg.lower().replace('-',''),s.encode()).digest()
    W=wif(ent); tail=s.split()[-1]
    rows.append((key,alg,tail,W))
print(f"{'block':<7}{'link field':<56}{'matches own key?'}")
ok=0; bad=[]
for i,(key,alg,tail,W) in enumerate(rows):
    nxt=rows[i+1] if i+1<len(rows) else None
    tgt=nxt[2] if nxt and nxt[0].split(':')[0]==key.split(':')[0] else None
    match = tgt is not None and (tgt==W or W.endswith(tgt) or W.endswith(tgt[-7:]))
    if match: ok+=1
    else: bad.append((key,tgt or '-',W[-12:]))
    print(f"{key:<7}{tail[:52]:<56}{'YES' if match else 'no'}")
print('\nchained links validated:',ok,'of',len(rows)-1,'consecutive pairs')
print('unvalidated pairs:',bad[:8])
