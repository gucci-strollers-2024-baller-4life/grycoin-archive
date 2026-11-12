import hashlib,itertools,json,re
import demo_oracle as D
ESC="1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"; PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
raw=open('demo_base.txt').read().replace('\r\n','\n')
paras=[p.strip() for p in raw.split('\n\n') if p.strip()]
text='\n\n'.join(paras)
i5=text.index('I expected'); h=text.index('himself')
flipped=text[:i5]+'i'+text[i5+1:]
flipped=flipped[:h+6]+'F'+flipped[h+7:] if False else flipped.replace('himself','himselF')
bases={'unchanged':text,'flips':flipped}
def md5b(s): return hashlib.md5(s.encode()).digest()
print('--- A: demo + chained 3-char code (novel)')
tried=0; pref=[]
for bname,b in bases.items():
    for sep in (' ','.','_',''):
        for combo in itertools.product(B58,repeat=3):
            s=b+sep+''.join(combo); tried+=1
            d=md5b(s)
            if d.hex().startswith('3c6'): pref.append((bname,sep,''.join(combo),d))
print('  candidates',tried,'3c6-prefix survivors',len(pref))
hitA=[]
for bname,sep,code,d in pref:
    w,a=D.derive(d)
    if a==ESC: hitA.append((bname,sep,code))
print('  escrow hits:',hitA)
print('\n--- B: Finney post (stage-one solution) transformed again')
sol=open('safudev_stage1.txt').read().rstrip('\n')
lines=[l for l in sol.split('\n') if l.strip()]
def edges(s,mode):
    q=list(s); idx=[i for i,c in enumerate(q) if c.isalpha()]
    f,l=idx[0],idx[-1]
    if 'u' in mode: q[f]=q[f].upper()   # restore question capitals
    if 'd' in mode: q[l]=q[l].lower()   # restore lowercase last
    if 'f' in mode: q[f]=q[f].lower()
    if 'l' in mode: q[l]=q[l].upper()
    return ''.join(q)
variants={
 'orig':sol,
 'deflip':'\n'.join(edges(l,'ud') if l.strip() else l for l in sol.split('\n')),
 'allfl':'\n'.join(edges(l,'fl') if l.strip() else l for l in sol.split('\n')),
 'allud':'\n'.join(edges(l,'ud') if l.strip() else l for l in sol.split('\n')),
}
n=0; hits=[]
for vname,v in variants.items():
    for jn in ('\n','\n\n','\r\n\r\n','\r\n'):
        txt=jn.join([x for x in v.split('\n') if x.strip()])
        d=md5b(txt)
        for ix in range(0,4):
            w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
            if a in (PRIZE,ESC): hits.append((vname,jn,ix,'PRIZE' if a==PRIZE else 'ESC'))
print('  derivations',n,'hits',hits)
