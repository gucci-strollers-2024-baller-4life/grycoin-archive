import json, hashlib, sys
sys.path.insert(0,'.')
from demo_oracle import derive
wp = json.load(open('wp_paras.json'))
texts = [t for _, t in wp]
stripped = [t.rstrip() for t in texts]
firsts = [next((c for c in t if c.isalpha()), '') for t in texts]
SAT = set('SATOSHI')
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD  = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def build(join, base, mode='both', level='para'):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        if firsts[pi].upper() not in SAT:
            segs = [p]
            if level == 's1':
                idx = len(p)
                for i, c in enumerate(p):
                    if c in '.!?' and (i+1 >= len(p) or p[i+1] in ' \n'):
                        idx = i; break
                segs = [p[:idx+1]]
            for seg in segs:
                idxs = alpha_idx(seg)
                if not idxs: continue
                fi, li = idxs[0], idxs[-1]
                if mode in ('both','first') and newp[fi].isupper(): newp[fi] = newp[fi].lower()
                if mode in ('both','last') and newp[li].islower(): newp[li] = newp[li].upper()
        out.append(''.join(newp))
    return join.join(out).encode()
import time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
t0 = time.time()
for bname, b in [('exact',texts),('stripped',stripped)]:
    for mode in ('both','last','first'):
        for level in ('para','s1'):
            for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
                data = build(j, b, mode, level)
                d = hashlib.md5(data).hexdigest()
                for idx in range(100):
                    words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                    if addr == esc:
                        print(f"!!!!!! MATCH: {bname} mode={mode} level={level} join={j!r} idx={idx}")
                        print("addr:", addr); print("words:", words)
                        open('RBB_SOLUTION.txt','wb').write(data)
                        print("SOLUTION FOUND")
                        sys.exit(0)
print(f"non-Satoshi rule battery complete ({time.time()-t0:.0f}s), no match at indices 0-99")
