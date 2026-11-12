import sys, hashlib, itertools, time
R='/app/conversations/6ae63e0a707ef780407c8689/repo'
sys.path.insert(0,R); sys.path.insert(0,R+'/harness')
from fastaddr import address
import multiprocessing as mp
T="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
P=open(R+'/base_chapter_lf.txt',encoding='utf-8').read().split("\n\n")
def ha(p):
    for i,c in enumerate(p):
        if c.isalpha(): return i
def ta(p):
    for i in range(len(p)-1,-1,-1):
        if p[i].isalpha(): return i
G={}
def build(J):
    body=J.join(P); offs=[]; pos=0
    for p in P:
        h=ha(p); t=ta(p)
        if h is not None: offs.append((pos+h,'l'))
        if t is not None: offs.append((pos+t,'u'))
        pos+=len(p)+len(J)
    return body,offs
for k,J in enumerate(("\n\n","\r\n\r\n")): G[k]=build(J)
def mut(body,off1,op1,off2=None,op2=None):
    def ap(c,op): return c.lower() if op=='l' else c.upper()
    if off2 is None:
        return body[:off1]+ap(body[off1],op1)+body[off1+1:]
    a,b=sorted([(off1,op1),(off2,op2)])
    return body[:a[0]]+ap(body[a[0]],a[1])+body[a[0]+1:b[0]]+ap(body[b[0]],b[1])+body[b[0]+1:]
def work(args):
    k,i0=args
    body,offs=G[k]; hits=[]; n=0
    for i in range(i0,len(offs)):
        o1,p1=offs[i]
        s=mut(body,o1,p1); n+=1
        if address(hashlib.md5(s.encode()).hexdigest(),0)==T: hits.append(('single',k,i))
        for j in range(i+1,len(offs)):
            o2,p2=offs[j]; n+=1
            s2=mut(body,o1,p1,o2,p2)
            if address(hashlib.md5(s2.encode()).hexdigest(),0)==T: hits.append(('pair',k,i,j))
    return n,hits
if __name__=="__main__":
    t0=time.time(); tasks=[(k,i) for k in (0,1) for i in range(len(G[k][1]))]
    print("positions per join:",len(G[0][1]),"tasks:",len(tasks),flush=True)
    tot=0; allh=[]
    with mp.Pool(4) as pool:
        done=0
        for n,h in pool.imap_unordered(work,tasks,chunksize=4):
            tot+=n; allh+=h; done+=1
            if done%25==0:
                print("  tasks %d/%d  derivations %d  hits %d  %.0fs"%(done,len(tasks),tot,len(allh),time.time()-t0),flush=True)
    print("derivations:",tot,"seconds:",round(time.time()-t0,1),"rate:",round(tot/(time.time()-t0)),"/s")
    print("HITS:",len(allh))
    for h in allh: print("***",h)
