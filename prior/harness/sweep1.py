import json, hashlib, btc, time, itertools, sys

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
wp=json.load(open('../repos/grycoin-rbb-hunt/wp_paras.json'))
P=[p[1] for p in wp]
JOIN='\r\n\r\n'
TGT=bytes.fromhex("2bc16867479a8d01179a6452651abe14a65eb61a")
def tgt_hit(text):
    h=hashlib.md5(text.encode()).hexdigest()
    try:
        return btc.hash160(btc.derive_path(btc.mnemonic_seed(btc.entropy_to_mnemonic(bytes.fromhex(h))), btc.DEFAULT_PATH))==TGT, h
    except Exception:
        return False, h
def flip_first(s,up=False):
    i=0
    while i<len(s) and not s[i].isalpha(): i+=1
    if i>=len(s): return s
    c=s[i]
    return s[:i]+(c.upper() if up else c.lower())+s[i+1:]
def flip_last(s,up=True):
    i=len(s)-1
    while i>=0 and not s[i].isalpha(): i-=1
    if i<0: return s
    c=s[i]
    return s[:i]+(c.upper() if up else c.lower())+s[i+1:]
def build(mode, idxs):
    out=list(P)
    for i in idxs:
        s=out[i-1]
        if mode in('both','first_down'): s=flip_first(s,False)
        if mode in('both','last_up'): s=flip_last(s,True)
        if mode=='first_up': s=flip_first(s,True)
        if mode=='last_down': s=flip_last(s,False)
        if mode=='inverse': s=flip_first(s,True); s=flip_last(s,False)
        if mode=='swapcase':
            s=''.join(c.swapcase() if c.isalpha() else c for c in s)
        out[i-1]=s
    return JOIN.join(out)

W=[list(range(5,9)),list(range(93,97)),list(range(168,172)),[231,232,233,235],[231,232,233,234,235],
   [5,6,7,8,93,94,95,96],[93,94,95,96,168,169,170,171],[5,6,7,8,168,169,170,171],
   list(range(5,9))+list(range(93,97))+list(range(168,172)),[34,78],[222],[229,230]]
modes=['both','first_down','last_up','first_up','last_down','inverse']
cands=[]
for w in W:
    for m in modes: cands.append((m,w))
# paragraphs containing 'sign'
sg=[i+1 for i,t in enumerate(P) if 'sign' in t.lower()]
for m in modes: cands.append((m,sg))
for m in modes: cands.append((m,[i for i in range(1,274)]))  # all paragraphs
t0=time.time(); hits=0
for m,w in cands:
    ok,h=tgt_hit(build(m,w))
    if ok: print("HIT",m,w,h); hits+=1
print("tested",len(cands),"hits",hits,"%.1fs"%(time.time()-t0))
# also plain-text variants of serialization: strip trailing spaces; drop trailing-space paras; no final newline etc.
variants={'plain':JOIN.join(P),'stripped':JOIN.join(p.strip() for p in P),'lf':'\n\n'.join(P)}
for k,v in variants.items():
    ok,h=tgt_hit(v); print(k,h,"HIT" if ok else "")
