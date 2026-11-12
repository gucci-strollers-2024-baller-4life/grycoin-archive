"""k=1 solo sweep: lowercase each paragraph's first character and uppercase its last alphabetic
character, one paragraph at a time, over all 273, derived at index 0."""
import json, hashlib, sys
sys.path.insert(0, 'sweeps')
from polarity_flip import addr0

TARGET = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
P = [("\n".join(p) if isinstance(p, list) else p) for p in json.load(open('wp_paras_br.json'))]


def flip(t):
    t = t[0].lower() + t[1:]
    i = max(k for k, c in enumerate(t) if c.isalpha())
    return t[:i] + t[i].upper() + t[i + 1:]


hits = []
for i in range(273):
    Q = list(P)
    Q[i] = flip(Q[i])
    s = "\n\n".join(Q)
    h = hashlib.md5(s.encode()).hexdigest()
    a = addr0(h)
    if a == TARGET:
        hits.append((i + 1, h))
print(f"solo k=1 endpoint inversion, 273 candidates at index 0: {len(hits)} hits")
for i, h in hits:
    print(f"  *** MATCH ¶{i} md5 {h}")
