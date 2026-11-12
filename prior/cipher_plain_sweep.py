import hashlib,itertools,time
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
def addr(ent,path):
    words=D.entropy_to_words(ent)
    seed=Bip39SeedGenerator(words).Generate("")
    ch=Bip32Slip10Secp256k1.FromSeed(seed).DerivePath(path)
    pub=ch.PrivateKey().PublicKey().RawCompressed().ToBytes()
    h=D.rmd160(hashlib.sha256(pub).digest()); v=b"\x00"+h
    c=hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4]
    return D.b58(v+c)
CT=["Earth","network","infrastructure","nonce"]
PT=["keys","that","again","purposes","budget","emission","this","object","Dorian","them"]
LINK=[""," 62tGor2"," isUB1bT"," gAELXgr"," KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2"]
strings=set()
for ct1 in itertools.combinations(range(4),2):
    rest=[i for i in range(4) if i not in ct1]
    ct2=tuple(rest)
    for pt in itertools.combinations(range(len(PT)),4):
        p1=pt[:2]; p2=pt[2:]
        a=[CT[i] for i in ct1]; b=[CT[i] for i in ct2]
        q1=[PT[i] for i in p1]; q2=[PT[i] for i in p2]
        strings.add(" ".join(a+q1+b+q2))
        strings.add(" ".join(q1+a+q2+b))
print("strings",len(strings))
t0=time.time(); hits=[]; n=0
for s in strings:
    for lk in LINK:
        d=hashlib.md5((s+lk).encode()).digest()
        for i in (0,1):
            a=addr(d,f"m/44'/0'/0'/0/{i}"); n+=1
            if a in (PRIZE,LUCKY): hits.append((s,lk,i))
    if time.time()-t0>240: print("time guard hit"); break
print("derivations",n,"secs",round(time.time()-t0,1),"hits",hits)
