"""Small-class pass: the plausible masks first.

The author's own manual says the marks are a small, judgement-placed set, not a rule
(R1 block 2 is "(family name Yang)", R1 block 29 changes exactly two letters). A class
that marks paragraphs by initial is therefore most likely a SHORT letter set. This
enumerates every class of at most six of the 21 initials, on the as-is base and on all
six serialization variants, both joins, indices 0-2, against both escrows.
"""
import hashlib, itertools, json, os, sys
import rtl_ci as R
import mega

MAXK = int(os.environ.get("MAXK", "6"))
IDX = (0, 1, 2)
BASES = ["as-is", "CLSN", "CLSS", "CLDB", "CLPX", "CLCR", "CLWS"]


def base_texts(P0, name):
    if name == "as-is":
        return P0
    return mega.apply_variant(P0, name)


def run():
    P0 = R.load()
    mega.gate(P0)
    letters = mega.first_axes(P0)[0]
    print("small-class: %d initials %s, classes of at most %d letters"
          % (len(letters), "".join(letters), MAXK), flush=True)
    total = 0
    hits = []
    for name in BASES:
        P = base_texts(P0, name)
        norm = [p.encode() for p in P]
        flip = [R.flips(p).encode() for p in P]
        let, bits = mega.first_axes(P)
        seg = b"\r\n\r\n" if name == "CLWS" else None
        n = 0
        for k in range(0, MAXK + 1):
            for chosen in itertools.combinations(range(len(let)), k):
                sel = set(chosen)
                marked = [bits[i] is not None and bits[i] in sel for i in range(len(P))]
                for sep in (b"\n\n", b"\r\n\r\n" if seg is None else b"\r\n"):
                    body = sep.join([flip[i] if marked[i] else norm[i] for i in range(len(P))])
                    d = hashlib.md5(body).hexdigest()
                    n += 1
                    for ix in IDX:
                        a = R.addr(d, ix)
                        if a in R.TARGETS:
                            hits.append(dict(base=name, cls="".join(let[j] for j in chosen),
                                             sep=repr(sep), md5=d, idx=ix, escrow=R.TARGETS[a]))
                            print("***HIT", hits[-1], flush=True)
                            open("HIT_SMALL_%s_%s_%d.txt" % (name, "".join(let[j] for j in chosen), ix), "wb").write(body)
        total += n
        print("DONE small-class %-6s texts=%d derivations=%d" % (name, n, n * len(IDX)), flush=True)
        json.dump(dict(total=total, hits=hits, maxk=MAXK),
                  open("smallclass_results.json", "w"), indent=1)
    print("SMALLCLASS DONE texts=%d derivations=%d hits=%d" % (total, total * len(IDX), len(hits)), flush=True)


if __name__ == "__main__":
    run()
