"""Sentence-unit class family: the unit of marking is the sentence, not the paragraph.

Every sweep in this hunt marks PARAGRAPHS: the certified stage-one mechanic lowers a
paragraph's first alphabetic and raises its last.  The author's own format demo
(cleczc, "Grycoin Block 2") marks something else: he says the answer changes "the 'I'
at the beginning of the previous paragraph" to "i" AND "himself" to "himselF", and
"himself" sits at a SENTENCE end in the middle of that paragraph.  A mark inside a
paragraph cannot come from a paragraph-edge rule.

So the unit is a sentence, and the class rule that is closed at paragraph granularity
(n_every subset of the 21 paragraph-initial letters) has never been hashed at sentence
granularity.  This lane enumerates it: for every subset of the 22 letters the chapter's
sentences actually start with, mark every sentence whose initial is outside the subset,
lower its first alphabetic, raise its last.

Each paragraph is rebuilt from its own sentences and their own separators, so with the
empty mask the document is byte-identical to the certified base.  The gate proves that
against all three certified digests before anything is derived.
"""
import hashlib, re, time

import rtl_ci as R

CERT = R.CERT
SEPS = re.compile(r'(?<=[.!?])[ \n]+')

P = R.load()


def parse():
    """[(para_index, sentence_text, separator_after)] preserving every byte."""
    out = []
    for pi, p in enumerate(P):
        last = 0
        for m in SEPS.finditer(p):
            out.append([pi, p[last:m.start()], m.group(0)])
            last = m.end()
        out.append([pi, p[last:], ""])
    return out


SENT = parse()
N = len(SENT)
NORM = [s[1] for s in SENT]


def flips(t):
    a = [i for i, c in enumerate(t) if c.isalpha()]
    if not a:
        return t
    c = list(t)
    c[a[0]] = c[a[0]].lower()
    c[a[-1]] = c[a[-1]].upper()
    return "".join(c)


FLIP = [flips(t) for t in NORM]
HEAD = [next((c.upper() for c in t if c.isalpha()), None) for t in NORM]
LET = sorted({h for h in HEAD if h})
BIT = [LET.index(h) if h else None for h in HEAD]
NMASK = 1 << len(LET)


def build(mask, sep):
    """sep is a str: "\n\n" or "\r\n\r\n"."""
    parts = []
    for k in range(N):
        pi = SENT[k][0]
        parts.append(FLIP[k] if (BIT[k] is not None and not (mask >> BIT[k]) & 1) else NORM[k])
        parts.append(SENT[k][2])
        if k + 1 < N and SENT[k + 1][0] != pi:
            parts.append(sep)
    return "".join(parts)


def gate():
    for sep, want in CERT.items():
        got = hashlib.md5(sep.join(p.encode() for p in P)).hexdigest()
        assert got == want, ("base drift", sep, got, want)
    # A mask bit means "member of the class"; a sentence is marked when its initial is
    # NOT in the class, so the identity document is the all-members mask NMASK-1.
    for mask in (NMASK - 1, NMASK - 2, 0, (NMASK * 5) // 7):
        for sep in ("\n\n", "\r\n\r\n"):
            got = hashlib.md5(build(mask, sep).encode()).hexdigest()
            if mask == NMASK - 1:
                assert got == CERT[sep.encode()], ("identity-mask drift", sep, got)
        # construction equality: the same document built two independent ways
        assert build(mask, "\r\n\r\n") == "".join(
            (FLIP[k] if (BIT[k] is not None and not (mask >> BIT[k]) & 1) else NORM[k]) + SENT[k][2]
            + ("\r\n\r\n" if (k + 1 < N and SENT[k + 1][0] != SENT[k][0]) else "")
            for k in range(N)), "sentence construction mismatch at mask %d" % mask
    print("gate OK [SENT]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) "
          "reproduced; identity mask byte-identical to both certified joins; %d sentences, "
          "%d initial letters %s; targets %s"
          % (N, len(LET), "".join(LET), "+".join(R.TARGETS.values())), flush=True)


gate()


def run(start, end, join, idxs):
    sep = "\r\n\r\n" if join == "crlf" else "\n\n"
    hi = min(end, NMASK)
    if start >= NMASK:
        print("DONE sent %s %d..%d n=0 (space is 2^%d)" % (join, start, end, len(LET)), flush=True)
        return
    print("axes sentences=%d letters=%s join=%r indices=%s masks=%d"
          % (N, "".join(LET), sep.encode(), idxs, NMASK), flush=True)
    t0 = time.time(); n = 0; hits = 0
    for mask in range(start, hi):
        body = build(mask, sep).encode()
        d = hashlib.md5(body).hexdigest()
        n += 1
        for ix in idxs:
            a = R.addr(d, ix)
            if a in R.TARGETS:
                hits += 1
                print("***HIT sent mask=%d join=%s idx=%d md5=%s escrow=%s"
                      % (mask, join, ix, d, R.TARGETS[a]), flush=True)
                open("HIT_SENT_%s_%d_%d.txt" % (join, mask, ix), "wb").write(body)
        if n % 20000 == 0:
            print("n=%d mask=%d rate=%.0f/s" % (n, mask, n / (time.time() - t0)), flush=True)
    print("DONE sent %s %d..%d n=%d hits=%d in %ds"
          % (join, start, hi, n, hits, time.time() - t0), flush=True)
