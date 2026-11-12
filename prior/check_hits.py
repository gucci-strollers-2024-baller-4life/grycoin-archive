import sys,hashlib
sys.path.insert(0,'sweeps')
from polarity_flip import addr0
ESC='1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi'
TARGET2='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
rows=[l.split() for l in open('k3_full_hits.txt') if l.startswith('HIT')]
print("hits to derive:",len(rows),flush=True)
for k,(_,pos,md5) in enumerate(rows,1):
    a=addr0(md5)
    if a in (ESC,TARGET2):
        print("*** PREIMAGE FOUND",pos,md5,a,flush=True)
    if k%1000==0: print("  derived",k,flush=True)
print("done",flush=True)
