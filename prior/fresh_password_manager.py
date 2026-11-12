import json,hashlib
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
ALPH="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58c(b):
    b=b+hashlib.sha256(hashlib.sha256(b).digest()).digest()[:4]
    n=int.from_bytes(b,'big'); s=''
    while n: n,r=divmod(n,58); s=ALPH[r]+s
    pad=len(b)-len(b.lstrip(b'\x00'))
    return '1'*pad+s
def wif_at(d16,path):
    words=D.entropy_to_words(d16)
    seed=Bip39SeedGenerator(words).Generate("")
    ch=Bip32Slip10Secp256k1.FromSeed(seed).DerivePath(path)
    raw=ch.PrivateKey().Raw().ToBytes()
    return b58c(b'\x80'+raw+b'\x01'), ch.PrivateKey().PublicKey().RawCompressed().ToBytes()

P=[t for _,t in json.load(open('wp_paras.json'))]; N=len(P)
fa=lambda p:next((c for c in p if c.isalpha()),'.')
la=lambda p:next((c for c in reversed(p) if c.isalpha()),'.')
FFWW={('F','s'),('F','t'),('W','n'),('W','m')}
def edge(p,mode):
    q=list(p); idx=[i for i,c in enumerate(q) if c.isalpha()]
    if not idx: return p
    f,l=idx[0],idx[-1]
    if 'f' in mode and q[f].isupper(): q[f]=q[f].lower()
    if 'l' in mode and q[l].islower(): q[l]=q[l].upper()
    return ''.join(q)
def variants():
    out={}
    out['plain']=[p for p in P]
    out['allfl']=[edge(p,'fl') for p in P]
    out['notFFWW']=[p if (fa(p),la(p)) in FFWW else edge(p,'fl') for p in P]
    out['FFWWonly']=[edge(p,'fl') if (fa(p),la(p)) in FFWW else p for p in P]
    return out
hits=[]; n=0
for name,body in variants().items():
    for jn in ('\n\n','\n'):
        txt=jn.join(body)
        d1=hashlib.md5(txt.encode()).digest()
        for k in range(0,78):
            wif,pub=wif_at(d1,f"m/44'/0'/0'/0/{k}")
            d2=hashlib.md5(wif.encode()).digest()
            words,addr=D.derive(d2)          # index 0 of the second wallet
            n+=1
            if addr==PRIZE: hits.append((name,jn,k,wif))
            # also try the same index k on the second wallet
            words,addr2=D.derive(d2,f"m/44'/0'/0'/0/{k}"); n+=1
            if addr2==PRIZE: hits.append((name,jn,k,'idx2',wif))
print('derivations',n,'hits',hits)
