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
HEAD=["Today, Satoshi's true identity","Today, Satoshi's real identity","Today Satoshi's true identity",
      "Today, Satoshi's true identity,","today, satoshi's true identity","Today, Satoshis true identity"]
TAIL=["I recognize the signs.","so I recognize the signs.","I recognize the signs","i recognize the signs.",
      "So I recognize the signs.","and I recognize the signs."]
LINK=[""," 62tGor2"," isUB1bT"," gAELXgr",
      " KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2",
      " Kx2YSerLwDfLvwLji6Ci4poW28hcbhnVC4yN8Q2i9HhwbisUB1bT"]
strings=set()
for h in HEAD:
    for t in TAIL:
        for s in (h+" "+t, t+" "+h, h+" "+t+" TOMI", h+" TOMI "+t):
            strings.add(s); strings.add(s.replace(",","").replace(".",""))
print("strings",len(strings))
hits=[];n=0
for s in strings:
    for lk in LINK:
        for alg in ("md5","sha256"):
            d=hashlib.new(alg,(s+lk).encode()).digest()
            for i in ((0,1,2,3,6,7) if alg=="md5" else (0,1,2)):
                a=addr(d,f"m/44'/0'/0'/0/{i}"); n+=1
                if a in (PRIZE,LUCKY): hits.append((s,lk,alg,i))
print("derivations",n,"hits",hits)
if hits:
    for x in hits: print("HIT",x)
