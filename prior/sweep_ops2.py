import re, hashlib, time
from multiprocessing import Pool
import fastlane
TARGET="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
RAW=open("base_chapter_lf.txt",encoding="utf-8").read()
BASES=[RAW+"\n", RAW]

# --- op B: first alphabetic char AFTER each terminator (quote-skipping) ---
after=[]
for m in re.finditer(r'[.?!]+["\u201d]?(?=\s)', RAW):
    e=m.end()
    while e<len(RAW) and not RAW[e].isalpha(): e+=1
    if e<len(RAW): after.append(e)
PAIRS_B=[(i,j) for x,i in enumerate(after) for j in after[x+1:]]

# --- paragraph pairs: certified flip on both paragraphs of the pair ---
P=RAW.split("\n\n")
def flip_para(p):
    al=[i for i,c in enumerate(p) if c.isalpha()]
    if not al: return p
    fi,li=al[0],al[-1]
    c=list(p); c[fi]=p[fi].lower(); c[li]=p[li].upper()
    return "".join(c)
PARA_PAIRS=[(x,j) for x in range(len(P)) for j in range(x+1,len(P))]

def workB(band):
    lo,hi=band; hits=[]; n=0
    for a in range(lo,hi):
        i,j=PAIRS_B[a]
        for k,base in enumerate(BASES):
            c=list(base); 
            for pos in (i,j):
                c[pos]=c[pos].lower() if c[pos].isupper() else c[pos].upper()
            h=hashlib.md5("".join(c).encode()).hexdigest()
            if fastlane.addr(h)==TARGET: hits.append(("B",i,j,k))
            n+=1
    return hits,n

def workP(band):
    lo,hi=band; hits=[]; n=0
    for a in range(lo,hi):
        i,j=PARA_PAIRS[a]
        q=list(P); q[i]=flip_para(P[i]); q[j]=flip_para(P[j])
        body="\n\n".join(q)
        for k,base in enumerate((body+"\n",body)):
            h=hashlib.md5(base.encode()).hexdigest()
            if fastlane.addr(h)==TARGET: hits.append(("P",i,j,k))
            n+=1
    return hits,n

t0=time.time(); tot=0; allhits=[]
with Pool(4) as pool:
    for fn,items in ((workB,PAIRS_B),(workP,PARA_PAIRS)):
        step=max(1,len(items)//32)
        for hits,n in pool.imap_unordered(fn,[(a,min(a+step,len(items))) for a in range(0,len(items),step)]):
            tot+=n; allhits+=hits
            if hits: print("HIT",hits,flush=True)
print("op B boundaries:",len(after),"pairs:",len(PAIRS_B))
print("paragraph pairs:",len(PARA_PAIRS))
print("total addresses derived: %d in %.0fs  hits: %s" % (tot,time.time()-t0,allhits or "none"))
