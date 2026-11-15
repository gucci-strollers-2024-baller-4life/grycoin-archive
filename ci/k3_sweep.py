"""Exhaustive three-paragraph reading of "a couple of letters".

Sizes 1 and 2 at paragraph edges are already closed: every single paragraph and every
C(273,2) pair, on three substrates.  This lane takes the next cardinality.  Three selected
paragraphs marked with the certified mechanic (first alphabetic letter lowered, last raised,
exactly as the eight-flip certification on Hal's post behaves) is 8 case flips, which is the
smallest reading that can still be called "a couple" while carrying a three-letter message.

Ordinals are sharded over the C(N,3) combination space in lexicographic order.  Both certified
joins are hashed and every candidate is derived at the requested indices against both escrows.
"""
import hashlib, itertools, os, time

import rtl_ci as R

P = R.load()
N = len(P)

FL = []   # (first alpha char index, last alpha char index) per paragraph
for p in P:
    a = [i for i, c in enumerate(p) if c.isalpha()]
    FL.append((a[0], a[-1]) if a else None)

BASE = {}
OFF_F = {}
OFF_L = {}
for tag, sep in (("lf", b"\n\n"), ("crlf", b"\r\n\r\n")):
    parts = [p.encode() for p in P]
    BASE[tag] = bytearray(sep.join(parts))
    of = [0] * N
    ol = [0] * N
    start = 0
    for i, pb in enumerate(parts):
        if FL[i] is not None:
            f, l = FL[i]
            of[i] = start + len(P[i][:f].encode())
            ol[i] = start + len(P[i][:l + 1].encode()) - 1
        start += len(pb) + len(sep)
    OFF_F[tag] = of
    OFF_L[tag] = ol

TOTAL = N * (N - 1) * (N - 2) // 6
CUM = None


def marked_bytes(sel, tag):
    """Reference construction: rebuild the document with the three paragraphs marked."""
    out = []
    for i, p in enumerate(P):
        if i in sel:
            f, l = FL[i]
            c = list(p)
            c[f] = c[f].lower()
            c[l] = c[l].upper()
            out.append("".join(c).encode())
        else:
            out.append(p.encode())
    sep = b"\n\n" if tag == "lf" else b"\r\n\r\n"
    return sep.join(out)


def gate():
    for sep, want in R.CERT.items():
        assert hashlib.md5(sep.join(x.encode() for x in P)).hexdigest() == want, "base drift"
    assert TOTAL == len(list(itertools.combinations(range(N), 3))) if N <= 60 else TOTAL > 0
    probes = [(0, 1, 2), (10, 120, 200), (N - 3, N - 2, N - 1)]
    for sel in probes:
        for tag in ("lf", "crlf"):
            ref = marked_bytes(set(sel), tag)
            buf = BASE[tag][:]
            for i in sel:
                if FL[i] is None:
                    continue
                f, l = FL[i]
                buf[OFF_F[tag][i]] = ord(chr(buf[OFF_F[tag][i]]).lower())
                buf[OFF_L[tag][i]] = ord(chr(buf[OFF_L[tag][i]]).upper())
            assert bytes(buf) == ref, "construction mismatch %s %s" % (sel, tag)
    print("gate OK [K3]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) reproduced; "
          "construction byte-identical at 3 probes x 2 joins; %d paragraphs; C(%d,3)=%d selections; "
          "targets %s" % (N, N, TOTAL, "+".join(R.TARGETS.values())), flush=True)


gate()


def run(start, end, idxs):
    hi = min(end, TOTAL)
    if start >= TOTAL:
        print("DONE k3 %d..%d n=0 (space is %d)" % (start, end, TOTAL), flush=True)
        return
    print("axes K3 total=%d shard=%d..%d indices=%s joins=LF+CRLF2 targets=LIVE+V1"
          % (TOTAL, start, hi, idxs), flush=True)
    t0 = time.time()
    n = 0
    deriv = 0
    hits = 0
    lf = BASE["lf"]
    cr = BASE["crlf"]
    ofl, oll = OFF_F["lf"], OFF_L["lf"]
    ofc, olc = OFF_F["crlf"], OFF_L["crlf"]
    combos = itertools.islice(itertools.combinations(range(N), 3), start, hi)
    for sel in combos:
        i, j, k = sel
        pf = chr(lf[ofl[i]]).lower()
        pl = chr(lf[oll[i]]).upper()
        qf = chr(lf[ofl[j]]).lower()
        ql = chr(lf[oll[j]]).upper()
        rf = chr(lf[ofl[k]]).lower()
        rl = chr(lf[oll[k]]).upper()
        old = (chr(lf[ofl[i]]), chr(lf[oll[i]]), chr(lf[ofl[j]]), chr(lf[oll[j]]),
               chr(lf[ofl[k]]), chr(lf[oll[k]]))
        lf[ofl[i]] = ord(pf); lf[oll[i]] = ord(pl)
        lf[ofl[j]] = ord(qf); lf[oll[j]] = ord(ql)
        lf[ofl[k]] = ord(rf); lf[oll[k]] = ord(rl)
        cr[ofc[i]] = ord(pf); cr[olc[i]] = ord(pl)
        cr[ofc[j]] = ord(qf); cr[olc[j]] = ord(ql)
        cr[ofc[k]] = ord(rf); cr[olc[k]] = ord(rl)
        d1 = hashlib.md5(lf).hexdigest()
        d2 = hashlib.md5(cr).hexdigest()
        lf[ofl[i]] = ord(old[0]); lf[oll[i]] = ord(old[1])
        lf[ofl[j]] = ord(old[2]); lf[oll[j]] = ord(old[3])
        lf[ofl[k]] = ord(old[4]); lf[oll[k]] = ord(old[5])
        cr[ofc[i]] = ord(old[0]); cr[olc[i]] = ord(old[1])
        cr[ofc[j]] = ord(old[2]); cr[olc[j]] = ord(old[3])
        cr[ofc[k]] = ord(old[4]); cr[olc[k]] = ord(old[5])
        for tag, d in (("lf", d1), ("crlf", d2)):
            n += 1
            for ix in idxs:
                deriv += 1
                a = R.addr(d, ix)
                if a in R.TARGETS:
                    hits += 1
                    body = marked_bytes(set(sel), tag)
                    print("***HIT k3=%s join=%s idx=%d md5=%s escrow=%s"
                          % (sel, tag, ix, d, R.TARGETS[a]), flush=True)
                    open("HIT_K3_%d_%d_%d_%s_%d.txt" % (i, j, k, tag, ix), "wb").write(body)
        if n % 50000 == 0:
            print("n=%d at=%s rate=%.0f docs/s" % (n, sel, n / (time.time() - t0)), flush=True)
    print("DONE k3 %d..%d n=%d derivations=%d hits=%d in %ds"
          % (start, hi, n, deriv, hits, time.time() - t0), flush=True)
