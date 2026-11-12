"""Demo (grycoin block 2) families re-checked with the REPAIRED harness.
The md5 '3c6' oracle is harness-independent; the escrow comparison was impossible before the fix."""
import re,hashlib,sys,time
sys.path.insert(0,'/tmp'); import fast
H=fast.H
ESC={'1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi','129jw1GUGwiJbf4rL7qEANPbxvSRC5zfHN'}
IDX=(0,1,2,76)
def derive(h,idx):
    return fast.p2pkh(fast.key_at(fast.seed_from(bytes.fromhex(h)),(44+H,0+H,0+H,0,idx)))
tot=[0,0,0]
def hcheck(txt,tag):
    h=hashlib.md5(txt).hexdigest()
    if not h.startswith('3c6'): return
    tot[1]+=1
    for idx in IDX:
        a=derive(h,idx); tot[0]+=1
        if a in ESC: tot[2]+=1; print('*** ESCROW',tag,idx,h,a,flush=True)

raw=open('demo_base.txt',encoding='utf-8').read()
paras=[p.strip() for p in re.split(r'\n\s*\n',raw.strip()) if p.strip()]
TEXTS={}
for jn,join in [('LF','\n\n'),('CRLF','\r\n\r\n')]:
    TEXTS['recon-'+jn]=join.join(paras).encode()
for f in ('demo_post_lf.txt','demo_post_crlf.txt'):
    try: TEXTS[f]=open(f,'rb').read()
    except FileNotFoundError: pass

def firstlast(t,a,b):
    fi=next((i for i in range(a,b) if t[i].isalpha()),None)
    li=next((i for i in range(b-1,a-1,-1) if t[i].isalpha()),None)
    return fi,li

t0=time.time()
for name,base in TEXTS.items():
    b=base.decode('utf-8')
    # paragraph spans and sentence spans
    psp=[]
    if '\r\n\r\n' in b: sep='\r\n\r\n'
    else: sep='\n\n'
    pos=0
    for p in b.split(sep):
        psp.append((pos,pos+len(p))); pos+=len(p)+len(sep)
    ssp=[];start=0
    for m in re.finditer(r'[.!?]+["\u201d]?\s+', b):
        e=m.end()
        while e>start and b[e-1].isspace(): e-=1
        ssp.append((start,e)); start=m.end()
    if start<len(b): ssp.append((start,len(b)))
    for label,spans in (('para',psp),('sent',ssp)):
        slots=[]
        for a,bb in spans:
            fi,li=firstlast(b,a,bb)
            if fi is not None and b[fi].isupper(): slots.append((fi,b[fi].lower()))
            if li is not None and b[li].islower(): slots.append((li,b[li].upper()))
        buf=bytearray(base); n=len(slots)
        def rec(k,start):
            if k>0: hcheck(bytes(buf),f'{name}-{label}-sub')
            if k==8: return
            for j in range(start,n):
                i,c=slots[j]; old=buf[i]
                buf[i]=ord(c) if isinstance(c,str) else c
                rec(k+1,j+1); buf[i]=old
        rec(0,0)
        print(f'-- {name} {label} slots={n} escrowhits={tot[2]} {time.time()-t0:.0f}s',flush=True)
print('TOTAL derivations=%d 3c6=%d escrow=%d %.0fs'%(tot[0],tot[1],tot[2],time.time()-t0))
