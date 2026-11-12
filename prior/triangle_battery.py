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
def run(name, units, mode='both'):
    for bname, b in [('exact',texts),('stripped',stripped)]:
        for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
            data = build(units, j, b, mode)
            d = hashlib.md5(data).hexdigest()
            for idx in range(2):
                words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                if addr == esc:
                    print(f"!!! MATCH {name} mode={mode} {bname} join={j!r} idx={idx}")
                    print("words:", words)
                    open('RBB_SOLUTION.txt','wb').write(data)
                    return True
    return False
# cluster rows: position 1..4 in each cluster
rows = {1:[5,93,168], 2:[6,94,169], 3:[7,95,170], 4:[8,96,171]}
rowsI = {0:[4,92,167], 1:[5,93,168], 2:[6,94,169], 3:[7,95,170], 4:[8,96,171]}
Qrows = {1:[231,232,233,235]}  # quote as 4th "cluster" column-wise: 231,232,233,235
# class combos (which positions flipped)
for r in range(1,5):
    for pos_combo in itertools.combinations([1,2,3,4], r):
        units = [p for pos in pos_combo for p in rows[pos]]
        run(f"rows {pos_combo}", units)
        run(f"rows {pos_combo} last", units, 'last')
        run(f"rows {pos_combo} first", units, 'first')
# with quote column added
for r in range(1,5):
    for pos_combo in itertools.combinations([1,2,3,4], r):
        units = [p for pos in pos_combo for p in rows[pos]] + [231,232,233,235][ [1,2,3,4].index(pos_combo[0]) ] if False else [p for pos in pos_combo for p in rows[pos]]
# one-from-each-cluster combos (64) + the I-paras optionally
found = False
for combo in itertools.product([5,6,7,8],[93,94,95,96],[168,169,170,171]):
    if run(f"triangle {combo}", list(combo)): found=True; break
if not found:
    for combo in itertools.product([5,6,7,8],[93,94,95,96],[168,169,170,171]):
        if run(f"triangle-last {combo}", list(combo), 'last'): found=True; break
if not found:
    for combo in itertools.product([4,5,6,7,8],[92,93,94,95,96],[167,168,169,170,171]):
        if run(f"triangle+I {combo}", list(combo)): found=True; break
# quote-in-triangle: one para from each cluster + one from quote
if not found:
    for c3 in itertools.product([5,6,7,8],[93,94,95,96],[168,169,170,171],[231,232,233,235]):
        if run(f"quad {c3}", list(c3)): found=True; break
print("triangle battery complete")
