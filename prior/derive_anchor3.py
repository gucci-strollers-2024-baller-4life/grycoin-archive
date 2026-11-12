import sys, re, time
sys.path.insert(0,'.')
from demo_oracle import derive
ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
seen=set(); hits=[]
for line in open('anchor3_out.txt'):
    m = re.match(r"K3 pos=([\d,]+) md5=([0-9a-f]{32})", line)
    if not m: continue
    if m.group(2) not in seen:
        seen.add(m.group(2)); hits.append(m.group(2))
print(f"{len(hits)} unique k3-anchored hits", flush=True)
t0=time.time()
for n,md5 in enumerate(hits):
    for idx in range(7):
        w_,addr = derive(bytes.fromhex(md5), f"m/44'/0'/0'/0/{idx}")
        if addr == ESCROW:
            print(f"!!!!!! DEMO SOLVED: md5={md5} idx={idx} !!!!!!"); print("words:", w_)
            open('DEMO_FOUND.txt','w').write(f"md5={md5} idx={idx}\nwords={w_}\n")
            sys.exit(0)
    if n%2000==0 and n:
        el=time.time()-t0; print(f"{n}/{len(hits)} ({el:.0f}s) eta {(len(hits)-n)*el/n/60:.0f}m", flush=True)
print("k3-anchored: no escrow match")
