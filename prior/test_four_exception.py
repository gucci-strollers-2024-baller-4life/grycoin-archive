"""Litmus test: 'all paragraphs except four' read as a literal flip rule.

Corpora: corrected (wp_paras_br.json, internal <br> breaks kept) and legacy
(chapter_paras_exact.json). Each joined CRLFCRLF and LFLF.
Sets: all-but-four / four-only / all-273.
Modes: certified stage-one direction (first down, last up), and its inverse.
"""
import json, hashlib, sys, time
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

brs   = json.load(open('wp_paras_br.json'))      # list of segment lists
exact = json.load(open('chapter_paras_exact.json'))  # list of paragraph strings
assert len(brs) == len(exact) == 273

def para_from_br(segs, ibr):
    return ibr.join(segs)

def flip(p, ops):
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

bases = {
 'corr_crlf': ('br', '\r\n\r\n', '\r\n'),
 'corr_lf':   ('br', '\n\n', '\n'),
 'leg_crlf':  ('exact', '\r\n\r\n', '\r\n'),
 'leg_lf':    ('exact', '\n\n', '\n'),
}

ex4 = [221, 230, 242, 243]           # 1-indexed 222, 231, 243, 244
sets = {
 'all_but_four': [i for i in range(273) if i not in ex4],
 'four_only':    ex4,
 'all_273':      list(range(273)),
}
modes = {'fd_lu': ('fd', 'lu'), 'fu_ld': ('fu', 'ld')}
idxs = [0, 1, 2, 3, 4, 5, 6, 7, 44, 76, 77]

cands = 0
hits = []
t0 = time.time()
for bname, (corpus, join, ibr) in bases.items():
    paras = [para_from_br(s, ibr) for s in brs] if corpus == 'br' else list(exact)
    plain = join.join(paras)
    ph = hashlib.md5(plain.encode()).hexdigest()
    print(f'{bname:9s} plain md5 {ph}')
    for sname, sel in sets.items():
        for mname, ops in modes.items():
            ps = list(paras)
            for i in sel:
                ps[i] = flip(ps[i], ops)
            text = join.join(ps)
            h = hashlib.md5(text.encode()).hexdigest()
            for i in idxs:
                a = btc.addr_from_md5hex(h, (44 + H, 0 + H, 0 + H, 0, i))
                cands += 1
                if a in (LIVE, OLD):
                    hits.append((bname, sname, mname, i, h, a))
                    print('*** HIT', bname, sname, mname, i, h, a, flush=True)
            print(f'  {sname:13s} {mname} md5={h}')
print(f'derivations={cands} hits={len(hits)} elapsed={time.time()-t0:.1f}s')
