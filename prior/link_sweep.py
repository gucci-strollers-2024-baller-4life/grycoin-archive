import json,hashlib
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
ALPH="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58c(b):
    b=b+hashlib.sha256(hashlib.sha256(b).digest()).digest()[:4]
    n=int.from_bytes(b,'big'); s=''
    while n: n,r=divmod(n,58); s=ALPH[r]+s
    return '1'*(len(b)-len(b.lstrip(b'\x00')))+s
# stage one key (certified 19TbyN5 at idx 0)
d1=bytes.fromhex("9dd2efb9bc976c2095bd534d7b8d431c")
words=D.entropy_to_words(d1); seed=Bip39SeedGenerator(words).Generate("")
ch=Bip32Slip10Secp256k1.FromSeed(seed).DerivePath("m/44'/0'/0'/0/0")
raw=ch.PrivateKey().Raw().ToBytes(); wif=b58c(b'\x80'+raw+b'\x01')
print('stage-one WIF:',wif)
print('hex:',raw.hex())
links={
 'wif7':wif[-7:], 'wif3':wif[-3:], 'hex7':raw.hex()[-7:], 'hex3':raw.hex()[-3:],
 'md5_7':"9dd2efb9bc976c2095bd534d7b8d431c"[-7:],
}
print('link candidates:',links)
P=[t for _,t in json.load(open('wp_paras.json'))]; N=len(P)
fa=lambda p:next((c for c in p if c.isalpha()),'.')
la=lambda p:next((c for c in reversed(p) if c.isalpha()),'.')
FFWW={('F','s'),('F','t'),('W','n'),('W','m')}
def edge(p,mode='fl'):
    q=list(p); idx=[i for i,c in enumerate(q) if c.isalpha()]
    if not idx: return p
    f,l=idx[0],idx[-1]
    if 'f' in mode and q[f].isupper(): q[f]=q[f].lower()
    if 'l' in mode and q[l].islower(): q[l]=q[l].upper()
    return ''.join(q)
bases={
 'plain':P,
 'allfl':[edge(p) for p in P],
 'notFFWW':[p if (fa(p),la(p)) in FFWW else edge(p) for p in P],
 'windows':[edge(p) if i+1 in {5,6,7,8,93,94,95,96,168,169,170,171} else p for i,p in enumerate(P)],
}
hits=[]; n=0
for bname,body in bases.items():
    for jn in ('\r\n\r\n','\n\n'):
        base=jn.join(body)
        for lname,link in links.items():
            for sep in (' ',''):
                for tail in ('','\r\n\r\n'):
                    d=hashlib.md5((base+sep+link+tail).encode()).digest()
                    for ix in (0,1,2,3):
                        w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
                        if a in (PRIZE,LUCKY): hits.append((bname,jn,lname,repr(sep),ix,a[:10]))
print('derivations',n,'hits',hits)
