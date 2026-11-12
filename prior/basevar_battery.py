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
LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD  = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def build(units, join, base, remap=None):
    out = []
    for pi, p in enumerate(base):
        newp = list(p)
        P = pi+1 if remap is None else remap.get(pi+1)
        if P and P in units:
            idxs = alpha_idx(p)
            if idxs:
                if newp[idxs[0]].isupper(): newp[idxs[0]] = newp[idxs[0]].lower()
                if newp[idxs[-1]].islower(): newp[idxs[-1]] = newp[idxs[-1]].upper()
        out.append(''.join(newp))
    return join.join(out).encode()
C1 = [4,5,6,7,8]; C2 = [92,93,94,95,96]; C3 = [167,168,169,170,171]
C1x = [5,6,7,8]; C2x = [93,94,95,96]; C3x = [168,169,170,171]
Q = [231,232,233,235]
rules = {
    "clusters+I": C1+C2+C3, "clusters": C1x+C2x+C3x,
    "clusters+quote": C1x+C2x+C3x+Q, "clusters+I+quote": C1+C2+C3+Q,
    "quote": Q,
}
bases = {
    "full": texts, "full-stripped": stripped,
    "no-para1": texts[1:], "no-para1-stripped": stripped[1:],
    "no-para1-3": texts[3:], "no-para1-3-stripped": stripped[3:],
    "no-para1-2": texts[2:], "no-para1-2-stripped": stripped[2:],
}
for rname, units in rules.items():
    for bname, b in bases.items():
        # remap paragraph numbers for sliced bases
        off = len(texts) - len(b)
        remap = {i+1: i+1+off for i in range(len(b))} if off else None
        for j, esc, trail in [('\n\n',LIVE,''),(' \n\n',LIVE,''),('\n\n',LIVE,'\n\n'),('\r\n\r\n',LIVE,''),('\r\n\r\n',LIVE,'\r\n\r\n'),('\n',OLD,''),('\n',OLD,'\n'),('\r\n',OLD,'')]:
            data = build(units, j, b, remap) + trail.encode()
            d = hashlib.md5(data).hexdigest()
            for idx in range(2):
                words, addr = derive(bytes.fromhex(d), f"m/44'/0'/0'/0/{idx}")
                if addr == esc:
                    print(f"!!! MATCH {rname} base={bname} join={j!r} trail={trail!r} idx={idx}")
                    print("words:", words)
                    open('RBB_SOLUTION.txt','wb').write(data)
                    print("STOP")
                    sys.exit(0)
print("base-variant battery complete (no match)")
