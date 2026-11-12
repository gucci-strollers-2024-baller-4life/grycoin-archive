import json,re,difflib,glob

def parse(path):
    src=open(path).read()
    m=re.search(r'BLOCKS = \[(.*?)\n\]', src, re.S)
    E=re.findall(r"Block\(number=(\d+), algorithm='([^']+)', exact_input=(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")\)", m.group(1), re.S)
    return {int(n): (a if a or not b else b).encode().decode('unicode_escape') for n,algo,a,b in E}

q1=parse('ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py')
q2=parse('ninjaops-puzzle-lanes/quizchain/calib/quiz2_blocks.py')

paras=[x.strip() for x in json.load(open('chapter_paras_exact.json'))]
full='\n'.join(paras)
norm=lambda s: re.sub(r'\s+',' ',s)
fn=norm(full).casefold()
fmap=[]
for i,p in enumerate(paras): fmap += [i+1]*(len(norm(p))+1)
paracf=[norm(p).casefold() for p in paras]

def analyse(txt):
    raw=txt.rstrip('\n')
    b=norm(raw).casefold()
    sm=difflib.SequenceMatcher(None,b,fn,autojunk=False)
    ops=sm.get_opcodes()
    mb=[o for o in ops if o[0]=='equal' and o[2]-o[1]>=20]
    cov=sum(o[2]-o[1] for o in mb)/max(1,len(b))
    span=None
    if mb:
        span=(fmap[mb[0][3]], fmap[min(mb[-1][4],len(fmap)-1)])
    # case-only flips inside equal runs
    flips=[]
    for tag,i1,i2,j1,j2 in mb:
        # equal runs are on casefolded strings; map back to raw via proportional offsets is unsafe,
        # so do a direct substring comparison on the normalized originals
        pass
    return dict(cov=round(cov,3), matched=sum(o[2]-o[1] for o in mb), n=len(b), span=span, nrun=len(mb)), raw, b

rows=[]
for label,q in (('q1',q1),('q2',q2)):
    for num in sorted(q):
        r,raw,b=analyse(q[num])
        cls = 'EMBEDDED' if r['cov']>=0.85 and r['matched']>=200 else \
              'PARTIAL' if r['cov']>=0.40 and r['matched']>=100 else \
              'FRAGMENT' if r['matched']>=25 else 'NONE'
        rows.append(dict(quiz=label, block=num, cls=cls, **r))
json.dump(rows, open('verify_blocks.json','w'), indent=1)

from collections import Counter

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
print('total inputs:',len(rows))
print(Counter(r['cls'] for r in rows))
print('--- non-NONE / non-FRAGMENT:')
for r in sorted(rows,key=lambda r:-r['cov']):
    if r['cls'] in ('EMBEDDED','PARTIAL','FRAGMENT'):
        print(f"{r['quiz']} b{r['block']:>2} {r['cls']:9s} cov={r['cov']:.2f} matched={r['matched']:>5}/{r['n']:<5} paras {r['span']}")
print('--- largest NONE inputs (real texts, no 20-char run):')
for r in sorted([r for r in rows if r['cls']=='NONE'],key=lambda r:-r['n'])[:8]:
    print(f"{r['quiz']} b{r['block']:>2} n={r['n']} best={r['matched']}")
