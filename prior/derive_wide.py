import sys, re, time
sys.path.insert(0,'.')
from demo_oracle import derive
ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
part = int(sys.argv[1]); nparts = int(sys.argv[2])
lo_idx = int(sys.argv[3]); hi_idx = int(sys.argv[4])
seen = set(); hits = []
for i in range(8):
    for line in open(f'bnd_{i}.txt'):
        m = re.match(r"MATCH mask=(\d+) flips=([\d,]*) md5=([0-9a-f]{32})", line)
        if not m: continue
        md5 = m.group(3)
        if md5 not in seen:
            seen.add(md5); hits.append(md5)
lo = len(hits)*part//nparts; hi = len(hits)*(part+1)//nparts
t0=time.time()
for n, md5 in enumerate(hits[lo:hi]):
    for idx in range(lo_idx, hi_idx):
        w_, addr = derive(bytes.fromhex(md5), f"m/44'/0'/0'/0/{idx}")
        if addr == ESCROW:
            print(f"!!!!!! SOLUTION: md5={md5} idx={idx} !!!!!!"); print("words:", w_)
            open(f'DEMO_FOUND_w{part}.txt','w').write(f"md5={md5} idx={idx}\nwords={w_}\n")
            sys.exit(0)
    if n % 3000 == 0 and n:
        el=time.time()-t0; print(f"w{part}: {n}/{hi-lo} ({el:.0f}s) eta {(hi-lo-n)*el/n/60:.0f}m", flush=True)
print(f"w{part}: done no match")
