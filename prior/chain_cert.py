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
def wif_c(ent):
    seed=Bip39SeedGenerator(mnem(ent)).Generate("")
    k=K.FromSeed(seed).DerivePath("m/44'/0'/0'/0/0").PrivateKey().Raw().ToBytes()
    v=b'\x80'+k+b'\x01'; return b58(v+hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4])
A=json.load(open('answers_raw.json'))
keys=sorted(A,key=lambda k:(k.split(':')[0],int(k.split(':')[1])))
W={}
for k in keys:
    alg,s=A[k]; W[k]=wif_c(hashlib.new(alg.lower().replace('-',''),s.encode()).digest())
ok=0;pairs=0;miss=[]
for a,b in zip(keys,keys[1:]):
    if a.split(':')[0]!=b.split(':')[0]: continue
    pairs+=1; tail=A[b][1].rstrip()[-3:]
    if W[a].endswith(tail): ok+=1
    else: miss.append((a,b,tail))
print(f'pair audit: {ok}/{pairs} consecutive blocks carry the previous block compressed WIF last-3')
print('misses:',miss[:12])
json.dump(miss,open('chain_misses.json','w'),indent=1)
