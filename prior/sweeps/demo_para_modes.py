import re,hashlib,sys,time
sys.path.insert(0,'harness')
import btc
ESC='1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi'
raw=open('demo_base.txt',encoding='utf-8').read()
paras=[p.strip() for p in re.split(r'\n\s*\n',raw.strip()) if p.strip()]

def firstlast(t,a,b):
    fi=next((i for i in range(a,b) if t[i].isalpha()),None)
    li=next((i for i in range(b-1,a-1,-1) if t[i].isalpha()),None)
    return fi,li

MODES={'n':(), 'fd':('fd',), 'lu':('lu',), 'fdlu':('fd','lu'), 'fu':('fu',), 'ld':('ld',)}

def sweep(base, spans, label, modes):
    n=len(spans); fl=[firstlast(base,a,b) for a,b in spans]
    t0=time.time(); hits=0; esc=0; tot=0
    # per unit per mode: list of (pos,newchar)
    table=[]
    for (a,b),(fi,li) in zip(spans,fl):
        row={}
        for m in modes:
            mm=[]
            for op in MODES[m]:
                if op=='fd' and fi is not None and base[fi].isupper(): mm.append((fi,base[fi].lower()))
                if op=='fu' and fi is not None and base[fi].islower(): mm.append((fi,base[fi].upper()))
                if op=='lu' and li is not None and base[li].islower(): mm.append((li,base[li].upper()))
                if op=='ld' and li is not None and base[li].isupper(): mm.append((li,base[li].lower()))
            row[m]=mm
        table.append(row)
    K=len(modes)
    for idx in range(K**n):
        t=list(base); x=idx
        for k in range(n):
            for i,c in table[k][modes[x%K]]: t[i]=c
            x//=K
        tot+=1
        h=hashlib.md5(''.join(t).encode()).hexdigest()
        if h.startswith('3c6'):
            hits+=1
            a=btc.addr_from_md5hex(h)
            if a==ESC:
                esc+=1; print('*** ESCROW',label,h,a,[modes[(idx//(K**k))%K] for k in range(n)],flush=True)
    print(f'{label} n={n} modes={modes} cands={tot} 3c6={hits} esc={esc} {time.time()-t0:.1f}s',flush=True)

for jn,join in [('LF','\n\n'),('CRLF','\r\n\r\n')]:
    base=join.join(paras)
    pspans=[];pos=0
    for p in paras: pspans.append((pos,pos+len(p))); pos+=len(p)+len(join)
    sweep(base,pspans,'para-'+jn,['n','fd','lu','fdlu'])
