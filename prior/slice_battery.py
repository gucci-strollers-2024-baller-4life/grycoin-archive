import json, hashlib, sys
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
def build(units, join, base, off, mode='both', level='para'):
    out = []
    for pi, p in enumerate(base):
        P = pi+1+off  # original numbering
        newp = list(p)
        if P in units:
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
rules = {
    "clusters+I": [4,5,6,7,8,92,93,94,95,96,167,168,169,170,171],
    "clusters": [5,6,7,8,93,94,95,96,168,169,170,171],
    "clusters+quote": [5,6,7,8,93,94,95,96,168,169,170,171,231,232,233,235],
    "quote": [231,232,233,235],
    "eight-222": [218,219,220,221,223,224,225,226],
    "signs+254": [20,42,220,222,223,225,226,230,236,244,246,273,254],
}
slices = [("full",0), ("no1",1), ("no12",2), ("no123",3)]
def run():
    for rname, units in rules.items():
        for sname, off in slices:
            for bname, b in [('exact',texts),('stripped',stripped)]:
                bb = b[off:]
                for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
                    for mode in ('both','last'):
                        data = build(units, j, bb, off, mode)
                        d = hashlib.md5(data).hexdigest()
                        for idx in range(2):
                            words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                            if addr == esc:
                                print(f"!!! MATCH {rname} {sname} {bname} join={j!r} mode={mode} idx={idx}")
                                print("words:", words)
                                open('RBB_SOLUTION.txt','wb').write(data)
                                return True
    return False
if not run():
    print("slice battery complete, no match")
