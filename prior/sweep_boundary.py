import re, sys, hashlib, time
from multiprocessing import Pool
import fastlane
TARGET="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
RAW=open("base_chapter_lf.txt",encoding="utf-8").read()
P=RAW.split("\n\n")

# --- sentence boundaries: last alphabetic char before each terminator ---
bounds=[]
for m in re.finditer(r'[.?!]+["\u201d]?(?=\s)', RAW):
    j=m.start()-1
    while j>0 and not RAW[j].isalpha(): j-=1
    if RAW[j].isalpha(): bounds.append(j)
B=[RAW+"\n", RAW]

def flip_chars(s, idxs):
    for j in idxs:
        c=s[j]
        s=s[:j]+(c.lower() if c.isupper() else c.upper())+s[j+1:]
    return s

def work(args):
    lo,hi=args
    hits=[]; n=0
    for a in range(lo,hi):
        i,j=PAIRS[a]
        for k,base in enumerate(B):
            h=hashlib.md5(flip_chars(base,(i,j)).encode()).hexdigest()
            if fastlane.addr(h)==TARGET: hits.append(("sent",i,j,k,h))
            n+=1
    return hits,n

PAIRS=None
if __name__=="__main__":
    print("sentence boundaries:",len(bounds),flush=True)
    pairs=[(i,j) for x,i in enumerate(bounds) for j in bounds[x+1:]]
    globals()["PAIRS"]=pairs
    print("distinct terminator-pairs:",len(pairs),"x2 join styles =",len(pairs)*2,flush=True)
    t0=time.time(); tot=0
    step=20000
    with Pool(4) as pool:
        for hits,n in pool.imap_unordered(work,[(a,min(a+step,len(pairs))) for a in range(0,len(pairs),step)]):
            tot+=n
            if hits: print("HIT",hits,flush=True)
    print("derived %d addresses in %.0fs, hits: none" % (tot,time.time()-t0))
