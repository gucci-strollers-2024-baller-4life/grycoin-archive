import hashlib, sys
sys.path.insert(0,'.')
from demo_oracle import derive
q = open('demo_base.txt','rb').read().decode()
chars = list(q)
# stated pair positions in the FLAT string (recompute para offsets)
paras = q.split('\n\n')
off = 0
p5 = paras[4]
base5 = sum(len(x)+2 for x in paras[:4])
i5 = base5 + next(i for i,c in enumerate(p5) if c.isalpha())
him5 = base5 + p5.find('himself') + len('himself') - 1
print("flat positions: I5:", i5, "(=", q[i5], ") him5:", him5, "(=", q[him5], ")")
assert q[i5] == 'I' and q[him5] == 'f'
# all alpha positions that COULD flip (case-flippable letters)
flip_pos = [i for i,c in enumerate(chars) if c.isalpha()]
print(f"{len(flip_pos)} flippable alpha positions")
def md5_of(active):
    c2 = chars[:]
    for pos in active:
        c2[pos] = c2[pos].lower() if c2[pos].isupper() else c2[pos].upper()
    return hashlib.md5(''.join(c2).encode()).hexdigest()
# k=0: stated pair alone
base_pair = {i5, him5}
h = md5_of(base_pair)
print("pair alone:", h[:7])
# k=1
found = []
for p in flip_pos:
    if p in base_pair: continue
    h = md5_of(base_pair | {p})
    if h.startswith('3c6'):
        print("3c6 k=1 pos:", p, q[p], h)
        found.append((base_pair | {p}, h))
# k=2
import itertools
n = len(flip_pos)
cnt = 0
for a in range(n):
    pa = flip_pos[a]
    if pa in base_pair: continue
    for b in range(a+1, n):
        pb = flip_pos[b]
        if pb in base_pair: continue
        h = md5_of(base_pair | {pa, pb})
        if h.startswith('3c6'):
            print("3c6 k=2:", pa, pb, q[pa], q[pb], h)
            found.append((base_pair | {pa,pb}, h))
print(f"{len(found)} hits; deriving...")
for active, h in found:
    for idx in range(200):
        words, addr = derive(bytes.fromhex(h), f"m/44'/0'/0'/0/{idx}")
        if addr == "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi":
            print("!!!!!! ESCROW MATCH !!!!!! flips at:", sorted(active), "idx:", idx)
            print("words:", words)
            c2 = chars[:]
            for pos in active:
                c2[pos] = c2[pos].lower() if c2[pos].isupper() else c2[pos].upper()
            open('SOLUTION_demo.txt','w').write(''.join(c2))
            open('RBB_SOLUTION.txt','wb').write(''.join(c2).encode())
            sys.exit(0)
print("no escrow in pair+k<=2")
