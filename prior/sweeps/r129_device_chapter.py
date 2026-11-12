"""R1:29's device applied to the chapter: one word marked AOI, the author's own chapter-answer habit."""
import json,re,sys,hashlib

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
br=json.load(open('wp_paras_br.json'))
lines=[[x] if not isinstance(x,list) else x for x in br]
def build(inner,outer):
    ps=[inner.join(L) for L in lines]
    return outer.join(ps), ps
IDX=(0,1,2,76)
def derive(h):
    out=[]
    for i in IDX:
        a=fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,i)))
        if a in (LIVE,OLD): out.append((i,a))
    return out
tot=0; hits=0
for inner,outer in (('\n','\n\n'),('\r\n','\r\n\r\n')):
    text,ps=build(inner,outer)
    sent=[];start=0
    for m in re.finditer(r'[.!?]+["\u201d]?[ \t]*(?:\r?\n| |$)',text):
        sent.append((start,m.end())); start=m.end()
    sent.append((start,len(text)))
    cands=[]
    for a,b in sent:
        s=text[a:b]
        arts=[m for m in re.finditer(r'(?<![A-Za-z])[Aa](?![A-Za-z])',s)]
        words=[m for m in re.finditer(r"[A-Za-z]+",s)]
        for m in arts:
            for w in words:
                if w.start()<=m.end(): continue
                lw=w.group().lower()
                if 'o' in lw and lw.index('o')<lw.rfind('i'):
                    cands.append((a+m.start(), a+w.start(), lw, a+w.start()+lw.index('o'), a+w.start()+lw.rfind('i')))
    for art,ws,lw,op,ip in cands:
        for mode in ('aoi','oi'):
            b=bytearray(text.encode())
            # byte offsets
            def bo(i): return len(text[:i].encode())
            for pos in ((art,ws,op,ip) if mode=='aoi' else (ws,op,ip)):
                p=bo(pos); b[p]=b[p]-32 if 97<=b[p]<=122 else b[p]
            h=hashlib.md5(bytes(b)).hexdigest(); tot+=1
            r=derive(h)
            if r: hits+=1; print('*** HIT',mode,lw,r,flush=True)
    print(f'-- {inner!r}/{outer!r} cands={len(cands)*2} total={tot} hits={hits}',flush=True)
print(f'TOTAL [{tot}, {hits}]')
