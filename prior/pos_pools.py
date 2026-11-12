#!/usr/bin/env python3
"""Eligible-byte pools for the demo, derived from the only six certified up-marks.

The six case marks that are certified anywhere in this corpus, with their part of speech:

    block 29   vOIce      NOUN     marks at letters 2-3 of 5, word-interior
    demo  ¶5   himselF    PRONOUN  mark at letter 7 of 7, word-final before the full stop
    stage one  activitieS NOUN     word-final before the full stop
    stage one  iT         PRONOUN  word-final before the full stop
    stage one  reactioN   NOUN     word-final before the full stop
    stage one  theM       PRONOUN  word-final before the full stop

Invariants that hold in 6 of 6:
  * never the word's FIRST letter (all six are non-initial)
  * never a verb, adjective, adverb, article, preposition or conjunction
  * never inside a proper name (Satoshi, Bitcointalk are never touched)
Position within the word is NOT invariant: 2 of 6 are word-interior, 4 of 6 are word-final.
So 'word-internal only' is falsified by himselF itself; 'non-initial' survives.
"""
import re, json

txt = open('demo_base.txt', encoding='utf-8', newline='').read()
P = [p.strip() for p in re.split(r'\r?\n\r?\n', txt.strip()) if p.strip()]
BASE = '\n\n'.join(P)

# hand classification of the demo's 140 distinct words.  N=noun P=pronoun V=verb A=adjective
# D=adverb F=function word.  Ambiguous tokens are put in the permissive class and flagged.
CLS = {}
for w in """bit format block example reference people couple letters capitalization letter
end paragraph part solution signs post method result detail hand beginning rest problems
stages stage light script mind thinking text worth n N capitalizatioN himselF""".split():
    CLS[w.lower()] = 'N'
for w in "i you it that which their them this anyone someone himself one all what i".split():
    CLS[w.lower()] = 'P'
for w in """thought would write giving is are supposed keep change was be expected do
recognize explained used changing think take sees should may mining solve finding end take
write""".split():
    CLS[w.lower()] = 'V'
for w in "simple clear whole long obvious able many other previous easy enough remaining correct both last first faster possible".split():
    CLS[w.lower()] = 'A'
for w in "already actually not only well up now least completely too".split():
    CLS[w.lower()] = 'D'
for w in """a an about the for to and of in at from if as once where while until when on
after with by but because so""".split():
    CLS[w.lower()] = 'F'
for w in ("satoshi's", "bitcointalk"):
    CLS[w] = 'PROPER'
CLS['it\'s'] = 'F'
for w in ("I", "i"): CLS[w.lower()] = 'P'

words = [(m.start(), m.group()) for m in re.finditer(r"[A-Za-z']+", BASE)]
def cls(w):
    return CLS.get(w.lower(), '?')

# sentence spans
sent = []
s = 0
for m in re.finditer(r'[.!?]+["\u201d]?(?=\s|$)', BASE):
    sent.append((s, m.end())); s = m.end()
if s < len(BASE): sent.append((s, len(BASE)))
def in_sent(i):
    for k, (a, b) in enumerate(sent, 1):
        if a <= i < b: return k
    return None

ALL, UP_NONINIT, UP_NP, UP_NP_SENTFINAL, DOWN_INIT = [], [], [], [], []
for st, w in words:
    c = cls(w)
    for j, ch in enumerate(w):
        if not ch.isalpha(): continue
        i = st + j
        ALL.append((i, w, c, j == 0))
        if j > 0:
            if ch.islower(): UP_NONINIT.append((i, w, c))
            if ch.islower() and c in ('N', 'P'): UP_NP.append((i, w, c))
            if ch.islower() and c == 'N' and j == len(w) - 1: UP_NP_SENTFINAL.append((i, w, c))
        else:
            if ch.isupper(): DOWN_INIT.append((i, w, c))

print(f'base {len(BASE)} bytes, {len(words)} words, {len(ALL)} letters, {len(sent)} sentences')
print(f'L0 every letter                                   {len(ALL):5d}')
print(f'L1 up-mark pool: non-initial, lowercase           {len(UP_NONINIT):5d}')
print(f'L2 up-mark pool: non-initial in NOUN/PRONOUN      {len(UP_NP):5d}')
print(f'L3 up-mark pool: word-final of a NOUN only        {len(UP_NP_SENTFINAL):5d}')
print(f'D  down-mark pool: word-initial currently capital {len(DOWN_INIT):5d}')
print()
n = len(UP_NP) + len(DOWN_INIT)
import math
print(f'pool for a five-edit answer, anchored on the two named edits (removed): ')
fixed = [i for i, w, c, f in ALL if (w == 'himself' and i == 656 - 0) ]
print()
print('space sizes for the remaining free edits, after the two named edits are fixed:')
for label, pool in (('L0 all letters', [a for a,_,_,_ in ALL]),
                    ('L1 non-initial only', [p[0] for p in UP_NONINIT] + [d[0] for d in DOWN_INIT]),
                    ('L2 noun/pronoun non-initial + initials', [p[0] for p in UP_NP] + [d[0] for d in DOWN_INIT]),
                    ('L3 noun-final + initials', [p[0] for p in UP_NP_SENTFINAL] + [d[0] for d in DOWN_INIT])):
    m = len(pool) - 2
    print(f'  {label:40s} pool {len(pool):5d}  C(n,3)={math.comb(m,3):>15,}  C(n,4)={math.comb(m,4):>18,}')
print()
print('L3 pool detail (every position a certified-style mark could occupy):')
for i, w, c in UP_NP_SENTFINAL:
    print(f'   up   {i:5d}  {w:12s} {c}  sentence {in_sent(i)}')
for i, w, c in DOWN_INIT:
    print(f'   down {i:5d}  {w:12s} {c}  sentence {in_sent(i)}')
json.dump({'L1':[p[0] for p in UP_NONINIT],'L2':[p[0] for p in UP_NP],
           'L3':[p[0] for p in UP_NP_SENTFINAL],'D':[d[0] for d in DOWN_INIT]},
          open('pos_pools.json','w'))
