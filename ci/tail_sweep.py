"""Tail-only mutation family, selected by the paragraph's final letter.

The 2^18 tail-class sweep already running selects by last_alpha but mutates BOTH ends
(first alpha lowered, terminal alpha raised), i.e. the certified Stage One mechanic.
Paragraph 235 says only "look at the last letter of each of these", which licenses a
tail-only mutation as a separate reading: uppercase the final alphabetic character and
leave the head untouched. Nothing in this hunt has ever swept that.
"""
import hashlib, json, os

import rtl_ci as R

CERT = R.CERT


def flips_tail(p):
    a = [i for i, c in enumerate(p) if c.isalpha()]
    if not a:
        return p
    c = list(p)
    c[a[-1]] = c[a[-1]].upper()
    return "".join(c)


def gate(P):
    norm = [p.encode() for p in P]
    for sep, want in CERT.items():
        got = hashlib.md5(sep.join(norm)).hexdigest()
        assert got == want, ("base drift", sep, got, want)
    probes = [0, 1, (1 << 17), (1 << 18) - 1]
    for mask in probes:
        a = b"\r\n".join(TFLIP[i] if (TBIT[i] is not None and not (mask >> TBIT[i]) & 1)
                         else norm[i] for i in range(273))
        b = "\r\n".join(flips_tail(P[i]) if (TBIT[i] is not None and not (mask >> TBIT[i]) & 1)
                        else P[i] for i in range(273)).encode()
        assert a == b, "tail construction mismatch at mask %d" % mask
    print("targets %s" % "+".join(R.TARGETS.values()), flush=True)
    print("gate OK [TAIL]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) "
          "reproduced; construction byte-identical at %d probes; mutation tail-only "
          "(last_alpha.upper(), heads untouched); %d tail axes %s"
          % (len(probes), len(LET), "".join(LET)), flush=True)


P = R.load()
NORM = [p.encode() for p in P]
TFLIP = [flips_tail(p).encode() for p in P]
TAIL = [next((c.upper() for c in reversed(p) if c.isalpha()), None) for p in P]
LET = sorted({t for t in TAIL if t})
BIT = {c: k for k, c in enumerate(LET)}
TBIT = [BIT[t] if t else None for t in TAIL]
gate(P)


def run(start, end, join, idxs):
    sep = b"\r\n\r\n" if join == "crlf" else b"\n\n"
    nmasks = 1 << len(LET)
    hi = min(end, nmasks)
    hits = 0
    n = 0
    if start >= nmasks:
        print("DONE tail %s %d..%d n=0 derivations=0 hits=0 (space is 2^%d)"
              % (join, start, end, len(LET)), flush=True)
        return
    for mask in range(start, hi):
        body = sep.join([NORM[i] if (TBIT[i] is None or (mask >> TBIT[i]) & 1) else TFLIP[i]
                         for i in range(273)])
        d = hashlib.md5(body).hexdigest()
        n += 1
        for ix in idxs:
            a = R.addr(d, ix)
            if a in R.TARGETS:
                hits += 1
                print("***HIT mask=%d join=%s idx=%d md5=%s escrow=%s"
                      % (mask, join, ix, d, R.TARGETS[a]), flush=True)
                open("HIT_tail_%s_%d_%d.txt" % (join, mask, ix), "wb").write(body)
    print("DONE tail %s %d..%d n=%d derivations=%d hits=%d"
          % (join, start, hi, n, n * len(idxs), hits), flush=True)
