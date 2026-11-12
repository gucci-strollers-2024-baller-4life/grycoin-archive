import hashlib,itertools,time,multiprocessing as mp
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
def work(s):
    out=[]
    for lk in LINKS:
        d=hashlib.md5((s+lk).encode()).digest()
        for i in (0,1,2):
            a=addr(d,i)
            if a in (PRIZE,LUCKY): out.append((s,lk,i,a))
    return out
if __name__=="__main__":
    tasks=[a+" "+b for a in S1 for b in S2]
    print("strings",len(tasks),"expected derivations",len(tasks)*len(LINKS)*3,flush=True)
    t0=time.time(); hits=[]; done=0
    with mp.Pool(8) as pool:
        for r in pool.imap_unordered(work,tasks,chunksize=200):
            done+=1
            if r: hits+=r; print("HIT",r,flush=True)
            if done%5000==0: print(f"  {done}/{len(tasks)} {time.time()-t0:.0f}s",flush=True)
    print("DONE",done,"derivations",done*len(LINKS)*3,"secs",round(time.time()-t0,1),"HITS",hits,flush=True)
