import json,re,difflib

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
src=open('ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py').read()
m=re.search(r'BLOCKS = \[(.*?)\n\]', src, re.S)
entries=re.findall(r"Block\(number=(\d+), algorithm='([^']+)', exact_input=(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")\)", m.group(1), re.S)
blocks={int(n): (a if a or not b else b).encode().decode('unicode_escape') for n,algo,a,b in entries}
paras=[x.strip() for x in json.load(open('chapter_paras_exact.json'))]
full='\n'.join(paras); pmap=[]
for i,p in enumerate(paras): pmap+=[i+1]*(len(p)+1)
norm=lambda s: re.sub(r'\s+',' ',s).casefold()
fn=norm(full); fmap=[]
for i,p in enumerate(paras): fmap += [i+1]*(len(norm(p))+1)

out=[]
for num in sorted(blocks):
    b=norm(blocks[num])
    sm=difflib.SequenceMatcher(None,b,fn,autojunk=False)
    blk=sm.find_longest_match(0,len(b),0,len(fn))
    cov=blk.size/len(b)
    out.append((num, round(cov,3), blk.a, blk.b, blk.size, len(b),
                (fmap[blk.b], fmap[min(blk.b+blk.size,len(fmap)-1)])))
out.sort(key=lambda r:-r[1])
emb=[r for r in out if r[1]>=0.5]
print('blocks with >=50% longest-common-substring coverage:',len(emb),'of',len(out))
for r in out[:18]:
    print(f'b{r[0]:>2} cov={r[1]:.2f} paras {r[6][0]}-{r[6][1]} len={r[3]}')
json.dump(out, open('pal2.json','w'), indent=0)
