import hashlib,itertools,time
import demo_oracle as D
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1 as K
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
WL=D.WL
C1=["1A1","efi2DM","efiYDM","efiYNN"]; P1=["Hal","Finney","TOM"]
C2=["TS","mN","NmST"]; P2=["Satoshi","Nakamoto"]
LINKS=[""," 62tGor2"," isUB1bT"," gAELXgr"," 19TbyN5"," KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2"]
def mnem(e):
    n=len(e)*8; cs=n//32
    b=''.join(f'{x:08b}' for x in e)+''.join(f'{x:08b}' for x in hashlib.sha256(e).digest())[:cs]
    return ' '.join(WL[int(b[i:i+11],2)] for i in range(0,len(b),11))
def addr(e,i):
    seed=Bip39SeedGenerator(mnem(e)).Generate("")
    ch=K.FromSeed(seed).DerivePath(f"m/44'/0'/0'/0/{i}")
    pub=ch.PrivateKey().PublicKey().RawCompressed().ToBytes()
    h=D.rmd160(hashlib.sha256(pub).digest()); v=b"\x00"+h
    return D.b58(v+hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4])
S1=[" ".join(x) for c in itertools.combinations(C1,2) for p in itertools.combinations(P1,2) for x in itertools.permutations(tuple(c)+tuple(p))]
S2=[" ".join(x) for c in itertools.combinations(C2,2) for x in itertools.permutations(tuple(c)+tuple(P2))]
tasks=[a+" "+b for a in S1 for b in S2]
tail=tasks[24000:]
print("tail",len(tail),flush=True)
t0=time.time();hits=[];n=0
for s in tail:
    for lk in LINKS:
        d=hashlib.md5((s+lk).encode()).digest()
        for i in (0,1,2):
            if addr(d,i) in (PRIZE,LUCKY): hits.append((s,lk,i))
            n+=1
print("derivations",n,"secs",round(time.time()-t0,1),"HITS",hits,flush=True)
