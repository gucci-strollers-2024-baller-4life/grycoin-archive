import json,re,difflib,collections

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

def parse(path):
    src=open(path).read(); m=re.search(r'BLOCKS = \[(.*?)\n\]', src, re.S)
    E=re.findall(r"Block\(number=(\d+), algorithm='([^']+)', exact_input=(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")\)", m.group(1), re.S)
    return {int(n):(a if a or not b else b).encode().decode('unicode_escape') for n,algo,a,b in E}
q1=parse('ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py')
q2=parse('ninjaops-puzzle-lanes/quizchain/calib/quiz2_blocks.py')

P=[t for _,t in json.load(open('wp_paras.json'))]
norm=lambda s: re.sub(r'\s+',' ',s)
chap=norm('\n'.join(P)); chcf=chap.casefold()
pmap=[]
for i,p in enumerate(P): pmap += [i+1]*(len(norm(p))+1)
K=12
kgrams={chcf[i:i+K] for i in range(len(chcf)-K+1)}
words=re.findall(r"[a-z0-9']+", chcf)
wset={tuple(words[i:i+6]) for i in range(len(words)-5)}

def lcs_info(b):
    """returns (longest common substring length, chapter offset, paragraph) using 12-gram anchors + exact extension"""
    anchors=[i for i in range(len(b)-K+1) if b[i:i+K] in kgrams]
    if not anchors: return 0,None,None
    # cluster anchors, try a sample of them
    best=(0,None)
    step=max(1,len(anchors)//40)
    for a in anchors[::step]+[anchors[-1]]:
        probe=b[a:a+K]; pos=chcf.find(probe)
        if pos<0: continue
        # extend left
        l=0
        while a-l>0 and pos-l>0 and b[a-l-1]==chcf[pos-l-1]: l+=1
        r=K
        while a+r<len(b) and pos+r<len(chcf) and b[a+r]==chcf[pos+r]: r+=1
        if l+r>best[0]: best=(l+r,pos-l)
    return best[0],best[1],pmap[best[1]] if best[1] is not None else None

rows=[]
for lbl,q in (('q1',q1),('q2',q2)):
    for n in sorted(q):
        raw=q[n].rstrip('\n'); b=norm(raw).casefold()
        L,off,para=lcs_info(b)
        # sentence coverage
        sents=[s.strip() for s in re.split(r'(?<=[.!?])\s+',norm(raw)) if len(s.strip())>=30]
        found=sum(1 for s in sents if norm(s).casefold() in chcf)
        # 6-gram word overlap
        bw=re.findall(r"[a-z0-9']+", b); bgs={tuple(bw[i:i+6]) for i in range(len(bw)-5)}
        ov=len(bgs&wset)/len(bgs) if bgs else 0.0
        rows.append(dict(quiz=lbl,block=n,n=len(b),lcs=L,para=para,sent=round(found/max(1,len(sents)),2),
                         nsent=len(sents),g6=round(ov,3)))
json.dump(rows,open('verify_full.json','w'),indent=1)

def verdict(r):
    if r['lcs']>=200: return 'EMBEDDED'
    if r['lcs']>=60: return 'SENTENCE+'
    if r['lcs']>=25: return 'PHRASE'
    if r['lcs']>=12: return 'FRAGMENT'
    return 'NONE'
for r in rows: r['v']=verdict(r)
c=collections.Counter(r['v'] for r in rows)
print('inputs',len(rows),dict(c))
print('\nnon-NONE, sorted:')
for r in sorted([r for r in rows if r['v']!='NONE'],key=lambda r:-r['lcs']):
    print(f"{r['quiz']} b{r['block']:<3} {r['v']:9s} lcs={r['lcs']:>5} para={str(r['para']):>5} len={r['n']:>5} sent={r['sent']:.2f}({r['nsent']}) g6={r['g6']:.2f}")
print('\nNONE with highest 6-gram overlap (<=5%):')
for r in sorted([r for r in rows if r['v']=='NONE'],key=lambda r:-r['g6'])[:10]:
    print(f"{r['quiz']} b{r['block']:<3} lcs={r['lcs']:>3} len={r['n']:>5} g6={r['g6']:.2f} sent={r['sent']:.2f}")
