"""Short marks on every case channel: the user's SN / EU, their reversals, and their Atbash foldovers.

Atbash matters here because the author's own round-two block 30 answer is "EU IQ KO" with TOMI
"Atbash foldover", so EU is a string her corpus already treats as a foldover token. Under Atbash
A<->Z B<->Y ... : SN -> HM, EU -> VF.

Channels (every one where a two-letter mark can live):
  P  paragraph initials (273 units)
  S  sentence initials  (621 units)
  W  word edges inside a paragraph, in-order (the block-2 constraint)
Readings per embedding: dense surviving-capitals, sparse surviving-capitals, and uppercase marking (W only).
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
AB={chr(65+i):chr(90-i) for i in range(26)}
def atbash(s): return ''.join(AB.get(c,c) for c in s.upper())
br=json.load(open('wp_paras_br.json')); ex=json.load(open('chapter_paras_exact.json'))
BASES={'br-crlf':(['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n\r\n'),
       'br-lf':(['\n'.join(x) if isinstance(x,list) else x for x in br],'\n\n'),
       'ex-crlf':(ex,'\r\n\r\n')}
MARKS=['SN','EU']
marks=[]
for m in MARKS:
    for v in (m, m[::-1], atbash(m), atbash(m)[::-1]):
        if v not in marks: marks.append(v)
print('marks',marks,flush=True)
def _lower(paras,i,pin):
    p=paras[i]; L=list(p)
    for j,c in enumerate(L):
        if c.isalpha(): L[j]=c.lower(); break
    return ''.join(L)
tot=[0,0]; t0=time.time()
def hit(h,tag):
    for ix in IDX:
        a=derive(h,ix); tot[0]+=1
        if a in (LIVE,OLD): tot[1]+=1; print('*** HIT',tag,ix,h,a,flush=True)
for bname,(paras,join) in BASES.items():
    N=len(paras)
    pin=[]  # (para index, char index, letter)
    for i,p in enumerate(paras):
        for j,c in enumerate(p):
            if c.isalpha(): pin.append((i,j,c)); break
    text=join.join(paras)
    # sentence initials -> (para index, offset in para, letter)
    offs=[]; acc=0
    for p in paras:
        offs.append(acc); acc+=len(p)+len(join)
    sin=[]
    start=0
    for m in re.finditer(r'[.!?]+["\u201d]?[ \t]*(?:\r?\n| |$)',text):
        end=m.end()
        for k in range(start,end):
            if text[k].isalpha():
                i=max(j for j in range(N) if offs[j]<=k)
                sin.append((i,k-offs[i],text[k])); break
        start=end
    for mark in marks:
        up=[c.upper() for _,_,c in pin]
        pos=[[k for k,c in enumerate(up) if c==ch] for ch in mark]
        if any(not p for p in pos): print(' no P channel for',mark,flush=True); 
        else:
            emb=[]
            def rec(i,last,cur):
                if i==len(mark): emb.append(tuple(cur)); return
                for k in pos[i]:
                    if k>last: rec(i+1,k,cur+[k])
            rec(0,-1,[])
            for keep in emb:
                ks=set(keep)
                ps=[paras[i] if i in ks else _lower(paras, i, pin) for i in range(N)]
                hit(hashlib.md5(join.join(ps).encode()).hexdigest(),f'{bname} P-dense {mark} {keep}')
                sel={k for k,c in enumerate(up) if c in set(mark)}-ks
                if sel:
                    ps=[_lower(paras,i,pin) if i in sel else paras[i] for i in range(N)]
                    hit(hashlib.md5(join.join(ps).encode()).hexdigest(),f'{bname} P-sparse {mark} {sorted(sel)}')
            print(f'  {bname} P {mark} emb={len(emb)} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
    print(f'-- {bname} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
