"""Sentence-unit families: the unit of marking is the sentence, not the paragraph.

Every sweep before this one marks PARAGRAPHS: the certified stage-one mechanic lowers a
paragraph's first alphabetic and raises its last.  The author's own format demo
(cleczc, "Grycoin Block 2") marks something else.  He says the answer changes "the 'I'
at the beginning of the previous paragraph" to "i" AND "himself" to "himselF", and in
the text he actually posted "himself" sits at a SENTENCE end inside that paragraph
("...outing himself. Even after I explained the method used and the result in detail.").
No paragraph-edge rule can produce that mark, so the unit of marking was never
controlled by anything in this hunt.

The chapter parses into 670 sentences with 22 distinct initials and 21 distinct finals.
Each family below enumerates one complete class space at sentence granularity:

  token   select by                 mutate              masks
  SENT    sentence initial letter   both ends           2^22
  SENTT   sentence final letter     both ends           2^21
  SENTA   sentence initial letter   last letter only    2^22
  SENTB   sentence initial letter   first letter only   2^22
  SENTC   sentence final letter     last letter only    2^21
  SENTD   sentence final letter     first letter only   2^21

A mask bit means "member of the class"; a sentence is marked when its selector letter is
NOT in the class, which is the certified polarity read backwards.  Each paragraph is
rebuilt from its own sentences and their own separators, so the all-members mask
reproduces the certified base byte for byte.  The gate proves that against the three
certified digests and against an independent per-sentence rebuild before deriving.
"""
import hashlib, os, re, time

import rtl_ci as R

CERT = R.CERT
SEPS = re.compile(r'(?<=[.!?])[ \n]+')
P = R.load()

CONFIG = {
    "SENT":  ("head", "both"),
    "SENTT": ("tail", "both"),
    "SENTA": ("head", "tail"),
    "SENTB": ("head", "head"),
    "SENTC": ("tail", "tail"),
    "SENTD": ("tail", "head"),
}
TOKEN = os.environ.get("RTL_SUFFIX", "SENT")
SELECT, MUTATE = CONFIG.get(TOKEN, CONFIG["SENT"])


def parse():
    """[[paragraph_index, sentence_text, separator_after], ...] preserving every byte."""
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


def _alpha(t):
    return [i for i, c in enumerate(t) if c.isalpha()]


def flip_both(t):
    a = _alpha(t)
    if not a:
        return t
    c = list(t)
    c[a[0]] = c[a[0]].lower()
    c[a[-1]] = c[a[-1]].upper()
    return "".join(c)


def flip_head(t):
    a = _alpha(t)
    if not a:
        return t
    c = list(t)
    c[a[0]] = c[a[0]].lower()
    return "".join(c)


def flip_tail(t):
    a = _alpha(t)
    if not a:
        return t
    c = list(t)
    c[a[-1]] = c[a[-1]].upper()
    return "".join(c)


FLIPPER = {"both": flip_both, "head": flip_head, "tail": flip_tail}
FLIP = [FLIPPER[MUTATE](t) for t in NORM]

HEAD = [next((c.upper() for c in t if c.isalpha()), None) for t in NORM]
TAIL = [next((c.upper() for c in reversed(t) if c.isalpha()), None) for t in NORM]
SEL = HEAD if SELECT == "head" else TAIL
LET = sorted({c for c in SEL if c})
BIT = [LET.index(c) if c else None for c in SEL]
NMASK = 1 << len(LET)


def build(mask, sep):
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
    for mask in (NMASK - 1, NMASK - 2, 0, (NMASK * 5) // 7):
        for sep in ("\n\n", "\r\n\r\n"):
            got = hashlib.md5(build(mask, sep).encode()).hexdigest()
            if mask == NMASK - 1:
                assert got == CERT[sep.encode()], ("identity-mask drift", sep, got, CERT[sep.encode()])
        f = FLIPPER[MUTATE]
        assert build(mask, "\r\n\r\n") == "".join(
            (f(SENT[k][1]) if (BIT[k] is not None and not (mask >> BIT[k]) & 1) else SENT[k][1])
            + SENT[k][2]
            + ("\r\n\r\n" if (k + 1 < N and SENT[k + 1][0] != SENT[k][0]) else "")
            for k in range(N)), "sentence construction mismatch at mask %d" % mask
    print("gate OK [%s]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) reproduced; "
          "all-members mask byte-identical to both certified joins; %d sentences; "
          "select=%s(%d axes %s) mutate=%s; targets %s"
          % (TOKEN, N, SELECT, len(LET), "".join(LET), MUTATE, "+".join(R.TARGETS.values())),
          flush=True)


gate()


def run(start, end, join, idxs):
    sep = "\r\n\r\n" if join == "crlf" else "\n\n"
    hi = min(end, NMASK)
    if start >= NMASK:
        print("DONE %s %s %d..%d n=0 (space is 2^%d)" % (TOKEN, join, start, end, len(LET)), flush=True)
        return
    print("axes %s sentences=%d select=%s letters=%s join=%r indices=%s masks=%d mutate=%s"
          % (TOKEN, N, SELECT, "".join(LET), sep.encode(), idxs, NMASK, MUTATE), flush=True)
    t0 = time.time(); n = 0; hits = 0
    for mask in range(start, hi):
        body = build(mask, sep).encode()
        d = hashlib.md5(body).hexdigest()
        n += 1
        for ix in idxs:
            a = R.addr(d, ix)
            if a in R.TARGETS:
                hits += 1
                print("***HIT %s mask=%d join=%s idx=%d md5=%s escrow=%s"
                      % (TOKEN, mask, join, ix, d, R.TARGETS[a]), flush=True)
                open("HIT_%s_%s_%d_%d.txt" % (TOKEN, join, mask, ix), "wb").write(body)
        if n % 20000 == 0:
            print("n=%d mask=%d rate=%.0f/s" % (n, mask, n / (time.time() - t0)), flush=True)
    print("DONE %s %s %d..%d n=%d hits=%d in %ds" % (TOKEN, join, start, hi, n, hits, time.time() - t0), flush=True)
