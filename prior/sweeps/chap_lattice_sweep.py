import json,hashlib,sys,itertools,time
sys.path.insert(0,'harness')
import btc

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
paras=json.load(open('chapter_paras_exact.json'))
N=len(paras)

def apply(idxs, ops, join):
    ps=list(paras)
    for i in idxs:
        if not (0<=i<N): continue
        L=list(ps[i])
        if 'fd' in ops:
            for j,c in enumerate(L):
                if c.isalpha():
                    if c.isupper(): L[j]=c.lower()
                    break
        if 'fu' in ops:
            for j,c in enumerate(L):
                if c.isalpha():
                    if c.islower(): L[j]=c.upper()
                    break
        if 'lu' in ops:
            for j in range(len(L)-1,-1,-1):
                if L[j].isalpha():
                    if L[j].islower(): L[j]=L[j].upper()
                    break
        if 'ld' in ops:
            for j in range(len(L)-1,-1,-1):
                if L[j].isalpha():
                    if L[j].isupper(): L[j]=L[j].lower()
                    break
        ps[i]=''.join(L)
    return join.join(ps)

def check(txt, tag, res):
    h=hashlib.md5(txt.encode()).hexdigest()
    for pn,path in [("44'",(44+2**31,2**31,2**31,0,0)),("0'",(2**31,2**31,2**31,0,0))]:
        a=btc.addr_from_md5hex(h,path); res[0]+=1
        if a in (LIVE,OLD):
            res[1]+=1; print('*** HIT',tag,pn,h,a,flush=True)

res=[0,0]; t0=time.time()
modes=[('fd',),('lu',),('fd','lu'),('fu',),('ld',),('fu','ld'),('fd','ld'),('fu','lu')]
joins=[('CRLF','\r\n\r\n'),('LF','\n\n')]

# ---- lattice families (1-indexed positions)
fams={}
for base in (34,78,44,93,222,5):
    for m in (34,78,44):
        s=[i for i in range(1,N+1) if (i-base)%m==0]
        if s: fams[f'base{base}mod{m}']=s
for k in range(1,N+1):
    pass
# mirrors around 34/78 anchor
for start in (1,5,16,34,78,230):
    fams[f'stride44from{start}']=[start+44*k for k in range(7) if start+44*k<=N]
fams['anchor_pair']=[34,78]
fams['anchor_mirror']=[34,78,274-34,274-78]
fams['whatplus']=[33,34,77,78]
fams['lattice34_shift'] = sorted({x+d for x in [34,78,122,166,210,254] for d in (-1,0,1) if 1<=x+d<=N})
fams['lattice44']=[44,88,132,176,220,264]
fams['lattice44s']=sorted({x+d for x in [44,88,132,176,220,264] for d in (-1,0,1) if 1<=x+d<=N})
fams['windows']=[5,6,7,8,93,94,95,96,168,169,170,171]
fams['hint222']=[222]
fams['signpara']=[20,42,220,222,223,225,226,227,228,230,236,244,246,273]
for name,idxs in fams.items():
    idx=[i-1 for i in idxs]
    for ops in modes:
        for jn,join in joins:
            check(apply(idx,ops,join), f'{name}{idxs[:8]}{ops}{jn}', res)
print('lattice family candidates',res,'%.1fs'%(time.time()-t0))

# ---- subsets of the 6-paragraph 34-lattice
lat=[34,78,122,166,210,254]
for k in range(1,7):
    for comb in itertools.combinations(lat,k):
        for ops in modes:
            for jn,join in joins:
                check(apply([i-1 for i in comb],ops,join), f'lat{comb}{ops}{jn}', res)
print('lattice subsets',res,'%.1fs'%(time.time()-t0))

# ---- tagged serializations
for jn,join in joins:
    for tag in ('plain','p','pidattr'):
        if tag=='plain': t=join.join(paras)
        elif tag=='p': t=join.join(f'<p>{p}</p>' for p in paras)
        else:
            t=join.join(f'<p data-p-id="{hashlib.md5(p.encode()).hexdigest()}">{p}</p>' for p in paras)
        check(t,'tag-'+tag+jn,res)
print('tagged',res,'%.1fs'%(time.time()-t0))
