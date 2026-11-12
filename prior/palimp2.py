import json,re,glob

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
P=[t for _,t in json.load(open('wp_paras.json'))]
norm=lambda s: re.sub(r'\s+',' ',s).strip()
# source sentences: posts + local parts
src=[]
for x in json.load(open('grycoin_posts.json'))['data']:
    st=norm(x.get('selftext') or '')
    for s in re.split(r'(?<=[.!?])\s+', st):
        if len(s)>=40: src.append((x.get('title','')[:44], s))
for f in glob.glob('part_*_paras.json'):
    for i,t in enumerate(json.load(open(f))):
        if isinstance(t,str):
            for s in re.split(r'(?<=[.!?])\s+', norm(t)):
                if len(s)>=40: src.append((f.split('_')[1]+'#'+str(i), s))
print('source sentences',len(src))
K=18
idx={}
for si,(tag,s) in enumerate(src):
    b=s.casefold()
    for i in range(0,len(b)-K+1,3):
        idx.setdefault(b[i:i+K],[]).append(si)
print('anchors',len(idx))
found=[]
for pi,p in enumerate(P):
    b=norm(p).casefold(); best=(0,None)
    for i in range(0,max(1,len(b)-K+1)):
        for si in idx.get(b[i:i+K],[]):
            s=src[si][1].casefold()
            if len(b)<K: continue
            pos=s.find(b[i:i+K])
            if pos<0: continue
            l=0
            while i-l>0 and pos-l>0 and b[i-l-1]==s[pos-l-1]: l+=1
            r=K
            while i+r<len(b) and pos+r<len(s) and b[i+r]==s[pos+r]: r+=1
            if l+r>best[0]: best=(l+r,si)
    if best[0]>=45: found.append((best[0],pi+1,src[best[1]][0],P[pi][:70]))
found.sort(reverse=True)
print('\nchapter paragraphs reusing source text (LCS>=45):',len(found))
for L,para,tag,txt in found[:25]: print(f'  L={L:<4} para {para:<4} <- {tag:<16} {txt!r}')
