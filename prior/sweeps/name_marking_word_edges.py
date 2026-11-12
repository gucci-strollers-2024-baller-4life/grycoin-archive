"""R1, exactly as block 2's certified answer uses it.

Block 2's answer marks one occurrence of each letter of the hidden name, in reading order, and every
marked letter sits at a WORD EDGE: "a"->"A" (word-initial), "messaGe" (word-final), "You" (initial),
"oN" (final). The corpus tested minimal-span, all-occurrence and next-occurrence chains, but never the
word-edge restriction, which is the only one the solved example actually exhibits.

Here: per paragraph, every in-order chain of word-edge occurrences of the name, uppercased, whole
chapter hashed at the author's indices. Also anchored at the chapter's one planted interior capital
("ppM", para 73) for names that contain M.
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
def derive(h,idx):
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,idx)))
br=json.load(open('wp_paras_br.json'))
paras=['\r\n'.join(x) if isinstance(x,list) else x for x in br]
text='\r\n\r\n'.join(paras)
raw=text.encode('utf-8')
base=bytearray(raw)
# char index -> byte offset
boff=[0]*len(text); o=0
for i,c in enumerate(text):
    boff[i]=o; o+=len(c.encode('utf-8'))
def flip(js,delta):
    for j in js: base[boff[j]]+=delta
# paragraph spans in char indices
psp=[];start=0
for m in re.finditer(r'\r\n\r\n',text):
    psp.append((start,m.start())); start=m.end()
psp.append((start,len(text)))
# word edges per paragraph
edges=[[] for _ in psp]
for k,(a,b) in enumerate(psp):
    seg=text[a:b]
    for m in re.finditer(r"[A-Za-z']+", seg):
        s,e=m.start()+a,m.end()+a
        for j in range(s,e):
            if text[j].isalpha(): edges[k].append(j); break
        for j in range(e-1,s-1,-1):
            if text[j].isalpha(): edges[k].append(j); break
NAMES=['NAKAMOTO','AOI','STNM','SECOND','THOMAS','FINNEY','SATOSHI','GRYCOIN','SATOMMI','HALFINNEY']
tot=[0,0]; t0=time.time()
def run(namemap,label):
    for k,(a,b) in enumerate(psp):
        pos={}
        for j in edges[k]:
            c=text[j]
            if c.islower(): pos.setdefault(c,[]).append(j)
        for name in NAMES:
            seq=list(name.lower())
            lists=[pos.get(ch,[]) for ch in seq]
            if any(not l for l in lists): continue
            def rec(i,cur,marks):
                if i==len(seq):
                    flip(marks,-32)
                    h=hashlib.md5(bytes(base)).hexdigest()
                    flip(marks,32)
                    for ix in IDX:
                        ad=derive(h,ix); tot[0]+=1
                        if ad in (LIVE,OLD): tot[1]+=1; print('*** HIT',label,name,'para',k+1,marks,ix,h,ad,flush=True)
                    return
                for j in lists[i]:
                    if j>cur: rec(i+1,j,marks+[j])
            rec(0,-1,[])
    print(f'-- {label} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
run(None,'word-edge chains')
# anchored at the ppM capital in paragraph 73
seed_para=72
seedpos=text.index('ppM',psp[seed_para][0])+2
print('seed M at',seedpos,'para',seed_para+1,flush=True)
for name in ('NAKAMOTO','THOMAS','SATOMMI','AOINAKAMOTO'):
    seq=list(name.lower()); mi=seq.index('m')
    pos={}
    for j in edges[seed_para]:
        c=text[j]
        if c.islower(): pos.setdefault(c,[]).append(j)
    def rec(i,cur,marks):
        if i==len(seq):
            flip(marks,-32)
            h=hashlib.md5(bytes(base)).hexdigest()
            flip(marks,32)
            for ix in IDX:
                ad=derive(h,ix); tot[0]+=1
                if ad in (LIVE,OLD): tot[1]+=1; print('*** HIT seed',name,marks,ix,h,ad,flush=True)
            return
        if i==mi: rec(i+1,seedpos,marks+[seedpos]); return
        for j in pos.get(seq[i],[]):
            if j>cur: rec(i+1,j,marks+[j])
    rec(0,-1-0,[])
print('TOTAL',tot,'%.0fs'%(time.time()-t0))
