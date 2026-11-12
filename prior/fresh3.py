import hashlib,json
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; ESC="1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
sol=open('safudev_stage1.txt').read().rstrip('\n')
lines=[l for l in sol.split('\n') if l.strip()]
P=[t for _,t in json.load(open('wp_paras.json'))]
fa=lambda s:next((c for c in s if c.isalpha()),'.')
def edge(s,mode):
    q=list(s); idx=[i for i,c in enumerate(q) if c.isalpha()]
    if not idx: return s
    f,l=idx[0],idx[-1]
    if 'f' in mode and q[f].isupper(): q[f]=q[f].lower()
    if 'l' in mode and q[l].islower(): q[l]=q[l].upper()
    return ''.join(q)
def posflip(s,positions,mode='u'):
    q=list(s)
    for p in positions:
        if 0<=p<len(q) and q[p].isalpha():
            q[p]=q[p].upper() if mode=='u' and q[p].islower() else (q[p].lower() if mode=='d' and q[p].isupper() else q[p])
    return ''.join(q)
tests={}
# A: Finney post selection families
L=lines
tests['A_ITASM']=[''.join(edge(x,'fl') if fa(x).upper() in 'ITASM' else x for x in L)]
tests['A_notITASM']=[''.join(edge(x,'fl') if fa(x).upper() not in 'ITASM' else x for x in L)]
tests['A_firsts']=[''.join(edge(x,'f') for x in L)]
tests['A_lasts']=[''.join(edge(x,'l') for x in L)]
tests['A_p1_4']=['\n'.join(edge(x,'fl') if i<4 else x for i,x in enumerate(L))]
tests['A_p13_16']=['\n'.join(edge(x,'fl') if i>=len(L)-4 else x for i,x in enumerate(L))]
tests['A_two_sets_4']=['\n'.join(edge(x,'fl') if i in (0,1,2,3,8,9,10,11) else x for i,x in enumerate(L))]
tests['A_even']=['\n'.join(edge(x,'fl') if i%2==0 else x for i,x in enumerate(L))]
tests['A_odd']=['\n'.join(edge(x,'fl') if i%2 else x for i,x in enumerate(L))]
# B: position-44 flips (both directions) on chapter and on Finney post
chap='\n\n'.join(P)
tests['B_chap44L']=[posflip(chap,[43,44,45,46],'u')]
tests['B_chap44R']=[posflip(chap,[len(chap)-45,len(chap)-44,len(chap)-43,len(chap)-42],'u')]
tests['B_chap44both']=[posflip(chap,[43,44,45,46,len(chap)-45,len(chap)-44,len(chap)-43,len(chap)-42],'u')]
tests['B_chap44both_d']=[posflip(chap,[43,44,45,46,len(chap)-45,len(chap)-44,len(chap)-43,len(chap)-42],'d')]
fin='\n'.join(L)
tests['B_fin44both']=[posflip(fin,[43,44,45,46,len(fin)-45,len(fin)-44,len(fin)-43,len(fin)-42],'u')]
n=0; hits=[]
for name,texts in tests.items():
    for t in texts:
        for jn in ('\n','\n\n'):
            body=t if name.startswith('A') else t
            if name.startswith('A'):
                txt=jn.join(body.split('\n'))
            else:
                txt=body
            d=hashlib.md5(txt.encode()).digest()
            for ix in range(0,4):
                w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
                if a in (PRIZE,ESC): hits.append((name,jn,ix))
print('derivations',n,'hits',hits)
