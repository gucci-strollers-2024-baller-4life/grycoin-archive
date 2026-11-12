import hashlib,re,itertools,time
import demo_oracle as D
ESC=D.ESCROW
raw=open('demo_base.txt').read().replace('\r\n','\n')
paras=[p.strip() for p in raw.split('\n\n') if p.strip()]
text='\n\n'.join(paras)
HH=lambda s: hashlib.md5(s.encode()).digest()
print('Q md5',HH(text).hex()[:10])
a=D.derive(HH(text)); print('unchanged ->',a,'*** ESCROW' if a==ESC else '')

sites=[(m.start(),'I') for m in re.finditer(r'\bI\b',text)]+[(m.start(),'H') for m in re.finditer(r'\bhimself\b',text)]
print('sites',len(sites))
def build(mask):
    out=[];last=0
    for i,(pos,w) in enumerate(sites):
        if not (mask>>i)&1: continue
        out.append(text[last:pos]); out.append('i' if w=='I' else 'himselF'); last=pos+len(w)
    out.append(text[last:]); return ''.join(out)
t0=time.time(); sol=None
for mask in range(1,1<<len(sites)):
    s=build(mask)
    if D.derive(HH(s))==ESC: sol=('I/H',mask); break
print('phase1 I/himself subsets',2**len(sites)-1,'solutions',sol,'%.1fs'%(time.time()-t0))

# paragraph-edge space: per paragraph none / first-down / last-up / both
def edges(mode_list):
    out=[]
    for p,m in zip(paras,mode_list):
        q=list(p)
        idx=[i for i,c in enumerate(q) if c.isalpha()]
        if m in ('first','both') and q[idx[0]].isupper(): q[idx[0]]=q[idx[0]].lower()
        if m in ('last','both') and q[idx[-1]].islower(): q[idx[-1]]=q[idx[-1]].upper()
        out.append(''.join(q))
    return '\n\n'.join(out)
modes=['none','first','last','both']
t0=time.time(); pref=[]; n=0
for combo in itertools.product(modes,repeat=len(paras)):
    s=edges(combo); h=HH(s); n+=1
    if h[:3]==b'\x3c\x6f'[0:0]: pass
    if h.hex().startswith('3c6'): pref.append((combo,h))
print('edge space',n,'prefix3c6',len(pref),'%.1fs'%(time.time()-t0))
hits=[]
for combo,h in pref:
    if D.derive(h)==ESC: hits.append(combo)
print('edge-space ESCROW hits:',hits)
