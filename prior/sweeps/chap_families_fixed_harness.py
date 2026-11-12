"""Chapter families re-evaluated with the REPAIRED harness (base58 leading-zero fix)
and across the author's index convention (block N -> Nth private key)."""
import json,hashlib,sys,itertools,time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX=(0,1,2,76)
res={'cands':0,'hits':0}
def derive(h,idx):
    ent=bytes.fromhex(h)
    return fast.p2pkh(fast.key_at(fast.seed_from(ent),(44+H,0+H,0+H,0,idx)))
def check(text,tag):
    h=hashlib.md5(text.encode()).hexdigest()
    for idx in IDX:
        a=derive(h,idx); res['cands']+=1
        if a in (LIVE,OLD):
            res['hits']+=1
            print('*** HIT',tag,'idx',idx,h,a,flush=True)

ex=json.load(open('chapter_paras_exact.json'))
br=json.load(open('wp_paras_br.json'))
BASES=[]
BASES.append(('ex-crlf',ex,'\r\n','\r\n\r\n'))
BASES.append(('br-crlf',['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n','\r\n\r\n'))
BASES.append(('br-lf',['\n'.join(x) if isinstance(x,list) else x for x in br],'\n','\n\n'))

def apply(paras,idx,ops,join):
    ps=list(paras)
    for i in idx:
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

MODES=[('fd',),('fu',),('lu',),('ld',),('fd','lu'),('fu','ld'),('fd','ld'),('fu','lu')]
SETS={'ITASM':'ITASM','SATOSHI':'SATOSHI','THOMAS':'THOMAS','NAKAMOTO':'NAKAMOTO','FINNEY':'FINNEY',
      'HALFINNEY':'HALFINNEY','STNM':'STNM','AOI':'AOI','SATOMI':'SATOMI','SH':'SH','OH':'OH'}
t0=time.time()
for bname,paras,one,join in BASES:
    N=len(paras)
    first=[next((c for c in p if c.isalpha()),'') for p in paras]
    last=[next((c for c in reversed(p) if c.isalpha()),'') for p in paras]
    # --- families 1: sign-letter sets
    for sname,S in SETS.items():
        groups={'in':[i for i,f in enumerate(first) if f.upper() in S],
                'out':[i for i,f in enumerate(first) if f.upper() not in S],
                'lastin':[i for i,l in enumerate(last) if l.upper() in S],
                'lastout':[i for i,l in enumerate(last) if l.upper() not in S]}
        for gname,idxs in groups.items():
            if not idxs: continue
            for ops in MODES:
                check(apply(paras,idxs,ops,join),f'{bname} sign-{sname}-{gname}-{"+".join(ops)}')
    # --- families 2: 44 lattice
    fams={'anchor':[34,78],'anchor_mirror':[34,78,240,196],'whatplus':[33,34,77,78],
          'lattice34':[34,78,122,166,210,254],'lattice44':[44,88,132,176,220,264],
          'stride44_5':[5,49,93,137,181,225,269],'windows':[5,6,7,8,93,94,95,96,168,169,170,171],
          'orig235':[231,232,233,235],'orig234':[230,231,232,233,235],
          'signs':[20,42,220,222,223,225,226,227,228,230,236,244,246,273],'hint222':[222]}
    for fname,pos in fams.items():
        idx=[p-1 for p in pos if 1<=p<=N]
        for ops in MODES:
            check(apply(paras,idx,ops,join),f'{bname} lat-{fname}-{"+".join(ops)}')
    for k in range(1,7):
        for comb in itertools.combinations([34,78,122,166,210,254],k):
            for ops in (('fd','lu'),('fu','ld'),('fd',),('lu',)):
                check(apply(paras,[c-1 for c in comb],ops,join),f'{bname} latsub{comb}-{"+".join(ops)}')
    print(f'-- {bname} families done, cands={res["cands"]} hits={res["hits"]} {time.time()-t0:.0f}s',flush=True)
print(json.dumps(res),'%.0fs'%(time.time()-t0))
