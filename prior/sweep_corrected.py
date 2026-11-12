import json, hashlib, sys, time
sys.path.insert(0,'.')
from demo_oracle import derive

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
LIVE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; OLD="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
segs=json.load(open('wp_paras_br.json'))
# normalize into list of paragraph strings (internal breaks preserved as \n)
def para(p):
    if isinstance(p,str): return p
    if isinstance(p,list): return "\n".join(p)
    return str(p)
P=[para(p) for p in segs]
print("paras:", len(P), flush=True)
SIGN=[4,5,6,7,92,93,94,95,167,168,169,170,230,231,232,234]
t0=time.time(); n=0
for jn,J in (("CRLFCRLF","\r\n\r\n"),("LF","\n\n")):
    for mode in ('both','first','last'):
        for mask in range(1<<16):
            out=[]
            for i,p in enumerate(P):
                if i in SIGN and (mask >> SIGN.index(i)) & 1:
                    idx=[k for k,c in enumerate(p) if c.isalpha()]
                    if idx:
                        b=list(p)
                        if mode in ('both','first') and b[idx[0]].isupper(): b[idx[0]]=b[idx[0]].lower()
                        if mode in ('both','last') and b[idx[-1]].islower(): b[idx[-1]]=b[idx[-1]].upper()
                        p=''.join(b)
                out.append(p)
            txt=J.join(out)
            h=hashlib.md5(txt.encode()).hexdigest()
            w,a=derive(bytes.fromhex(h)); n+=1
            if a in (LIVE,OLD):
                print("!!!! MATCH", jn, mode, mask, a, w, flush=True)
                open('RBB_SOLUTION.txt','w').write(txt); sys.exit(0)
            if n%50000==0: print(f"...{n} {time.time()-t0:.0f}s", flush=True)
print("done",n,"no match", flush=True)
