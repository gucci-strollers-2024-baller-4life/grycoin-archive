import json,re,hashlib
import demo_oracle as D
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1 as K

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
WL=D.WL
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
P=[t for _,t in json.load(open('wp_paras.json'))]
occ=[(i+1,m.start()) for i,p in enumerate(P) for m in re.finditer(r'satommi',p,re.I)]
print('satommi occurrences:',occ)
txt='\n'.join(P)
print('total occurrences in chapter:',len(re.findall(r'satommi',txt,re.I)))
hits=[];n=0
def variants(s):
    out={s}
    out.add(s.replace('satommi','satomMi')); out.add(s.replace('satommi','satommI'))
    out.add(s.replace('satommi','satomMI')); out.add(s.replace('satommi','sAtommi'))
    out.add(s.replace('satommi','satoMmi')); out.add(s.replace('satommi','SATOMMI'))
    return out
for jn in ('\r\n\r\n','\n\n'):
    base=jn.join(P)
    for s in variants(base):
        for alg in ('md5','sha256'):
            d=hashlib.new(alg,s.encode()).digest()
            for k in (0,1,2,3,4,5):
                if addr(d,k) in (PRIZE,LUCKY): hits.append((alg,k))
                n+=1
print('derivations',n,'HITS',hits)
