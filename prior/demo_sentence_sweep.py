"""Demo (cleczc) sentence-level state sweep behind the author's 3c6 MD5 oracle.

Inner loop optimised: 10 precomputed paragraph variants per state, incremental MD5 over
the parts plus separator, prefix test on the first two digest bytes. No string join, no
hex conversion, no derivation unless the prefix matches.

States per paragraph (family A):
  0 unchanged
  1 first letter of the paragraph lowered
  2 last letter of the FIRST sentence raised
  3 first lowered + first-sentence-last raised
  4 last letter of EVERY sentence raised
Family B swaps in the last sentence and drops the paired state.

Every survivor of the 3c6 prefix is derived at m/44'/0'/0'/0/i, i in 0..77, and compared
with the demo escrow 1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi.
"""
import hashlib, re, time, sys

P = open("demo_base.txt", encoding="utf-8").read().rstrip("\n").split("\n\n")
assert len(P) == 10
DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
SEP = b"\r\n\r\n"
N = 10


def first_down(p):
    for j, c in enumerate(p):
        if c.isalpha():
            return p[:j] + c.lower() + p[j + 1:]
    return p


def raise_last_alpha(s):
    for j in range(len(s) - 1, -1, -1):
        if s[j].isalpha():
            return s[:j] + s[j].upper() + s[j + 1:]
    return s


def sents(p):
    return re.split(r"(?<=[.!?\u2026])\s+", p)


def variants(p):
    ss = sents(p)
    first = first_down(p)
    s1 = " ".join([raise_last_alpha(ss[0])] + ss[1:])
    s_last = " ".join(ss[:-1] + [raise_last_alpha(ss[-1])])
    all_s = " ".join(raise_last_alpha(x) for x in ss)
    return [p, first, s1, first_down(s1), all_s, s_last, first_down(all_s)]


V = [[v.encode() for v in variants(p)] for p in P]

FAMILIES = {
    "A": (0, 1, 2, 3, 4),
    "B": (0, 2, 5, 4, 6),
}


def run(family_name, states):
    idx = list(states)
    # per paragraph, the tuple of state-variant byte strings for this family
    T = [[V[i][s] for s in idx] for i in range(10)]
    v0, v1, v2, v3, v4, v5, v6, v7, v8, v9 = T
    n = 0
    surv = []
    t0 = time.time()
    h = hashlib.md5
    for i0 in range(5):
        p0 = v0[i0]
        for i1 in range(5):
            p1 = v1[i1]
            for i2 in range(5):
                p2 = v2[i2]
                for i3 in range(5):
                    p3 = v3[i3]
                    for i4 in range(5):
                        p4 = v4[i4]
                        for i5 in range(5):
                            p5 = v5[i5]
                            for i6 in range(5):
                                p6 = v6[i6]
                                for i7 in range(5):
                                    p7 = v7[i7]
                                    for i8 in range(5):
                                        p8 = v8[i8]
                                        for i9 in range(5):
                                            m = h()
                                            m.update(p0); m.update(SEP)
                                            m.update(p1); m.update(SEP)
                                            m.update(p2); m.update(SEP)
                                            m.update(p3); m.update(SEP)
                                            m.update(p4); m.update(SEP)
                                            m.update(p5); m.update(SEP)
                                            m.update(p6); m.update(SEP)
                                            m.update(p7); m.update(SEP)
                                            m.update(p8); m.update(SEP)
                                            m.update(v9[i9])
                                            d0 = m.digest()
                                            if d0[0] == 0x3C and d0[1] == 0x60:
                                                surv.append(((i0, i1, i2, i3, i4, i5, i6, i7, i8, i9), d0))
                                                n += 0
                                            n += 1
    el = time.time() - t0
    print(f"family {family_name}: candidates={n} rate={n/el:.0f}/s survivors={len(surv)} elapsed={el:.0f}s", flush=True)
    return surv


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    surv = run(which, FAMILIES[which])
    if surv:
        from rbb_probe import addr_at
        found = 0
        for combo, dig in surv:
            for k in range(78):
                if addr_at(dig, k) == DEMO:
                    print("*** DEMO MATCH ***", combo, dig.hex(), "idx", k, flush=True)
                    found += 1
        print(f"derived {len(surv)} survivors x 78 indices; matches={found}", flush=True)
