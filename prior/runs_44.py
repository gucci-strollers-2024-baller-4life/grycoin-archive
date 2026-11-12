import hashlib,itertools,re
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
WL=D.WL
P=[t for _,t in json.load(open('wp_paras.json'))] if False else [t for _,t in __import__('json').load(open('wp_paras.json'))]
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
def lastw(p):
    w=re.findall(r"[A-Za-z']+",p)
    return w[-1] if w else ''
runs={'A':[5,6,7,8],'B':[93,94,95,96],'C':[168,169,170,171]}
toks={k:[lastw(P[i-1]) for i in v] for k,v in runs.items()}
print('run last words:',toks)
# +/-44 paragraph last words around each window start
extra={}
for k,start in (('A',5),('B',93),('C',168)):
    for off in (-44,44):
        j=start+off
        if 1<=j<=273: extra[f'{k}{off:+d}']=lastw(P[j-1])
print('pm44 tokens:',extra)
cands={}
for a,b in itertools.permutations('ABC',2):
    cands[f'{a}+{b}']=' '.join(toks[a]+toks[b])
cands['dorian_pair']=' '.join(toks['C'])
cands['AB_C']=' '.join(toks['A']+toks['B'])
cands['pm44']=' '.join(extra.values())
LINK=[""," 62tGor2"," isUB1bT"," gAELXgr"," KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2"]
hits=[];n=0
for name,b in cands.items():
    for lk in LINK:
        for alg in ("md5","sha256"):
            d=hashlib.new(alg,(b+lk).encode()).digest()
            for i in ((0,1,2,6,7) if alg=="md5" else (0,1,2)):
                a=addr(d,f"m/44'/0'/0'/0/{i}"); n+=1
                if a in (PRIZE,LUCKY): hits.append((name,lk,alg,i,b))
print("derivations",n,"hits",hits)
for k,v in cands.items(): print(' ',k,'=',v)
