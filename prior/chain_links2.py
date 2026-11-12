import json,re,hashlib
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
ALPH="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
WL=[l.strip() for l in open('ninjaops-puzzle-lanes/bip39_english.txt')]
def b58c(b):
    b=b+hashlib.sha256(hashlib.sha256(b).digest()).digest()[:4]
    n=int.from_bytes(b,'big'); s=''
    while n: n,r=divmod(n,58); s=ALPH[r]+s
    return '1'*(len(b)-len(b.lstrip(b'\x00')))+s
def words32(d32):
    bits=''.join(f'{x:08b}' for x in d32); chk=hashlib.sha256(d32).digest()
    allb=bits+''.join(f'{x:08b}' for x in chk)[:8]
    return ' '.join(WL[int(allb[i:i+11],2)] for i in range(0,264,11))
def wif_of(inp,algo):
    d=hashlib.sha256(inp.encode()).digest() if algo=='SHA-256' else hashlib.md5(inp.encode()).digest()
    w=words32(d) if algo=='SHA-256' else D.entropy_to_words(d)
    seed=Bip39SeedGenerator(w).Generate("")
    ch=Bip32Slip10Secp256k1.FromSeed(seed).DerivePath("m/44'/0'/0'/0/0")
    raw=ch.PrivateKey().Raw().ToBytes()
    return b58c(b'\x80'+raw+b'\x01'), raw.hex()
def parse(p):
    src=open(p).read(); m=re.search(r'BLOCKS = \[(.*?)\n\]',src,re.S)
    E=re.findall(r"Block\(number=(\d+), algorithm='([^']+)', exact_input=(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")\)",m.group(1),re.S)
    return {int(n):(a if a or not b else b).encode().decode('unicode_escape') for n,algo,a,b in E}
q1=parse('ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py')
links={}
for n in (74,75,76,77):
    w,h=wif_of(q1[n],'SHA-256'); links[f'b{n}_wif']=w; links[f'b{n}_7']=w[-7:]; links[f'b{n}_3']=w[-3:]
w1,_=wif_of(open('safudev_stage1.txt').read().rstrip('\n'),'MD5')
links['stage1_wif']=w1; links['stage1_7']=w1[-7:]
P=[t for _,t in json.load(open('wp_paras.json'))]; N=len(P)
fa=lambda p:next((c for c in p if c.isalpha()),'.')
la=lambda p:next((c for c in reversed(p) if c.isalpha()),'.')
FFWW={('F','s'),('F','t'),('W','n'),('W','m')}
def edge(p):
    idx=[i for i,c in enumerate(p) if c.isalpha()]
    if not idx: return p
    q=list(p); f,l=idx[0],idx[-1]
    if q[f].isupper(): q[f]=q[f].lower()
    if q[l].islower(): q[l]=q[l].upper()
    return ''.join(q)
bases={'plain':P,'allfl':[edge(p) for p in P],
       'notFFWW':[p if (fa(p),la(p)) in FFWW else edge(p) for p in P],
       'windows':[edge(p) if i+1 in {5,6,7,8,93,94,95,96,168,169,170,171} else p for i,p in enumerate(P)]}
hits=[];n=0
for bname,body in bases.items():
    for jn in ('\r\n\r\n','\n\n'):
        base=jn.join(body)
        for lname,link in links.items():
            d=hashlib.md5((base+' '+link).encode()).digest()
            for ix in (0,1):
                w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
                if a in (PRIZE,LUCKY): hits.append((bname,jn,lname,ix))
print('links:',{k:(v[:8]+'...'+v[-4:]) for k,v in links.items()})
print('derivations',n,'hits',hits)
