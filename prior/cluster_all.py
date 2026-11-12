import json, hashlib, sys, time
sys.path.insert(0,'.')
from demo_oracle import derive

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
wp = json.load(open('wp_paras.json'))
texts = [t for _, t in wp]
stripped = [t.rstrip() for t in texts]
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD  = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def s1_end(p):
    idx = len(p)
    for i,c in enumerate(p):
        if c in '.!?' and (i+1>=len(p) or p[i+1] in ' \n'):
            idx = i; break
    return p[:idx+1]
# ALL CLUSTER SETS identified across the investigation
C1   = [5,6,7,8]
C1I  = [4,5,6,7,8]
C2   = [93,94,95,96]
C2I  = [92,93,94,95,96]
C3   = [168,169,170,171]
C3I  = [167,168,169,170,171]
Q    = [231,232,233,235]
QI   = [231,232,233,234,235]
ALL  = C1+C2+C3
ALLI = C1I+C2I+C3I
ALLQ = ALL+Q
ALLQI= ALLI+QI
A1   = C1+C2; A1I = C1I+C2I
A2   = C1+C3; A2I = C1I+C3I
A3   = C2+C3; A3I = C2I+C3I
A4   = C1+Q;  A5 = C2+Q; A6 = C3+Q
A7   = C1+C2+Q; A8 = C1+C3+Q; A9 = C2+C3+Q
# four-around-222 sets
B1 = list(range(218,222)); B2 = list(range(223,227)); B222=[222]; B44 = list(range(218,227))
sets = {"C1":C1,"C1I":C1I,"C2":C2,"C2I":C2I,"C3":C3,"C3I":C3I,"Q":Q,"QI":QI,
        "ALL":ALL,"ALLI":ALLI,"ALLQ":ALLQ,"ALLQI":ALLQI,
        "A1":A1,"A1I":A1I,"A2":A2,"A2I":A2I,"A3":A3,"A3I":A3I,
        "A4":A4,"A5":A5,"A6":A6,"A7":A7,"A8":A8,"A9":A9,
        "B1":B1,"B2":B2,"B222":B222,"B44":B44}
def flip(units, mode, gran, base):
    out = []
    for pi, p in enumerate(base):
        np = list(p)
        if (pi+1) in units and np:
            seg = s1_end(p) if gran=='s1' else p
            idxs = alpha_idx(seg)
            if not idxs: out.append(''.join(np)); continue
            fi = alpha_idx(p)[0]
            li = idxs[-1]
            if mode in ('both','first') and np[fi].isupper(): np[fi] = np[fi].lower()
            if mode in ('both','last')  and np[li].islower(): np[li] = np[li].upper()
        out.append(''.join(np))
    return out
t0=time.time(); n=0; total=0
for sname, units in sets.items():
    for bname, b in (('exact',texts),('stripped',stripped)):
        for mode in ('both','last','first'):
            for gran in ('para','s1'):
                for join in ('\n\n','\r\n\r\n','\n','\r\n'):
                    data = join.join(flip(units, mode, gran, b)).encode()
                    h = hashlib.md5(data).hexdigest()
                    for idx in range(100):
                        total+=1
                        words, addr = derive(bytes.fromhex(h), f"m/44'/0'/0'/0/{idx}")
                        if addr in (LIVE, OLD):
                            print(f"!!!!!! MATCH: set={sname} mode={mode} gran={gran} join={join!r} base={bname} idx={idx} md5={h}")
                            print("words:", words)
                            open('RBB_SOLUTION.txt','wb').write(data)
                            sys.exit(0)
                n+=1
        if n % 6 == 0: print(f"{sname}... {total} derives ({time.time()-t0:.0f}s)", flush=True)
print(f"CLUSTER MEGA-BATTERY COMPLETE: {total} derives in {(time.time()-t0)/60:.0f} min, no match")
