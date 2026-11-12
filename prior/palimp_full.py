import json,re,html,os
P=[t for _,t in json.load(open('wp_paras.json'))]
norm=lambda s: re.sub(r'\s+',' ',s).strip()
meta={p['id']:p['title'] for p in json.load(open('wparts.json'))['parts']}
src=[]
for pid,title in meta.items():
    if pid==720888559: continue
    raw=open(f'/tmp/ap/{pid}.txt',encoding='utf-8',errors='replace').read()
    for m in re.finditer(r'<p[^>]*data-p-id="[0-9a-f]+"[^>]*>(.*?)</p>',raw,re.S):
        t=norm(html.unescape(re.sub(r'<[^>]+>','',m.group(1))))
        for s in re.split(r'(?<=[.!?])\s+',t):
            if len(s)>=45: src.append((title,s))
for x in json.load(open('grycoin_posts.json'))['data']:
    for s in re.split(r'(?<=[.!?])\s+',norm(x.get('selftext') or '')):
        if len(s)>=45: src.append(('REDDIT:'+x.get('title','')[:32],s))
print('source sentences',len(src))
K=25; idx={}
for si,(tag,s) in enumerate(src):
    b=s.casefold()
    for i in range(0,len(b)-K+1,2): idx.setdefault(b[i:i+K],[]).append(si)
res=[]
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
    if best[0]>=70: res.append((pi+1,best[0],src[best[1]][0]))
from collections import Counter

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
print('paragraphs with a >=70-char source:',len(res))
c=Counter(t for _,_,t in res)
for t,k in c.most_common(): print(f'  {k:>3} paragraphs  <- {t}')
print('\nfirst 30:',res[:30])
