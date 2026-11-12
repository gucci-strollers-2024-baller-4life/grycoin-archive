"""Word-level wordplay rules (block 2 / block 29 lineage) applied to the repaired chapter base.

Rule (block 2, verbatim): one letter of the author's family name is planted in the wrong case in the
question; the solver changes the OTHER letters of that name the same way. Rule (block 29): the
marked letters are the name, one occurrence each, in reading order, minimal span inside a sentence.
Here the seed is one of the planted case-odd capitals of the chapter; the chain then walks the name.
"""
import json,hashlib,sys,time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX=(0,1,2,76)
def derive(h,idx):
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,idx)))
res=[0,0]
def check(text,tag):
    h=hashlib.md5(text.encode()).hexdigest()
    for idx in IDX:
        a=derive(h,idx); res[0]+=1
        if a in (LIVE,OLD): res[1]+=1; print('*** HIT',tag,idx,h,a,flush=True)

ex=json.load(open('chapter_paras_exact.json'))
br=json.load(open('wp_paras_br.json'))
bases={
 'ex-crlf':'\r\n\r\n'.join(ex),
 'br-crlf':'\r\n\r\n'.join(['\r\n'.join(x) if isinstance(x,list) else x for x in br]),
 'br-lf':'\n\n'.join(['\n'.join(x) if isinstance(x,list) else x for x in br]),
}
SEEDS=[('ppM','M'),('VIrgin','I'),('BItcoin','I'),('abcdefghijkLmnopqrstuvwxyz','L')]
NAMES=['NAKAMOTO','AOI','THOMAS','SATOSHI','FINNEY','HALFINNEY','GRYCOIN','SECOND','AOINAKAMOTO','SATOMMI','STNM']
t0=time.time()
for bname,text in bases.items():
    low=text.lower()
    for word,letter in SEEDS:
        p=text.find(word)
        if p<0: continue
        seed=p+word.index(letter)
        if not text[seed].isupper(): continue
        for name in NAMES+[n[::-1] for n in NAMES]:
            order=list(name)
            # the seed's letter must be one of the name's letters; align it
            ls=low
            for align in range(len(order)):
                if order[align]!=letter: continue
                # S1: forward chain from the seed, index-aligned
                for wrap in (False,True):
                    t=list(text); pos=seed; ok=True
                    seq=[(align,j) for j in range(len(order))]
                    # walk: seed is order[align]; then align+1..len-1, then 0..align-1
                    marks=[seed]
                    cur=seed
                    for j in list(range(align+1,len(order)))+list(range(0,align)):
                        ch=order[j].lower()
                        nxt=ls.find(ch,cur+1)
                        if nxt<0:
                            if wrap: nxt=ls.find(ch,0,cur+1)
                            else: ok=False; break
                        marks.append(nxt); cur=nxt
                    if not ok: continue
                    for m in marks:
                        if t[m].islower(): t[m]=t[m].upper()
                    check(''.join(t),f'{bname} seed{word}@{letter} name={name} align{align} wrap{int(wrap)}')
            # S3: chain from the first occurrence of the name's first letter
            start=ls.find(order[0].lower())
            if start>=0:
                t=list(text); cur=start; marks=[start]; ok=True
                for j in range(1,len(order)):
                    nxt=ls.find(order[j].lower(),cur+1)
                    if nxt<0: ok=False; break
                    marks.append(nxt); cur=nxt
                if ok:
                    for m in marks:
                        if t[m].islower(): t[m]=t[m].upper()
                    check(''.join(t),f'{bname} greedy name={name}')
    print(f'-- {bname} cands={res[0]} hits={res[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',res)
