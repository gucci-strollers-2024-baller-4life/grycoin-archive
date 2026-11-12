"""Re-tests two families that were run before the base58 repair (their negatives are void):
(1) every contiguous run of paragraphs as the ENTIRE preimage  -- the demo's own preimage was a slice
    with an explicit start and stop, so the chapter's may be a slice too;
(2) 'the capitals travel to the end of each item' (the stage-one answer's own device) applied to every
    occurrence of the story's names in the chapter.
All at the author's index convention 0/1/2/76, on the repaired base and the old one."""
import json,hashlib,sys,time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX=(0,1,2,76,44,77)
def derive(h,idx):
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,idx)))
res=[0,0]
def check(text,tag):
    h=hashlib.md5(text.encode()).hexdigest()
    for idx in IDX:
        a=derive(h,idx); res[0]+=1
        if a in (LIVE,OLD): res[1]+=1; print('*** HIT',tag,'idx',idx,h,a,flush=True)

ex=json.load(open('chapter_paras_exact.json'))
br=json.load(open('wp_paras_br.json'))
brp=['\r\n'.join(x) if isinstance(x,list) else x for x in br]
brl=['\n'.join(x) if isinstance(x,list) else x for x in br]
BASES={'ex-crlf':(ex,'\r\n\r\n'),'br-crlf':(brp,'\r\n\r\n'),'br-lf':(brl,'\n\n')}
t0=time.time()

# (1) contiguous runs as whole preimage
for bname,(paras,join) in BASES.items():
    N=len(paras)
    for i in range(N):
        for j in range(i,N):
            check(join.join(paras[i:j+1]),f'{bname} run{i+1}-{j+1}')
    print(f'-- runs {bname} cands={res[0]} hits={res[1]} {time.time()-t0:.0f}s',flush=True)

# also: leading and trailing truncations are a subset of runs, done above.
# (2) capitals travel / name-case families
NAMES=['Satoshi','Nakamoto','Thomas','Finney','Hal','Bitcoin','Aoi','Second','Andrew','Yang','Grycoin','Satommi','TOM','Finney II']
def variants(word):
    w=word
    low=w.lower()
    out={}
    out['lastup']=low[:-1]+low[-1].upper()                 # satoshI  (initial lowered, last raised)
    out['lastup_keepinit']=w[:-1]+w[-1].upper()            # SatoshI
    out['allup']=w.upper()                                 # SATOSHI
    out['alldown']=low                                     # satoshi
    out['firstlow']=low                                    # same as alldown for capitals
    return out
for bname,(paras,join) in BASES.items():
    text=join.join(paras)
    for word in NAMES:
        if word not in text: continue
        for vname,rep in variants(word).items():
            if rep==word: continue
            check(text.replace(word,rep),f'{bname} case-{word}-{vname}-all')
    # combined: every name in one document, lastup
    t=text
    for word in NAMES:
        if word in t:
            low=word.lower(); t=t.replace(word,low[:-1]+low[-1].upper())
    check(t,f'{bname} case-ALL-lastup')
    t=text
    for word in NAMES:
        if word in t: t=t.replace(word,word.upper())
    check(t,f'{bname} case-ALL-allup')
    print(f'-- case {bname} cands={res[0]} hits={res[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',res,'%.0fs'%(time.time()-t0))
