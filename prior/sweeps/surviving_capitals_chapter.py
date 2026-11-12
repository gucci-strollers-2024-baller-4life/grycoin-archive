"""Surviving-capitals reading, chapter side (the piece left open on 2026-10-30).

Rule: the paragraph INITIALS are the sign channel (the chapter says so for stage one). The answer does not
add capitals to spell the name - it removes them, so the initials that stay upper case spell it.

V1 dense : lower every paragraph initial except the embedding.
V2 sparse: lower only the initials that are the same letter as a name letter but not in the embedding
           (this is the variant that matches "change only a couple of letters"; in the demo it lowers 4
           initials, and the one the author names in C3 is among them).
"""
import json,hashlib,sys,time

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
br=json.load(open('wp_paras_br.json'))
paras=['\r\n'.join(x) if isinstance(x,list) else x for x in br]
join='\r\n\r\n'
f=[]
for p in paras:
    for j,c in enumerate(p):
        if c.isalpha(): f.append((j,c)); break
    else: f.append((0,''))
init=[c.upper() for _,c in f]
def lower_at(p,idx):
    L=list(p); L[idx]=L[idx].lower(); return ''.join(L)
tot=[0,0]; t0=time.time()
for name in ['AOI','STNM','AOIN','THOMAS','NAKAMOTO','SATO']:
    pos=[[i for i,c in enumerate(init) if c==ch] for ch in name]
    if any(not p for p in pos): print('skip',name); continue
    emb=[]
    def rec(i,last,cur):
        if i==len(name): emb.append(tuple(cur)); return
        for j in pos[i]:
            if j>last: rec(i+1,j,cur+[j])
    rec(0,-1,[])
    print(name,'embeddings',len(emb),flush=True)
    for keep in emb:
        ks=set(keep)
        # V1 dense
        ps=[p if i in ks else lower_at(p,f[i][0]) for i,p in enumerate(paras)]
        h=hashlib.md5(join.join(ps).encode()).hexdigest()
        for ix in IDX:
            a=derive(h,ix); tot[0]+=1
            if a in (LIVE,OLD): tot[1]+=1; print('*** HIT V1',name,keep,ix,h,a,flush=True)
        # V2 sparse: only initials equal to a name letter, outside the embedding
        sel={i for i,c in enumerate(init) if c in set(name)} - ks
        if sel:
            ps=[lower_at(p,f[i][0]) if i in sel else p for i,p in enumerate(paras)]
            h=hashlib.md5(join.join(ps).encode()).hexdigest()
            for ix in IDX:
                a=derive(h,ix); tot[0]+=1
                if a in (LIVE,OLD): tot[1]+=1; print('*** HIT V2',name,keep,sorted(sel),ix,h,a,flush=True)
    print(f'-- {name} cands={tot[0]} hits={tot[1]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL',tot,'%.0fs'%(time.time()-t0))
