import json,hashlib
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
P=[t for _,t in json.load(open('wp_paras.json'))]; N=len(P)
fa=lambda p:next((c for c in p if c.isalpha()),'.')
la=lambda p:next((c for c in reversed(p) if c.isalpha()),'.')
FFWW={('F','s'),('F','t'),('W','n'),('W','m')}
def edge(p,mode):
    q=list(p); idx=[i for i,c in enumerate(q) if c.isalpha()]
    if not idx: return p
    f,l=idx[0],idx[-1]
    if 'f' in mode and q[f].isupper(): q[f]=q[f].lower()
    if 'u' in mode and q[f].islower(): q[f]=q[f].upper()
    if 'l' in mode and q[l].islower(): q[l]=q[l].upper()
    if 'd' in mode and q[l].isupper(): q[l]=q[l].lower()
    return ''.join(q)
sels={
 'all':set(range(N)),
 'ITASM_f':{i for i in range(N) if fa(P[i]).upper() in 'ITASM'},
 'notITASM':{i for i in range(N) if fa(P[i]).upper() not in 'ITASM'},
 'windows':{4,5,6,7,92,93,94,95,167,168,169,170},
 'FFWWsig':{i for i in range(N) if (fa(P[i]),la(P[i])) in FFWW},
 'finney4':{230,231,232,233},
 'notfinney4':set(range(N))-{230,231,232,233},
 'first44':set(range(0,44)),
 'last44':set(range(N-44,N)),
 'both44':set(range(0,44))|set(range(N-44,N)),
 'story':set(range(0,87)),
 'stride44':set(range(0,N,44)),
 'ends4':{0,1,2,3,N-4,N-3,N-2,N-1},
}
modes=['f','l','fl','ud','fu','ld']
hits=[]; n=0
for sname,S in sels.items():
    for m in modes:
        body=[edge(P[i],m) if i in S else P[i] for i in range(N)]
        for jn in ('\r\n\r\n','\n\n'):
            for trail in ('','\r\n\r\n'):
                txt=jn.join(body)+trail
                d=hashlib.md5(txt.encode()).digest()
                for ix in (0,1,2,3):
                    w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
                    if a in (PRIZE,LUCKY): hits.append((sname,m,jn,repr(trail),ix,a[:8]))
print('derivations',n,'hits',hits)
