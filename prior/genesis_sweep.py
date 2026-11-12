import hashlib, itertools
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
WL=D.WL
def w24(d32):
    bits="".join(f"{b:08b}" for b in d32); chk=hashlib.sha256(d32).digest()
    allb=bits+f"{chk[0]:08b}"[:8]
    return " ".join(WL[int(allb[i:i+11],2)] for i in range(0,264,11))
def addr(ent, path):
    words = D.entropy_to_words(ent) if len(ent)==16 else w24(ent)
    seed=Bip39SeedGenerator(words).Generate("")
    ch=Bip32Slip10Secp256k1.FromSeed(seed).DerivePath(path)
    pub=ch.PrivateKey().PublicKey().RawCompressed().ToBytes()
    h=D.rmd160(hashlib.sha256(pub).digest())
    v=b"\x00"+h; c=hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4]
    return D.b58(v+c), words
TOK=["NmST","efi2DM","efiYDM","efiYNN","DN","NN","Aa","1A1","Hal Finney","HalFinney",
     "ihsotaS otomakaN","Satoshinakamoto","Aoi Nakamoto","SATOSHI","NAKAMOTO"]
LINK=[""," 62tGor2"," isUB1bT"," gAELXgr"," KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2"]
cands=set()
for t in TOK: cands.add(t)
for a,b in itertools.permutations(TOK,2):
    cands.add(a+" "+b); cands.add(a+" TOMI "+b); cands.add(a+b)
hits=[]; n=0
for base in cands:
    for lk in LINK:
        s=base+lk
        for alg in ("md5","sha256"):
            d=hashlib.new(alg, s.encode()).digest()
            idxs=(0,1,2,6,7) if alg=="md5" else (0,1,2)
            for i in idxs:
                a,words=addr(d, f"m/44'/0'/0'/0/{i}"); n+=1
                if a in (PRIZE,LUCKY): hits.append((s,alg,i,words))
print("candidates",len(cands),"derivations",n,"hits",hits)
