import re, json, hashlib, sys, html as ihtml, urllib.request
def fetch_text(part_id):
    url = f"https://www.wattpad.com/apiv2/storytext?id={part_id}&output=text"
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    raw = urllib.request.urlopen(req).read().decode('utf-8','replace')
    return raw
def extract_paras(raw):
    # case A: apiv2 debug dump: Array\n(\n    [text] => <p ...>...</p>\n)
    m = re.search(r'\[text\] => (.*)\n\)', raw, re.S)
    src = m.group(1) if m else raw
    # case B: v4 style [data] => ...
    if not m:
        m2 = re.search(r'"text":"(.*)"', raw)
        if m2: src = m2.group(1).encode().decode('unicode_escape')
    # extract <p data-p-id="...">...</p> blocks
    blocks = re.findall(r'<p data-p-id="([0-9a-f]+)"[^>]*>(.*?)</p>', src, re.S)
    out = []
    for pid, content in blocks:
        # inline breaks -> nothing; tags stripped
        content = re.sub(r'<br\s*/?>', '\n', content)
        content = re.sub(r'<[^>]+>', '', content)
        content = ihtml.unescape(content)
        out.append((pid, content))
    return out
pid_arg = sys.argv[1]
raw = fetch_text(pid_arg)
paras = extract_paras(raw)
ok = bad = 0
texts = []
mism = []
for i, (pid, t) in enumerate(paras):
    texts.append(t)
    if hashlib.md5(t.encode()).hexdigest() == pid: ok += 1
    else:
        bad += 1; mism.append((i+1, pid, hashlib.md5(t.encode()).hexdigest(), t[:70]))
json.dump(texts, open(f"part_{pid_arg}_paras.json","w"))
print(f"part {pid_arg}: {len(paras)} paras, pid ok={ok} bad={bad}")
for x in mism[:8]: print("  MISMATCH:", x)
