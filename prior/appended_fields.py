import json,hashlib
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; ESC="1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
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
chapter={
 'plain':[p for p in P],
 'allfl':[edge(p,'fl') for p in P],
 'notFFWW':[p if (fa(p),la(p)) in FFWW else edge(p,'fl') for p in P],
 'FFWWonly':[edge(p,'fl') if (fa(p),la(p)) in FFWW else p for p in P],
 'windows':[edge(p,'fl') if i+1 in set(list(range(5,9))+list(range(93,97))+list(range(168,172))) else p for i,p in enumerate(P)],
}
demo=open('demo_base.txt').read().replace('\r\n','\n')
dp=[p.strip() for p in demo.split('\n\n') if p.strip()]
dtext='\n\n'.join(dp)
dflip=dtext.replace('I expected','i expected').replace('himself','himselF')
fields=['14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W','1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi',
 'f11eca9925c7809210796a3c8d95677dfaf0becb4f6df4c74e7261c3011a2e3c',
 'ccf5ad645f069dfe263e3df63c906ed6ce449813b968c12c0f862b475014b4bb',
 'TOMI','STNM','HAL','Satoshi','signs','777','Grycoin','Aoi','Aoi Nakamoto','Thomas',
 'himself','himselF','i','Second Life','Second Coming','44','44:44','second','Second',
 'upside down','MasK','U2','Jesus','Easter TOMI Second Life']
hits=[]; n=0
for name,body in chapter.items():
    base='\n\n'.join(body)
    for f in fields:
        for sep in (' ',''):
            d=hashlib.md5((base+sep+f).encode()).digest()
            for ix in (0,1,2):
                w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
                if a==PRIZE: hits.append(('chapter',name,repr(sep),f,ix))
for bname,base in (('demo',dtext),('demoflip',dflip)):
    for f in fields:
        for sep in (' ',''):
            d=hashlib.md5((base+sep+f).encode()).digest()
            for ix in (0,1,2):
                w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
                if a==ESC: hits.append(('demo',bname,repr(sep),f,ix))
print('derivations',n,'hits',hits)
