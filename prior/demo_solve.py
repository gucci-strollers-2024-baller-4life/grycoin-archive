import hashlib, sys, itertools
sys.path.insert(0,'.')
from demo_oracle import derive
q = open('demo_base.txt','rb').read().decode()
paras = q.split('\n\n')
def alpha_idx(s): return [i for i,c in enumerate(s) if c.isalpha()]
def s1_end(p):
    idx = len(p)
    for i,c in enumerate(p):
        if c in '.!?' and (i+1>=len(p) or p[i+1] in ' \n'):
            idx = i; break
    return p[:idx+1]
def build(units, joinstr, mode, level):
    out = []
    for pi, p in enumerate(paras):
        np = list(p)
        if (pi+1) in units:
            seg = s1_end(p) if level=='s1' else p
            idxs = alpha_idx(seg)
            fi, li = idxs[0], idxs[-1]
            if mode in ('both','first') and np[fi].isupper(): np[fi] = np[fi].lower()
            if mode in ('both','last') and np[li].islower(): np[li] = np[li].upper()
        out.append(''.join(np))
    return joinstr.join(out).encode()
hits = []
allsets = []
for r in range(1, 11):
    for c in itertools.combinations(range(1,11), r):
        allsets.append(set(c))
print(f"{len(allsets)} subsets")
for units in allsets:
    for level in ('s1','para'):
        for mode in ('both','last','first'):
            for join in ('\n\n','\r\n\r\n','\n','\r\n'):
                h = hashlib.md5(build(units, join, mode, level)).hexdigest()
                if h.startswith('3c6'):
                    hits.append((sorted(units), join, mode, level, h))
print(f"{len(hits)} hits with 3c6 prefix")
for units, join, mode, level, h in hits:
    for idx in range(100):
        words, addr = derive(bytes.fromhex(h), f"m/44'/0'/0'/0/{idx}")
        if addr == "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi":
            print("!!!!!! ESCROW MATCH !!!!!!")
            print("units:", units, "join:", repr(join), "mode:", mode, "level:", level)
            print("md5:", h)
            print("words:", words)
            data = build(set(units), join, mode, level)
            open('SOLUTION_demo.txt','wb').write(data)
            print("SAVED SOLUTION_demo.txt")
            sys.exit(0)
print("no escrow match among hits")
