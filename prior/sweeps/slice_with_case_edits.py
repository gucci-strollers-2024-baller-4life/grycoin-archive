"""Slice + case edits: the author says stage two's preimage 'has multiple paragraphs and two line
breaks between each of them'. Every contiguous run was tested as PLAIN text (negative). Never tested:
a multi-paragraph run WITH the case edits applied inside it. Three selectors inside the run:
  all      - every paragraph of the run, first lowered / last raised
  nonitasm - only the run's paragraphs whose first letter is not a sign letter
  ffww     - only the run's FFWW signature paragraphs
"""
import json,hashlib,sys,time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX=(0,1,2,76)
def derive(h,idx):
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,idx)))
ex=json.load(open('chapter_paras_exact.json'))
br=json.load(open('wp_paras_br.json'))
BASES={'br-crlf':(['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n\r\n'),
       'br-lf':(['\n'.join(x) if isinstance(x,list) else x for x in br],'\n\n')}
FFWW={5,6,7,8,93,94,95,96,168,169,170,171}
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
tot=[0,0]; t0=time.time()
for bname,(paras,join) in BASES.items():
    N=len(paras)
    first=[next((c for c in p if c.isalpha()),'').upper() for p in paras]
    for length in range(2,11):
        for i in range(0,N-length+1):
            j=i+length
            for sname,sel in (('all',set(range(i,j))),
                              ('nonitasm',{k for k in range(i,j) if first[k] not in 'ITASM'}),
                              ('ffww',{k for k in range(i,j) if (k+1) in FFWW})):
                if not sel: continue
                for ops in (('fd','lu'),('lu',),('fd',)):
                    ps=list(paras)
                    for k in sel: ps[k]=edit(ps[k],ops)
                    h=hashlib.md5(join.join(ps[i:j]).encode()).hexdigest()
                    for ix in IDX:
                        a=derive(h,ix); tot[0]+=1
                        if a in (LIVE,OLD): tot[1]+=1; print('*** HIT',bname,i+1,j,sname,ops,ix,h,a,flush=True)
        print(f'-- {bname} len{length} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
