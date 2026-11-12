"""Re-validate the signature-window subset closures on the repaired harness (base58 fix).
Pool = the 16 signature paragraphs (three FFWW windows + the Finney reprint run), plus the anchor pair.
Every subset, four edge modes, both joins, indices 0/1/2/76."""
import json,hashlib,sys,time,itertools

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX=(0,76)
def derive(h,idx):
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,idx)))
ex=json.load(open('chapter_paras_exact.json'))
br=json.load(open('wp_paras_br.json'))
BASES={'br-crlf':(['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n\r\n')}
POOL=[5,6,7,8,93,94,95,96,168,169,170,171,231,232,233,235,34,78]
MODES=[('fd','lu'),('fd',),('lu',),('fu','ld')]
def apply(paras,idxs,ops,join):
    ps=list(paras)
    for i in idxs:
        L=list(ps[i])
        for j,c in enumerate(L):
            if c.isalpha():
                if 'fd' in ops and c.isupper(): L[j]=c.lower()
                if 'fu' in ops and c.islower(): L[j]=c.upper()
                break
        for j in range(len(L)-1,-1,-1):
            if L[j].isalpha():
                if 'lu' in ops and L[j].islower(): L[j]=L[j].upper()
                if 'ld' in ops and L[j].isupper(): L[j]=L[j].lower()
                break
        ps[i]=''.join(L)
    return join.join(ps)
tot=[0,0]; t0=time.time()
for bname,(paras,join) in BASES.items():
    n=len(paras)
    pool=[p-1 for p in POOL if 1<=p<=n]
    base=join.join(paras)
    for mask in range(1,1<<len(pool)):
        idxs=[pool[i] for i in range(len(pool)) if mask>>i&1]
        for ops in MODES:
            h=hashlib.md5(apply(paras,idxs,ops,join).encode()).hexdigest()
            for ix in IDX:
                a=derive(h,ix); tot[0]+=1
                if a in (LIVE,OLD): tot[1]+=1; print('*** HIT',bname,idxs,ops,ix,h,a,flush=True)
    print(f'-- {bname} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
