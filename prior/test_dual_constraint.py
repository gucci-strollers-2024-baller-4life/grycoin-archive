"""Dual-constraint test: Vector A (the four non-voice exceptions + opener class)
crossed with Vector B (the delta-44 anchor at paragraphs 34 and 78).

Stage 1: anchor treatment for p34/p78 enumerated (none / first-down-last-up /
        first-up-last-down / whole-paragraph case swap), over every other paragraph
        in the selected set flipped in the certified direction.
Stage 2: direction splits at the anchor boundaries (34, 44, 78, 136).
"""
import json, hashlib, sys, time, itertools
sys.path.insert(0, 'harness')
import btc

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

H = 0x80000000
LIVE = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
OLD  = '1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
IDX = [0, 1, 2, 3, 4, 5, 6, 7, 44, 76, 77]
EX4 = {221, 230, 242, 243}
ANCH = (33, 77)

def edge(p, ops):
    L = list(p)
    if 'fd' in ops:
        for j, c in enumerate(L):
            if c.isalpha():
                if c.isupper(): L[j] = c.lower()
                break
    if 'fu' in ops:
        for j, c in enumerate(L):
            if c.isalpha():
                if c.islower(): L[j] = c.upper()
                break
    if 'lu' in ops:
        for j in range(len(L) - 1, -1, -1):
            if L[j].isalpha():
                if L[j].islower(): L[j] = L[j].upper()
                break
    if 'ld' in ops:
        for j in range(len(L) - 1, -1, -1):
            if L[j].isalpha():
                if L[j].isupper(): L[j] = L[j].lower()
                break
    return ''.join(L)

br    = json.load(open('wp_paras_br.json'))
exact = json.load(open('chapter_paras_exact.json'))
bases = {
 'br_crlf': '\r\n\r\n'.join('\r\n'.join(s) if isinstance(s, list) else s for s in br),
 'br_lf':   '\n\n'.join('\n'.join(s) if isinstance(s, list) else s for s in br),
 'ex_crlf': '\r\n\r\n'.join(exact),
 'ex_lf':   '\n\n'.join(exact),
}
first = [next((c for c in p if c.isalpha()), '') for p in exact]
ITASM = set('ITASM')
kept = [i for i in range(273) if i not in EX4]
sets = {
 'all_but_four':            kept,
 'all_but_four_outside_ITASM': [i for i in kept if first[i].upper() not in ITASM],
 'all_but_four_inside_ITASM':  [i for i in kept if first[i].upper() in ITASM],
}
MODES = {'fd_lu': ('fd', 'lu'), 'fu_ld': ('fu', 'ld')}
ANCHOR_OPS = {'none': None, 'fwd': ('fd', 'lu'), 'inv': ('fu', 'ld'), 'swap': 'swap'}

def apply_anchor(p, op):
    if op is None:   return p
    if op == 'swap': return p.swapcase()
    return edge(p, op)

cands = hits = 0
t0 = time.time()

# ---------- stage 1
for bname, text in bases.items():
    paras = text.split('\r\n\r\n') if '\r\n' in text else text.split('\n\n')
    assert len(paras) == 273, (bname, len(paras))
    for sname, sel in sets.items():
        body = [i for i in sel if i not in ANCH]
        for mname, ops in MODES.items():
            for combo in itertools.product(ANCHOR_OPS, repeat=2):
                ps = list(paras)
                for i in body:
                    ps[i] = edge(ps[i], ops)
                ps[ANCH[0]] = apply_anchor(ps[ANCH[0]], ANCHOR_OPS[combo[0]])
                ps[ANCH[1]] = apply_anchor(ps[ANCH[1]], ANCHOR_OPS[combo[1]])
                h = hashlib.md5('\r\n\r\n'.join(ps).encode() if '\r\n' in text else '\n\n'.join(ps).encode()).hexdigest()
                for i in IDX:
                    a = btc.addr_from_md5hex(h, (44 + H, 0 + H, 0 + H, 0, i)); cands += 1
                    if a in (LIVE, OLD):
                        hits += 1; print('*** HIT S1', bname, sname, mname, combo, i, h, a, flush=True)
print(f'stage1 derivations={cands} hits={hits} {time.time()-t0:.0f}s', flush=True)

# ---------- stage 2: direction splits at the anchor boundaries
c2 = h2 = 0
for bname, text in bases.items():
    paras = text.split('\r\n\r\n') if '\r\n' in text else text.split('\n\n')
    sep = '\r\n\r\n' if '\r\n' in text else '\n\n'
    for sname, sel in sets.items():
        for split in (34, 44, 78, 136):
            for flip_first in (('fd', 'lu'), ('fu', 'ld')):
                ps = list(paras)
                other = ('fu', 'ld') if flip_first == ('fd', 'lu') else ('fd', 'lu')
                for i in sel:
                    ps[i] = edge(ps[i], flip_first if i < split else other)
                h = hashlib.md5(sep.join(ps).encode()).hexdigest()
                for i in IDX:
                    a = btc.addr_from_md5hex(h, (44 + H, 0 + H, 0 + H, 0, i)); c2 += 1
                    if a in (LIVE, OLD):
                        h2 += 1; print('*** HIT S2', bname, sname, split, flip_first, i, h, a, flush=True)
print(f'stage2 derivations={c2} hits={h2} {time.time()-t0:.0f}s total', flush=True)
print(f'TOTAL preimage-derived addresses={cands + c2} hits={hits + h2} elapsed={time.time()-t0:.1f}s')
