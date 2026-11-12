"""Grammar-derived variant from the demo's own constraints.

The demo fixes three things at once:
  (1) the 'I' at the START of paragraph 5 becomes 'i'      -> paragraph-first letter, lowered
  (2) the final letter of that paragraph's FIRST sentence ('himself') becomes 'F'
  (3) the 'n' ending paragraph 2 ('capitalization.') is explicitly NOT part of the solution
(3) kills every reading that raises the final letter of the LAST sentence (P2 is one sentence, so
sentence-final and paragraph-final coincide there). (1)+(2) together fix the unit as
  "first letter of the paragraph, last letter of the paragraph's FIRST sentence".
That pairing has never been tested: the corpus tested paragraph-first with paragraph-final, and
sentence-first with sentence-final, but not paragraph-first with first-sentence-final.
"""
import json,re,sys,hashlib,time

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
def derive(h,idx):
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,idx)))
tot=[0,0]
def check(text,tag,esc,oracle=None):
    h=hashlib.md5(text.encode()).hexdigest()
    if oracle and not h.startswith(oracle): return
    for ix in IDX:
        a=derive(h,ix); tot[0]+=1
        if a in esc: tot[1]+=1; print('*** HIT',tag,ix,h,a,flush=True)

def units(text):
    """paragraph spans and, per paragraph, the end of its first sentence"""
    psp=[];start=0
    for m in re.finditer(r'(?:\r\n\r\n|\n\n)',text):
        psp.append((start,m.start())); start=m.end()
    psp.append((start,len(text)))
    fse=[]
    for a,b in psp:
        m=re.search(r'[.!?]',text[a:b])
        fse.append(a+m.start() if m else b)
    return psp,fse
def edit(p,first_sent_end,ops):
    L=list(p)
    if 'fd' in ops:
        for j,c in enumerate(L):
            if c.isalpha():
                if c.isupper(): L[j]=c.lower()
                break
    if 'lufs' in ops:
        e=first_sent_end-min(1,0)
        # index inside paragraph of the last alphabetic char at or before the first sentence end
        k=min(e,len(p))-0
        for j in range(min(e,len(p))-1,-1,-1):
            if L[j].isalpha():
                if L[j].islower(): L[j]=L[j].upper()
                break
    return ''.join(L)
def run(paras,join,label,esc,sets,oracle=None):
    text=join.join(paras)
    psp,fse=units(text)
    # map paragraph index -> first sentence end, offset inside paragraph
    offs=[]
    for i,(a,b) in enumerate(psp):
        offs.append(min(fse[i],b)-a)
    for sname,sel in sets.items():
        for ops in (('fd','lufs'),('fd',),('lufs',)):
            ps=list(paras)
            for k in sel: ps[k]=edit(ps[k],offs[k],ops)
            check(join.join(ps),f'{label} {sname} {"+".join(ops)}',esc,oracle)
    print(f'-- {label} cands={tot[0]} hits={tot[1]}',flush=True)

# ---- chapter
br=json.load(open('wp_paras_br.json'))
ex=json.load(open('chapter_paras_exact.json'))
B={'ex-crlf':(ex,'\r\n\r\n'),
   'br-crlf':(['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n\r\n'),
   'br-lf':(['\n'.join(x) if isinstance(x,list) else x for x in br],'\n\n')}
for bname,(paras,join) in B.items():
    first=[next((c for c in p if c.isalpha()),'').upper() for p in paras]
    N=len(paras)
    sets={'all':set(range(N)),
          'nonITASM':{i for i in range(N) if first[i] not in 'ITASM'},
          'SATOShi_anom':{i for i in range(N) if first[i] not in 'SATOI'},
          'ffww':{4,5,6,7,92,93,94,95,167,168,169,170,230,231,232,234},
          'signs14':{19,41,219,221,222,224,225,226,227,229,235,243,245,272},
          'lowercase10':{175,181,208,214,249,251,253,255,257,259}}
    run(paras,join,bname,{LIVE,OLD},sets)

# ---- demo, 2^10 subsets of paragraphs with the same mode
raw=open('demo_base.txt',encoding='utf-8').read()
paras=[p.strip() for p in re.split(r'\n\s*\n',raw.strip()) if p.strip()]
for jn,join in (('LF','\n\n'),('CRLF','\r\n\r\n')):
    text=join.join(paras); psp,fse=units(text)
    offs=[min(fse[i],b)-a for i,(a,b) in enumerate(psp)]
    ps0=list(paras)
    for mask in range(1,1<<len(paras)):
        ps=list(ps0)
        for k in range(len(paras)):
            if mask>>k&1: ps[k]=edit(ps[k],offs[k],('fd','lufs'))
        check(join.join(ps),f'demo-{jn} mask{mask}',{DEMO},oracle='3c6')
    print(f'-- demo {jn} cands={tot[0]} hits={tot[1]}',flush=True)
print('TOTAL',tot)
