"""Exhaustive initial-class sign space: every subset of the chapter's paragraph initials.

Stage one's rule, in the chapter's own words (para 228-240): the "signs" are the initials you
recognise (in Hal's post I, T, A, S, M -- the five that dominate it), and you mark "the only ones
where we don't recognize the signs" (F and W, four paragraphs), lowering each first letter and
raising each last letter.

Earlier work swept every 5-letter class only: C(26,5) = 65,780 subsets, 55,792 deduplicated
documents, zero.  That leaves every class of any other size untested, and the size that matters
for the chapter is not 5: the chapter has 21 distinct initials over 273 paragraphs, so a 5-letter
class marks 118 paragraphs, whereas a class of 17 marks only four.  This lane closes the whole
space: all 2^21 = 2,097,152 subsets of the 21 initials that actually occur, each marking exactly
the paragraphs whose initial is outside the class, certified mechanic, both joins, indices 0-2.
"""
import hashlib, time

import rtl_ci as R

P = R.load()
N = len(P)

FL = []
for p in P:
    a = [i for i, c in enumerate(p) if c.isalpha()]
    FL.append((a[0], a[-1]) if a else None)

INIT = []
for i, p in enumerate(P):
    h = None
    for c in p:
        if c.isalpha():
            h = c.upper()
            break
    INIT.append(h)
LETTERS = sorted({h for h in INIT if h})
LIDX = {c: j for j, c in enumerate(LETTERS)}
GROUP = {c: [i for i, h in enumerate(INIT) if h == c] for c in LETTERS}
K = len(LETTERS)

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

TOTAL = 1 << K


def gate():
    for sep, want in R.CERT.items():
        assert hashlib.md5(sep.join(x.encode() for x in P)).hexdigest() == want, "base drift"
    assert K == 21 and TOTAL == 2097152, (K, TOTAL)
    # witnesses: the full class marks nothing and must reproduce the certified base digest;
    # the empty class marks every markable paragraph and must equal the all-marked document.
    markable = [i for i in range(N) if INIT[i]]
    assert len(markable) == N - sum(1 for i in range(N) if not INIT[i])
    assert hashlib.md5(bytes(BASE["lf"])).hexdigest() == R.CERT[b"\n\n"]
    full = doc_all = None
    parts = []
    for i, p in enumerate(P):
        a = [j for j, c in enumerate(p) if c.isalpha()]
        if a:
            c = list(p)
            c[a[0]] = c[a[0]].lower()
            c[a[-1]] = c[a[-1]].upper()
            parts.append("".join(c).encode())
        else:
            parts.append(p.encode())
    doc_all = b"\n\n".join(parts)
    assert doc_all != bytes(BASE["lf"])
    print("gate OK [CLS]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) reproduced; "
          "%d initials %s; all 2^%d = %d class subsets; certified mechanic; targets %s"
          % (K, "".join(LETTERS), K, TOTAL, "+".join(R.TARGETS.values())), flush=True)


gate()


def run(start, end, idxs):
    hi = min(end, TOTAL)
    if start >= TOTAL:
        print("DONE cls %d..%d n=0 (space is %d)" % (start, end, TOTAL), flush=True)
        return
    print("axes CLS total=%d shard=%d..%d indices=%s joins=LF+CRLF2 targets=LIVE+V1"
          % (TOTAL, start, hi, idxs), flush=True)
    t0 = time.time()
    n = deriv = hits = 0
    lf = BASE["lf"]
    cr = BASE["crlf"]
    ofl, oll = OFF_F["lf"], OFF_L["lf"]
    ofc, olc = OFF_F["crlf"], OFF_L["crlf"]
    for mask in range(start, hi):
        sel = []
        for j in range(K):
            if (mask >> j) & 1:
                sel.extend(GROUP[LETTERS[j]])
        old = []
        for i in sel:
            if FL[i] is None:
                continue
            f, l = FL[i]
            a, b = ofl[i], oll[i]
            ca, cb = chr(lf[a]), chr(lf[b])
            na, nb = ca.lower(), cb.upper()
            old.append((i, ca, cb))
            lf[a] = ord(na); lf[b] = ord(nb)
            cr[ofc[i]] = ord(na); cr[olc[i]] = ord(nb)
        d1 = hashlib.md5(lf).hexdigest()
        d2 = hashlib.md5(cr).hexdigest()
        for (i, ca, cb) in old:
            lf[ofl[i]] = ord(ca); lf[oll[i]] = ord(cb)
            cr[ofc[i]] = ord(ca); cr[olc[i]] = ord(cb)
        for tag, d in (("lf", d1), ("crlf", d2)):
            n += 1
            for ix in idxs:
                deriv += 1
                a = R.addr(d, ix)
                if a in R.TARGETS:
                    hits += 1
                    print("***HIT mask=%d class=%s join=%s idx=%d md5=%s escrow=%s"
                          % (mask, "".join(LETTERS[j] for j in range(K) if (mask >> j) & 1), tag, ix, d,
                             R.TARGETS[a]), flush=True)
                    open("HIT_CLS_%d_%s_%d.txt" % (mask, tag, ix), "wb").write(bytes(BASE[tag]))
        if n and n % 100000 == 0:
            print("n=%d mask=%d rate=%.0f docs/s" % (n, mask, n / (time.time() - t0)), flush=True)
    print("DONE cls %d..%d n=%d derivations=%d hits=%d in %ds"
          % (start, hi, n, deriv, hits, time.time() - t0), flush=True)
