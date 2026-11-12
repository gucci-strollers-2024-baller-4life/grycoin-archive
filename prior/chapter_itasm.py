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
firsts = [next((c for c in t if c.isalpha()), '') for t in texts]
ITASM = set('ITASM')
# non-ITASM paras
units_full = [i+1 for i,f in enumerate(firsts) if f.upper() not in ITASM and f]
units_stripped = [i+1 for i,f in enumerate(firsts) if f.upper() not in ITASM and f]
print(f"{len(units_full)} non-ITASM paras of {len(texts)}")
print("first letters of flipped paras:", ''.join(firsts[u-1] for u in units_full))
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def s1_end(p):
    idx = len(p)
    for i,c in enumerate(p):
        if c in '.!?' and (i+1>=len(p) or p[i+1] in ' \n'):
            idx = i; break
    return p[:idx+1]
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD  = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
def build(units, base, join, level='para', mode='both'):
    out = []
    for pi, p in enumerate(base):
        np = list(p)
        if (pi+1) in units:
            seg = s1_end(p) if level=='s1' else p
            idxs = alpha_idx(seg)
            if not idxs: 
                out.append(''.join(np)); continue
            fi, li = idxs[0], idxs[-1]
            if mode in ('both','first') and np[fi].isupper(): np[fi] = np[fi].lower()
            if mode in ('both','last') and np[li].islower(): np[li] = np[li].upper()
        out.append(''.join(np))
    return join.join(out).encode()
t0 = time.time(); n = 0
combos = []
for units_name, units in [("full", units_full)]:
    for bname, base in [("exact", texts), ("stripped", stripped)]:
        for join in ('\n\n','\r\n\r\n','\n','\r\n'):
            for level in ('para','s1'):
                for mode in ('both','last','first'):
                    data = build(units, base, join, level, mode)
                    h = hashlib.md5(data).hexdigest()
                    for idx in range(30):
                        n += 1
                        words, addr = derive(bytes.fromhex(h), f"m/44'/0'/0'/0/{idx}")
                        for esc, nm in [(LIVE,'LIVE'),(OLD,'OLD')]:
                            if addr == esc:
                                print(f"!!!!!! {nm} MATCH !!!!!! join={join!r} level={level} mode={mode} idx={idx}")
                                print("words:", words)
                                open('RBB_SOLUTION.txt','wb').write(data)
                                sys.exit(0)
print(f"chapter ITASM battery: {n} derives in {time.time()-t0:.0f}s, no match")
