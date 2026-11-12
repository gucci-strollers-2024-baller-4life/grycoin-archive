import re,hashlib,sys,time
sys.path.insert(0,'harness')
import btc
ESC='1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi'
raw=open('demo_base.txt',encoding='utf-8').read()
paras=[p.strip() for p in re.split(r'\n\s*\n',raw.strip()) if p.strip()]

def span_edges(text,a,b):
    fi=next((i for i in range(a,b) if text[i].isalpha()),None)
    li=next((i for i in range(b-1,a-1,-1) if text[i].isalpha()),None)
    return fi,li

def run(base, spans, label, K):
    # slots: (pos, newchar)
    slots=[]
    for a,b in spans:
        fi,li=span_edges(base,a,b)
        if fi is not None and base[fi].isupper(): slots.append((fi,base[fi].lower()))
        if li is not None and base[li].islower(): slots.append((li,base[li].upper()))
    n=len(slots); print(label,'slots',n,flush=True)
    ba=bytearray(base.encode()); t0=time.time(); cnt=0; hits=0; esc=0
    def rec(k,start):
        nonlocal cnt,hits,esc
        if k>0:
            cnt+=1
            h=hashlib.md5(bytes(ba)).hexdigest()
            if h.startswith('3c6'):
                hits+=1
                a=btc.addr_from_md5hex(h)
                if a==ESC:
                    esc+=1; print('*** ESCROW',label,h,a,flush=True)
        if k==K: return
        for j in range(start,n):
            i,c=slots[j]
            old=ba[i]; ba[i]=ord(c)
            rec(k+1,j+1)
            ba[i]=old
    rec(0,0)
    print(f'{label} slots={n} K={K} cands={cnt} 3c6={hits} esc={esc} {time.time()-t0:.1f}s',flush=True)

for jn,join in [('LF','\n\n'),('CRLF','\r\n\r\n')]:
    base=join.join(paras)
    # paragraph spans
    psp=[];pos=0
    for p in paras: psp.append((pos,pos+len(p))); pos+=len(p)+len(join)
    # sentence spans
    ssp=[];start=0
    for m in re.finditer(r'[.!?]+["\u201d]?\s+', base):
        e=m.end()
        while e>start and base[e-1].isspace(): e-=1
        ssp.append((start,e)); start=m.end()
    if start<len(base): ssp.append((start,len(base)))
    run(base,psp,'para-'+jn,8)
    run(base,ssp,'sent-'+jn,8)
    # word spans
    wsp=[]
    for m in re.finditer(r"[A-Za-z']+", base): wsp.append((m.start(),m.end()))
    run(base,wsp,'word-'+jn,0)
