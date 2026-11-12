import json, hashlib, sys
sys.path.insert(0,'.')
from demo_oracle import derive
wp = json.load(open('wp_paras.json'))
texts = [t for _, t in wp]
stripped = [t.rstrip() for t in texts]
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD  = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def s1_end(p):
    idx = len(p)
    for i, c in enumerate(p):
        if c in '.!?' and (i+1 >= len(p) or p[i+1] in ' \n'):
            idx = i; break
    return p[:idx+1]
def build(units, join, base, gran):
    # gran: bitmask, bit i = unit i at s1 level (else para level); first-down + last-up both
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        if (pi+1) in units:
            gi = units.index(pi+1)
            seg = s1_end(p) if (gran >> gi & 1) else p
            idxs = alpha_idx(seg)
            if idxs:
                fi, li = idxs[0], idxs[-1]
                if newp[fi].isupper(): newp[fi] = newp[fi].lower()
                if newp[li].islower(): newp[li] = newp[li].upper()
        out.append(''.join(newp))
    return join.join(out).encode()
def sweep(units, label):
    n = len(units)
    for bname, b in [('exact',texts),('stripped',stripped)]:
        for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
            for gran in range(1 << n):
                data = build(units, j, b, gran)
                d = hashlib.md5(data).hexdigest()
                for idx in range(2):
                    words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                    if addr == esc:
                        print(f"!!! MATCH {label} gran={gran:0{n}b} {bname} join={j!r} idx={idx}")
                        print("words:", words)
                        open('RBB_SOLUTION.txt','wb').write(data)
                        return True
    return False
C1 = [4,5,6,7,8]; C2 = [92,93,94,95,96]; C3 = [167,168,169,170,171]
C1x = [5,6,7,8]; C2x = [93,94,95,96]; C3x = [168,169,170,171]
import itertools, time

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
t0 = time.time()
# 12-unit FFWW clusters, granularity mix
if not sweep(C1x+C2x+C3x, "FFWW12"):
    print(f"FFWW12 done ({time.time()-t0:.0f}s)")
    t0 = time.time()
    # 15-unit with I paras
    if not sweep(C1+C2+C3, "I+FFWW15"):
        print(f"I+FFWW15 done ({time.time()-t0:.0f}s)")
print("mixed-granularity sweep complete")
