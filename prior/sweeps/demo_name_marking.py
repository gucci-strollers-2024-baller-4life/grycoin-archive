import re,hashlib,sys,time
sys.path.insert(0,'harness')
import btc
ESC='1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi'
raw=open('demo_base.txt',encoding='utf-8').read()
paras=[p.strip() for p in re.split(r'\n\s*\n',raw.strip()) if p.strip()]
base='\n\n'.join(paras).encode()
ba=bytearray(base)

def sweep(name, up=True):
    n=name.lower()
    L=len(n)
    # positions per letter (lowercase occurrences only, so the flip is visible)
    pos=[[i for i,c in enumerate(base) if chr(c).lower()==ch and (chr(c).islower() if up else chr(c).isupper())] for ch in n]
    cnt=0; hits=0; t0=time.time(); esc=0
    # DFS
    stack=[]
    def rec(k, start):
        nonlocal cnt,hits,esc
        if k==L:
            cnt+=1
            h=hashlib.md5(bytes(ba)).hexdigest()
            if h.startswith('3c6'):
                hits+=1
                a=btc.addr_from_md5hex(h)
                if a==ESC:
                    esc+=1; print('*** ESCROW HIT',name,h,a,flush=True)
                else: print('  hit',name,h,a,flush=True)
            return
        for i in pos[k]:
            if i<start: continue
            c=ba[i]; ba[i]= ord(chr(c).upper()) if up else ord(chr(c).lower())
            rec(k+1,i+1)
            ba[i]=c
    rec(0,0)
    print(f'{name} up={up} cands={cnt} 3c6={hits} esc={esc} {time.time()-t0:.1f}s',flush=True)

for nm in ['AOI','STNM','AGYN','YANG','NAKA','HAL','GRYN','AOIN']:
    sweep(nm)
