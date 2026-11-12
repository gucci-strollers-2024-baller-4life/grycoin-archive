"""The typography channel: six non-breaking spaces are the chapter's only non-ASCII bytes.

Every one sits immediately before a normal space, e.g. "as a\\xa0 mechanism", "of\\xa0 transactions",
"anagram.\\xa0 What" - the signature of a copy-paste that carries both a NBSP and a space where the
author's own copy most likely had one space. That is a difference between our bytes and hers that no
case sweep can reach, and it is enumerable: six sites, 2^6 = 64 subsets, two readings
(NBSP deleted, or NBSP turned into a plain space), four joins.
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
IDX=(0,1,2,76,44,77)
def derive(h,ix): return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,ix)))
br=json.load(open('wp_paras_br.json'))
lines=[[x] if not isinstance(x,list) else x for x in br]
tot=[0,0]
def hit(txt,tag):
    h=hashlib.md5(txt.encode()).hexdigest()
    for ix in IDX:
        a=derive(h,ix); tot[0]+=1
        if a in (LIVE,OLD): tot[1]+=1; print('*** HIT',tag,ix,h,a,flush=True)
t0=time.time()
for inner in ('\n','\r\n'):
    for outer in ('\n\n','\r\n\r\n'):
        for reading in ('del','space'):
            for mask in range(64):
                ps=[]
                k=0
                for L in lines:
                    out=[]
                    for seg in L:
                        s=''
                        for ch in seg:
                            if ch=='\xa0':
                                if mask>>k & 1:
                                    s += '' if reading=='del' else ' '
                                else: s += ch
                                k+=1
                            else: s+=ch
                        out.append(s)
                    ps.append(inner.join(out))
                hit(outer.join(ps),f'{repr(inner)}/{repr(outer)} nbsp-{reading} mask{mask}')
        print(f'-- {repr(inner)}/{repr(outer)} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
