import sys, re, time
sys.path.insert(0,'.')
from demo_oracle import derive
ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
import hashlib
seen = set()
hits = []
for fn in ['bnd_0.txt','bnd_1.txt','bnd_2.txt','bnd_3.txt','bnd_4.txt','bnd_5.txt','bnd_6.txt','bnd_7.txt']:
    try:
        for line in open(fn):
            m = re.match(r"MATCH mask=(\d+) flips=([\d,]*) md5=([0-9a-f]{32})", line)
            if not m: continue
            mask = int(m.group(1)); md5 = m.group(3)
            if md5 in seen: continue
            seen.add(md5)
            pc = bin(mask).count('1')
            hits.append((pc, mask, md5))
    except FileNotFoundError: pass
print(f"{len(seen)} unique hit md5s from boundary sweep so far")
hits.sort()
t0 = time.time()
print("deriving in popcount order...")
for n, (pc, mask, md5) in enumerate(hits):
    words, addr = derive(bytes.fromhex(md5))
    if addr == ESCROW:
        print(f"!!!! DEMO SOLUTION FOUND: mask={mask} popcount={pc} md5={md5}")
        print("words:", words)
        print("flips:", end=' ')
        # re-find flip positions
        print(open('demo_bounds.txt').read())
        break
    if n % 20000 == 0 and n:
        el = time.time()-t0
        print(f"  {n}/{len(hits)} derived ({el:.0f}s, {n/el:.0f}/s), eta {(len(hits)-n)/(n/el+1e-9)/60:.1f} min", flush=True)
else:
    print("no escrow match yet in current hits")
