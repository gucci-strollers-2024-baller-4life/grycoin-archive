import json,re,difflib

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
src=open('ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py').read()
m=re.search(r'BLOCKS = \[(.*?)\n\]', src, re.S)
E=re.findall(r"Block\(number=(\d+), algorithm='([^']+)', exact_input=(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")\)", m.group(1), re.S)
blk={int(n):(a if a or not b else b).encode().decode('unicode_escape') for n,algo,a,b in E}[29]
paras=[x.strip() for x in json.load(open('chapter_paras_exact.json'))]
seg='\n'.join(paras[10:29])   # paras 11..29
a=blk.rstrip('\n'); b=seg
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
flips=[];diffs=[]
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal':
        for k in range(i2-i1):
            x,y=a[i1+k],b[j1+k]
            if x!=y and x.isalpha() and y.isalpha():
                ctx=a[max(0,i1+k-12):i1+k+12].replace('\n','|')
                flips.append((i1+k,x,y,ctx))
    else:
        diffs.append((tag,repr(a[i1:i2])[:90],repr(b[j1:j2])[:90]))
print('matched chars:',sum(i2-i1 for t,i1,i2,j1,j2 in sm.get_opcodes() if t=='equal'),'of',len(a))
print('\nCASE FLIPS (%d):'%len(flips))
for p,x,y,ctx in flips: print(f'  pos {p:>4} block={x!r} chapter={y!r}  ...{ctx}...')
print('\nTEXT DIFFS (%d):'%len(diffs))
for t,x,y in diffs: print(f'  {t:8s} block={x}\n           chapter={y}')
