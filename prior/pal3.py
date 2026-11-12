import json,re,difflib

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
src=open('ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py').read()
m=re.search(r'BLOCKS = \[(.*?)\n\]', src, re.S)
E=re.findall(r"Block\(number=(\d+), algorithm='([^']+)', exact_input=(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")\)", m.group(1), re.S)
blocks={int(n): (a if a or not b else b).encode().decode('unicode_escape') for n,algo,a,b in E}
paras=[x.strip() for x in json.load(open('chapter_paras_exact.json'))]
full='\n'.join(paras)
fn=re.sub(r'\s+',' ',full).casefold()
# map normalized index -> paragraph
fmap=[]
for i,p in enumerate(paras): fmap += [i+1]*(len(re.sub(r'\s+',' ',p))+1)
rows=[]
for num in sorted(blocks):
    raw=blocks[num].rstrip('\n')
    b=re.sub(r'\s+',' ',raw).casefold()
    sm=difflib.SequenceMatcher(None,b,fn,autojunk=False)
    mb=[x for x in sm.get_matching_blocks() if x.size>=20]
    cov=sum(x.size for x in mb)/max(1,len(b))
    span=None; flips=[]
    if mb:
        p0=fmap[mb[0].b]; p1=fmap[min(mb[-1].b+mb[-1].size,len(fmap)-1)]
        span=(p0,p1)
        for x in mb:
            seg_b=raw[x.a:x.a+x.size] if x.size==1 else None
        # case diffs over exact-equal normalized runs: use raw offsets approx via equal opcodes on raw
    rows.append(dict(block=num,cov=round(cov,3),span=span,n=len(b),matched=sum(x.size for x in mb),nmatch=len(mb)))
rows.sort(key=lambda r:-r['cov'])
json.dump(rows,open('palimpsest_index.json','w'),indent=1)
strong=[r for r in rows if r['cov']>=0.5]
print('total blocks',len(rows),'| >=0.5 coverage:',len(strong))
for r in rows[:20]:
    print(f"b{r['block']:>2} cov={r['cov']:.2f} matched={r['matched']:>5}/{r['n']:<5} paras {r['span']}")
