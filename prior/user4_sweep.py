import sys, hashlib, json, itertools, unicodedata
sys.path.insert(0,'.')
from demo_oracle import derive

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

T1 = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"   # live RBB escrow, 0.777 BTC (two line breaks)
T2 = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"   # original escrow, refunded (one line break)
P = json.load(open('chapter_paras_exact.json'))
print("paras:", len(P))

def first_letter(s):
    s = s.strip()
    return s[0] if s else ''
def last_letter(s):
    s = s.strip()
    for ch in reversed(s):
        if ch.isalpha(): return ch
    return s[-1] if s else ''
def last_char(s):
    s = s.rstrip()
    return s[-1] if s else ''

modes = {
 'raw':          lambda seg: seg,
 'first_letter': lambda seg: ''.join(first_letter(x) for x in seg),
 'last_letter':  lambda seg: ''.join(last_letter(x) for x in seg),
 'last_char':    lambda seg: ''.join(last_char(x) for x in seg),
 'first_word':   lambda seg: ' '.join(x.strip().split()[0] if x.strip() else '' for x in seg),
}
joins = {'2break':'\\r\\n\\r\\n', 'crlf':'\\r\\n', 'lf2':'\\n\\n', 'lf':'\\n', 'none':''}
ranges = [(1,77),(33,77),(34,78),(1,78),(2,78),(3,78),(4,78),(1,273),(1,44),(34,44)]

targets = {'T1_live_0.777':T1, 'T2_refunded':T2}
best = {}
hits = []
n = 0
for (a,b) in ranges:
    seg = P[a-1:b]
    for mn, mf in modes.items():
        body = mf(seg)
        if not body: continue
        for jn, j in joins.items():
            js = j.encode().decode('unicode_escape')
            txt = js.join(mf([x]) for x in seg) if mn != 'raw' else js.join(seg)
            for tail in ('', js):
                t = txt + tail
                h = hashlib.md5(t.encode('utf-8')).hexdigest()
                n += 1
                for idx in (0,1,2):
                    w, addr = derive(bytes.fromhex(h), f"m/44'/0'/0'/0/{idx}")
                    for tn, tv in targets.items():
                        if addr == tv:
                            hits.append((a,b,mn,jn,repr(tail),idx,tn,w,h))
print("texts tested:", n)
print("hits:", len(hits))
for x in hits: print("HIT", x)
