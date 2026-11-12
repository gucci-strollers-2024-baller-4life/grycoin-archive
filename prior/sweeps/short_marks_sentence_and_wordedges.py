"""SN / EU and their foldovers on the two channels the paragraph initials cannot reach.

Established in the previous run: the paragraph-initial channel has no U at all, and the sentence-initial
channel has no U either (621 sentence initials: S40 N16 H21 M13 E7, U0). So EU cannot be a
surviving-capitals mark anywhere in the initials. What is left:
  S-channel : dense / sparse surviving-capitals on the 621 sentence initials
  W-channel : word-edge marks inside a paragraph, up and down direction (the block-2 constraint)
Marks: SN, NS, EU, UE plus their Atbash foldovers HM, MH, VF, FV.
"""
import json,re,sys,hashlib,time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX=(0,1,2,76)
def derive(h,ix): return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,ix)))
tot=[0,0]; t0=time.time()
def hit(h,tag):
    for ix in IDX:
        a=derive(h,ix); tot[0]+=1
        if a in (LIVE,OLD): tot[1]+=1; print('*** HIT',tag,ix,h,a,flush=True)
br=json.load(open('wp_paras_br.json')); ex=json.load(open('chapter_paras_exact.json'))
BASES={'br-crlf':(['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n\r\n'),
       'br-lf':(['\n'.join(x) if isinstance(x,list) else x for x in br],'\n\n'),
       'ex-crlf':(ex,'\r\n\r\n')}
MARKS=['SN','NS','EU','UE','HM','MH','VF','FV']
for bname,(paras,join) in BASES.items():
    N=len(paras); text=join.join(paras)
    offs=[];acc=0
    for p in paras: offs.append(acc); acc+=len(p)+len(join)
    # --- S channel
    sin=[];start=0
    for m in re.finditer(r'[.!?]+["\u201d]?[ \t]*(?:\r?\n| |$)',text):
        for k in range(start,m.end()):
            if text[k].isalpha():
                i=max(j for j in range(N) if offs[j]<=k)
                sin.append((i,k-offs[i],text[k].upper())); break
        start=m.end()
    for mark in MARKS:
        pos=[[k for k,(_,_,c) in enumerate(sin) if c==ch] for ch in mark]
        if any(not p for p in pos): continue
        emb=[]
        def rec(i,last,cur):
            if i==len(mark): emb.append(tuple(cur)); return
            for k in pos[i]:
                if k>last: rec(i+1,k,cur+[k])
        rec(0,-1,[])
        for keep in emb:
            ks=set(keep)
            ps=[]
            for i,p in enumerate(paras):
                L=list(p)
                for k,(pi,off,_) in enumerate(sin):
                    if pi==i and off<len(L) and L[off].isalpha():
                        if k in ks: L[off]=L[off].upper()
                        elif sin[k][2] in set(mark): L[off]=L[off].lower()
                ps.append(''.join(L))
            hit(hashlib.md5(join.join(ps).encode()).hexdigest(),f'{bname} S {mark} {keep}')
        print(f'  {bname} S {mark} emb={len(emb)} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
    # --- W channel
    edges=[]
    for p in paras:
        e=set()
        for m in re.finditer(r"[A-Za-z']+",p):
            for j in range(m.start(),m.end()):
                if p[j].isalpha(): e.add(j); break
            for j in range(m.end()-1,m.start()-1,-1):
                if p[j].isalpha(): e.add(j); break
        edges.append([j for j in sorted(e) if p[j].islower()])
    base_bytes=text.encode()
    for mark in MARKS:
        up=[c.upper() for _,c in [(0,c) for c in mark]]
        n_mark=0
        for i,p in enumerate(paras):
            seq=[p[j].upper() for j in edges[i]]
            pos=[[k for k,c in enumerate(seq) if c==ch] for ch in mark]
            if any(not q for q in pos): continue
            emb=[]
            def rec2(a,last,cur):
                if a==len(mark): emb.append(tuple(cur)); return
                for k in pos[a]:
                    if k>last: rec2(a+1,k,cur+[k])
            rec2(0,-1,[])
            for keep in emb:
                n_mark+=1
                for direction in ('up','down'):
                    L=list(p)
                    for k in keep:
                        j=edges[i][k]
                        L[j]=L[j].upper() if direction=='up' else L[j].lower()
                    ps=list(paras); ps[i]=''.join(L)
                    hit(hashlib.md5(join.join(ps).encode()).hexdigest(),f'{bname} W-{direction} {mark} p{i+1} {keep}')
        print(f'  {bname} W {mark} emb={n_mark} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
    print(f'-- {bname} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
