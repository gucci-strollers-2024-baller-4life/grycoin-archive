import hashlib, itertools, sys, time
sys.path.insert(0,'.')
from demo_oracle import derive
ESC = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
lf = open('demo_base.txt','rb').read()
crlf = open('demo_base_crlf.txt','rb').read()
t = lf.decode()
def to_crlf(p):
    n=0; i=0
    while True:
        i = lf.find(b'\n\n', i)
        if i==-1 or i+2>p: break
        n+=1; i+=2
    return p+2*n
import re
# word instances (LF coords): (first_pos, last_pos)
def word_instances(word):
    out=[]
    for m in re.finditer(r"\b"+re.escape(word)+r"\b", t):
        out.append((m.start(), m.start()+len(word)-1))
    return out
types = ["I","signs","sign","recognize","himself","solution","Satoshi","letters","capitalization","method","result","format","paragraph"]
inst = {w: word_instances(w) for w in types}
for w in types: print(w, len(inst[w]), flush=True)
p_I5 = t.index('I expected'); p_him5 = t.index('himself')+7
crlf_pI5, crlf_phim5 = to_crlf(p_I5), to_crlf(p_him5)
t0=time.time(); n=0
opts = ['n','f','l','b']  # none, first-down, last-up, both
for combo in itertools.product(opts, repeat=len(types)):
    ps=[]; ds=[]
    for (w, o) in zip(types, combo):
        if o=='n': continue
        for (fp, lp) in inst[w]:
            if o in ('f','b'): ps.append(fp); ds.append('D')
            if o in ('l','b'): ps.append(lp); ds.append('U')
    for ser, base in (("LF", lf), ("CRLF", crlf)):
        pp = [to_crlf(p) if ser=="CRLF" else p for p in ps]
        b = bytearray(base)
        for p, d in zip(pp, ds):
            c = b[p]
            b[p] = c+32 if 65<=c<=90 else (c-32 if 97<=c<=122 else c)
        h = hashlib.md5(bytes(b)).hexdigest()
        n += 1
        if h.startswith("3c6"):
            words, addr = derive(bytes.fromhex(h))
            tag = f"{ser} {dict((w,o) for w,o in zip(types,combo) if o!='n')}"
            print("3c6:", tag, h, "->", addr, flush=True)
            if addr==ESC:
                print("!!!!!! ESCROW MATCH:", tag, words, flush=True)
                open('DEMO_SOLUTION.txt','a').write(tag+" "+h+" "+words+"\n")
    if n % 200000 == 0: print(f"...{n} hashes {time.time()-t0:.0f}s", flush=True)
print("done", n, f"{time.time()-t0:.0f}s")
