import json,re,itertools,sys
from rbb_probe import check, addr_at, md5b, LIVE, OLD
# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

paras=json.load(open("chapter_paras_exact.json",encoding="utf-8"))
N=len(paras)

def first_down(p):
    for i,ch in enumerate(p):
        if ch.isalpha(): return p[:i]+ch.lower()+p[i+1:]
    return p
def last_up(p):
    for i in range(len(p)-1,-1,-1):
        if p[i].isalpha(): return p[:i]+p[i].upper()+p[i+1:]
    return p
def both(p): return last_up(first_down(p))
def swap_edges(p):
    q=p
    for i,ch in enumerate(q):
        if ch.isalpha(): q=q[:i]+ch.lower()+q[i+1:]; break
    for i in range(len(q)-1,-1,-1):
        if q[i].isalpha(): q=q[:i]+q[i].upper()+q[i+1:]; break
    return q
MODES={"first_down":first_down,"last_up":last_up,"both":both,
       "first_up":lambda p: p, "none":lambda p:p}

def build(sel, mode, join):
    f=MODES[mode]
    return join.join(f(p) if i+1 in sel else p for i,p in enumerate(paras))

# ---- anomaly paragraph sets (word has lowercase AND an uppercase at index>=1) ----
odd={}
for i,p in enumerate(paras,1):
    for m in re.finditer(r"[A-Za-z][A-Za-z']*",p):
        w=m.group(0)
        if any(c.isupper() for c in w[1:]) and any(c.islower() for c in w):
            odd.setdefault(i,[]).append(w)
print("anomaly paragraphs:",{k:v for k,v in odd.items()})
five=[i for i,v in odd.items() if any(w in("ppM","VIrgin","BItcoin","BITcoin","AHScoin") for w in v)]
print("five-mark set:",sorted(five))

SETS={
 "marks5":set(five),
 "marks_all12":set(odd),
 "marks5_no209":set(five)-{209},
 "i_only":{i for i,v in odd.items() if any(w in("VIrgin","BItcoin") for w in v)},
 "ffww_5_8":set(range(5,9)),
 "ffww_93_96":set(range(93,97)),
 "ffww_168_171":set(range(168,172)),
 "quote_231_235":{231,232,233,235},
 "signs_words":{20,42,220,222,223,225,226,227,228,230,236,244,246,273},
}
# recognised-sign rules on the whole chapter
ITASM=set("ITASM")
def _fa(p):
    import re as _r
    m=_r.search(r"[A-Za-z]",p); return m.group(0) if m else ""
not_itasm={i for i,p in enumerate(paras,1) if _fa(p) not in ITASM}
itasm={i for i,p in enumerate(paras,1) if _fa(p) in ITASM}
lower_start={i for i,p in enumerate(paras,1) if p[:1].islower()}
SETS["not_ITASM"]=not_itasm; SETS["ITASM"]=itasm; SETS["lower_start"]=lower_start
print({k:len(v) for k,v in SETS.items()})

JOINS={"crlfcrlf":"\r\n\r\n","lf2":"\n\n","crlf":"\r\n","lf":"\n"}
IDX=[0,1,2,3,4,5,6,7,44,76,77]
n=0;hits=[]
for sname,sel in SETS.items():
    if not sel: continue
    for mname in MODES:
        if mname=="none" and sname not in("marks5",): continue
        for jname,j in JOINS.items():
            t=build(sel,mname,j); n+=1
            if check(t,IDX,f"{sname}/{mname}/{jname}",hits):
                print("HIT",sname,mname,jname)
print(f"derivations: {n} candidates x {len(IDX)} indices = {n*len(IDX)}")
print("hits:",hits)
