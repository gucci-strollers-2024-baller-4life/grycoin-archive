"""Demo (cleczc) exhaustive-per-paragraph-state sweep, filtered by the author's 3c6 oracle.

Per paragraph the state set varies by family; states are:
  0 none
  1 first letter lowered
  2 last letter of the paragraph raised
  3 last letter of the FIRST sentence raised
  4 last letter of the LAST sentence raised
  5 last letter of EVERY sentence raised
  6 first lowered + state 3
  7 first lowered + state 5
A family is a 4-tuple of states, swept over all 10 paragraphs (4^10 = 1,048,576 texts).
Every text whose MD5 begins 3c6 is derived at m/44'/0'/0'/0/i, i in 0..77, and compared
with the demo escrow.
"""
import hashlib, itertools, re, time, sys
from rbb_probe import addr_at

P = open("demo_base.txt", encoding="utf-8").read().rstrip("\n").split("\n\n")
DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"


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


def make_states(p):
    ss = sents(p)
    first = first_down(p)
    out = [p]
    out.append(first)                                            # 1
    out.append(raise_last_alpha(p))                              # 2
    out.append(" ".join([raise_last_alpha(ss[0])] + ss[1:]))     # 3
    out.append(" ".join(ss[:-1] + [raise_last_alpha(ss[-1])]))    # 4
    out.append(" ".join(raise_last_alpha(s) for s in ss))        # 5
    q3 = " ".join([raise_last_alpha(ss[0])] + ss[1:])
    out.append(first_down(q3))                                   # 6
    q5 = " ".join(raise_last_alpha(s) for s in ss)
    out.append(first_down(q5))                                   # 7
    return out


ST = [make_states(p) for p in P]

FAMILIES = [
    ("F1 none/first/sent1/first+sent1", (0, 1, 3, 6)),
    ("F2 none/first/lastsent/first+lastsent", (0, 1, 4, 7)),
    ("F3 none/first/allsents/first+allsents", (0, 1, 5, 7)),
    ("F4 none/first/para-last/sent1-last", (0, 1, 2, 3)),
    ("F5 none/para-last/lastsent/allsents", (0, 2, 4, 5)),
    ("F6 none/first/sent1/allsents", (0, 1, 3, 5)),
]

total = hits = 0
t0 = time.time()
for fname, states in FAMILIES:
    for join_name, join in (("crlfcrlf", "\r\n\r\n"),):
        n = 0
        for combo in itertools.product(range(len(states)), repeat=10):
            t = join.join(ST[i][states[combo[i]]] for i in range(10))
            n += 1
            h = hashlib.md5(t.encode()).hexdigest()
            if h.startswith("3c6"):
                hits += 1
                b = bytes.fromhex(h)
                for idx in range(78):
                    if addr_at(b, idx) == DEMO:
                        print("*** DEMO MATCH ***", fname, combo, h, "idx", idx, flush=True)
        total += n
        print(f"{fname:42s} {join_name} candidates={n} elapsed={time.time()-t0:.0f}s", flush=True)
print(f"TOTAL candidates={total} 3c6hits={hits} runtime={time.time()-t0:.0f}s")
