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
firsts = [next((c for c in t if c.isalpha()), '') for t in texts]
lasts = [next((c for c in reversed(t) if c.isalpha()), '') for t in texts]
ITASM = set('ITASM')
nonit = set(i+1 for i,f in enumerate(firsts) if f and f.upper() not in ITASM)
stnm = set(i+1 for i,l in enumerate(lasts) if l.lower() in 'stnm')
inter = sorted(nonit & stnm)
print(f"non-ITASM: {len(nonit)}, stnm-ending: {len(stnm)}, INTERSECTION: {len(inter)}")
print("intersection paras:", inter)
print("their ups-message:", ''.join(lasts[p-1] for p in inter).upper())
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD  = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def s1_end(p):
    idx = len(p)
    for i,c in enumerate(p):
        if c in '.!?' and (i+1>=len(p) or p[i+1] in ' \n'):
            idx = i; break
    return p[:idx+1]
def flip(units, mode, gran, base):
    out = []
    for pi, p in enumerate(base):
        np = list(p)
        if (pi+1) in units:
            seg = p if gran=='para' else s1_end(p)
            idxs = alpha_idx(seg)
            if not idxs: continue
            fi, li = idxs[0], idxs[-1]
            if mode in ('both','first') and np[fi].isupper(): np[fi] = np[fi].lower()
            if mode in ('both','last') and np[li].islower(): np[li] = np[li].upper()
        out.append(''.join(np))
    return out
t = 0
for mode in ('both','last','first'):
    for gran in ('para','s1'):
        for bname, b in (('exact',texts),('stripped',stripped)):
            for join,esc in (('\n\n',LIVE),('\r\n\r\n',LIVE),('\n',OLD),('\r\n',OLD)):
                outp = flip(inter, mode, gran, b)
                data = join.join(outp).encode()
                h = hashlib.md5(data).hexdigest()
                for idx in range(30):
                    w_, addr = derive(bytes.fromhex(h), f"m/44'/0'/0'/0/{idx}")
                    t += 1
                    if addr == esc:
                        print(f"!!!!!! MATCH: mode={mode} gran={gran} base={bname} join={join!r} idx={idx}")
                        print("words:", w_)
                        open('RBB_SOLUTION.txt','w').write(f"mode={mode} gran={gran} join={join!r} idx={idx} md5={h}\nwords={w_}\n")
                        open('RBB_solution_text.txt','wb').write(data)
                        sys.exit(0)
print(f"intersection battery: {t} derives, no match")
