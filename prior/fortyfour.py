import hashlib
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
S="1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN"
print("len",len(S),"items",len(S.split()),"items:",S.split())
variants={
 "exact":S,
 "lower":"1A1 efi2dm Hal Finney TS mN ihsotaS otomakaN".lower(),
 "reversed":"NaN otomakaN ihsotaS mN TS yenniF laH MD2ife 1A1",
 "no_mN":S.replace(" mN",""),
 "ts_mn_swapped":"1A1 efi2DM Hal Finney mN TS ihsotaS otomakaN",
 "names_only":"Hal Finney ihsotaS otomakaN",
 "addr_form":"1A1 efi2DM Hal Finney NmST ihsotaS otomakaN",
 "with_nmst":"1A1 efi2DM Hal Finney TS mN NmST ihsotaS otomakaN",
}
LINK=[""," 62tGor2"," isUB1bT"," gAELXgr"," KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2"," isUB1b"," tGor2"," 62tGor"]
hits=[]; n=0
for name,b in variants.items():
    for lk in LINK:
        for tomi in (""," TOMI"):
            for sep in (""," "):
                s=b+tomi+lk if tomi else b+lk
                for alg in ("md5","sha256"):
                    d=hashlib.new(alg,s.encode()).digest()
                    for i in ((0,1,2,6,7) if alg=="md5" else (0,1,2)):
                        a=addr(d,f"m/44'/0'/0'/0/{i}"); n+=1
                        if a in (PRIZE,LUCKY): hits.append((name,lk,tomi,alg,i,s))
print("derivations",n,"hits",hits)
