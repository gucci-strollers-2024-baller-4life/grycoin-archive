"""R1:29's precedent, unlocked: block 76's key is now known.

eyaler's 2026-10-31 correction on issue #49 supplies block 76's exact input
"EMERGENCY TOMI climate EMERGENCY"; its md5 f8e5edbc... matches the published f8e prefix and derives
13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd at index 0, so its WIF is certified. R1:29 - the closest precedent
for a multi-line chapter answer - is chapter draft + space + the last THREE characters of the previous
block's key. That was untestable until now.
"""
import json,hashlib,sys,itertools,time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
sys.path.insert(0,'/tmp'); import fast
H=fast.H
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
WIF=open('/tmp/b76_wif.txt').read().strip()
STAGE1='KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2'
B76ANS='EMERGENCY TOMI climate EMERGENCY'
B76MD5=hashlib.md5(B76ANS.encode()).hexdigest()
print('b76 wif',WIF,'tail',WIF[-7:])
def derive(h,idx,acct=44):
    if isinstance(h,str): h=h
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(acct+H,0+H,0+H,0,idx)))
IDX=(0,1,2,76)
br=json.load(open('wp_paras_br.json'))
lines=[[x] if not isinstance(x,list) else x for x in br]
paras_lf=['\n'.join(L) for L in lines]
paras_crlf=['\r\n'.join(L) for L in lines]
BASES={'br-lf':paras_lf,'br-crlf':paras_crlf}
JOIN={'br-lf':'\n\n','br-crlf':'\r\n\r\n'}
def flips(paras,join,sel,mode):
    out=[]
    for i,p in enumerate(paras):
        q=p
        if i in sel:
            if mode in ('fd','fdlu','fdS'):
                for j,ch in enumerate(q):
                    if ch.isalpha() and ch.isupper(): q=q[:j]+ch.lower()+q[j+1:]; break
                    if ch.isalpha(): break
            if mode in ('lu','fdlu'):
                for j in range(len(q)-1,-1,-1):
                    if q[j].isalpha():
                        if q[j].islower(): q=q[:j]+q[j].upper()+q[j+1:]
                        break
            if mode=='fdS':
                k=q.find('. ')
                seg=q if k<0 else q[:k+1]
                for j in range(len(seg)-1,-1,-1):
                    if seg[j].isalpha():
                        if seg[j].islower(): q=q[:j]+seg[j].upper()+q[j+1:]
                        break
        out.append(q)
    return join.join(out)
sets={
 'none':set(),
 'all':set(range(len(paras_lf))),
 'nonITASM':{i for i,p in enumerate(paras_lf) if next((c for c in p if c.isalpha()),'A').upper() not in 'ITASM'},
 'windows':set(range(4,8))|set(range(92,96))|set(range(167,171)),
 'reprint':{230,231,232,234},
 'signs':{i for i,p in enumerate(paras_lf) if 'sign' in p.lower()},
}
tails=[]
for k in (3,4,5,6,7):
    tails.append((f'wif{k}',WIF[-k:]))
tails.append(('ans','EMERGENCY TOMI climate EMERGENCY'))
tails.append(('md5',B76MD5))
tails.append(('stage1-3',STAGE1[-3:]))
tails.append(('none',''))
cands=0;hits=0
t0=time.time()
for bname,paras in BASES.items():
    join=JOIN[bname]
    for sname,sel in sets.items():
        for mode in ('fdlu','lu','fd','fdS'):
            text=flips(paras,join,sel,mode)
            for tname,tail in tails:
                for sep in (' ',''):
                    t=text+sep+tail if tail else text
                    h=hashlib.md5(t.encode()).hexdigest()
                    cands+=1
                    for idx in IDX:
                        a=derive(h,idx)
                        if a in (LIVE,OLD):
                            hits+=1; print('*** HIT',bname,sname,mode,tname,repr(sep),idx,h,a,flush=True)
print(f'cands={cands} hits={hits} {time.time()-t0:.0f}s')
