"""Demo (cleczc) search against the author's own oracle: solution MD5 begins 3c6.

Rule shape from her hints: keep the text unchanged, change only capitalisation, for all
paragraphs where you recognise the signs. Her worked example is paragraph 5:
'I'->'i' (paragraph-initial lowercased) and 'himself'->'himselF' (a word-final letter
raised, not the paragraph's last letter).

Family swept: first-letter lowering per paragraph (6 sign-set variants) x one raised
word-final letter in each of paragraphs 1, 5 and 9 x two joins. Every candidate whose
MD5 begins 3c6 is then derived at m/44'/0'/0'/0/i for i in 0..77 and compared with the
demo escrow 1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi and the two RBB escrows.
"""
import hashlib, itertools, re, time

P = open("demo_base.txt", encoding="utf-8").read().rstrip("\n").split("\n\n")
assert len(P) == 10
DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"


def first_down(p):
    for j, c in enumerate(p):
        if c.isalpha():
            return p[:j] + c.lower() + p[j + 1:]
    return p


ENDS = {}
for i, p in enumerate(P, 1):
    ENDS[i] = [m.end() - 1 for m in re.finditer(r"[A-Za-z']+", p) if p[m.end() - 1].islower()]

DOWN_SETS = {
    "none": set(),
    "p5": {5},
    "I-paras": {1, 5, 9},
    "A+I-paras": {1, 2, 5, 9, 10},
    "nonITASM": {3, 4, 6, 7, 8},
    "all": set(range(1, 11)),
}
JOINS = {"crlfcrlf": "\r\n\r\n", "lf2": "\n\n"}
RAISE = (1, 5, 9)

hits = []
n = 0
t0 = time.time()
for jn, join in JOINS.items():
    for dname, down in DOWN_SETS.items():
        for combo in itertools.product(*[ENDS[i] + [None] for i in RAISE]):
            raises = {i: q for i, q in zip(RAISE, combo) if q is not None}
            parts = []
            for i, p in enumerate(P, 1):
                q = first_down(p) if i in down else p
                if i in raises:
                    k = raises[i]
                    q = q[:k] + q[k].upper() + q[k + 1:]
                parts.append(q)
            t = join.join(parts)
            n += 1
            h = hashlib.md5(t.encode()).hexdigest()
            if h.startswith("3c6"):
                hits.append((jn, dname, tuple(sorted(raises.items())), h, t))
el = time.time() - t0
print(f"candidates={n}  runtime={el:.1f}s  rate={n/el:.0f}/s  3c6-hits={len(hits)}")

with open("demo_3c6_hits.txt", "w", encoding="utf-8") as f:
    f.write(f"# demo 3c6 candidates: {n} swept, {len(hits)} with md5 prefix 3c6\n")
    for jn, dname, r, h, t in hits:
        f.write(f"{jn}\t{dname}\t{r}\t{h}\n")

if hits:
    from rbb_probe import addr_at
    found = 0
    for jn, dname, r, h, t in hits:
        b = bytes.fromhex(h)
        for idx in range(78):
            a = addr_at(b, idx)
            if a == DEMO:
                print("*** DEMO MATCH ***", jn, dname, r, h, "idx", idx)
                found += 1
    print("derived all 3c6 candidates at indices 0-77; matches:", found,
          f"({len(hits)*78} derivations)")
