import json,re,collections
P=json.load(open('cq_paras.json')); T=[t for _,t in P]
# split into sections at Block headings
secs=[]; cur=None
for t in T:
    m=re.match(r'^Block (\d+)$',t.strip())
    if m:
        cur={'block':int(m.group(1)),'lines':[]}; secs.append(cur)
    elif cur is not None:
        if t.strip() in ('Round 2','Hints'): cur=None
        else: cur['lines'].append(t.strip())
print('sections:',len(secs))
# split rounds
b=[s['block'] for s in secs]
r2start=next(i for i in range(1,len(b)) if b[i]<b[i-1])
rounds=[('R1',secs[:r2start]),('R2',secs[r2start:])]
for lbl,ss in rounds: print(lbl,'blocks',[s['block'] for s in ss][:5],'...',[s['block'] for s in ss][-3:],'count',len(ss))

fmt=collections.Counter(); kw=collections.Counter()
KEY=['first letter','last letter','vowel','ciphertext','plaintext','anagram','foldover','upside','44','eight','four','left','right','TOMI','password manager','private key','chapter','Wattpad','sign','genesis','address','MD5','hash','eleven','seven','five','pointer','Fibonacci','M ','W','double','mirror','reverse']
for lbl,ss in rounds:
    for s in ss:
        txt=' '.join(s['lines'])
        for line in s['lines']:
            if line.startswith('Format:'): fmt[re.sub(r'\[[^\]]*\]','[X]',line) if False else line]+=1
        low=txt.lower()
        for k in KEY:
            if k.lower() in low: kw[k]+=1
print('\nformat-line variants (top):')
for f,c in fmt.most_common(8): print(f'  {c:>3}  {f[:90]}')
print('\nkeyword frequency across',len(secs),'block entries:')
for k,c in kw.most_common(20): print(f'  {c:>3}  {k}')
json.dump({'rounds':{lbl:[{'block':s['block'],'lines':s['lines']} for s in ss] for lbl,ss in rounds}},open('cq_blocks.json','w'),indent=1)
