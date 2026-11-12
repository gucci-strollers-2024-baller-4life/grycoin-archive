import json,hashlib,re
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
P=[t for _,t in json.load(open('wp_paras.json'))]; N=len(P)
fa=lambda p:next((c for c in p if c.isalpha()),'.')
la=lambda p:next((c for c in reversed(p) if c.isalpha()),'.')
def fl(p,mode):
    q=list(p); idx=[i for i,c in enumerate(q) if c.isalpha()]
    if not idx: return p
    f,l=idx[0],idx[-1]
    if 'f' in mode and q[f].isupper(): q[f]=q[f].lower()
    if 'l' in mode and q[l].islower(): q[l].upper(); q[l]=q[l].upper()
    return ''.join(q)
# structural segments (1-indexed inclusive)
segs={'whole':(1,273),'I':(2,87),'II':(88,162),'III':(163,273),
      'I-1':(3,53),'I-2':(54,70),'I-3':(71,87),'II-abs':(89,90),
      'II-1':(91,114),'II-2':(115,129),'II-3':(130,151),'II-4':(152,156),
      'II-5':(157,160),'II-6':(161,162),'III-1':(164,174),'III-2':(175,246),
      'III-3':(247,264),'III-4':(265,273),'I+II':(2,162),'II+III':(88,273),
      'tail':(215,273),'sat-code':(175,246)}
def apply(rule,lo,hi):
    idxs=range(lo-1,hi); out=list(P)
    if rule=='plain': return out
    if rule=='allfl':
        for i in idxs: out[i]=fl(P[i],'fl')
    elif rule=='allf':
        for i in idxs: out[i]=fl(P[i],'f')
    elif rule=='alll':
        for i in idxs: out[i]=fl(P[i],'l')
    elif rule=='notFFWW':      # flip every paragraph in span EXCEPT the FFWW/stnm ones
        for i in idxs:
            if (fa(P[i]),la(P[i])) not in {('F','s'),('F','t'),('W','n'),('W','m')}: out[i]=fl(P[i],'fl')
    elif rule=='notFinney4':   # para 229's literal instruction, Finney four = 231-234
        for i in idxs:
            if i+1 not in (231,232,233,234): out[i]=fl(P[i],'fl')
    elif rule=='notFinney5':
        for i in idxs:
            if i+1 not in (230,231,232,233,234): out[i]=fl(P[i],'fl')
    elif rule=='ITASM':
        for i in idxs:
            if fa(P[i]).upper() in 'ITASM': out[i]=fl(P[i],'fl')
    elif rule=='strip':        # trailing spaces removed everywhere
        out=[p.rstrip() for p in P]
    return out
rules=['plain','allfl','allf','alll','notFFWW','notFinney4','notFinney5','ITASM','strip']
hits=[];n=0
for sname,(lo,hi) in segs.items():
    for rule in rules:
        body=apply(rule,lo,hi)[lo-1:hi]
        for jn in ('\n\n','\n','\r\n\r\n'):
            txt=jn.join(body)
            d=hashlib.md5(txt.encode()).digest()
            for ix in (0,1,2,3):
                w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
                if a==PRIZE: hits.append((sname,rule,jn,ix,w))
print('derivations',n,'hits',hits)
