import re, json, hashlib, sys, urllib.request
def fetch(part_id):
    url = f"https://www.wattpad.com/apiv2/storytext?id={part_id}&output=text"
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    return urllib.request.urlopen(req).read().decode()
def fetch_html(part_id):
    url = f"https://www.wattpad.com/{part_id}"
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    return urllib.request.urlopen(req).read().decode('utf-8', 'replace')
pid = sys.argv[1]
html = fetch_html(pid)
text = fetch(pid)
open(f"part_{pid}.txt", "w").write(text)
paras = [p for p in text.split("\n\n")]
print(f"part {pid}: {len(text)} chars, {len(paras)} paras (\\n\\n split)")
# pid verification
pid_re = re.findall(r'data-p-id="([0-9a-f]+)"', html)
ok = bad = 0
bad_list = []
for i, p in enumerate(paras):
    h = hashlib.md5(p.encode()).hexdigest()
    if i < len(pid_re):
        if h == pid_re[i]: ok += 1
        else:
            bad += 1; bad_list.append((i+1, pid_re[i], h, p[:60]))
    else:
        bad_list.append((i+1, 'NO-PID', h, p[:60])); bad += 1
print(f"pid verify: {ok} ok, {bad} mismatch")
for b in bad_list[:10]: print("  MISMATCH para", b)
