import json, hashlib, sys, time
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
firsts = [next((c for c in t if c.isalpha()), '') for t in texts]
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD  = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
WIF = open('stage1_wif.txt').read().strip()
SAT = set('SATOSHI'); ITASM = set('ITASM')
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def flip_paras(units, join, base, mode='both'):
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
nonsat = [i+1 for i,f in enumerate(firsts) if f.upper() not in SAT]
nonit = [i+1 for i,f in enumerate(firsts) if f.upper() not in ITASM]
rule_sets = {
    "none": [],
    "nonsat": nonsat, "nonit": nonit,
    "C1": [5,6,7,8], "C1I": [4,5,6,7,8],
    "C2I": [92,93,94,95,96], "C3I": [167,168,169,170,171],
    "all3": [5,6,7,8,93,94,95,96,168,169,170,171],
    "all3I": [4,5,6,7,8,92,93,94,95,96,167,168,169,170,171],
    "quote": [231,232,233,235], "quoteI": [231,232,233,234,235],
    "all3q": [5,6,7,8,93,94,95,96,168,169,170,171,231,232,233,235],
}
# link/TOMI joiners
def variants(chap, wif):
    yield chap + b" " + wif.encode()
    yield chap + b" TOMI Omit TOMI " + wif.encode()
    yield chap + b" TOMI " + wif.encode()
    yield chap + b"TOMI" + wif.encode()
    yield chap + b"\n" + wif.encode()
    yield chap + b"\n\n" + wif.encode()
    yield wif.encode() + b" " + chap
    yield wif.encode() + chap
    yield chap + b" TOMI Omit TOMI"
    yield chap
t0=time.time(); n=0
for rname, units in rule_sets.items():
    for mode in (['none'] if not units else ['both','last','first']):
        for bname, b in [('exact',texts),('stripped',stripped)]:
            for join in ('\n\n','\r\n\r\n','\n','\r\n'):
                core = flip_paras(units, join, b, mode if mode!='none' else 'both')
                for vi, data in enumerate(variants(core, WIF)):
                    d = hashlib.md5(data).hexdigest()
                    for idx in range(10):
                        n += 1
                        words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                        for esc, nm in [(LIVE,'LIVE'),(OLD,'OLD')]:
                            if addr == esc:
                                print(f"!!!!!! {nm} MATCH: rule={rname} mode={mode} base={bname} join={join!r} variant={vi} idx={idx}")
                                print("words:", words)
                                open('RBB_SOLUTION.txt','wb').write(data)
                                sys.exit(0)
print(f"tomi battery: {n} derives ({time.time()-t0:.0f}s), no match")
