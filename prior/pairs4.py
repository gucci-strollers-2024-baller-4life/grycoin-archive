"""Exhaustive two-paragraph edge-edit sweep: both endpoints of paragraph i and of paragraph j
(4 letters), across 2 joins, 2 trailing variants and 2 derivation indices, against both escrows."""
import json, hashlib, hmac, sys
sys.path.insert(0, 'sweeps')
import polarity_flip as pf
H = pf.HARD
NEW = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
OLD = '1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
RAW = json.load(open('wp_paras_br.json'))
SEG = [list(p) if isinstance(p, list) else [p] for p in RAW]

def flip(p):
    a = [i for i, c in enumerate(p) if c.isalpha()]
    if not a: return p
    p = p[:a[0]] + p[a[0]].swapcase() + p[a[0]+1:]
    return p[:a[-1]] + p[a[-1]].swapcase() + p[a[-1]+1:]

# per-paragraph rendered text under two joins
LF = [flip("\n".join(s)) for s in SEG]
CR = [flip("\r\n".join(s)) for s in SEG]
LF0 = ["\n".join(s) for s in SEG]
CR0 = ["\r\n".join(s) for s in SEG]

def derive(md5hex, idx):
    I = hmac.new(b'Bitcoin seed', pf.seed(bytes.fromhex(md5hex)), hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32], 'big'), I[32:]
    for x in (44+H, 0+H, 0+H, 0, idx):
        k, c = pf.ckd(k, c, x)
    return pf.b58(b'\x00' + hashlib.new('ripemd160', hashlib.sha256(pf.pub(k)).digest()).digest())

n = 0
for join_name, sep, mod, orig in (('LF', '\n\n', LF, LF0), ('CRLF', '\r\n\r\n', CR, CR0)):
    for trail in ('', '\n'):
        for i in range(273):
            for j in range(i+1, 273):
                P = list(orig); P[i] = mod[i]; P[j] = mod[j]
                body = sep.join(P) + trail
                h = hashlib.md5(body.encode()).hexdigest()
                n += 1
                for idx in (0, 1):
                    a = derive(h, idx)
                    if a in (NEW, OLD):
                        print("*** MATCH", join_name, repr(trail), '¶%d,¶%d' % (i+1, j+1), 'idx', idx, a, h, flush=True)
        print("  done", join_name, repr(trail), "cumulative", n, flush=True)
print("finished", n, flush=True)
