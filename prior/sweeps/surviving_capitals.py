"""Inverse-R1 reading: the answer does not ADD capitals to spell the name, it REMOVES them so the
capitals that survive spell it. Block 29's answer marks AOI by case; in the demo the paragraph INITIALS
already contain A, O, I in order (paras 2, 6, 9) - and C3 of GRAMMAR_CONSTRAINTS says paragraph 5's
initial I is lowered, which this rule explains directly: P5 is not part of the name."""
import json,re,sys,hashlib,time,itertools

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
DEMO='1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi'
IDX=(0,1,2,76,44,77)
def derive(h,ix): return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,ix)))
tot=[0,0]
def check(text,tag,esc,oracle=None):
    h=hashlib.md5(text.encode()).hexdigest()
    if oracle and not h.startswith(oracle): return
    for ix in IDX:
        a=derive(h,ix); tot[0]+=1
        if a in esc: tot[1]+=1; print('*** HIT',tag,ix,h,a,flush=True)

def firsts(paras):
    return [next((c for c in p if c.isalpha()),'') for p in paras]
def lower_first(p):
    L=list(p)
    for j,c in enumerate(L):
        if c.isalpha():
            if c.isupper(): L[j]=c.lower()
            break
    return ''.join(L)
def raise_first(p):
    L=list(p)
    for j,c in enumerate(L):
        if c.isalpha():
            if c.islower(): L[j]=c.upper()
            break
    return ''.join(L)
def raise_lastsent(p):
    m=re.search(r'[.!?]',p)
    e=m.start() if m else len(p)
    L=list(p)
    for j in range(e-1,-1,-1):
        if L[j].isalpha():
            if L[j].islower(): L[j]=L[j].upper()
            break
    return ''.join(L)
def raise_last(p):
    L=list(p)
    for j in range(len(L)-1,-1,-1):
        if L[j].isalpha():
            if L[j].islower(): L[j]=L[j].upper()
            break
    return ''.join(L)

# ---------- demo
raw=open('demo_base.txt',encoding='utf-8').read()
paras=[p.strip() for p in re.split(r'\n\s*\n',raw.strip()) if p.strip()]
f=firsts(paras)
print('demo initials:',''.join(f),flush=True)
keep={1,5,8}   # 0-idx of paras 2 (A), 6 (O), 9 (I)
for jn,join in (('LF','\n\n'),('CRLF','\r\n\r\n')):
    # D1 keep-only
    ps=[paras[i] if i in keep else lower_first(paras[i]) for i in range(len(paras))]
    check(join.join(ps),f'demo-{jn} D1-keepAOI',{DEMO},oracle='3c6')
    # D2 + first-sentence-final raised on the paragraphs whose initial was lowered
    ps2=[raise_lastsent(p) if i not in keep else p for i,p in enumerate(ps)]
    check(join.join(ps2),f'demo-{jn} D2-keepAOI+fsl',{DEMO},oracle='3c6')
    # D3 + paragraph-final raised on lowered paragraphs
    ps3=[raise_last(p) if i not in keep else p for i,p in enumerate(ps)]
    check(join.join(ps3),f'demo-{jn} D3-keepAOI+pl',{DEMO},oracle='3c6')
    # D4 keep AOI, raise firsts of the AOI paragraphs too (i.e. inverted selection)
    ps4=[raise_first(paras[i]) if i in keep else lower_first(paras[i]) if i not in keep else paras[i] for i in range(len(paras))]
    check(join.join(ps4),f'demo-{jn} D4-keepAOI-inv',{DEMO},oracle='3c6')
    # D5 all initials lowered except A,O,I embeddings of every triple
    print(f'-- demo {jn} cands={tot[0]} hits={tot[1]}',flush=True)

# ---------- chapter: enumerate embeddings of a name in the initial string
br=json.load(open('wp_paras_br.json'))
ex=json.load(open('chapter_paras_exact.json'))
BASES={'ex-crlf':(ex,'\r\n\r\n'),
       'br-crlf':(['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n\r\n'),
       'br-lf':(['\n'.join(x) if isinstance(x,list) else x for x in br],'\n\n')}
NAMES=['AOI','STNM','NAKAMOTO','FINNEY','HAL','THOMAS','SATOMMI','SECOND']
t0=time.time()
for bname,(parasx,join) in BASES.items():
    f=[c.upper() for c in firsts(parasx)]
    N=len(parasx)
    for name in NAMES:
        # all in-order embeddings of name in the initial string
        pos=[[i for i,c in enumerate(f) if c==ch] for ch in name]
        if any(not p for p in pos): continue
        cnt=[0]
        def rec(i,last,keepset):
            if i==len(name):
                cnt[0]+=1
                if cnt[0]>200000: return
                ps=[parasx[k] if k in keepset else lower_first(parasx[k]) for k in range(N)]
                check(join.join(ps),f'{bname} keep-{name}-{sorted(keepset)}',{LIVE,OLD})
                return
            for j in pos[i]:
                if j>last:
                    rec(i+1,j,keepset|{j})
                    if cnt[0]>200000: return
        rec(0,-1,set())
    print(f'-- {bname} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
