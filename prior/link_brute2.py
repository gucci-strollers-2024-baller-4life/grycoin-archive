import hashlib, sys, itertools, time
sys.path.insert(0,'.')
from demo_oracle import derive
LIVE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; OLD="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"; DEMO="1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
E={LIVE:'LIVE',OLD:'OLD',DEMO:'DEMO'}
B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
base="1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN"
forms=[lambda L: f"{base} TOMI Omit TOMI {L}", lambda L: f"{base} {L}", lambda L: f"{base} TOMI omit TOMI {L}"]
t0=time.time(); n=0
for ln in (3,4):
    for tup in itertools.product(B58, repeat=ln):
        L="".join(tup)
        for f in forms:
            body=f(L)
            h=hashlib.md5(body.encode()).hexdigest()
            try: w,a=derive(bytes.fromhex(h))
            except Exception: continue
            n+=1
            if a in E:
                print("!!!! MATCH",E[a],repr(body),w,flush=True)
                open('RBB_SOLUTION.txt','a').write(f"{h} {body} {w} {a}\n")
        if n % 200000 == 0:
            print(f"...{n} len={ln} {time.time()-t0:.0f}s", flush=True)
    print(f"done length {ln} at {time.time()-t0:.0f}s, n={n}", flush=True)
print("ALL DONE", n, flush=True)
