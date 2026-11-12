import json,hashlib,itertools
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
import demo_oracle as D
# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"; LUCKY="1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
WL=D.WL
P=[t for _,t in json.load(open('wp_paras.json'))]

def words_entropy(b):
    n=len(b)*8; cs=n//32
    bits="".join(f"{x:08b}" for x in b)
    chk=hashlib.sha256(b).digest()
    allb=bits+"".join(f"{x:08b}" for x in chk)[:cs]
    return " ".join(WL[int(allb[i:i+11],2)] for i in range(0,len(allb),11))

def addr_from(entropy_bytes, path="m/44'/0'/0'/0/0"):
    w=words_entropy(entropy_bytes)
    seed=Bip39SeedGenerator(w).Generate("")
    ch=Bip32Slip10Secp256k1.FromSeed(seed).DerivePath(path)
    pub=ch.PrivateKey().PublicKey().RawCompressed().ToBytes()
    h=D.rmd160(hashlib.sha256(pub).digest())
    v=b"\x00"+h; ck=hashlib.sha256(hashlib.sha256(v).digest()).digest()[:4]
    return D.b58(v+ck), w

def lastword(p):
    import re
    ws=[w for w in re.findall(r"[A-Za-z']+",p)]
    return ws[-1] if ws else ''
def firstword(p):
    import re
    ws=[w for w in re.findall(r"[A-Za-z']+",p)]
    return ws[0] if ws else ''

W1=[lastword(P[i]) for i in range(4,8)]        # paras 5-8
W2=[lastword(P[i]) for i in range(167,171)]    # paras 168-171
W3=[lastword(P[i]) for i in range(92,96)]      # paras 93-96
F1=[firstword(P[i]) for i in range(4,8)]
F2=[firstword(P[i]) for i in range(167,171)]
print('last-word windows:'); print(' 5-8 ',W1); print(' 93-96 ',W3); print(' 168-171 ',W2)
print('first-word windows:'); print(' 5-8 ',F1); print(' 168-171 ',F2)
print('paras 231-235 lasts:',[lastword(P[i]) for i in range(230,235)])
print('paras 231-235 firsts:',[firstword(P[i]) for i in range(230,235)])

anchors=["Hal Finney","ihsotaS otomakaN"]
fold=["Aa","1N","zf","Pv","1i","eD","P7","5v"]

tokensets={
 'W1+W2':W1+W2,'W2+W1':W2+W1,'W3+W2':W3+W2,'W1+W3':W1+W3,
 'F1+F2':F1+F2,'W1+W2+anchors':W1+W2+anchors,
 'anchors':anchors,'fold8':fold,'fold8+anchors':fold+anchors,
 'finney5_lasts':[lastword(P[i]) for i in range(230,235)],
 'finney5_firsts':[firstword(P[i]) for i in range(230,235)],
}
links=['','62tGor2','isUB1bT','KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2',
       'Kx2YSerLwDfLvwLji6Ci4poW28hcbhnVC4yN8Q2i9HhwbisUB1bT','d7qGeip']
hits=[];n=0
for tname,toks in tokensets.items():
    for sep in (' ',''):
        core=sep.join(toks)
        for tomi in ('', ' TOMI '):
            body=core+(tomi+core if tomi else '')
            for link in links:
                for lsep in (' ',''):
                    s=body+((lsep+link) if link else '')
                    for algo in ('md5','sha256'):
                        d=hashlib.new(algo,s.encode()).digest()
                        for i in (0,1,2,6,7,76,77):
                            a,_=addr_from(d,f"m/44'/0'/0'/0/{i}"); n+=1
                            if a in (PRIZE,LUCKY): hits.append((tname,sep,tomi,link[:12],lsep,algo,i,s[:80]))
print('\nderivations',n,'| hits',hits)
