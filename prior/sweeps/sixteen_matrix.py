"""The 16-paragraph matrix: every 4-subset of the four FFWW/stnm windows, fully derived.

Universe (union of the four verified windows):
  W1 5,6,7,8   W2 93,94,95,96   W3 168,169,170,171   W4 231,232,233,235
C(16,4) = 1,820 quads, x 4 serialisations, every text hashed and fully derived.

Fast lane: BIP32 with coincurve (the C library the repo already runs elsewhere), which is
~100x the pure-python harness and takes the whole space to seconds. It is validated against
the certified stage-one pair before the sweep starts.
"""
import hashlib, hmac, itertools, json, os, struct, sys, time
import coincurve

ESCROW = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
IDX = (0, 1, 2, 5, 6, 7, 44, 76, 77)
H = 0x80000000
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
WINDOWS = {"W1": (5, 6, 7, 8), "W2": (93, 94, 95, 96),
           "W3": (168, 169, 170, 171), "W4": (231, 232, 233, 235)}
UNIVERSE = tuple(p - 1 for w in WINDOWS.values() for p in w)
HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = open(os.path.join(HERE, "..", "harness", "bip39_english.txt")).read().split()

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58check(payload):
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(payload + chk, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = B58[r] + s
    pad = len(payload + chk) - len((payload + chk).lstrip(b"\0"))
    return "1" * pad + s


def p2pkh(compressed_pub):
    h = hashlib.new("ripemd160", hashlib.sha256(compressed_pub).digest()).digest()
    return b58check(b"\x00" + h)


def pub(k):
    return coincurve.PublicKey.from_valid_secret(k.to_bytes(32, "big")).format(compressed=True)


def ckd(k, c, i):
    if i >= H:
        data = b"\x00" + k.to_bytes(32, "big") + struct.pack(">I", i)
    else:
        data = pub(k) + struct.pack(">I", i)
    I = hmac.new(c, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + k) % N, I[32:]


def mnemonic(ent):
    cs = hashlib.sha256(ent).digest()[0] >> 4
    n = int.from_bytes(ent, "big") << 4 | cs
    total = len(ent) * 8 // 11 + 1
    return " ".join(WORDS[(n >> (11 * (total - 1 - i))) & 0x7FF] for i in range(total))


def addrs(md5hex):
    seed = hashlib.pbkdf2_hmac("sha512", mnemonic(bytes.fromhex(md5hex)).encode(),
                               b"mnemonic", 2048, 64)
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32], "big"), I[32:]
    for d in (44 + H, 0 + H, 0 + H, 0):
        k, c = ckd(k, c, d)
    out = {}
    for i in IDX:
        ki, _ = ckd(k, c, i)
        out[i] = p2pkh(pub(ki))
    return out


def paragraphs():
    d = json.load(open(os.path.join(HERE, "..", "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    return [("\n".join(x) if isinstance(x, list) else x) for x in ps]


def last_alpha(s):
    return next((c for c in reversed(s) if c.isalpha()), "")


def mark(paras, quad):
    out = list(paras)
    for i in quad:
        p = out[i]
        a = next(j for j, ch in enumerate(p) if ch.isalpha())
        b = next(j for j in range(len(p) - 1, -1, -1) if p[j].isalpha())
        q = list(p)
        q[a] = p[a].lower()
        q[b] = p[b].upper()
        out[i] = "".join(q)
    return out


def serialisations(paras):
    for join, tag in ((b"\n\n", "LF"), (b"\r\n\r\n", "CRLF")):
        for trail in (False, True):
            yield join.join(p.encode() for p in paras) + (join if trail else b""), tag + ("+t" if trail else "")


def validate():
    got = addrs("9dd2efb9" + "0" * 24)[0] if False else None
    import sys as _s
    _s.path.insert(0, os.path.join(HERE, "..", "harness"))
    import btc as ref
    for h in ("9dd2efb9" + "0" * 24, "3c6" + "0" * 29):
        a, b = addrs(h), ref.addr_from_md5hex(h)
        assert a[0] == b, (h[:6], a[0], b)
    print("  fast lane == pure-python harness on two digests (incl. index 0 path)")


def main():
    validate()
    paras = paragraphs()
    assert len(paras) == 273, len(paras)
    for name, w in WINDOWS.items():
        ini = "".join(next(c for c in paras[i - 1] if c.isalpha()).upper() for i in w)
        fin = "".join(last_alpha(paras[i - 1]) for i in w)
        assert ini == "FFWW" and fin.lower() == "stnm", (name, ini, fin)
        print(f"  {name} ¶{w[0]}-{w[-1]}: {ini} / {fin}  certified")
    quads = list(itertools.combinations(UNIVERSE, 4))
    print(f"quads={len(quads)} texts={len(quads)*4} derivations={len(quads)*4*len(IDX)}")
    t0, n, hits = time.time(), 0, []
    for quad in quads:
        marked = mark(paras, quad)
        for blob, tag in serialisations(marked):
            n += 1
            h = hashlib.md5(blob).hexdigest()
            for i, a in addrs(h).items():
                if a == ESCROW:
                    hits.append((quad, tag, h, i))
        if n % 2000 == 0:
            el = time.time() - t0
            print(f"  {n} texts {el:.1f}s {n/el:.0f}/s", flush=True)
    print(f"texts={n} elapsed={time.time()-t0:.1f}s hits={len(hits)}")
    for x in hits:
        print("  HIT", x)


if __name__ == "__main__":
    main()
