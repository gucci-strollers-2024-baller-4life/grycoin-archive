#!/usr/bin/env python3
"""Background sweep: all subsets of chapter 'signs-paragraphs' x modes x bases x joins."""
import json, hashlib, sys, itertools
sys.path.insert(0, '.')
from demo_oracle import derive

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
wp = json.load(open('wp_paras.json'))
texts = [t for _, t in wp]
stripped = [t.rstrip() for t in texts]
ESC = {'14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W': ('\n\n', '\r\n\r\n'),
       '1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC': ('\n', '\r\n')}
signs_paras = [20, 42, 220, 222, 223, 225, 226, 230, 236, 244, 246, 273]
def alpha_idx(s): return [i for i, c in enumerate(s) if c.isalpha()]
def build(units, mode, join, base):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        if (pi + 1) in units:
            idxs = alpha_idx(p)
            if idxs:
                fi, li = idxs[0], idxs[-1]
                if mode in ('both', 'first') and newp[fi].isupper(): newp[fi] = newp[fi].lower()
                if mode in ('both', 'last') and newp[li].islower(): newp[li] = newp[li].upper()
        out.append(''.join(newp))
    return join.join(out).encode()
log = open('subset_sweep_hits.txt', 'a')
total = 0
for r in range(1, 13):
    for units in itertools.combinations(signs_paras, r):
        uset = set(units)
        for mode in ('last', 'both', 'first'):
            for bname, b in [('exact', texts), ('stripped', stripped)]:
                for j in ('\n\n', '\r\n\r\n', '\n', '\r\n'):
                    data = build(uset, mode, j, b)
                    d = hashlib.md5(data).hexdigest()
                    total += 1
                    words, addr = derive(bytes.fromhex(d))
                    esc = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W' if j in ESC['14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'] else '1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
                    if addr == esc:
                        msg = f"!!! MATCH units={units} mode={mode} base={bname} join={j!r} addr={addr} md5={d}"
                        print(msg); log.write(msg + '\n'); log.flush()
                        open('RBB_SOLUTION.txt', 'wb').write(data)
    print(f"done r={r} ({total} derived)", flush=True)
print(f"COMPLETE: {total} derivations, no more", flush=True)
