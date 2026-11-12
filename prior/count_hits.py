import re
seen=set()
for i in range(8):
    for line in open(f'bnd_{i}.txt'):
        m=re.match(r'MATCH mask=(\d+) flips=([\d,]*) md5=([0-9a-f]{32})', line)
        if m: seen.add(m.group(3))
print(len(seen))
