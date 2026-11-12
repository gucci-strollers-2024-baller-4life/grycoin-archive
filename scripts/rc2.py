import sys, hashlib, time, json
from multiprocessing import Pool
sys.path.insert(0,'.'); sys.path.insert(0,'harness')
from fastaddr import address
T="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
P=open('base_chapter_lf.txt',encoding='utf-8').read().split("\n\n")
assert len(P)==273
def flip(p):
    q=p[0].swapcase()+p[1:]
    js=[k for k,c in enumerate(q) if c.isalpha()]
    if not js: return q
    j=js[-1]; return q[:j]+q[j].swapcase()+q[j+1:]
F=[flip(p) for p in P]
def work(as_):
    out=[]
    for a in as_:
        for b in range(a,274):
            q=list(P)
            q[a-1:b]=F[a-1:b]
            body="\n\n".join(q)
            for s in (body, body+"\n", "\r\n\r\n".join(q), "\r\n\r\n".join(q)+"\n"):
                d=hashlib.md5(s.encode()).hexdigest()
                for idx in (0,1):
                    if address(d,idx)==T: out.append([a,b,idx,len(s)])
    return out
if __name__=="__main__":
    cal=address('9dd2efb9bc976c2095bd534d7b8d431c')
    print("calibration:",cal,"OK" if cal.startswith("19TbyN5") else "FAIL",flush=True)
    if not cal.startswith("19TbyN5"): raise SystemExit("harness not certified")
    groups=[[] for _ in range(4)]; load=[0]*4
    for a in range(1,274):
        i=load.index(min(load)); groups[i].append(a); load[i]+=274-a
    print("load balance:",load,flush=True)
    t=time.time(); hits=[]
    with Pool(4) as pool:
        for r in pool.imap_unordered(work,groups):
            hits+=r; print(f"  group done hits={len(hits)} t={time.time()-t:.0f}s",flush=True)
    n=273*274//2
    print(f"\nRESULT ranges={n} derivations={n*8} hits={len(hits)} elapsed={time.time()-t:.0f}s",flush=True)
    open('range_closure_result.json','w').write(json.dumps({"ranges":n,"derivations":n*8,"hits":hits}))
    for h in hits: print("***HIT",h,flush=True)
