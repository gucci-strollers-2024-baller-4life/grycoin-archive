import sys,hashlib,time
R='/app/conversations/6ae63e0a707ef780407c8689/repo'
sys.path.insert(0,R); sys.path.insert(0,R+'/harness')
from fastaddr import address
T="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
P=open(R+'/base_chapter_lf.txt',encoding='utf-8').read().split("\n\n")
def ha(p):
    for i,c in enumerate(p):
        if c.isalpha(): return i
def ta(p):
    for i in range(len(p)-1,-1,-1):
        if p[i].isalpha(): return i
def ap(c,op): return c.lower() if op=='l' else c.upper()
log=open('edge3.log','w')
def say(s):
    log.write(s+"\n"); log.flush()
say("START")
tot=0; hits=0; t0=time.time()
for k,J in enumerate(("\n\n","\r\n\r\n")):
    body=J.join(P); offs=[]; pos=0
    for p in P:
        h,t=ha(p),ta(p)
        if h is not None: offs.append((pos+h,'l'))
        if t is not None: offs.append((pos+t,'u'))
        pos+=len(p)+len(J)
    n=len(offs); say("join %d: %d positions, %d pairs" % (k,n,n*(n-1)//2))
    for i in range(n):
        o1,p1=offs[i]
        s=body[:o1]+ap(body[o1],p1)+body[o1+1:]
        tot+=1
        if address(hashlib.md5(s.encode()).hexdigest(),0)==T:
            hits+=1; say("***HIT single join=%d i=%d" % (k,i))
        pre=body[:o1]; mid0=ap(body[o1],p1)
        for j in range(i+1,n):
            o2,p2=offs[j]
            s2=pre+mid0+body[o1+1:o2]+ap(body[o2],p2)+body[o2+1:]
            tot+=1
            if address(hashlib.md5(s2.encode()).hexdigest(),0)==T:
                hits+=1; say("***HIT pair join=%d i=%d j=%d" % (k,i,j))
        if i%40==0:
            say("  join %d i=%d  tot=%d hits=%d  %.0fs  %.0f/s" % (k,i,tot,hits,time.time()-t0,tot/(time.time()-t0)))
say("DONE tot=%d hits=%d %.0fs" % (tot,hits,time.time()-t0))
