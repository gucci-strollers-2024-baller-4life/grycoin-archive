import json,hashlib,itertools,re
import demo_oracle as D
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
P=[t for _,t in json.load(open('wp_paras.json'))]
N=len(P); print('paras',N)
def fl(p,mode):
    q=list(p); idx=[i for i,c in enumerate(q) if c.isalpha()]
    if not idx: return p
    f,l=idx[0],idx[-1]
    if mode in('fd','both','flipf'):
        q[f]=q[f].lower() if q[f].isupper() else q[f].upper()
    if mode in('lu','both','flipl'):
        q[l]=q[l].upper() if q[l].islower() else q[l].lower()
    return ''.join(q)
first=lambda p:next((c for c in p if c.isalpha()),'')
last =lambda p:next((c for c in reversed(p) if c.isalpha()),'')
def sel(name):
    if name=='all': return set(range(N))
    if name=='ITASM': return {i for i in range(N) if first(P[i]).upper() in 'ITASM'}
    if name=='notITASM': return {i for i in range(N) if first(P[i]).upper() not in 'ITASM'}
    if name=='lastSTNM': return {i for i in range(N) if last(P[i]).lower() in 'stnm'}
    if name=='notlastSTNM': return {i for i in range(N) if last(P[i]).lower() not in 'stnm'}
    if name=='finney4': return {230,231,232,233}
    if name=='finney5': return {230,231,232,233,234}
    if name.startswith('stride44_'):
        off=int(name.split('_')[1]); return set(range(off,N,44))
    if name=='empty': return set()
    if name=='it': return {i for i in range(N) if re.search(r'\bI\b',P[i])}
    raise SystemExit('bad '+name)
sels=['all','ITASM','notITASM','lastSTNM','notlastSTNM','finney4','finney5','it']+[f'stride44_{o}' for o in range(0,44)]
modes=['fd','lu','both','flipf','flipl']
joins={'\n\n':'\n\n','\n':'\n','\r\n\r\n':'\r\n\r\n','\r\n':'\r\n','<br><br>':'<br><br>','<br>':'<br>'}
hits=[]; n=0
import time; t0=time.time()

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
for s in sels:
    S=sel(s)
    for m in modes:
        for jn,j in joins.items():
            txt=j.join(fl(P[i],m) if i in S else P[i] for i in range(N))
            d=hashlib.md5(txt.encode()).digest(); n+=1
            w,a=D.derive(d)
            if a==PRIZE: hits.append((s,m,jn,w))
print('candidates',n,'hits',hits,'%.1fs'%(time.time()-t0))
# also report the plain chapter md5/addr for reference
for jn,j in [('\n\n','\n\n'),('\n','\n')]:
    txt=j.join(P); print('plain',jn,hashlib.md5(txt.encode()).hexdigest()[:8],D.derive(hashlib.md5(txt.encode()).digest())[1])
