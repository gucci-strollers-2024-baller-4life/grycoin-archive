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
for idx in range(0,6):
  for jn,J in (("CRLFCRLF","\r\n\r\n"),):
    for mode in ('both','first','last'):
        for mask in range(1<<16):
            out=[]
            for i,p in enumerate(P):
                if i in SIGN and (mask >> SIGN.index(i)) & 1:
                    aix=[k for k,c in enumerate(p) if c.isalpha()]
                    if aix:
                        b=list(p)
                        if mode in ('both','first') and b[aix[0]].isupper(): b[aix[0]]=b[aix[0]].lower()
                        if mode in ('both','last') and b[aix[-1]].islower(): b[aix[-1]]=b[aix[-1]].upper()
                        p=''.join(b)
                out.append(p)
            txt=J.join(out)
            h=hashlib.md5(txt.encode()).hexdigest()
            w,a=derive(bytes.fromhex(h), "m/44'/0'/0'/0/%d" % idx); n+=1
            if a in (LIVE,OLD):
                print("!!!! MATCH idx",idx, jn, mode, mask, a, w, flush=True)
                open('RBB_SOLUTION.txt','w').write(txt); sys.exit(0)
            if n%50000==0: print(f"...{n} {time.time()-t0:.0f}s", flush=True)
print("done",n,"no match", flush=True)
