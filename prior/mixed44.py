import hashlib,itertools
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
WL=D.WL
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
S=["1A1 efi2DM Hal Finney TS mN Satoshi Nakamoto",
   "1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN",
   "1A1 efi2DM Hal Finney mN TS ihsotaS otomakaN",
   "1A1 efi2DM Hal Finney mN TS Satoshi Nakamoto",
   "otomakaN ihsotaS mN TS Finney Hal efi2DM 1A1",
   "otomakaN ihsotaS TS mN Finney Hal efi2DM 1A1",
   "Satoshi Nakamoto TS mN Hal Finney efi2DM 1A1",
   "1A1 efi2DM TOM RIDDLE TS mN ihsotaS otomakaN",
   "1A1 efi2DM hal finney TS mN ihsotaS otomakaN",
   "1A1 efi2DM Hal Finney TS mN NmST",
   "1A1 efi2DM Hal Finney TS mN Nm ST",
   "1A1 efi2DM Hal Finney TS mN NmST Satoshi",
   "1A1efi2DMHal FinneyTSmNihsotaSotomakaN",
   "1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN TOMI",
   "1A1 TOM efi2DM Finney TS mN ihsotaS otomakaN"]
LINK=[""," 62tGor2"," isUB1bT"," gAELXgr"," KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2"]
hits=[];n=0
for b in S:
    for lk in LINK:
        for alg in ("md5","sha256"):
            d=hashlib.new(alg,(b+lk).encode()).digest()
            for i in ((0,1,2,6,7) if alg=="md5" else (0,1,2)):
                a=addr(d,f"m/44'/0'/0'/0/{i}"); n+=1
                if a in (PRIZE,LUCKY): hits.append((b,lk,alg,i))
print("derivations",n,"hits",hits)
for b in S[:5]: print(len(b),repr(b))
