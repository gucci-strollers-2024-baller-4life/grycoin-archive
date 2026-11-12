import json, hashlib, sys, time
sys.path.insert(0,'.')
from demo_oracle import derive

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
paras = json.load(open('chapter_paras_exact.json'))
N=len(paras)
LIVE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD ="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
SIGN=[5,6,7,8,93,94,95,96,168,169,170,171,230,231,232,234]
SIGN=[p-1 for p in SIGN]  # 0-based
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def flip_para(p, mode):
    idx=alpha_idx(p)
    if not idx: return p
    b=list(p)
    if mode in ('both','first') and b[idx[0]].isupper(): b[idx[0]]=b[idx[0]].lower()
    if mode in ('both','last') and b[idx[-1]].islower(): b[idx[-1]]=b[idx[-1]].upper()
    return ''.join(b)
def build(units, join, mode):
    return join.join(flip_para(p,mode) if i in units else p for i,p in enumerate(paras)).encode()
t0=time.time(); n=0
for jn, j in (("CRLF","\r\n"),):
    for mode in ('both','first','last'):
        for mask in range(1<<16):
            units = {SIGN[i] for i in range(16) if mask>>i&1}
            data = build(units, j, mode)
            h = hashlib.md5(data).hexdigest()
            words, addr = derive(bytes.fromhex(h))
            n+=1
            if addr in (LIVE,OLD):
                print("!!!!!!!! MATCH", jn, mode, "mask", mask, sorted(u+1 for u in units), addr, words, flush=True)
                open('RBB_SOLUTION.txt','wb').write(data)
                print("md5:", h, flush=True)
                sys.exit(0)
            if n % 50000 == 0:
                print(f"...{n} derived {time.time()-t0:.0f}s", flush=True)
print(f"done {n} candidates, no match, {time.time()-t0:.0f}s")
