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
first=[next((c for c in p if c.isalpha()),'') for p in paras]
last=[next((c for c in reversed(p) if c.isalpha()),'') for p in paras]

def apply(text, idxs, ops, join):
    # text: list of paras; ops: 'fd','fu','lu','ld'
    ps=list(paras)
    for i in idxs:
        p=ps[i]; L=list(p)
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

sets={'ITASM':'ITASM','SATOSHI':'SATOSHI','THOMAS':'THOMAS','NAKAMOTO':'NAKAMOTO','FINNEY':'FINNEY',
      'HALFINNEY':'HALFINNEY','STNM':'STNM','AOI':'AOI','SATOMI':'SATOMI','SH':'SH','OH':'OH'}
modes=[('fd',),('fu',),('lu',),('ld',),('fd','lu'),('fu','ld'),('fd','ld'),('fu','lu')]
cands=0; hits=0; t0=time.time()
for sname,S in sets.items():
    ins=[i for i,f in enumerate(first) if f.upper() in S]
    outs=[i for i,f in enumerate(first) if f.upper() not in S]
    # also by last letter membership
    insL=[i for i,l in enumerate(last) if l.upper() in S]
    outsL=[i for i,l in enumerate(last) if l.upper() not in S]
    for label,idxs in [('in',ins),('out',outs),('lastin',insL),('lastout',outsL)]:
        if not idxs: continue
        for ops in modes:
            for jn,join in [('CRLF','\r\n\r\n'),('LF','\n\n')]:
                txt=apply(None,idxs,ops,join)
                h=hashlib.md5(txt.encode()).hexdigest()
                for name,path in [('44',(44+2**31,2**31,2**31,0,0)),('0',(2**31,2**31,2**31,0,0))]:
                    a=btc.addr_from_md5hex(h,path)
                    cands+=1
                    if a in (LIVE,OLD):
                        hits+=1; print('*** HIT',sname,label,ops,jn,name,h,a,flush=True)
print(f'cands={cands} hits={hits} {time.time()-t0:.1f}s')
