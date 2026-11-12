import hashlib,itertools
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
WL=D.WL
AB={chr(65+i):chr(90-i) for i in range(26)}
def atb(w): return "".join(AB.get(c.upper(),c).lower() if c.isalpha() else c for c in w)
def w24(d32):
    bits="".join(f"{b:08b}" for b in d32); chk=hashlib.sha256(d32).digest()
    allb=bits+f"{chk[0]:08b}"[:8]
    return " ".join(WL[int(allb[i:i+11],2)] for i in range(0,264,11))
def addr(ent,path):
    words=D.entropy_to_words(ent) if len(ent)==16 else w24(ent)
    seed=Bip39SeedGenerator(words).Generate("")
    ch=Bip32Slip10Secp256k1.FromSeed(seed).DerivePath(path)
    pub=ch.PrivateKey().PublicKey().RawCompressed().ToBytes()
    h=D.rmd160(hashlib.sha256(pub).digest()); v=b"\x00"+h
    c=hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4]
    return D.b58(v+c)
A=["Today,","Satoshi's","true","identity"]
B=["I","recognize","the","signs."]
LINK=[""," 62tGor2"," isUB1bT"," gAELXgr",
      " KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2"]
strings=set()
for ca in itertools.combinations(range(4),2):
    for cb in itertools.combinations(range(4),2):
        wa=[atb(w) if i in ca else w for i,w in enumerate(A)]
        wb=[atb(w) if i in cb else w for i,w in enumerate(B)]
        strings.add(" ".join(wa+wb))
        strings.add(" ".join(wb+wa))
print("strings",len(strings),"example:",sorted(strings)[0])
hits=[];n=0
for s in strings:
    for lk in LINK:
        for alg in ("md5","sha256"):
            d=hashlib.new(alg,(s+lk).encode()).digest()
            for i in ((0,1,2,6,7) if alg=="md5" else (0,1,2)):
                a=addr(d,f"m/44'/0'/0'/0/{i}"); n+=1
                if a in (PRIZE,LUCKY): hits.append((s,lk,alg,i))
print("derivations",n,"hits",hits)
