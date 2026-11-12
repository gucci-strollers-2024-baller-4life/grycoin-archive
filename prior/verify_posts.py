import json,re

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
P=[t for _,t in json.load(open('wp_paras.json'))]
norm=lambda s: re.sub(r'\s+',' ',s)
chap=norm('\n'.join(P)); chcf=chap.casefold()
pmap=[]
for i,p in enumerate(P): pmap += [i+1]*(len(norm(p))+1)
K=20
kg={chcf[i:i+K] for i in range(len(chcf)-K+1)}
d=json.load(open('grycoin_posts.json'))['data']
print('author posts:',len(d))
rows=[]
for x in d:
    t=norm((x.get('selftext') or ''))
    if len(t)<K: continue
    b=t.casefold(); best=(0,None)
    for i in range(len(b)-K+1):
        if b[i:i+K] in kg:
            pos=chcf.find(b[i:i+K]); l=0
            while i-l>0 and pos-l>0 and b[i-l-1]==chcf[pos-l-1]: l+=1
            r=K
            while i+r<len(b) and pos+r<len(chcf) and b[i+r]==chcf[pos+r]: r+=1
            if l+r>best[0]: best=(l+r,pos-l)
    rows.append((best[0],pmap[best[1]] if best[1] is not None else None,x.get('id'),x.get('title','')[:60]))
rows.sort(reverse=True)
print('posts with LCS>=40 vs chapter:')
for L,para,pid,title in rows:
    if L>=40: print(f'  L={L:<5} para={para:<4} {pid} {title!r}')
print('top 5 overall:',rows[:5])
