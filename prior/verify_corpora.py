import json,glob,re,collections

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
def parse(path):
    src=open(path).read(); m=re.search(r'BLOCKS = \[(.*?)\n\]', src, re.S)
    E=re.findall(r"Block\(number=(\d+), algorithm='([^']+)', exact_input=(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")\)", m.group(1), re.S)
    return {int(n):(a if a or not b else b).encode().decode('unicode_escape') for n,algo,a,b in E}
Q={'q1':parse('ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py'),
   'q2':parse('ninjaops-puzzle-lanes/quizchain/calib/quiz2_blocks.py')}
norm=lambda s: re.sub(r'\s+',' ',s)

# corpus B: quizchain introduction / guide pages (10 part dumps, 315 paras)
B=[]
for f in sorted(glob.glob('part_*_paras.json')):
    B += [x if isinstance(x,str) else str(x) for x in json.load(open(f))]
corpB=norm('\n'.join(B))

# corpus A: the 273-paragraph chapter
A=[t for _,t in json.load(open('wp_paras.json'))]
corpA=norm('\n'.join(A))

K=12
def lcs(b, chcf, kg):
    best=(0,None)
    for i in range(len(b)-K+1):
        w=b[i:i+K]
        if w in kg:
            pos=chcf.find(w); l=0
            while i-l>0 and pos-l>0 and b[i-l-1]==chcf[pos-l-1]: l+=1
            r=K
            while i+r<len(b) and pos+r<len(chcf) and b[i+r]==chcf[pos+r]: r+=1
            if l+r>best[0]: best=(l+r,pos-l)
    return best

res={}
for name,corp in (('chapter',corpA),('quizchain-guide',corpB)):
    cf=corp.casefold(); kg={cf[i:i+K] for i in range(len(cf)-K+1)}
    hits=[]
    for lbl in ('q1','q2'):
        for n in sorted(Q[lbl]):
            b=norm(Q[lbl][n].rstrip('\n')).casefold()
            L,pos=lcs(b,cf,kg)
            if L>=15: hits.append((lbl,n,L,corp[pos:pos+L] if pos is not None else ''))
    hits.sort(key=lambda t:-t[2])
    res[name]=hits
    print(f'== corpus {name}: {len(corp)} chars | inputs with LCS>=15: {len(hits)}')
    for lbl,n,L,frag in hits[:14]:
        print(f'   {lbl} b{n:<3} L={L:<5} {frag[:95]!r}')
json.dump({k:[list(t) for t in v] for k,v in res.items()},open('verify_corpora.json','w'),indent=1)
