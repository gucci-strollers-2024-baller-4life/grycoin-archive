import json, re, sys, hashlib
sys.path.insert(0,'.')
from demo_oracle import derive
wp = json.load(open('wp_paras.json'))
texts = [t for _, t in wp]
stripped = [t.rstrip() for t in texts]
# full mid-word capital scan: any capital at index >= 1
print("=== ALL words with capital at index>=1 (manual inspect) ===")
sig_paras = set()
for pi, p in enumerate(texts):
    for m in re.finditer(r"[A-Za-z0-9']+", p):
        w = m.group(0)
        if len(w) < 2: continue
        caps = [i for i in range(1, len(w)) if w[i].isupper()]
        if caps and not w[1:].isupper():  # exclude ALLCAPS like MD5, ASCII, CPU
            ctx = p[max(0,m.start()-30):m.end()+30].replace('\n',' ')
            print(f"para {pi+1}: [{w}]  ...{ctx}...")
            sig_paras.add(pi+1)
print("\nsign paras:", sorted(sig_paras))
ESC = {'14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W': ('\n\n','\r\n\r\n'),
       '1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC': ('\n','\r\n')}
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def build(units, mode, level, join, base):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        if (pi+1) in units:
            segs = [p]
            if level == 's1':
                idx = len(p)
                for i, c in enumerate(p):
                    if c in '.!?' and (i+1 >= len(p) or p[i+1] in ' \n'):
                        idx = i; break
                segs = [p[:idx+1]]
            for seg in segs:
                idxs = alpha_idx(seg)
                if not idxs: continue
                fi, li = idxs[0], idxs[-1]
                if mode in ('both','first') and newp[fi].isupper(): newp[fi] = newp[fi].lower()
                if mode in ('both','last') and newp[li].islower(): newp[li] = newp[li].upper()
        out.append(''.join(newp))
    return join.join(out).encode()
def run(name, units, mode='both', level='para'):
    for bname, b in [('exact',texts),('stripped',stripped)]:
        for j in ('\n\n','\r\n\r\n','\n','\r\n'):
            data = build(units, mode, level, j, b)
            d = hashlib.md5(data).hexdigest()
            words, addr = derive(bytes.fromhex(d))
            for esc, js in ESC.items():
                if j in js and addr == esc:
                    print(f"!!! MATCH: {name} {bname} join={j!r} mode={mode} level={level}")
                    print("addr:", addr); print("words:", words)
                    open('RBB_SOLUTION.txt','wb').write(data)
                    return True
    return False
sp = sorted(sig_paras)
import itertools

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
for name, units, mode, level in [
    ("sign paras all", sp, 'both','para'),
    ("sign paras last", sp, 'last','para'),
    ("sign paras first", sp, 'first','para'),
    ("sign paras s1", sp, 'both','s1'),
    ("sign paras 73/126/128/136", [73,126,128,136], 'both','para'),
    ("VIrgin+BItcoin", [128,136], 'both','para'),
    ("VIrgin+BItcoin+ppM", [73,128,136], 'both','para'),
    ("VIrgin+BItcoin last", [128,136], 'last','para'),
]:
    run(name, units, mode, level)
# subsets of sign paras
found=False
for r in range(1, len(sp)+1):
    for combo in itertools.combinations(sp, r):
        if run(f"subset {combo}", list(combo)): found=True; break
    if found: break
print("rescan battery complete")
