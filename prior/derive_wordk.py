import sys, re, time
sys.path.insert(0,'.')
from demo_oracle import derive
ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
seen = set()
for line in open('wordk3_out.txt'):
    m = re.match(r"K(\d) flips=([\d,]+) md5=([0-9a-f]{32})", line)
    if not m: continue
    md5 = m.group(3)
    if md5 in seen: continue
    seen.add(md5)
print(f"{len(seen)} unique k<=3 word-boundary hits", flush=True)
t0 = time.time()
for n, md5 in enumerate(seen):
    for idx in range(21):
        words, addr = derive(bytes.fromhex(md5), f"m/44'/0'/0'/0/{idx}")
        if addr == ESCROW:
            print(f"!!!!!! DEMO ESCROW MATCH: md5={md5} idx={idx}")
            print("words:", words)
            open('DEMO_FOUND.txt','w').write(f"md5={md5} idx={idx}\nwords={words}\n")
            sys.exit(0)
    if n % 1000 == 0 and n:
        el=time.time()-t0; print(f"  {n}/{len(seen)} ({el:.0f}s), eta {(len(seen)-n)*el/n/60:.0f} min", flush=True)
print("no match in word k<=3")
