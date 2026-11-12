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
eight = [218,219,220,221,223,224,225,226]
for name, units, mode, level in [
    ("eight around 222", eight, 'both', 'para'),
    ("eight+222", eight+[222], 'both', 'para'),
    ("four before", [218,219,220,221], 'both', 'para'),
    ("four after", [223,224,225,226], 'both', 'para'),
    ("eight last", eight, 'last', 'para'),
    ("eight first", eight, 'first', 'para'),
    ("eight s1", eight, 'both', 's1'),
    ("eight+222 last", eight+[222], 'last', 'para'),
    ("eight s1 last", eight, 'last', 's1'),
]:
    run(name, units, mode, level)
found = False
for r in range(1, 9):
    for combo in itertools.combinations(eight, r):
        if run(f"subset {combo}", list(combo)): found=True; break
    if found: break
print("hint-para-neighborhood battery complete")
