import sys, time
sys.path.insert(0,'.')
from demo_oracle import derive
ESC = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
t0=time.time(); n=0
for line in open('uniq_3c6.txt'):
    h=line.strip()
    if not h: continue
    words, addr = derive(bytes.fromhex(h), "m/44'/0'/0'/0/0")
    n+=1
    if addr == ESC:
        print(f"!!!!!! ESCROW MATCH md5={h} words={words}")
        open('DEMO_SOLUTION.txt','a').write(f"{h} {words}\n")
    if n % 20000 == 0:
        print(f"{n} done, {time.time()-t0:.0f}s elapsed", flush=True)
print(f"complete: {n} derivations, {time.time()-t0:.0f}s")
