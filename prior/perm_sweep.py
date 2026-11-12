import hashlib, sys, itertools
sys.path.insert(0,'.')
from demo_oracle import derive
LIVE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; OLD="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
sets = {
 "A": ["1A1","efi2DM","Hal","Finney","Nm","ST","ihsotaS","otomakaN"],
 "B": ["1A1","efi2DM","Hal","Finney","TS","mN","ihsotaS","otomakaN"],
}
links = {"none":"", "w7":" dBEhAz3", "h7":" 4c19f4f", "st":" 62tGor2"}
n=0
for tag, items in sets.items():
    for perm in itertools.permutations(range(8)):
        s = " ".join(items[i] for i in perm)
        for lt, link in links.items():
            body = s + link
            h = hashlib.md5(body.encode()).hexdigest()
            w,a = derive(bytes.fromhex(h)); n+=1
            if a in (LIVE, OLD):
                print("!!!! MATCH", tag, lt, perm, repr(body), w, a, flush=True)
                open('RBB_SOLUTION.txt','a').write(f"{tag} {lt} {h} {body} {w} {a}\n")
            if n % 100000 == 0: print("...", n, flush=True)
print("done", n, flush=True)
