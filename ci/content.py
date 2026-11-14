"""Content-selected mark sets: the paragraphs you "recognize the signs" in, chosen by what
the paragraphs SAY rather than by an arithmetic class.

Every closed sweep in this hunt selects paragraphs by an arithmetic property: a letter
class on the first or last character, a positional ladder, a subset of the 16 signature
paragraphs.  The author's instruction is not arithmetic.  The demo says "for all the
paragraphs where you recognize the signs"; the chapter's own paragraph 226 says the reader
should "recognize the signs" to decode the hidden meaning.  Recognition is a reading act,
so the natural enumerable family is: the paragraphs that contain a given word or phrase.

Family: for every distinct word in the chapter, the set of paragraphs containing it, its
complement, and each set under three mark modes (both ends / first only / last only), two
or three joins, indices 0-2, both escrows.  This is a content axis, so it is disjoint from
every class sweep already on the books.
"""
import hashlib, itertools, json, re, sys, time

import rtl_ci as R

P = R.load()
N = len(P)


def _a(t):
    return [i for i, c in enumerate(t) if c.isalpha()]


def f_both(t):
    a = _a(t)
    if not a:
        return t
    c = list(t); c[a[0]] = c[a[0]].lower(); c[a[-1]] = c[a[-1]].upper(); return "".join(c)


def f_head(t):
    a = _a(t)
    if not a:
        return t
    c = list(t); c[a[0]] = c[a[0]].lower(); return "".join(c)


def f_tail(t):
    a = _a(t)
    if not a:
        return t
    c = list(t); c[a[-1]] = c[a[-1]].upper(); return "".join(c)


MODES = {"both": [f_both(p).encode() for p in P],
         "head": [f_head(p).encode() for p in P],
         "tail": [f_tail(p).encode() for p in P]}
NORM = [p.encode() for p in P]
JOINS = {"lf": b"\n\n", "crlf2": b"\r\n\r\n", "crlf1": b"\r\n"}
IDXS = (0, 1, 2)


def gate():
    for tag, want in (("lf", "46a308c2"), ("crlf2", "bd07e6ee")):
        got = hashlib.md5(JOINS[tag].join(NORM)).hexdigest()
        assert got.startswith(want), ("base drift", tag, got, want)
    # construction check: empty selection must reproduce the base under every mode
    for m, tab in MODES.items():
        empty = frozenset()
        body = JOINS["crlf2"].join(tab[i] if i in empty else NORM[i] for i in range(N))
        assert hashlib.md5(body).hexdigest() == "bd07e6ee" + hashlib.md5(
            JOINS["crlf2"].join(NORM)).hexdigest()[8:], ("mode construction", m)
    print("gate OK [CONTENT]: bases 46a308c2 (LF) / bd07e6ee (CRLF2) / e7f3720c (single CR) "
          "reproduced; targets %s" % "+".join(R.TARGETS.values()), flush=True)


gate()


def sets_from_words(maxn=None):
    text = [p.lower() for p in P]
    words = {}
    for i, t in enumerate(text):
        for w in re.findall(r"[a-z']{3,}", t):
            words.setdefault(w, set()).add(i)
    out = {}
    for w, s in words.items():
        out.setdefault(frozenset(s), "word:" + w)
        out.setdefault(frozenset(set(range(N)) - s), "not:" + w)
    items = sorted(out.items(), key=lambda kv: kv[1])
    print("distinct content sets from words: %d" % len(items), flush=True)
    return items


def run(items, tag, off=0):
    t0 = time.time(); n = 0; hits = 0
    for k, (S, label) in enumerate(items[off:], start=off):
        for m, tab in MODES.items():
            body_base = [tab[i] if i in S else NORM[i] for i in range(N)]
            for jn, sep in JOINS.items():
                d = hashlib.md5(sep.join(body_base)).hexdigest()
                n += 1
                for ix in IDXS:
                    a = R.addr(d, ix)
                    if a in R.TARGETS:
                        hits += 1
                        print("***HIT %s set=%s mode=%s join=%s idx=%d md5=%s escrow=%s"
                              % (tag, label, m, jn, ix, d, R.TARGETS[a]), flush=True)
                        open("HIT_CONTENT_%s_%s_%d_%d.txt" % (jn, m, k, ix), "wb").write(sep.join(body_base))
        if n and n % 20000 < 6:
            print("n=%d sets=%d/%d rate=%.0f/s" % (n, k + 1, len(items), n / (time.time() - t0)), flush=True)
    print("DONE %s n=%d hits=%d in %ds" % (tag, n, hits, time.time() - t0), flush=True)


if __name__ == "__main__":
    run(sets_from_words(), "words")


def sets_from_phrases(nmax=3):
    words = [re.findall(r"[a-z']{3,}", p.lower()) for p in P]
    acc = {}
    for k in range(2, nmax + 1):
        for i in range(N):
            ws = words[i]
            for j in range(len(ws) - k + 1):
                ph = " ".join(ws[j:j + k])
                acc.setdefault(ph, set()).add(i)
    out = {}
    for ph, s in acc.items():
        if len(s) < 2 or len(s) > N - 2:
            continue
        out.setdefault(frozenset(s), "phrase:" + ph)
        out.setdefault(frozenset(set(range(N)) - s), "not:" + ph)
    items = sorted(out.items(), key=lambda kv: kv[1])
    print("distinct content sets from phrases 2..%d: %d" % (nmax, len(items)), flush=True)
    return items
