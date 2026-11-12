"""Chapter analogue of the certified Hal/Genesis 'Aa' polarity operation.

HAL_BOUNDARY certifies the operation as endpoint case inversion on the anomalous set:
F...s -> f...S, F...t -> f...T, W...n -> w...N, W...m -> w...M, internal prose untouched.

Applied here to the chapter's anomalous set (the four known windows), on the certified
base text (LF, paragraphs joined by \\n\\n, no trailing newline), derived at index 0.
"""
import json, hashlib, hmac, struct, sys
from coincurve import PrivateKey

HARD = 0x80000000
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
WL = [w.strip() for w in open('harness/bip39_english.txt') if w.strip()]


def mnemonic(ent):
    cs = hashlib.sha256(ent).digest()[0] >> 4
    n = int.from_bytes(ent, 'big') << 4 | cs
    tot = len(ent) * 8 // 11 + 1
    return ' '.join(WL[(n >> (11 * (tot - 1 - i))) & 0x7FF] for i in range(tot))


def seed(ent):
    return hashlib.pbkdf2_hmac('sha512', mnemonic(ent).encode(), b'mnemonic', 2048, 64)


def pub(k):
    return PrivateKey(k.to_bytes(32, 'big')).public_key.format(compressed=True)


def ckd(k, c, i):
    data = (b'\x00' + k.to_bytes(32, 'big') + struct.pack('>I', i)) if i >= HARD else (pub(k) + struct.pack('>I', i))
    I = hmac.new(c, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], 'big') + k) % N, I[32:]


def b58(payload):
    A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    x = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(x, 'big'); s = ''
    while n: n, r = divmod(n, 58); s = A[r] + s
    return '1' * (len(x) - len(x.lstrip(b'\x00'))) + s


def addr0(h):
    I = hmac.new(b'Bitcoin seed', seed(bytes.fromhex(h)), hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32], 'big'), I[32:]
    for i in (44 + HARD, 0 + HARD, 0 + HARD, 0, 0):
        k, c = ckd(k, c, i)
    p = pub(k)
    return b58(b'\x00' + hashlib.new('ripemd160', hashlib.sha256(p).digest()).digest())


def main():
    d = json.load(open('wp_paras_br.json'))
    P = [("\n".join(p) if isinstance(p, list) else p) for p in d]
    W = {'W1': [5, 6, 7, 8], 'W2': [93, 94, 95, 96], 'W3': [168, 169, 170, 171], 'W4': [231, 232, 233, 235]}
    TARGET = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
    all16 = [p for v in W.values() for p in v]
    Fs = [p for p in all16 if P[p - 1][0] in 'FW']
    Ws = [p for p in all16 if P[p - 1][0] in 'FW']
    Ft = [6, 94, 169, 232]

    def flip(sel, ini=True, fin=True, tag=''):
        Q = list(P)
        for p in sel:
            t = Q[p - 1]
            if ini and t[0].islower() is False:
                t = t[0].lower() + t[1:]
            if fin:
                idx = max(i for i, ch in enumerate(t) if ch.isalpha())
                t = t[:idx] + t[idx].upper() + t[idx + 1:]
            Q[p - 1] = t
        s = "\n\n".join(Q)
        h = hashlib.md5(s.encode()).hexdigest()
        a = addr0(h)
        ok = (a == TARGET)
        print(f"  {tag:38s} chars {len(s)}  md5 {h[:8]}…  idx0 {a}  {'*** MATCH' if ok else ''}")
        return ok

    print("target", TARGET)
    base = "\n\n".join(P)
    print(f"  {'unmodified base':38s} chars {len(base)}  md5 {hashlib.md5(base.encode()).hexdigest()[:8]}…  idx0 {addr0(hashlib.md5(base.encode()).hexdigest())}")
    hits = []
    for tag, sel, i, f in [
        ("all 16, both endpoints", all16, True, True),
        ("all 16, initials only", all16, True, False),
        ("all 16, finals only", all16, False, True),
        ("8 F-initial, both", [p for p in all16 if P[p-1][0] == 'F'], True, True),
        ("8 W-initial, both", [p for p in all16 if P[p-1][0] == 'W'], True, True),
        ("4 F...t, both", Ft, True, True),
        ("4 window openers, both", [v[0] for v in W.values()], True, True),
        ("4 window openers, initials", [v[0] for v in W.values()], True, False),
        ("4 F...t, finals only", Ft, False, True),
    ]:
        if flip(sel, i, f, tag): hits.append(tag)
    print("\nhits:", hits or "none")


if __name__ == '__main__':
    main()
