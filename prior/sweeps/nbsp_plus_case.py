"""NBSP normalisation combined with the case families (the author's copy most likely had plain spaces)."""
import json,hashlib,sys,time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX=(0,1,2,76,44,77)
def derive(h,ix): return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,ix)))
br=json.load(open('wp_paras_br.json'))
lines=[[x] if not isinstance(x,list) else x for x in br]
tot=[0,0]
def hit(txt,tag):
    h=hashlib.md5(txt.encode()).hexdigest()
    for ix in IDX:
        a=derive(h,ix); tot[0]+=1
        if a in (LIVE,OLD): tot[1]+=1; print('*** HIT',tag,ix,h,a,flush=True)
def edit(p,ops):
    L=list(p)
    if 'fd' in ops:
        for j,c in enumerate(L):
            if c.isalpha():
                if c.isupper(): L[j]=c.lower()
                break
    if 'lu' in ops:
        for j in range(len(L)-1,-1,-1):
            if L[j].isalpha():
                if L[j].islower(): L[j]=L[j].upper()
                break
    return ''.join(L)
t0=time.time()
for inner in ('\n','\r\n'):
    for outer in ('\n\n','\r\n\r\n'):
        for reading in ('del','space'):
            paras=[inner.join(L).replace('\xa0','' if reading=='del' else ' ') for L in lines]
            N=len(paras)
            first=[next((c for c in p if c.isalpha()),'').upper() for p in paras]
            sets={'all':set(range(N)),
                  'nonITASM':{i for i in range(N) if first[i] not in 'ITASM'},
                  'ffww':{4,5,6,7,92,93,94,95,167,168,169,170,230,231,232,234},
                  'signs14':{19,41,219,221,222,224,225,226,227,229,235,243,245,272},
                  'trailing13':{85,107,121,127,138,146,164,165,191,200,208,219,266}}
            for sname,sel in sets.items():
                for ops in (('fd','lu'),('lu',),('fd',)):
                    ps=list(paras)
                    for k in sel: ps[k]=edit(ps[k],ops)
                    hit(outer.join(ps),f'{repr(inner)}/{repr(outer)} nbsp-{reading} {sname} {"+".join(ops)}')
        print(f'-- {repr(inner)}/{repr(outer)} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
