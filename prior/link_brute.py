import hashlib, sys, itertools
sys.path.insert(0,'.')
from demo_oracle import derive
LIVE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; OLD="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"; DEMO="1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
bases = ["1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN",
         "1A1 efi2DM Hal Finney otomakaN ihsotaS mN TS"]
n=0
for b in bases:
    for t in itertools.product(B58, repeat=3):
        link="".join(t)
        for sep in (" ", ""):
            s = b+sep+link
            h=hashlib.md5(s.encode()).hexdigest()
            w,a=derive(bytes.fromhex(h))
            n+=1
            if a in (LIVE,OLD,DEMO):
                print("!!!! MATCH", repr(s), a, w, flush=True)
                open('RBB_SOLUTION.txt','a').write(f"{h} {s} {w} {a}\n")
print("done", n, flush=True)
