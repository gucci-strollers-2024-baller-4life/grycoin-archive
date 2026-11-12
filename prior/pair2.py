"""Complete two-letter space at paragraph boundaries: flip any two of the 546
paragraph-endpoint characters (head or last letter of each of the 273 paragraphs)."""
import json, hashlib, sys
sys.path.insert(0, 'sweeps')
from polarity_flip import addr0
T = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
P = [("\n".join(p) if isinstance(p, list) else p) for p in json.load(open('wp_paras_br.json'))]
def al(p): return [i for i, c in enumerate(p) if c.isalpha()]
def fl(p, which):
    a = al(p)
    if not a: return p
    if 'h' in which:
        p = p[:a[0]] + p[a[0]].swapcase() + p[a[0]+1:]
    if 't' in which:
        p = p[:a[-1]] + p[a[-1]].swapcase() + p[a[-1]+1:]
    return p
cache = {}
def get(i, which):
    k = (i, which)
    if k not in cache: cache[k] = fl(P[i], which)
    return cache[k]
toks = [(i, w) for i in range(273) if al(P[i]) for w in ('h', 't')]
print("endpoint tokens:", len(toks), flush=True)
n = 0
for a in range(len(toks)):
    ia, wa = toks[a]
    for b in range(a+1, len(toks)):
        ib, wb = toks[b]
        if ia == ib:
            Q = list(P); Q[ia] = get(ia, 'ht')
        else:
            Q = list(P); Q[ia] = get(ia, wa); Q[ib] = get(ib, wb)
        h = hashlib.md5("\n\n".join(Q).encode()).hexdigest()
        n += 1
        if addr0(h) == T:
            print("*** MATCH", toks[a], toks[b], h, flush=True)
    if a % 20 == 0:
        print("  a=", a, "tested", n, flush=True)
print("done", n, flush=True)
