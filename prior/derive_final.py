import sys, re, time, hashlib
sys.path.insert(0,'.')
from demo_oracle import derive
ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
part = int(sys.argv[1]); nparts = int(sys.argv[2])
seen = set(); hits = []
for i in range(8):
    for line in open(f'bnd_{i}.txt'):
        m = re.match(r"MATCH mask=(\d+) flips=([\d,]*) md5=([0-9a-f]{32})", line)
        if not m: continue
        md5 = m.group(3)
        if md5 in seen: continue
        seen.add(md5)
        hits.append((bin(int(m.group(1))).count('1'), int(m.group(1)), md5, m.group(2)))
hits.sort()
lo = len(hits)*part//nparts; hi = len(hits)*(part+1)//nparts
t0 = time.time()
for n, (pc, mask, md5, flips) in enumerate(hits[lo:hi]):
    for idx in range(3):
        words, addr = derive(bytes.fromhex(md5), f"m/44'/0'/0'/0/{idx}")
        if addr == ESCROW:
            print(f"!!!!!! DEMO SOLUTION: mask={mask} pc={pc} flips={flips} idx={idx} md5={md5}")
            print("words:", words)
            open(f'DEMO_FOUND_p{part}.txt','w').write(f"flips={flips} idx={idx} md5={md5}\nwords={words}\n")
            sys.exit(0)
    if n % 5000 == 0 and n:
        el = time.time()-t0
        print(f"p{part}: {n}/{hi-lo} ({el:.0f}s)", flush=True)
print(f"p{part}: done, no match")
