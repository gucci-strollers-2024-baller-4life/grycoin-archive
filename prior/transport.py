#!/usr/bin/env python3
"""Transport model: paired head-down / tail-up moves with mass balance.

A 'transport' is a down-move at a unit head plus an up-move at a unit tail. Enumerating all
balanced sets (|downs| == |ups|) is a *subset* of the flip space the sweeper already covers,
not a different machine: the sweeper flips both directions freely, so a transport is just two
flips whose directions are constrained. The value here is the constraint, which makes the
8-edit shape of the certified stage-one answer reachable at all.

Stage one, for the record, is exactly four transports: F->f at four paragraph heads and
s,t,n,m -> S,T,N,M at the matching four paragraph tails. Eight character edits, four units.
"""
import hashlib, re, itertools, sys, time
sys.path.insert(0,'harness'); import btc

txt = open('demo_base.txt', encoding='utf-8', newline='').read()
P = [p.strip() for p in re.split(r'\r?\n\r?\n', txt.strip()) if p.strip()]
ESC = {'1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi': 'demo escrow',
       '1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC': 'demo address'}

def spans(B, join):
    out, pos = [], 0
    for p in P:
        out.append((pos, pos+len(p))); pos += len(p)+len(join)
    return out
def fa(B,a,b): return next((i for i in range(a,b) if B[i].isalpha()), None)
def la(B,a,b): return next((i for i in range(b-1,a-1,-1) if B[i].isalpha()), None)
def first_sent(B,a,b):
    m = re.search(r'[.!?]+["\u201d]?(?=\s|$)', B[a:b])
    return (a, a+m.end()) if m else (a,b)

total = 0; surv = []
t0 = time.time()
for join, jn in (('\r\n\r\n','CRLF'), ('\n\n','LF')):
    for trail in (False, True):
        B = join.join(P) + (join if trail else '')
        bs = B.encode(); sp = spans(B, join)
        heads = [fa(B,a,b) for a,b in sp]
        for tailname, tails in (('para-final', [la(B,a,b) for a,b in sp]),
                                ('sent1-final', [la(B,*first_sent(B,a,b)) for a,b in sp])):
            for k in range(1, 11):
                for D in itertools.combinations(heads, k):
                    if any(not chr(bs[i]).isupper() for i in D):   # a down-move needs a capital
                        continue
                    for U in itertools.combinations(tails, k):
                        if any(not chr(bs[i]).islower() for i in U):  # an up-move needs a lower
                            continue
                        o = bytearray(bs)
                        for i in D: o[i] += 32
                        for i in U: o[i] -= 32
                        total += 1
                        h = hashlib.md5(bytes(o)).hexdigest()
                        if h.startswith('3c6'):
                            surv.append((jn, '+t' if trail else '', tailname, k, D, U, h, bytes(o)))
print(f'{total} balanced transport configurations in {time.time()-t0:.1f}s')
print(f'3c6 survivors: {len(surv)}')
for s in surv:
    print('  ', s[0], s[1], s[2], 'k=%d'%s[3], 'down', s[4], 'up', s[5], s[6])
# derive
from fastaddr import address
hits = 0
for s in surv:
    a = address(s[6])
    if a in ESC:
        hits += 1; print('*** ESCROW ***', s[6], '->', a, ESC[a])
print('escrow hits:', hits)
