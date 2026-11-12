"""Exhaustive closure: every contiguous paragraph range 1..273, flipped head-down/tail-up."""
import sys, hashlib, time
from multiprocessing import Pool
sys.path.insert(0,'.'); sys.path.insert(0,'harness')
from fastaddr import address
T = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
P = open('base_chapter_lf.txt',encoding='utf-8').read().split("\n\n")
assert len(P)==273
def flip(p):
    q=p[0].swapcase()+p[1:]
    js=[k for k,c in enumerate(q) if c.isalpha()]
    if not js: return q            # ¶15 '"2020."' has no letters: no-op both edges
    j=js[-1]
    return q[:j]+q[j].swapcase()+q[j+1:]
F=[flip(p) for p in P]
def work(args):
    lo,hi=args; out=[]
    for a in range(lo,hi+1):
        for b in range(a,274):
            q=list(P)
            for i in range(a,b+1): q[i-1]=F[i-1]
            body="\n\n".join(q); crlf="\r\n\r\n".join(q)
            for s in (body, body+"\n", crlf, crlf+"\n"):
                d=hashlib.md5(s.encode()).hexdigest()
                for idx in (0,1):
                    if address(d,idx)==T: out.append((a,b,idx,s is body or s.startswith(body)))
    return out
if __name__=="__main__":
    print("calibration:", address('9dd2efb9bc976c2095bd534d7b8d431c'), "(want 19TbyN5...)")
    t=time.time(); total=0; hits=[]
    chunks=[(a,a+1499) for a in range(1,274,1500)]
    chunks=[(a,min(b,273)) for a,b in chunks]
    with Pool(4) as pool:
        for r in pool.imap_unordered(work,chunks):
            hits+=r; total+=1
            print(f"  chunk done ({total}/{len(chunks)}) hits so far {len(hits)}  {time.time()-t:.0f}s")
    n=273*274//2
    print(f"\nranges swept: {n}  derivations: {n*8}  hits: {len(hits)}  elapsed {time.time()-t:.0f}s")
    for h in hits: print("***HIT",h)
