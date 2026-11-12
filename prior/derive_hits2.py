import sys, re
sys.path.insert(0,'.')
from demo_oracle import derive
ESC = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
PUB = "039ad91b631e5e2f0915b682c6ab8a29d81bb464a2ffc8ebf9702aad7b238192dc"
import coincurve
n=0
for line in sys.stdin:
    m = re.search(r'md5=([0-9a-f]{32})', line)
    if not m: continue
    h = m.group(1)
    for path in ("m/44'/0'/0'/0/0",):
        words, addr = derive(bytes.fromhex(h), path)
        n+=1
        if addr == ESC:
            print("!!!!!! ESCROW MATCH:", line.strip(), "words:", words, flush=True)
            open('DEMO_SOLUTION.txt','a').write(line.strip()+" "+words+"\n")
print(f"derived {n}, done", file=sys.stderr)
