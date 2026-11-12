"""Granularity combination never tested: choose paragraphs by a sign test, then flip at SENTENCE edges
inside those paragraphs (the demo's certified device is sentence-level; stage one's selection is
paragraph-level). Also runs the same selection on the demo, where the md5 '3c6' oracle is available."""
import json,hashlib,re,sys,time,itertools

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
def check(text,tag,escrows,oracle=None):
    h=hashlib.md5(text.encode()).hexdigest()
    if oracle and not h.startswith(oracle): return
    for idx in IDX:
        a=derive(h,idx); tot[0]+=1
        if a in escrows: tot[1]+=1; print('*** HIT',tag,idx,h,a,flush=True)

def spans(text):
    psp=[];start=0
    for m in re.finditer(r'(?:\r\n\r\n|\n\n)', text):
        psp.append((start,m.start())); start=m.end()
    psp.append((start,len(text)))
    ssp=[]
    for a,b in psp:
        s=0
        for m in re.finditer(r'[.!?]+["\u201d]?[ \t]*(?:\r?\n|$| )', text[a:b]):
            e=m.end()
            while e>s and text[a+e-1].isspace(): e-=1
            if e>s: ssp.append((a+s,a+e))
            s=m.end()
        if s< b-a:
            e=b-a
            while e>s and text[a+e-1].isspace(): e-=1
            if e>s: ssp.append((a+s,a+e))
    return psp,ssp

def flip(text, spans_, ops):
    t=list(text)
    for a,b in spans_:
        if 'fd' in ops:
            for j in range(a,b):
                if t[j].isalpha():
                    if t[j].isupper(): t[j]=t[j].lower()
                    break
        if 'lu' in ops:
            for j in range(b-1,a-1,-1):
                if t[j].isalpha():
                    if t[j].islower(): t[j]=t[j].upper()
                    break
    return ''.join(t)

SETS={'ITASM':'ITASM','SATOSHI':'SATOSHI','SATOI':'SATOI','SATOIH':'SATOIH','THOMAS':'THOMAS',
      'NAKAMOTO':'NAKAMOTO','FINNEY':'FINNEY','HALFINNEY':'HALFINNEY','AOI':'AOI','STNM':'STNM','GRYCOIN':'GRYCOIN'}
MODES=[('fd','lu'),('fd',),('lu',)]

# ---------- chapter
ex=json.load(open('chapter_paras_exact.json'))
br=json.load(open('wp_paras_br.json'))
BASES={'ex-crlf':'\r\n\r\n'.join(ex),
       'br-crlf':'\r\n\r\n'.join(['\r\n'.join(x) if isinstance(x,list) else x for x in br]),
       'br-lf':'\n\n'.join(['\n'.join(x) if isinstance(x,list) else x for x in br])}
t0=time.time()
for bname,text in BASES.items():
    psp,ssp=spans(text)
    pfirst=[next((text[j] for j in range(a,b) if text[j].isalpha()),'') for a,b in psp]
    # sentence -> paragraph index
    sidx=[]
    for a,b in ssp:
        k=next(i for i,(pa,pb) in enumerate(psp) if pa<=a<pb) if psp else 0
        sidx.append(k)
    for sname,S in SETS.items():
        sel=[i for i,f in enumerate(pfirst) if f.upper() in S]
        comp=[i for i,f in enumerate(pfirst) if f.upper() not in S]
        for gname,group in (('in',sel),('out',comp)):
            gs=set(group)
            vari={'all':[sp for sp,k in zip(ssp,sidx) if k in gs],
                  'firstS':[sp for sp,k in zip(ssp,sidx) if k in gs][:1],
                  'lastS':[sp for sp,k in zip(ssp,sidx) if k in gs][-1:]}
            for vname,vspans in vari.items():
                if not vspans: continue
                for ops in MODES:
                    check(flip(text,vspans,ops),f'{bname} {sname}-{gname}-{vname}-{"+".join(ops)}',{LIVE,OLD})
    print(f'-- {bname} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)

# ---------- demo (oracle)
raw=open('demo_base.txt',encoding='utf-8').read()
paras=[p.strip() for p in re.split(r'\n\s*\n',raw.strip()) if p.strip()]
for jn,join in [('LF','\n\n'),('CRLF','\r\n\r\n')]:
    text=join.join(paras)
    psp,ssp=spans(text)
    pfirst=[next((text[j] for j in range(a,b) if text[j].isalpha()),'') for a,b in psp]
    sidx=[next((i for i,(pa,pb) in enumerate(psp) if pa<=a<pb),0) for a,b in ssp]
    for sname,S in SETS.items():
        for gname,group in (('in',[i for i,f in enumerate(pfirst) if f.upper() in S]),
                            ('out',[i for i,f in enumerate(pfirst) if f.upper() not in S])):
            gs=set(group)
            ss=[sp for sp,k in zip(ssp,sidx) if k in gs]
            if not ss: continue
            vari={'all':ss,'firstS':ss[:1],'lastS':ss[-1:]}
            for vname,vspans in vari.items():
                for ops in MODES:
                    check(flip(text,vspans,ops),f'demo-{jn} {sname}-{gname}-{vname}-{"+".join(ops)}',{DEMO},oracle='3c6')
print('TOTAL',tot)
