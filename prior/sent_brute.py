import hashlib, sys, itertools, re
sys.path.insert(0,'.')
from demo_oracle import derive
q = open('demo_base.txt','rb').read().decode()
paras = q.split('\n\n')
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
# collect sentences: (para_idx, span_start, span_end)
sents = []
for pi, p in enumerate(paras):
    start = 0
    for i, c in enumerate(p):
        if c in '.!?' and (i+1 >= len(p) or p[i+1] in ' \n'):
            sents.append((pi, start, i+1))
            start = i+2
    if start < len(p):
        sents.append((pi, start, len(p)))
print(f"{len(sents)} sentences")
ns = len(sents)
hits = []
for mask in range(1, 1<<ns):
    pfl = [list(p) for p in paras]
    for si in range(ns):
        if mask >> si & 1:
            pi, a, b = sents[si]
            seg = ''.join(pfl[pi])[a:b]
            idxs = alpha_idx(seg)
            if not idxs: continue
            fi, li = a+idxs[0], a+idxs[-1]
            if pfl[pi][fi].isupper(): pfl[pi][fi] = pfl[pi][fi].lower()
            if pfl[pi][li].islower(): pfl[pi][li] = pfl[pi][li].upper()
    data = '\n\n'.join(''.join(x) for x in pfl).encode()
    h = hashlib.md5(data).hexdigest()
    if h.startswith('3c6'):
        bits = [si for si in range(ns) if mask>>si&1]
        hits.append((bits, h))
        print("3c6!!! sentences:", bits, h)
print(f"{len(hits)} hits; deriving vs escrow...")
for bits, h in hits:
    for idx in range(100):
        words, addr = derive(bytes.fromhex(h), f"m/44'/0'/0'/0/{idx}")
        if addr == "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi":
            print("!!!!!! ESCROW MATCH !!!!!! sentences:", bits, "idx:", idx)
            print("words:", words)
            sys.exit(0)
print("no escrow among sentence-level hits")
