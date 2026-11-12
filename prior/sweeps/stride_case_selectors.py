"""R3/R20 gap: stride keys used as CASE EDIT selectors. §20 applied only strides 7 and 44 at
paragraph/sentence/word granularity. Here every other stride the story supplies (2,3,4,5,11,21,22,37,
77,88) is used as a selector at word AND letter granularity, all offsets, four directions."""
import json,re,sys,hashlib,time

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

ex=json.load(open('chapter_paras_exact.json'))
br=json.load(open('wp_paras_br.json'))
BASES={'ex-crlf':'\r\n\r\n'.join(ex),
       'br-crlf':'\r\n\r\n'.join(['\r\n'.join(x) if isinstance(x,list) else x for x in br]),
       'br-lf':'\n\n'.join(['\n'.join(x) if isinstance(x,list) else x for x in br])}
STRIDES=[2,3,4,5,11,21,22,37,77,88]
t0=time.time()
for bname,text in BASES.items():
    words=[(m.start(),m.end()) for m in re.finditer(r"[A-Za-z']+", text)]
    letters=[i for i,c in enumerate(text) if c.isalpha()]
    def edit(units,sel,mode):
        t=list(text)
        for k in sel:
            a,b=units[k]
            if mode=='fu':
                for j in range(a,b):
                    if t[j].isalpha():
                        if t[j].islower(): t[j]=t[j].upper()
                        break
            elif mode=='fd':
                for j in range(a,b):
                    if t[j].isalpha():
                        if t[j].isupper(): t[j]=t[j].lower()
                        break
            elif mode=='lu':
                for j in range(b-1,a-1,-1):
                    if t[j].isalpha():
                        if t[j].islower(): t[j]=t[j].upper()
                        break
            elif mode=='ld':
                for j in range(b-1,a-1,-1):
                    if t[j].isalpha():
                        if t[j].isupper(): t[j]=t[j].lower()
                        break
        return ''.join(t)
    for s in STRIDES:
        for o in range(s):
            sel=[i for i in range(o,len(words),s)]
            for mode in ('fu','fd','lu','ld'):
                check(edit(words,sel,mode),f'{bname} word-s{s}o{o}-{mode}')
    for s in (4,7,11,22,44):
        for o in range(s):
            sel=[i for i in range(o,len(letters),s)]
            units=[(p,p+1) for p in letters]
            for mode in ('fu','fd'):
                check(edit(units,sel,mode),f'{bname} letter-s{s}o{o}-{mode}')
    print(f'-- {bname} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
