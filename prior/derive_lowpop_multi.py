import sys, re, time
sys.path.insert(0,'.')
from demo_oracle import derive
ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
seen = set(); lowpop = []
for i in range(8):
    for line in open(f'bnd_{i}.txt'):
        m = re.match(r"MATCH mask=(\d+) flips=([\d,]*) md5=([0-9a-f]{32})", line)
        if not m: continue
        mask = int(m.group(1)); md5 = m.group(3)
        if md5 in seen: continue
        seen.add(md5)
        pc = bin(mask).count('1')
        if pc <= 12:
            lowpop.append((pc, mask, md5, m.group(2)))
print(f"{len(lowpop)} unique hits with popcount<=8", flush=True)
t0 = time.time()
for n,(pc,mask,md5,flips) in enumerate(lowpop):
    for idx in range(21):
        words, addr = derive(bytes.fromhex(md5), f"m/44'/0'/0'/0/{idx}")
        if addr == ESCROW:
            print(f"!!!!!! DEMO ESCROW MATCH: popcount={pc} flips={flips} idx={idx} md5={md5}")
            print("words:", words)
            open('DEMO_FOUND.txt','w').write(f"flips={flips} idx={idx} md5={md5}\nwords={words}\n")
            sys.exit(0)
    if n % 500 == 0 and n:
        el = time.time()-t0
        print(f"  {n}/{len(lowpop)} ({el:.0f}s, {n/el:.0f}/s), eta {(len(lowpop)-n)/(n/el)/60:.0f} min", flush=True)
print("no match at popcount<=8 x idx 0-20")
