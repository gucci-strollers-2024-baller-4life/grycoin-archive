"""Three mutation/selection pairs that no sweep in this hunt has ever covered.

Both certified lanes pin ONE pairing of selector and mutation:

  CLASS  2^21  select by paragraph initial   mutate BOTH ends (head lowered, tail raised)
  TAIL   2^18  select by paragraph final     mutate TAIL ONLY (last alpha raised)

Paragraph 236 licenses reading the two halves separately: "We are directed to look at
the last letter of each of these."  If the sign tells you WHICH paragraphs and a second
sentence tells you WHAT to touch, the pairing is free, and three pairings are open:

  L1  head-selected 2^21 + tail-only mutation
  L2  head-selected 2^21 + head-only mutation
  L3  tail-selected 2^18 + head-only mutation

Every candidate is compared against BOTH escrows.  The gate reproduces the three
certified base digests and proves each lane's construction byte-identical to a plain
per-paragraph rebuild at four probes before anything is derived.
"""
import hashlib, os, time

import rtl_ci as R

CERT = R.CERT
IDX_DEFAULT = (0, 1, 2)

P = R.load()
NORM = [p.encode() for p in P]


def flip_both(p):
    return R.flips(p)


def flip_tail(p):
    a = [i for i, c in enumerate(p) if c.isalpha()]
    if not a:
        return p
    c = list(p)
    c[a[-1]] = c[a[-1]].upper()
    return "".join(c)


def flip_head(p):
    a = [i for i, c in enumerate(p) if c.isalpha()]
    if not a:
        return p
    c = list(p)
    c[a[0]] = c[a[0]].lower()
    return "".join(c)


DEFS = {"both": flip_both, "tail": flip_tail, "head": flip_head}
BITS = {k: [f(p).encode() for p in P] for k, f in DEFS.items()}

HEAD = [next((c.upper() for c in p if c.isalpha()), None) for p in P]
TAIL = [next((c.upper() for c in reversed(p) if c.isalpha()), None) for p in P]
HLET = sorted({c for c in HEAD if c})
TLET = sorted({c for c in TAIL if c})
HBIT = [HLET.index(c) if c else None for c in HEAD]
TBIT = [TLET.index(c) if c else None for c in TAIL]

LANES = [("L1", "head", "tail", HBIT, len(HLET)),
         ("L2", "head", "head", HBIT, len(HLET)),
         ("L3", "tail", "head", TBIT, len(TLET))]


def gate():
    for sep, want in CERT.items():
        got = hashlib.md5(sep.join(NORM)).hexdigest()
        assert got == want, ("base drift", sep, got, want)
    for name, sel, mut, bits, nb in LANES:
        nm = 1 << nb
        probes = [0, 1, nm - 1, (nm * 7) // 11]
        for mask in probes:
            a = b"\r\n".join(BITS[mut][i] if (bits[i] is not None and not (mask >> bits[i]) & 1)
                             else NORM[i] for i in range(273))
            b = "\r\n".join(DEFS[mut](P[i]) if (bits[i] is not None and not (mask >> bits[i]) & 1)
                            else P[i] for i in range(273)).encode()
            assert a == b, "construction mismatch %s mask %d" % (name, mask)
    print("gate OK [GAPS]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) "
          "reproduced; three lanes construction byte-identical at 4 probes each; "
          "targets %s" % "+".join(R.TARGETS.values()), flush=True)
    print("lanes: " + "; ".join("%s select=%s(%d axes) mutate=%s" % (n, s, nb, m)
                                for n, s, m, b, nb in LANES), flush=True)


gate()


def run(start, end, join, idxs):
    sep = b"\r\n\r\n" if join == "crlf" else b"\n\n"
    for name, selname, mutname, bits, nb in LANES:
        nm = 1 << nb
        flip = BITS[mutname]
        hi = min(end, nm)
        if start >= nm:
            print("DONE %s %s %d..%d n=0 (space is 2^%d)" % (name, join, start, end, nb), flush=True)
            continue
        t0 = time.time(); n = 0; hits = 0
        for mask in range(start, hi):
            body = sep.join([flip[i] if (bits[i] is not None and not (mask >> bits[i]) & 1)
                             else NORM[i] for i in range(273)])
            d = hashlib.md5(body).hexdigest()
            n += 1
            for ix in idxs:
                a = R.addr(d, ix)
                if a in R.TARGETS:
                    hits += 1
                    print("***HIT lane=%s mask=%d join=%s idx=%d md5=%s escrow=%s"
                          % (name, mask, join, ix, d, R.TARGETS[a]), flush=True)
                    open("HIT_GAPS_%s_%s_%d_%d.txt" % (name, join, mask, ix), "wb").write(body)
            if n % 20000 == 0:
                print("%s n=%d mask=%d rate=%.0f/s" % (name, n, mask, n / (time.time() - t0)),
                      flush=True)
        print("DONE %s %s %d..%d n=%d hits=%d in %ds"
              % (name, join, start, hi, n, hits, time.time() - t0), flush=True)
