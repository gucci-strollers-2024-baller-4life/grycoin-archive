import json,re

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
P=[t for _,t in json.load(open('wp_paras.json'))]
norm=lambda s: re.sub(r'\s+',' ',s).strip()
ch=' || '.join(norm(p) for p in P)
chcf=ch.casefold()
posts=json.load(open('grycoin_posts.json'))['data']
Q=[]
for x in posts:
    st=x.get('selftext') or ''
    m=re.search(r'Question:\s*(.+?)(?:\n\s*\n|$)', st, re.S)
    if m: Q.append((x.get('title','')[:52], norm(m.group(1))[:400]))
print('posts with a Question line:',len(Q))
K=18; hits=[]
for title,q in Q:
    b=q.casefold()
    best=(0,None)
    for i in range(0,max(1,len(b)-K+1)):
        frag=b[i:i+K]
        if len(frag)<K: break
        pos=chcf.find(frag)
        if pos<0: continue
        l=0
        while i-l>0 and pos-l>0 and b[i-l-1]==chcf[pos-l-1]: l+=1
        r=K
        while i+r<len(b) and pos+r<len(chcf) and b[i+r]==chcf[pos+r]: r+=1
        if l+r>best[0]: best=(l+r,pos)
    if best[0]>=40:
        para=ch[:best[1]].count(' || ')+1
        hits.append((best[0],para,title,q[:70]))
hits.sort(reverse=True)
print('\nembedded questions found (LCS>=40):',len(hits))
for L,para,title,q in hits: print(f'  L={L:<4} para {para:<4} {title!r} :: {q!r}')
