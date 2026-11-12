import json,hashlib
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
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
P=[t for _,t in json.load(open('wp_paras.json'))]
CAND=[222,225,226,229,230,236,240,241,242,245,246]
LINK=[""," 62tGor2"," isUB1bT"," gAELXgr"," KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2"]
hits=[];n=0
for pno in CAND:
    t=P[pno-1]; w=t.split()
    if len(w)<8: continue
    for form in (" ".join(w[:4]+w[-4:]), " ".join(w[-4:]+w[:4]),
                 " ".join(w[:4])+" "+" ".join(w[-4:]).replace(",","").replace(".","")):
        for lk in LINK:
            for alg in ("md5","sha256"):
                d=hashlib.new(alg,(form+lk).encode()).digest()
                for i in ((0,1,2,6,7) if alg=="md5" else (0,1,2)):
                    a=addr(d,f"m/44'/0'/0'/0/{i}"); n+=1
                    if a in (PRIZE,LUCKY): hits.append((pno,form,lk,alg,i))
print("derivations",n,"hits",hits)
for pno in CAND:
    w=P[pno-1].split()
    if len(w)>=8: print(f'  p{pno}: {" ".join(w[:4])} | {" ".join(w[-4:])}')
