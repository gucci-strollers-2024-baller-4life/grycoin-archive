"""Name marking on the format demo, the block-2 / block-29 shape.

The author's own manual documents the device twice: round-one block 2 is "(family name
Yang)" - the hidden name's letters capitalised at their own occurrences, one occurrence
per letter, in reading order - and block 29 is "just change the o and i in 'voice' in the
second sentence to 'O' and 'I', same method as in Block 2. Only two letters changed."
So the mark set is a name spelled by turning ONE occurrence of each of its letters to
upper case, in order through the text.

This lane enumerates that space exhaustively on the demo (cleczc, "Grycoin Block 2"), the
only place the device can be calibrated, because the demo's answer is known to exist and
its escrow `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` was redeemed the day after funding. The
demo's small names are already closed (AOI 158,366 embeddings, and every name in
CLUES 13.3); the large ones never were. FINNEY is 92,104,718 in-order embeddings, THOMAS
177,058,903, GRYCOIN 123,560,985.

Ordinals are contiguous: the whole space is ranked lexicographically by the position
tuple, so shard k with space_bits b takes ordinals [k*2^b/20, (k+1)*2^b/20).

Derivations are the scarce resource, so a candidate is only derived when its md5 begins
`3c`, which is the published prefix `3c6` widened by one digit: the author documents
getting the last digit of a published prefix wrong (block 59), so `3c*` is the honest
oracle and `3c6` is counted separately in every shard line.
"""
import hashlib, os, time

import rtl_ci as R

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "prior", "demo_base.txt"))
DEMO_MD5 = "7759227d7406d8230d7e3a8f7b9846d7"
DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"

TOK = os.environ.get("RTL_SUFFIX", "NFINNEY")
NAME = TOK[1:].upper()

raw = open(BASE, "rb").read()
assert hashlib.md5(raw).hexdigest() == DEMO_MD5, "demo base drift"
assert len(raw) == len(raw.decode("utf-8")), "demo base is not ASCII"
assert raw.count(b"\n\n") == 9 and raw.count(b"\n") == 18, "demo base paragraph structure changed"
CRLF = raw.replace(b"\n\n", b"\r\n\r\n")

L = len(raw)
low = raw.lower()
POS = [i for i, ch in enumerate(NAME) for i in []]
POS = [[i for i in range(L) if low[i:i + 1] == NAME[k].lower().encode()] for k in range(len(NAME))]
K = len(NAME)


def build_tables():
    C = [None] * K
    for i in range(K - 1, -1, -1):
        arr = [0] * (L + 2)
        ps = set(POS[i])
        nxt = C[i + 1] if i + 1 < K else None
        for p in range(L, -1, -1):
            c = (1 if nxt is None else nxt[p + 1]) if p in ps else 0
            arr[p] = c + arr[p + 1]
        C[i] = arr
    return C


C = build_tables()
TOTAL = C[0][0]
STEPS = [[(p, (1 if i == K - 1 else C[i + 1][p + 1])) for p in POS[i]
          if (1 if i == K - 1 else C[i + 1][p + 1]) > 0] for i in range(K)]


def unrank(ordinal):
    out = []
    cur = 0
    for i in range(K):
        for p, block in STEPS[i]:
            if p < cur:
                continue
            if ordinal < block:
                out.append(p)
                cur = p + 1
                break
            ordinal -= block
        else:
            raise AssertionError("unrank exhausted at letter %d ordinal %d" % (i, ordinal))
    return out


def mark(positions):
    b = bytearray(raw)
    for p in positions:
        c = b[p]
        b[p] = c - 32 if 97 <= c <= 122 else c
    return bytes(b)


def describe(positions):
    """Containment report for a winning placement.

    A hit on cleczc only transfers to the chapter if the winning placement is tight: on
    45,450 bytes FINNEY has about 1e14 in-order embeddings, so only a placement that sits
    inside one sentence, one word, or one short adjacent span narrows the chapter's space
    to something enumerable. Printed with every hit so the transfer question is answerable
    from the log alone.
    """
    para = sum(1 for i in range(L) if raw[max(0, i - 1):i + 1] == b"\n\n")
    pb = [0]
    for i in range(L - 1):
        if raw[i:i + 2] == b"\n\n":
            pb.append(i + 2)
    def para_of(p):
        return max(k for k, st in enumerate(pb) if st <= p)
    import re as _re
    words = [(m.start(), m.end()) for m in _re.finditer(rb"[A-Za-z]+", raw)]
    sents = []
    start = 0
    for m in _re.finditer(rb"[.!?][ \n]+", raw):
        sents.append((start, m.start()))
        start = m.end()
    sents.append((start, L))
    wpar = set(para_of(p) for p in positions)
    wsp = set(k for p in positions for k, (a, b) in enumerate(words) if a <= p < b)
    wse = set(k for p in positions for k, (a, b) in enumerate(sents) if a <= p <= b)
    gaps = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
    return ("paragraphs=%d words=%d sentences=%d span=%d..%d spread=%d maxgap=%d all_one_word=%s "
            "all_one_sentence=%s" % (len(wpar), len(wsp), len(wse), positions[0], positions[-1],
                                     positions[-1] - positions[0], max(gaps),
                                     len(wsp) == 1, len(wse) == 1))


def gate():
    for probe in (0, 1, TOTAL // 3, TOTAL - 1, TOTAL // 2):
        pos = unrank(probe)
        assert len(pos) == K and all(pos[i] < pos[i + 1] for i in range(K - 1)), pos
        assert all(chr(raw[pos[i]]).upper() == NAME[i] for i in range(K)), (probe, pos)
        m = mark(pos)
        assert len(m) == L
        diff = [i for i in range(L) if m[i] != raw[i]]
        assert diff == [p for p in pos if raw[p] != m[p]]
        assert sum(1 for d in diff if not (97 <= raw[d] <= 122)) == 0
    print("gate OK [NAME %s]: demo base %s reproduced (%d bytes, 10 paragraphs); %d in-order "
          "embeddings; construction verified at 5 probes; filter md5[0:2]=='3c'; target %s"
          % (NAME, DEMO_MD5, L, TOTAL, DEMO), flush=True)


gate()


def run(start, end, idxs):
    hi = min(end, TOTAL)
    if start >= TOTAL:
        print("DONE name %s %d..%d n=0 (space is %d)" % (NAME, start, end, TOTAL), flush=True)
        return
    print("axes NAME=%s total=%d shard=%d..%d indices=%s filter=3c* targets=DEMO(1tzieUf)"
          % (NAME, TOTAL, start, hi, idxs), flush=True)
    t0 = time.time()
    n = 0
    p3c = 0
    p3c6 = 0
    deriv = 0
    hits = 0
    for ordinal in range(start, hi):
        body = mark(unrank(ordinal))
        for tag, text in (("lf", body), ("crlf", body.replace(b"\n\n", b"\r\n\r\n"))):
            d = hashlib.md5(text).hexdigest()
            n += 1
            if d[:2] != "3c":
                continue
            p3c += 1
            if d[:3] == "3c6":
                p3c6 += 1
            for ix in idxs:
                deriv += 1
                a = R.addr(d, ix)
                if a == DEMO:
                    hits += 1
                    print("***HIT name=%s ordinal=%d join=%s idx=%d md5=%s escrow=%s %s"
                          % (NAME, ordinal, tag, ix, d, DEMO, describe(unrank(ordinal))), flush=True)
                    open("HIT_NAME_%s_%d_%s_%d.txt" % (NAME, ordinal, tag, ix), "wb").write(text)
        if n % 200000 == 0:
            print("n=%d ordinal=%d pfx3c=%d pfx3c6=%d deriv=%d rate=%.0f/s"
                  % (n, ordinal, p3c, p3c6, deriv, n / (time.time() - t0)), flush=True)
    print("DONE name %s %d..%d n=%d pfx3c=%d pfx3c6=%d derivations=%d hits=%d in %ds"
          % (NAME, start, hi, n, p3c, p3c6, deriv, hits, time.time() - t0), flush=True)
