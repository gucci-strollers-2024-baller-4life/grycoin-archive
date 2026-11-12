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
lasts = [next((c for c in reversed(t) if c.isalpha()), '') for t in texts]
firsts = [next((c for c in t if c.isalpha()), '') for t in texts]
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD  = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def build_last(join, base, sel):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        if sel(pi+1):
            idxs = alpha_idx(p)
            if idxs and newp[idxs[-1]].islower():
                newp[idxs[-1]] = newp[idxs[-1]].upper()
        out.append(''.join(newp))
    return join.join(out).encode()
def build_first_down(join, base, sel):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        if sel(pi+1):
            idxs = alpha_idx(p)
            if idxs and newp[idxs[0]].isupper():
                newp[idxs[0]] = newp[idxs[0]].lower()
        out.append(''.join(newp))
    return join.join(out).encode()
def run(name, sel):
    for bname, b in [('exact',texts),('stripped',stripped)]:
        for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
            data = build_last(j, b, sel)
            d = hashlib.md5(data).hexdigest()
            for idx in range(3):
                words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                if addr == esc:
                    print(f"!!! MATCH last-up: {name} {bname} join={j!r} idx={idx}")
                    print("words:", words)
                    open('RBB_SOLUTION.txt','wb').write(data)
                    return True
            data2 = build_first_down(j, b, sel)
            d2 = hashlib.md5(data2).hexdigest()
            for idx in range(3):
                words, addr = derive(bytes.fromhex(d2), f"m/44'/0'/0'/0/{idx}")
                if addr == esc:
                    print(f"!!! MATCH first-down: {name} {bname} join={j!r} idx={idx}")
                    print("words:", words)
                    open('RBB_SOLUTION.txt','wb').write(data2)
                    return True
    return False
tests = [
    ("ends s,t,n,m (STNM)", lambda p: lasts[p-1].lower() in 'stnm'),
    ("ends s only", lambda p: lasts[p-1].lower() == 's'),
    ("ends t only", lambda p: lasts[p-1].lower() == 't'),
    ("ends n only", lambda p: lasts[p-1].lower() == 'n'),
    ("ends m only", lambda p: lasts[p-1].lower() == 'm'),
    ("ends s,t", lambda p: lasts[p-1].lower() in 'st'),
    ("ends s,n", lambda p: lasts[p-1].lower() in 'sn'),
    ("ends s,m", lambda p: lasts[p-1].lower() in 'sm'),
    ("ends t,n", lambda p: lasts[p-1].lower() in 'tn'),
    ("ends t,m", lambda p: lasts[p-1].lower() in 'tm'),
    ("ends n,m", lambda p: lasts[p-1].lower() in 'nm'),
    ("ends i,t,a,s,m (ITASM)", lambda p: lasts[p-1].lower() in 'itasm'),
    ("ends i only", lambda p: lasts[p-1].lower() == 'i'),
    ("ITASM-first + STNM-last (both full)", None),
]
for name, sel in tests:
    if sel: run(name, sel)
# combined: flip firsts of non-ITASM down AND lasts of stnm up
def build_both(join, base):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        idxs = alpha_idx(p)
        if idxs:
            if firsts[pi] not in 'ITASM' and newp[idxs[0]].isupper():
                newp[idxs[0]] = newp[idxs[0]].lower()
            if lasts[pi].lower() in 'stnm' and newp[idxs[-1]].islower():
                newp[idxs[-1]] = newp[idxs[-1]].upper()
        out.append(''.join(newp))
    return join.join(out).encode()
for bname, b in [('exact',texts),('stripped',stripped)]:
    for j, esc in [('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)]:
        data = build_both(j, b)
        d = hashlib.md5(data).hexdigest()
        for idx in range(3):
            words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
            if addr == esc:
                print(f"!!! MATCH combined rule {bname} {j!r} idx={idx}"); print("words:", words)
                open('RBB_SOLUTION.txt','wb').write(data); break
print("lasts battery complete")
