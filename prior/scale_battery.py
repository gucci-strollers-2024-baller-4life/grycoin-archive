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
firsts = [next((c for c in t if c.isalpha()), '') for t in texts]
ESC = {'14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W': ('\n\n','\r\n\r\n'),
       '1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC': ('\n','\r\n')}
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
        for j in ('\n\n','\r\n\r\n','\n','\r\n'):
            data = build(units, mode, level, j, b)
            d = hashlib.md5(data).hexdigest()
            words, addr = derive(bytes.fromhex(d))
            for esc, js in ESC.items():
                if j in js and addr == esc:
                    print(f"!!! MATCH: {name} {bname} join={j!r} mode={mode} level={level}")
                    print("addr:", addr); print("words:", words)
                    open('RBB_SOLUTION.txt','wb').write(data)
                    return True
    return False
ITASM = set('ITASM')
nonit = [i+1 for i,f in enumerate(firsts) if f and f not in ITASM]
it = [i+1 for i,f in enumerate(firsts) if f in ITASM]
print(f"non-ITASM: {len(nonit)} paras, ITASM: {len(it)} paras")
for units, label in [(nonit, 'ALL-non-ITASM'), (it, 'ALL-ITASM')]:
    for mode in ('both','first','last'):
        for level in ('para','s1'):
            run(f"{label} {mode} {level}", units, mode, level)
# the lasts of non-ITASM paras, read as a string (message check)
lasts = ''.join(next((c for c in reversed(texts[p-1]) if c.isalpha()), '') for p in nonit).upper()
print("non-ITASM lasts string:", lasts[:120])
print("scale battery complete")
