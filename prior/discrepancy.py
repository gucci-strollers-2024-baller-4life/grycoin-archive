import json,re,difflib

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
def parse(path):
    src=open(path).read(); m=re.search(r'BLOCKS = \[(.*?)\n\]', src, re.S)
    E=re.findall(r"Block\(number=(\d+), algorithm='([^']+)', exact_input=(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")\)", m.group(1), re.S)
    return {int(n):(a if a or not b else b).encode().decode('unicode_escape') for n,algo,a,b in E}
Q={'q1':parse('ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py'),'q2':parse('ninjaops-puzzle-lanes/quizchain/calib/quiz2_blocks.py')}
P=[t for _,t in json.load(open('wp_paras.json'))]
norm=lambda s: re.sub(r'\s+',' ',s)

# ---- 1. b29 vs chapter 11-29 at word level
b29=norm(Q['q1'][29].rstrip('\n')); chap=norm('\n'.join(P[10:29]))
wa=re.findall(r"\S+|\s+",b29); wb=re.findall(r"\S+|\s+",chap)
sm=difflib.SequenceMatcher(None,[w.strip() for w in wa],[w.strip() for w in wb],autojunk=False)
ops=[o for o in sm.get_opcodes() if o[0]!='equal']
print('b29 vs chapter 11-29: word ops',len(ops))
ins=sum(o[4]-o[3] for o in ops if o[0]=='insert'); dele=sum(o[2]-o[1] for o in ops if o[0]=='delete')
rep=sum(1 for o in ops if o[0]=='replace')
print(f'  inserted words {ins}, deleted words {dele}, replacements {rep}')
for o in ops:
    t,i1,i2,j1,j2=o
    A=' '.join(x.strip() for x in wa[i1:i2]); B=' '.join(x.strip() for x in wb[j1:j2])
    if len(A)>90: A=A[:90]+'...'
    if len(B)>90: B=B[:90]+'...'
    print(f'   {t:8s} block=[{A}]  chapter=[{B}]')

# ---- 2. how much of the Finney post (q2 b77) does the chapter contain?
t77=Q['q2'][77].rstrip('\n')
paras77=[p.strip() for p in re.split(r'\n\s*\n|\n',t77) if p.strip()]
chcf=norm('\n'.join(P)).casefold()
print(f'\nq2 b77: {len(paras77)} paragraphs in the block')
found=0; tot=0; miss=[]
for i,p in enumerate(paras77,1):
    key=norm(p).casefold(); tot+=len(key)
    if key in chcf: found+=len(key)
    else:
        # partial: longest run
        best=0
        for L in (40,30,20):
            for k in range(0,len(key)-L,10):
                if key[k:k+L] in chcf: best=max(best,L); break
        miss.append((i,len(key),best,p[:50]))
print(f'  chapter contains {found}/{tot} chars of the block text ({found/tot:.2f})')
print(f'  paragraphs not fully present: {len(miss)}')
for m in miss[:8]: print('   para',m[0],'len',m[1],'bestrun',m[2],repr(m[3]))

# ---- 3. b66 vs the clause the chapter adds to the b29 scene
b66=norm(Q['q2'][66]).casefold()
print('\nq2 b66 in chapter para 29:', b66 in norm(P[28]).casefold())
print('q2 b66 in b29 text:', b66 in norm(Q['q1'][29]).casefold())
