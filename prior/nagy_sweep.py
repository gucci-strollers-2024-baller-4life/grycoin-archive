import hashlib, itertools, sys, time
sys.path.insert(0,'.')
from demo_oracle import derive
ESC = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
lf = open('demo_base.txt','rb').read()
crlf = open('demo_base_crlf.txt','rb').read()
t = lf.decode()
occ = {}
for i,c in enumerate(t):
    if c.isalpha(): occ.setdefault(c.lower(), []).append(i)
def to_crlf(p):
    n=0; i=0
    while True:
        i = lf.find(b'\n\n', i)
        if i==-1 or i+2>p: break
        n+=1; i+=2
    return p+2*n
# stated pair positions (LF)
p_I = t.index('I expected')
p_him = t.index('himself') + len('himself') - 1
# ITASM set {3,4,6,7,8}: para firsts/lasts
paras = t.split('\n\n')
def para_firstlast(pi):
    p = paras[pi]
    f = next(i for i,c in enumerate(p) if c.isalpha())
    l = max(i for i,c in enumerate(p) if c.isalpha())
    off = sum(len(x)+2 for x in paras[:pi])
    return off+f, off+l
itasm = []
for pi in (2,3,5,6,7):
    itasm += list(para_firstlast(pi))
crlf_map = {p: to_crlf(p) for p in set([p_I,p_him]+itasm)}
variants = {
  "plain": [],
  "stated": [p_I, p_him],
  "itasm": itasm,
  "stated+itasm": [p_I, p_him]+itasm,
}
t0=time.time(); n=0; hits=[]
for name, extra in variants.items():
    for ser, base in (("LF", lf), ("CRLF", crlf)):
        ex = [crlf_map.get(p,p) if ser=="CRLF" and p in crlf_map else (to_crlf(p) if ser=="CRLF" else p) for p in extra]
        for perm in itertools.permutations('nagy'):
            ps = [occ.get(ch,[]) for ch in perm]
            def rec(k, lo, chosen):
                global n
                if k==4:
                    poss = chosen + ex
                    b = bytearray(base)
                    for p in poss:
                        c = b[p]
                        b[p] = c+32 if 65<=c<=90 else (c-32 if 97<=c<=122 else c)
                    h = hashlib.md5(bytes(b)).hexdigest()
                    n += 1
                    if h.startswith("3c6"):
                        words, addr = derive(bytes.fromhex(h))
                        tag = f"{name} {ser} {''.join(perm)} {poss}"
                        print("3c6:", tag, h, "->", addr, flush=True)
                        if addr==ESC:
                            print("!!!!!! ESCROW MATCH:", tag, words); hits.append(tag)
                            open('DEMO_SOLUTION.txt','a').write(tag+" "+h+" "+words+"\n")
                    return
                for p in ps[k]:
                    if p>lo: rec(k+1, p, chosen+[p])
            rec(0,-1,[])
        print(f"[{name} {ser}] done, {n} hashes, {time.time()-t0:.0f}s", flush=True)
print("total:", n, "hits:", hits)
