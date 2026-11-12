"""The demo checks so far all derived at index 0 only. The published oracle (3c6) is
index-independent, so a true demo preimage would still be missed if the author used a
different leaf. Re-derive every 3c6 hit at indices 1..3 against both escrows."""
import hashlib, hmac, sys
sys.path.insert(0, 'sweeps')
import polarity_flip as pf

DEMO_ESC = '1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi'
B77_ESC = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
H = pf.HARD

def addr(h, idx):
    I = hmac.new(b'Bitcoin seed', pf.seed(bytes.fromhex(h)), hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32], 'big'), I[32:]
    for x in (44 + H, 0 + H, 0 + H, 0, idx):
        k, c = pf.ckd(k, c, x)
    return pf.b58(b'\x00' + hashlib.new('ripemd160', hashlib.sha256(pf.pub(k)).digest()).digest())

rows = [l.split() for l in open(sys.argv[1]) if l.startswith('HIT')]
print("candidates:", len(rows), flush=True)
for n, r in enumerate(rows, 1):
    md5 = r[-1]
    for idx in (1, 2, 3):
        a = addr(md5, idx)
        if a in (DEMO_ESC, B77_ESC):
            print("*** PREIMAGE", r[1], md5, "index", idx, a, flush=True)
    if n % 500 == 0:
        print("  done", n, flush=True)
print("finished", len(rows), "candidates x indices 1-3", flush=True)
