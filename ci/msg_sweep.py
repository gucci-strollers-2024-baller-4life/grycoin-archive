"""Message-first inversion: the raised tails spell a word, and the selection follows.

Every sweep in this hunt enumerates SELECTIONS and reads off whatever message they spell.
The certified stage-one preimage shows the device the other way round: the four marked
paragraphs of Hal's post have firsts f f w w and lasts S T N M, and the chapter reads that
as "the last letter of each of these" spelling a signature (para 236-240).  So the message
is the input and the selection is derived from it: pick, in reading order, one paragraph per
letter of the message whose final letter IS that letter, apply the certified mechanic to
exactly those paragraphs, and hash.

The message must therefore be spellable from the chapter's 19 tail letters
(S E N T M Y R G D L W K I H P O F C, plus one paragraph with no letter).  That rules out
every message containing A, B, J, Q, U, V, X or Z, which is why FINNEY, SATOSHI, NAKAMOTO,
HALFINNEY and YANG all have zero embeddings here: they cannot be spelled at this unit at all.
The vocabulary of the chapter itself is the natural message list (block 2's message, YANG, was
a name from its own text; block 29's was two letters inside its own word "voice"), and it is
taken with length 2..6 so the short signature-style messages are covered first.

Documents are sharded by contiguous ordinal over the whole (message, embedding) space, both
certified joins are hashed for each, and every candidate is derived at the requested indices
against both escrows.
"""
import bisect, hashlib, os, re, time

import rtl_ci as R

MAXLEN = int(os.environ.get("MSG_MAXLEN", "6"))
EXTRA = ["STNM", "STNME", "NMST", "FFWW", "UUUU", "TOMI", "SIGNS", "SIGN", "MYSTERY", "ST"]

P = R.load()
N = len(P)
FIRST = []
LAST = []
for p in P:
    a = [i for i, c in enumerate(p) if c.isalpha()]
    FIRST.append(a[0] if a else None)
    LAST.append(a[-1] if a else None)
TAIL = [P[i][LAST[i]].upper() if LAST[i] is not None else None for i in range(N)]
# MSG_UNIT=HEAD reads the message from paragraph heads instead of tails. Stage one's lowered heads
# spelled FFWW as a dedication message (para 241), so the head sequence is a message carrier too.
if os.environ.get("MSG_UNIT") == "HEAD":
    TAIL = [P[i][FIRST[i]].upper() if FIRST[i] is not None else None for i in range(N)]
ALPHA = sorted({c for c in TAIL if c})
POS = {c: [i for i in range(N) if TAIL[i] == c] for c in ALPHA}

vocab = set()
for p in P:
    for w in re.findall(r"[A-Za-z]+", p):
        vocab.add(w.upper())
vocab |= set(EXTRA)
# MSG_SET=SIG restricts the message list to the chapter's own signature strings.  Para 239 writes
# the reading as "I STNM" and para 240 calls the tails "the same signature" as the genesis block,
# so the candidate messages are the I-prefixed variants of the certified four-letter tail string.
SIG = ["ISTNM", "ISTN", "ISTNMI", "ISTNMS", "ISTNME", "ISTNMST",
       "STNMI", "STNMS", "STNMST", "NMS", "TNMS", "NMST"]
if os.environ.get("MSG_SET") == "SIG":
    vocab = set(SIG)
MSGS = [w for w in vocab if 2 <= len(w) <= max(MAXLEN, 6) and set(w) <= set(ALPHA)]
MSGS.sort(key=lambda w: (len(w), w))


def emb_count(msg):
    k = len(msg)
    nxt = None
    for i in range(k - 1, -1, -1):
        arr = [0] * (N + 2)
        for p in range(N - 1, -1, -1):
            c = (1 if i == k - 1 else nxt[p + 1]) if TAIL[p] == msg[i] else 0
            arr[p] = c + arr[p + 1]
        nxt = arr
    return nxt[0]


def emb_table(msg):
    k = len(msg)
    C = [None] * k
    for i in range(k - 1, -1, -1):
        arr = [0] * (N + 2)
        for p in range(N - 1, -1, -1):
            c = (1 if i == k - 1 else C[i + 1][p + 1]) if TAIL[p] == msg[i] else 0
            arr[p] = c + arr[p + 1]
        C[i] = arr
    return C


COUNT = [emb_count(m) for m in MSGS]
CUM = []
acc = 0
for c in COUNT:
    acc += c
    CUM.append(acc)
TOTAL = acc


def unrank(msg, C, ordinal):
    out = []
    cur = 0
    k = len(msg)
    for i in range(k):
        placed = False
        for p in POS[msg[i]]:
            if p < cur:
                continue
            block = 1 if i == k - 1 else C[i + 1][p + 1]
            if block == 0:
                continue
            if ordinal < block:
                out.append(p)
                cur = p + 1
                placed = True
                break
            ordinal -= block
        if not placed:
            raise AssertionError("unrank exhausted %s" % msg)
    return out


def build(sel, sep):
    parts = []
    for i, p in enumerate(P):
        if i in sel:
            c = list(p)
            c[FIRST[i]] = c[FIRST[i]].lower()
            c[LAST[i]] = c[LAST[i]].upper()
            parts.append("".join(c).encode())
        else:
            parts.append(p.encode())
    return sep.join(parts)


def gate():
    for sep, want in R.CERT.items():
        assert hashlib.md5(sep.join(x.encode() for x in P)).hexdigest() == want, "base drift"
    assert TOTAL > 0
    # construction: the certified stage-one reading, applied to the four Finney-window paragraphs
    for probe in (0, TOTAL // 3, TOTAL - 1):
        j = bisect.bisect_right(CUM, probe)
        prev = 0 if j == 0 else CUM[j - 1]
        msg = MSGS[j]
        C = emb_table(msg)
        emb = unrank(msg, C, probe - prev)
        assert len(emb) == len(msg) and all(emb[k] < emb[k + 1] for k in range(len(emb) - 1)), (msg, emb)
        assert all(TAIL[p] == msg[k] for k, p in enumerate(emb)), (msg, emb)
        sel = set(emb)
        for sep in (b"\n\n", b"\r\n\r\n"):
            doc = build(sel, sep)
            ref = sep.join(
                (lambda c: "".join(c).encode())(_flip(P[i], FIRST[i], LAST[i])) if i in sel else P[i].encode()
                for i in range(N))
            assert doc == ref, "construction mismatch"
    print("gate OK [%s]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) reproduced; "
          "construction verified at 3 probes; %d messages len 2..%d; %d in-order embeddings; "
          "%s alphabet %s; targets %s"
          % (os.environ.get("MSG_UNIT", "TAIL"), len(MSGS), MAXLEN, TOTAL, os.environ.get("MSG_UNIT", "TAIL").lower(),
             "".join(ALPHA), "+".join(R.TARGETS.values())), flush=True)


def _flip(p, f, l):
    c = list(p)
    c[f] = c[f].lower()
    c[l] = c[l].upper()
    return c


gate()


def run(start, end, idxs):
    hi = min(end, TOTAL)
    if start >= TOTAL:
        print("DONE msg %d..%d n=0 (space is %d)" % (start, end, TOTAL), flush=True)
        return
    print("axes MSG total=%d shard=%d..%d indices=%s joins=LF+CRLF2 targets=LIVE+V1"
          % (TOTAL, start, hi, idxs), flush=True)
    t0 = time.time()
    n = 0
    deriv = 0
    hits = 0
    cur_j = None
    C = None
    msg = None
    prev = 0
    for ordinal in range(start, hi):
        j = bisect.bisect_right(CUM, ordinal)
        if j != cur_j:
            cur_j = j
            msg = MSGS[j]
            C = emb_table(msg)
            prev = 0 if j == 0 else CUM[j - 1]
        emb = unrank(msg, C, ordinal - prev)
        sel = set(emb)
        for tag, sep in (("lf", b"\n\n"), ("crlf", b"\r\n\r\n")):
            body = build(sel, sep)
            d = hashlib.md5(body).hexdigest()
            n += 1
            for ix in idxs:
                deriv += 1
                a = R.addr(d, ix)
                if a in R.TARGETS:
                    hits += 1
                    print("***HIT msg=%s emb=%s join=%s idx=%d md5=%s escrow=%s"
                          % (msg, emb, tag, ix, d, R.TARGETS[a]), flush=True)
                    open("HIT_MSG_%s_%d_%s_%d.txt" % (msg, ordinal, tag, ix), "wb").write(body)
        if n % 100000 == 0:
            print("n=%d ordinal=%d msg=%s rate=%.0f/s" % (n, ordinal, msg, n / (time.time() - t0)), flush=True)
    print("DONE msg %d..%d n=%d derivations=%d hits=%d in %ds"
          % (start, hi, n, deriv, hits, time.time() - t0), flush=True)
