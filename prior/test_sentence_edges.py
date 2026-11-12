"""Sentence-edge flips, Gemini's Option (c): flip first/last letter of every SENTENCE,
with dialogue serving as the invariant exception set.

Variants: all sentences except those in quoted paragraphs; all sentences; quoted-paragraph
sentences only; all except sentences that themselves open with a quotation mark.
"""
import json, re, hashlib, sys, time
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

QUOTES = '"\u201c\u201d'

def spans(text):
    psp = []; start = 0
    for m in re.finditer(r'(?:\r\n\r\n|\n\n)', text):
        psp.append((start, m.start())); start = m.end()
    psp.append((start, len(text)))
    ssp = []
    for a, b in psp:
        s = 0
        for m in re.finditer(r'[.!?]+["\u201d]?[ \t]*(?:\r?\n|$| )', text[a:b]):
            e = m.end()
            while e > s and text[a + e - 1].isspace(): e -= 1
            if e > s: ssp.append((a + s, a + e, a, b))
            s = m.end()
        if s < b - a:
            e = b - a
            while e > s and text[a + e - 1].isspace(): e -= 1
            if e > s: ssp.append((a + s, a + e, a, b))
    return psp, ssp

def flip_span(t, a, b, ops):
    if 'fd' in ops:
        for j in range(a, b):
            if t[j].isalpha():
                if t[j].isupper(): t[j] = t[j].lower()
                break
    if 'fu' in ops:
        for j in range(a, b):
            if t[j].isalpha():
                if t[j].islower(): t[j] = t[j].upper()
                break
    if 'lu' in ops:
        for j in range(b - 1, a - 1, -1):
            if t[j].isalpha():
                if t[j].islower(): t[j] = t[j].upper()
                break
    if 'ld' in ops:
        for j in range(b - 1, a - 1, -1):
            if t[j].isalpha():
                if t[j].isupper(): t[j] = t[j].lower()
                break

br    = json.load(open('wp_paras_br.json'))
exact = json.load(open('chapter_paras_exact.json'))
bases = {
 'br_crlf':  '\r\n\r\n'.join('\r\n'.join(s) if isinstance(s, list) else s for s in br),
 'br_lf':    '\n\n'.join('\n'.join(s) if isinstance(s, list) else s for s in br),
 'ex_crlf':  '\r\n\r\n'.join(exact),
 'ex_lf':    '\n\n'.join(exact),
}
modes = {'fd_lu': ('fd', 'lu'), 'fu_ld': ('fu', 'ld')}
idxs = [0, 1, 2, 3, 4, 5, 6, 7, 44, 76, 77]

cands = hits = 0
t0 = time.time()
for bname, text in bases.items():
    psp, ssp = spans(text)
    para_quoted = [text[a:b].lstrip().startswith(tuple(QUOTES)) for a, b in psp]
    def pidx(pos):
        for k, (a, b) in enumerate(psp):
            if a <= pos < b: return k
        return len(psp) - 1
    variants = {
     'all_except_quoted_paras': [s for s in ssp if not para_quoted[pidx(s[0])]],
     'all_sentences': ssp,
     'quoted_paras_only': [s for s in ssp if para_quoted[pidx(s[0])]],
     'all_except_quote_opening_sentences': [s for s in ssp if not text[s[0]:s[1]].lstrip().startswith(tuple(QUOTES))],
    }
    for vname, sel in variants.items():
        for mname, ops in modes.items():
            t = list(text)
            for a, b, _, _ in sel: flip_span(t, a, b, ops)
            h = hashlib.md5(''.join(t).encode()).hexdigest()
            for i in idxs:
                a_ = btc.addr_from_md5hex(h, (44 + H, 0 + H, 0 + H, 0, i))
                cands += 1
                if a_ in (LIVE, OLD):
                    hits += 1; print('*** HIT', bname, vname, mname, i, h, a_, flush=True)
            print(f'{bname:8s} {vname:36s} {mname} sentences={len(sel):4d} md5={h}')
print(f'derivations={cands} hits={hits} elapsed={time.time()-t0:.1f}s')
