"""Semantic sign-set selection driven by the chapter's own instruction:
'if you want to know Satoshi's real identity, recognize the signs (at the end of the relevant paragraphs)'.
Paragraphs are selected by keyword, then flipped at their edges."""
import json,re,sys,hashlib,time,itertools

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX=(0,1,2,76,44,77)
def derive(h,idx):
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,idx)))
tot=[0,0]
def check(text,tag):
    h=hashlib.md5(text.encode()).hexdigest()
    for idx in IDX:
        a=derive(h,idx); tot[0]+=1
        if a in (LIVE,OLD): tot[1]+=1; print('*** HIT',tag,idx,h,a,flush=True)
def apply(paras,idxs,ops,join):
    ps=list(paras)
    for i in idxs:
        L=list(ps[i])
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
        if 'fu' in ops:
            for j,c in enumerate(L):
                if c.isalpha():
                    if c.islower(): L[j]=c.upper()
                    break
        if 'ld' in ops:
            for j in range(len(L)-1,-1,-1):
                if L[j].isalpha():
                    if L[j].isupper(): L[j]=L[j].lower()
                    break
        ps[i]=''.join(L)
    return join.join(ps)
ex=json.load(open('chapter_paras_exact.json'))
br=json.load(open('wp_paras_br.json'))
BASES={'ex-crlf':(ex,'\r\n\r\n'),
       'br-crlf':(['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n\r\n'),
       'br-lf':(['\n'.join(x) if isinstance(x,list) else x for x in br],'\n\n')}
KEYS=['sign','signs','recognize','identity','today','real','satoshi','hal','finney','nakamoto','thomas','aoi','genesis','what','second','satommi','turing','reverse','hidden','anagram','myth','secret','puzzle','solution']
MODES=[('fd','lu'),('fd',),('lu',),('fu','ld'),('fd','ld'),('fu','lu')]
t0=time.time()
for bname,(paras,join) in BASES.items():
    for k in KEYS:
        pat=re.compile(r'\b'+re.escape(k)+r'\w*',re.I)
        idx=[i for i,p in enumerate(paras) if pat.search(p)]
        if not idx: continue
        for ops in MODES:
            check(apply(paras,idx,ops,join),f'{bname} kw-{k}({len(idx)})-{"+".join(ops)}')
        # also complement
        comp=[i for i in range(len(paras)) if i not in set(idx)]
        for ops in (('fd','lu'),):
            check(apply(paras,comp,ops,join),f'{bname} kwNOT-{k}-{"+".join(ops)}')
    # unions of the instruction words
    words=['today','real','identity','recognize','signs']
    u=[i for i,p in enumerate(paras) if any(re.search(r'\b'+w+r'\w*',p,re.I) for w in words)]
    for ops in MODES:
        check(apply(paras,u,ops,join),f'{bname} hintWords({len(u)})-{"+".join(ops)}')
    print(f'-- {bname} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
