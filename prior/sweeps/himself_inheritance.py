"""R2 inheritance at word level: the demo's two worked changes are the exemplars, not the answer.

C3 lowers the 'I' that opens a paragraph; C4 raises the final letter of 'himself'. If the pattern is
inherited by WORD rather than by position, the chapter's own occurrences of those two tokens are the
candidate sites. The chapter has nine 'himself' tokens (paras 126, 205, 215, 218x2, 219, 248, 254) and
a large number of paragraphs that open on the word 'I'.
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
IDX=(0,1,2,76)
def derive(h,ix): return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,ix)))
br=json.load(open('wp_paras_br.json')); ex=json.load(open('chapter_paras_exact.json'))
BASES={'br-crlf':(['\r\n'.join(x) if isinstance(x,list) else x for x in br],'\r\n\r\n'),
       'br-lf':(['\n'.join(x) if isinstance(x,list) else x for x in br],'\n\n'),
       'ex-crlf':(ex,'\r\n\r\n')}
tot=[0,0]; t0=time.time()
for bname,(paras,join) in BASES.items():
    occ=[(i,m.start()) for i,p in enumerate(paras) for m in re.finditer(r'\bhimself\b',p)]
    Istart=[i for i,p in enumerate(paras) if re.match(r'"?(I)\b',p)]
    print(bname,'himself tokens',len(occ),'paragraphs opening on I',len(Istart),flush=True)
    for mask in range(1<<len(occ)):
        ps=list(paras)
        for k,(i,off) in enumerate(occ):
            if mask>>k&1:
                p=ps[i]; ps[i]=p[:off]+'himselF'+p[off+7:]
        base_text=join.join(ps)
        h=hashlib.md5(base_text.encode()).hexdigest()
        for ix in IDX:
            a=derive(h,ix); tot[0]+=1
            if a in (LIVE,OLD): tot[1]+=1; print('*** HIT himself',bname,mask,ix,h,a,flush=True)
        # + lower every paragraph-opening 'I'
        if mask in (0,(1<<len(occ))-1):
            ps2=list(ps)
            for i in Istart:
                p=ps2[i]; j=p.index('I'); ps2[i]=p[:j]+'i'+p[j+1:]
            h2=hashlib.md5(join.join(ps2).encode()).hexdigest()
            for ix in IDX:
                a=derive(h2,ix); tot[0]+=1
                if a in (LIVE,OLD): tot[1]+=1; print('*** HIT himself+I',bname,mask,ix,h2,a,flush=True)
    print(f'-- {bname} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot)
