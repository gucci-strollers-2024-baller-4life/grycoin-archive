import json, hashlib, sys, time
sys.path.insert(0,'.')
from demo_oracle import derive

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
LIVE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; OLD="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
raw=json.load(open('wp_paras_br.json'))
P=["\r\n".join(p) if isinstance(p,list) else p for p in raw]
base="\r\n\r\n".join(P)
print("base md5:", hashlib.md5(base.encode()).hexdigest(), "chars:", len(base), flush=True)
WIN=[4,5,6,7,92,93,94,95,167,168,169,170,230,231,232,233,234]
t0=time.time(); n=0
for idx in (0,1):
    for mode in ('both','first','last'):
        for mask in range(1<<17):
            out=[]
            for i,p in enumerate(P):
                if i in WIN and (mask >> WIN.index(i)) & 1:
                    aix=[k for k,c in enumerate(p) if c.isalpha()]
                    if aix:
                        b=list(p)
                        if mode in ('both','first') and b[aix[0]].isupper(): b[aix[0]]=b[aix[0]].lower()
                        if mode in ('both','last') and b[aix[-1]].islower(): b[aix[-1]]=b[aix[-1]].upper()
                        p=''.join(b)
                out.append(p)
            txt="\r\n\r\n".join(out)
            h=hashlib.md5(txt.encode()).hexdigest()
            w,a=derive(bytes.fromhex(h), "m/44'/0'/0'/0/%d" % idx); n+=1
            if a in (LIVE,OLD):
                print("!!!! MATCH idx",idx,mode,mask,a,w,flush=True)
                open('RBB_SOLUTION.txt','w').write(txt); sys.exit(0)
            if n%100000==0: print("...%d %ds"%(n,time.time()-t0), flush=True)
print("done",n,"no match",flush=True)
