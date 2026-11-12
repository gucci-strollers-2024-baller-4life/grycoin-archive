"""'The first four and last four words of the paragraph hinting at the solution' (chapter ¶242),
applied to the chapter itself: 4+4 = the eight-item shape of the certified sibling answer."""
import json, hashlib, sys
sys.path.insert(0, 'sweeps')
from polarity_flip import addr0

C = [("\n".join(p) if isinstance(p, list) else p) for p in json.load(open('wp_paras_br.json'))]
TARGET = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'


def f4(p): return p.split()[:4]
def l4(p): return p.split()[-4:]


def variants(p):
    a, b = f4(p), l4(p)
    out = set()
    for x, y in ((a, b), (b, a), (a, a), (b, b)):
        s = ' '.join(x + y)
        out.add(s)
        out.add(s.strip('"'))
        out.add(s.lower())
    return out


CANDS = {}
short = [i for i, p in enumerate(C, 1) if len(p.split()) <= 5]
for i in short:
    CANDS[f'¶{i}'] = C[i - 1]
for i in (5, 6, 7, 8, 93, 94, 95, 96, 168, 169, 170, 171, 231, 232, 233, 235):
    CANDS[f'¶{i}'] = C[i - 1]
CANDS['¶4 first + ¶273 last'] = ' '.join(f4(C[3]) + l4(C[-1]))
CANDS['¶273 first + ¶4 last'] = ' '.join(f4(C[-1]) + l4(C[3]))
CANDS['¶20 + ¶273'] = ' '.join(f4(C[19]) + l4(C[-1]))

print("target", TARGET)
seen = set(); n = 0; hits = []
for tag, p in CANDS.items():
    for s in variants(p):
        if s in seen:
            continue
        seen.add(s); n += 1
        h = hashlib.md5(s.encode()).hexdigest()
        if addr0(h) == TARGET:
            hits.append((tag, s)); print("  *** MATCH", tag, repr(s))
print(f"tested {n} distinct first-four/last-four strings across {len(CANDS)} paragraphs: hits={hits or 'none'}")
