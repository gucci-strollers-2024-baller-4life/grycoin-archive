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
def build(units, join, base, mode='both'):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        if (pi+1) in units:
            idxs = alpha_idx(p)
            if idxs:
                fi, li = idxs[0], idxs[-1]
                if mode in ('both','first') and newp[fi].isupper(): newp[fi] = newp[fi].lower()
                if mode in ('both','last') and newp[li].islower(): newp[li] = newp[li].upper()
        out.append(''.join(newp))
    return join.join(out).encode()
rules = {
    "C1+I": [4,5,6,7,8], "C1": [5,6,7,8],
    "C2+I": [92,93,94,95,96], "C3+I": [167,168,169,170,171],
    "all3+I": [4,5,6,7,8,92,93,94,95,96,167,168,169,170,171],
    "all3": [5,6,7,8,93,94,95,96,168,169,170,171],
    "quote": [231,232,233,235], "quote+I": [231,232,233,234,235],
    "all3+quote": [5,6,7,8,93,94,95,96,168,169,170,171,231,232,233,235],
}
t0 = time.time(); n = 0
for rname, units in rules.items():
    for mode in ('both','last'):
        for bname, b in [('exact',texts),('stripped',stripped)]:
            for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
                data = build(units, j, b, mode)
                d = hashlib.md5(data).hexdigest()
                for idx in range(100):
                    n += 1
                    words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                    if addr == esc:
                        print(f"!!!!!! MATCH: {rname} mode={mode} {bname} join={j!r} idx={idx}")
                        print("addr:", addr); print("words:", words)
                        open('RBB_SOLUTION.txt','wb').write(data)
                        sys.exit(0)
print(f"wide-index battery: {n} derives ({time.time()-t0:.0f}s), no match")
