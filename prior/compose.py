import json,re,html,os

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
P=[t for _,t in json.load(open('wp_paras.json'))]
norm=lambda s: re.sub(r'\s+',' ',s).strip()
meta={p['id']:p['title'] for p in json.load(open('wparts.json'))['parts']}
src=[]
for pid,title in meta.items():
    if pid==720888559: continue
    raw=open(f'/tmp/ap/{pid}.txt',encoding='utf-8',errors='replace').read()
    for m in re.finditer(r'<p[^>]*data-p-id="[0-9a-f]+"[^>]*>(.*?)</p>',raw,re.S):
        t=norm(html.unescape(re.sub(r'<[^>]+>','',m.group(1))))
        if len(t)>=30: src.append((title,t))
print('source paragraphs',len(src))
K=20; idx={}
for si,(title,s) in enumerate(src):
    b=s.casefold()
    for i in range(0,len(b)-K+1,2): idx.setdefault(b[i:i+K],[]).append(si)
comp=[]
for pi,p in enumerate(P):
    b=norm(p).casefold(); best=(0,None)
    for i in range(0,max(1,len(b)-K+1)):
        for si in idx.get(b[i:i+K],[]):
            s=src[si][1].casefold(); pos=s.find(b[i:i+K])
            if pos<0: continue
            l=0
            while i-l>0 and pos-l>0 and b[i-l-1]==s[pos-l-1]: l+=1
            r=K
            while i+r<len(b) and pos+r<len(s) and b[i+r]==s[pos+r]: r+=1
            if l+r>best[0]: best=(l+r,si)
    comp.append((best[1] is not None and best[0]>=60, src[best[1]][0] if best[1] is not None and best[0]>=60 else None, best[0]))
json.dump([[c[0],c[1],c[2]] for c in comp],open('composition.json','w'))
runs=[]
for i,(ok,title,L) in enumerate(comp):
    key=title if ok else 'ORIGINAL'
    if runs and runs[-1][2]==key: runs[-1][1]=i+1
    else: runs.append([i+1,i+1,key])
print('\ncomposition runs (start-end <- source):')
for a,b,k in runs: print(f'  {a:>3}-{b:<3} <- {k}')
print('\ndistinct sources used:',len({k for _,_,k in runs if k!="ORIGINAL"}))
