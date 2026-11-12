import hashlib,glob,json,re,os
TARGET="8b71bade9685d3388452bc4755b06a0d"
md5=lambda s: hashlib.md5(s.encode()).hexdigest()
hits=[]
def check(s,src):
    if not s or not s.strip(): return
    for v in {s, s.strip(), s.strip()+" ", " "+s.strip(), s.rstrip()}:
        if md5(v)==TARGET: hits.append((src,repr(v)[:140]))
texts=[]
for f in glob.glob('*.txt')+glob.glob('*.html')+glob.glob('*.json')+glob.glob('part_*_paras.json'):
    try:
        if os.path.getsize(f)>3_000_000: continue
        texts.append((f,open(f,errors='replace').read()))
    except Exception:
        pass
for f,t in texts:
    t2=t.replace('\\r\\n','\n').replace('\\n','\n')
    for p in re.split(r'\n\s*\n|(?=<p )', t2):
        check(p,f)
        for s in re.split(r'(?<=[.!?"])\s+',p):
            check(s,f)
print('hits:',len(hits))
for h in hits[:10]: print('  ',h)
for cand in ['"What?"','\\"What?\\"','\u201cWhat?\u201d','What?','"What?" ','"what?"','"What?"\n','"What?"\r\n','"What??"']:
    if md5(cand)==TARGET: print('variant hit',repr(cand))
print('md5("What?") =',md5('"What?"')[:8],' target',TARGET[:8])
