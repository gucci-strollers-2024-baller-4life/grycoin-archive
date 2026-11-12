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
def build(units, mode, level, join, base):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        if (pi+1) in units:
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
def run(name, units, mode='both', level='para'):
    for bname, b in [('exact',texts),('stripped',stripped)]:
        for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
            data = build(units, mode, level, j, b)
            d = hashlib.md5(data).hexdigest()
            for idx in range(10):
                words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                if addr == esc:
                    print(f"!!! MATCH: {name} {bname} join={j!r} mode={mode} level={level} idx={idx}")
                    print("addr:", addr); print("words:", words)
                    open('RBB_SOLUTION.txt','wb').write(data)
                    return True
    return False
C1 = [4,5,6,7,8]; C2 = [92,93,94,95,96]; C3 = [167,168,169,170,171]
C1x = [5,6,7,8]; C2x = [93,94,95,96]; C3x = [168,169,170,171]
Q = [231,232,233,235]; QI = [234]
I_paras = [4,92,167]
sets = [
    ("clusters+I", C1+C2+C3), ("clusters no I", C1x+C2x+C3x),
    ("clusters+I s1", C1+C2+C3), ("+quote", C1x+C2x+C3x+Q),
    ("+quote+I", C1+C2+C3+Q), ("+quote+I+QI", C1+C2+C3+Q+QI),
    ("quote only", Q), ("quote+QI", Q+QI),
    ("I-paras only", I_paras), ("I+quote", I_paras+Q),
]
n = 0
for name, units in sets:
    level = 's1' if 's1' in name else 'para'
    for mode in ('both','first','last'):
        n += 1
        if run(name, units, mode, level): break
print(f"multi-index battery complete ({n*3*4*2*10} derives)")
