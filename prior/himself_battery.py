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
firsts = [next((c for c in t if c.isalpha()), '') for t in texts]
lasts = [next((c for c in reversed(t) if c.isalpha()), '') for t in texts]
ESC = {'14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W': ('\n\n','\r\n\r\n'),
       '1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC': ('\n','\r\n')}
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def build(units, mode, join, base):
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
        for j in ('\n\n','\r\n\r\n','\n','\r\n'):
            data = build(units, mode, j, b)
            d = hashlib.md5(data).hexdigest()
            words, addr = derive(bytes.fromhex(d))
            for esc, js in ESC.items():
                if j in js and addr == esc:
                    print(f"!!! MATCH: {name} {bname} join={j!r} mode={mode}")
                    print("addr:", addr); print("words:", words)
                    open('RBB_SOLUTION.txt','wb').write(data)
                    return True
    return False
# core flips
run("254 himselF only", [254], 'last')
run("254 both", [254], 'both')
# with every I-starting para's first down
I_paras = [i+1 for i,f in enumerate(firsts) if f == 'I']
print(f"{len(I_paras)} I-first paras: {I_paras}")
for ip in I_paras:
    run(f"254-last + {ip}-first", [254, ip], 'both')
# signs-para neighborhoods with 254
signs = [20,42,220,222,223,225,226,230,236,244,246,273]
for sp in signs:
    run(f"254 + signsp {sp}", [254, sp], 'both')
    run(f"254-last + signsp-both {sp}", [254, sp], 'last')
# 254 + all subsets of 2 extra sign paras
for combo in itertools.combinations(signs, 2):
    run(f"254+{combo}", [254]+list(combo), 'both')
# 254 + VIrgin/BItcoin/ppM paras
for combo in itertools.chain.from_iterable(itertools.combinations([73,128,136], r) for r in range(0,4)):
    run(f"254+anomaly {combo}", [254]+list(combo), 'both')
    run(f"254+anomaly-last {combo}", [254]+list(combo), 'last')
# 244 (i recognize the signS) + 254
run("244+254", [244,254], 'both')
run("239 I STNM + 254", [239,254], 'both')
run("239+244+254", [239,244,254], 'both')
print("himself battery complete")
