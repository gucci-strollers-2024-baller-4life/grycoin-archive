import json, hashlib, sys, itertools
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
def build(units, join, base, mode='both', level='para'):
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
blocks = {
    'C1': [5,6,7,8], 'C2': [93,94,95,96], 'C3': [168,169,170,171], 'Q': [231,232,233,235],
}
Iheads = {'C1': 4, 'C2': 92, 'C3': 167, 'Q': 234}
combos = []
for r in range(1, 5):
    for bsel in itertools.combinations('C1 C2 C3 Q'.split(), r):
        for i_in in range(2):
            combos.append((bsel, i_in))
print(f"{len(combos)} block combos")
for bsel, i_in in combos:
    for mode in ('both','first','last'):
        for level in ('para','s1'):
            units = []
            for b in bsel:
                units += blocks[b]
                if i_in: units.append(Iheads[b])
            for bname, b in [('exact',texts),('stripped',stripped)]:
                for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
                    data = build(units, j, b, mode, level)
                    d = hashlib.md5(data).hexdigest()
                    for idx in range(2):
                        words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                        if addr == esc:
                            print(f"!!! MATCH blocks={bsel} I={i_in} mode={mode} level={level} {bname} join={j!r} idx={idx}")
                            print("words:", words)
                            open('RBB_SOLUTION.txt','wb').write(data)
                            sys.exit(0)
print("mirror-combinatorics battery complete, no match")
