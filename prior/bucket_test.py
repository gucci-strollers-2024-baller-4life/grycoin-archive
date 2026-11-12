import json,hashlib
import demo_oracle as D
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
P=[t for _,t in json.load(open('wp_paras.json'))]; N=len(P)
IDX=[0,1,2,6,7,76,77]
def ev(data,label,hits):
    variants=[('raw',data),('strip',data.strip())]
    for vn,txt in variants:
        if not txt: continue
        d=hashlib.md5(txt.encode()).digest()
        for i in IDX:
            w,a=D.derive(d,f"m/44'/0'/0'/0/{i}")
            if a in (PRIZE,LUCKY): hits.append((label,vn,i,w,a))
    return
hits=[]; n=0
# ---------- Bucket 2: the reprint paragraphs ----------
for lo,hi in ((230,234),(230,233),(231,234),(230,235)):
    seg=P[lo:hi]
    for js,jn in (('\r\n\r\n','CRLF2'),('\n\n','LF2'),('\r\n','CRLF1'),('\n','LF1')):
        ev(js.join(seg),f'reprint {lo+1}-{hi} {jn}',hits)
        fl=[]
        for p in seg:
            q=list(p); idx=[i for i,c in enumerate(q) if c.isalpha()]
            if idx:
                f,l=idx[0],idx[-1]
                if q[f].isupper(): q[f]=q[f].lower()
                if q[l].islower(): q[l]=q[l].upper()
            fl.append(''.join(q))
        ev(js.join(fl),f'reprint {lo+1}-{hi} flipped {jn}',hits)
# ---------- Bucket 3: full chapter, reprints flipped ----------
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
variants={'plain':P,
 'finney4_flip':[edge(p) if i+1 in (231,232,233,234) else p for i,p in enumerate(P)],
 'finney5_flip':[edge(p) if i+1 in (231,232,233,234,235) else p for i,p in enumerate(P)],
 'allFFWW_flip':[edge(p) if (fa(p),la(p)) in FFWW else p for i,p in enumerate(P)]}
for name,body in variants.items():
    for js,jn in (('\r\n\r\n','CRLF2'),('\n\n','LF2')):
        ev(js.join(body),f'chapter {name} {jn}',hits)
# ---------- Bucket 1: word-targeted ----------
base='\r\n\r\n'.join(P)
words=[('himself','himselF'),('legacy','legacY'),('signs','signS'),('Bitcoin','BitcoiN'),('credit','crediT')]
import itertools

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
for r in (1,2,3,len(words)):
    for combo in itertools.combinations(words,r):
        for js,jn in (('\r\n\r\n','CRLF2'),('\n\n','LF2')):
            t=js.join(P)
            for a,b in combo: t=t.replace(a,b)
            ev(t,f'words {"+".join(b for a,b in combo)} {jn}',hits)
print('hypothesis runs complete | hits:',hits)
for h in hits: print('  ***',h)
