import json,re,glob,difflib

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
P=[t for _,t in json.load(open('wp_paras.json'))]
norm=lambda s: re.sub(r'\s+',' ',s).strip()
parts={}
for f in glob.glob('part_*_paras.json'):
    tag=f.split('_')[1]
    parts[tag]=[t for t in json.load(open(f)) if isinstance(t,str)]
posts={x.get('title','')[:44]:x.get('selftext') or '' for x in json.load(open('grycoin_posts.json'))['data']}
pairs=[(183,757574334,0),(184,757574334,1),(185,757574334,3),(186,757574334,4),(187,757574334,5),
       (189,757574334,7),(190,757574334,8),(191,757574334,9),(192,757574334,10),(193,757574334,11),
       (194,757574334,12),(195,757574334,13),(196,757574334,14),(199,757574334,17),(200,757574334,18),
       (201,757574334,19),(204,757574334,22),(205,757574334,23),(206,757574334,24)]
diffs=[]
for pno,tag,idx in pairs:
    a=norm(P[pno-1]).split(); b=norm(parts[str(tag)][idx]).split()
    sm=difflib.SequenceMatcher(a=[w.lower() for w in a], b=[w.lower() for w in b])
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal':
            for k in range(i2-i1):
                w1,w2=a[i1+k],b[j1+k]
                if w1!=w2: diffs.append((pno,w2,w1))
print('case-only differences between chapter copy and its source part:',len(diffs))
for pno,src,cp in diffs[:60]: print(f'  p{pno}: source={src!r} chapter={cp!r}')
print('\nfirst letters of differing words:', ''.join((d[2][:1] if d[2] else '?') for d in diffs))
