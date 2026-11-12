import json,re,sys

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
br=json.load(open('wp_paras_br.json'))
def build(inner,outer):
    return outer.join(inner.join(x) if isinstance(x,list) else x for x in br)
bases={}
for nm,inner,outer in (('br-lf','\n','\n\n'),('br-crlf','\r\n','\r\n\r\n')):
    t=build(inner,outer); bases[nm]=t
text=bases['br-lf']
nums=set()
for m in re.finditer(r'\d[\d,\.]*',text):
    s=m.group().replace(',','').rstrip('.')
    try: nums.add(int(float(s)))
    except: pass
nums=sorted(nums)
print('numbers',nums)
N=273
def variant(t,paras,idx,mode):
    ps=list(paras)
    p=ps[idx]
    lo=next((k for k,c in enumerate(p) if c.isalpha()),None)
    hi=next((k for k in range(len(p)-1,-1,-1) if p[k].isalpha()),None)
    if lo is None: return None
    q=list(p)
    if mode in ('fd','both') and q[lo].isupper(): q[lo]=q[lo].lower()
    if mode in ('lu','both') and hi is not None and q[hi].islower(): q[hi]=q[hi].upper()
    ps[idx]=''.join(q); return ps
tot=0;hit=0
def derive(t):
    global tot,hit
    md5=__import__('hashlib').md5(t.encode()).hexdigest()
    for i in (0,1,2,76):
        tot+=1
        a=fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(md5)),(44+H,0+H,0+H,0,i)))
        if a in (LIVE,OLD):
            hit+=1; print('*** HIT',md5,i,a,flush=True)
for nm,t in bases.items():
    inner='\n' if nm=='br-lf' else '\r\n'; outer='\n\n' if nm=='br-lf' else '\r\n\r\n'
    ps=t.split(outer)
    for n in nums:
        tgt=set()
        for v in (n%N,(N-n%N)%N,sum(int(c) for c in str(n))%N):
            for off in (-1,0,1):
                i=(v+off)%len(ps); tgt.add(i)
        for i in tgt:
            for mode in ('fd','lu','both'):
                q=variant(t,ps,i,mode)
                if q: derive(outer.join(q))
    print('--',nm,'tot',tot,'hits',hit,flush=True)
print('TOTAL',tot,hit)
