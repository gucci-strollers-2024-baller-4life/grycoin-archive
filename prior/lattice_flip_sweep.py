import sys, hashlib, json
sys.path.insert(0,'.')
from demo_oracle import derive

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
T1="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; T2="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
P=json.load(open('chapter_paras_exact.json'))

def flip_para(s, mode):
    if not s: return s
    i0=next((i for i,c in enumerate(s) if c.isalpha()), None)
    i1=next((i for i in range(len(s)-1,-1,-1) if s[i].isalpha()), None)
    if i0 is None: return s
    b=list(s)
    if 'f' in mode:
        b[i0]=b[i0].lower()
    if 'l' in mode:
        b[i1]=b[i1].upper()
    return ''.join(b)

def test(txt, tag, hits):
    h=hashlib.md5(txt.encode()).hexdigest()
    for idx in (0,1,2):
        w,a=derive(bytes.fromhex(h),f"m/44'/0'/0'/0/{idx}")
        if a in (T1,T2):
            hits.append((tag, idx, 'T1' if a==T1 else 'T2', w, h))

hits=[]; n=0
# candidate position sets, 1-indexed
sets={
 'mod34_44':      [p for p in range(34,274,44)],
 'mod34_44_back': [p for p in range(34,0,-44)],
 'mod78_44':      [p for p in range(78,274,44)],
 'mirror34':      [34, 273+1-34],
 'stride44_full': [p for p in range(34,274,44)] + [p for p in range(240,0,-44)],
}
for tag,pos in sets.items():
    pos=[p for p in pos if 1<=p<=273]
    for mode in ('f','l','fl'):
        for join in ('\r\n\r\n','\r\n'):
            paras=list(P)
            for p in pos:
                paras[p-1]=flip_para(paras[p-1],mode)
            test(join.join(paras), f"{tag}|{mode}|{join!r}", hits); n+=1
# duplicate-pair only, both directions
for mode in ('f','l','fl'):
    for join in ('\r\n\r\n','\r\n'):
        paras=list(P)
        for p in (34,78): paras[p-1]=flip_para(paras[p-1],mode)
        test(join.join(paras), f"dup34_78|{mode}|{join!r}", hits); n+=1
print("tested",n,"hits",len(hits))
for h in hits: print("HIT",h)
print("mod34_44 set:", [p for p in range(34,274,44)])
