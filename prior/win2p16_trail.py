"""2^16 window-subset closure on the trailing-newline substrate (45,451 chars).
Every previous 2^16 closure ran only on the 45,450-char base; Wattpad stores 45,451."""
import json, hashlib, sys
sys.path.insert(0, 'sweeps')
from polarity_flip import addr0
T = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
P = [("\n".join(p) if isinstance(p, list) else p) for p in json.load(open('wp_paras_br.json'))]
WIN = [5,6,7,8,93,94,95,96,168,169,170,171,231,232,233,235]
def flip(p):
    al=[i for i,c in enumerate(p) if c.isalpha()]
    if not al: return p
    p=p[:al[0]]+p[al[0]].lower()+p[al[0]+1:]
    return p[:al[-1]]+p[al[-1]].upper()+p[al[-1]+1:]
wins=[P[i-1] for i in WIN]
hits=0
for m in range(1<<16):
    Q=list(P)
    for k,i in enumerate(WIN):
        if m>>k&1: Q[i-1]=flip(wins[k])
    t="\n\n".join(Q)+"\n"
    h=hashlib.md5(t.encode()).hexdigest()
    if addr0(h)==T:
        print("*** MATCH mask",m,bin(m),h,flush=True); hits+=1
print("done, hits:",hits,flush=True)
