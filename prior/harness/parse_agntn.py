import re,glob,os,json
def parse(path):
    s=open(path,encoding='utf-8').read()
    d={}
    m=re.search(r'id:\s*"([^"]+)"',s); d['id']=m.group(1) if m else None
    m=re.search(r'address:\s*"([^"]+)"',s); d['address']=m.group(1) if m else None
    m=re.search(r'status:\s*Status\.(\w+)',s); d['status']=m.group(1) if m else None
    m=re.search(r'wif\(\s*"([^"]+)"\s*\)',s); d['wif']=m.group(1) if m else None
    m=re.search(r'entropy\(\s*"([0-9a-f]{32})"',s); d['entropy']=m.group(1) if m else None
    m=re.search(r'compressed\(\s*"([0-9a-f]+)"\s*\)',s); d['pubkey']=m.group(1) if m else None
    m=re.search(r'prize:\s*([0-9.]+)',s); d['prize']=m.group(1) if m else None
    d['answers']=re.findall(r'answer\(\s*"((?:[^"\\]|\\.)*)"',s)
    d['officials']=re.findall(r'official\(\s*"((?:[^"\\]|\\.)*)"',s)
    return d
for coll in ('quizchain2','quizchain','grycoin'):
    files=sorted(glob.glob(f'puzzles-main/src/collections/{coll}/*.ts'), key=lambda p:(len(os.path.basename(p)),os.path.basename(p)))
    recs=[parse(f) for f in files]
    json.dump(recs,open(f'{coll}_records.json','w'),indent=1)
    print(coll, len(recs), 'with wif:', sum(1 for r in recs if r['wif']))
