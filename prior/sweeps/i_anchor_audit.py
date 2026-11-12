"""¶238's I anchor: what the text actually names, and what the four candidate paragraphs carry.

The question: ¶238 says "Combined with the I as the first letter in the paragraphs close to that",
then names a paragraph by its content. This script identifies that paragraph, prints the boundary
tokens of every candidate I paragraph, and tests the pentad (4+1) reading against the quad.

It also records two textual edits that fall out of the same block and that matter for the sweeps:
  * hal_original.txt ¶5 spells "facinating", the chapter's reprint ¶234 spells "fascinating"
  * hal_original.txt ¶7 has "true identity" (quoted verbatim at ¶222), the instruction fragment ¶243
    has "real identity"

Reads the certified base through harness/corpus.py. No derivation.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "harness"))
from guard import install                       # noqa: E402
install(__file__)
import corpus                                   # noqa: E402

WINDOWS = {"W1": (5, 6, 7, 8), "W2": (93, 94, 95, 96), "W3": (168, 169, 170, 171)}
LEADIN = {"W1": 4, "W2": 92, "W3": 167}
PENTADS = {"W1": (4, 5, 6, 7, 8), "W2": (92, 93, 94, 95, 96), "W3": (167, 168, 169, 170, 171)}
# the paragraph ¶238 names by content, in the chapter and in the source
NAMED = {"chapter": 234, "source": 5}


def paras():
    out = ["\n".join(s) if isinstance(s, list) else s for s in corpus.seeds()]
    assert len(out) == 273
    return out


def words(t):
    return re.findall(r"[A-Za-z']+", t)


def token_row(T, n, label=""):
    t = T[n - 1]
    w = words(t)
    return {"para": n, "label": label, "first": w[0], "last": w[-1], "last_letter": w[-1][-1],
            "chars": len(t), "words": len(w)}


def main():
    corpus.self_check()
    T = paras()
    hal = [x.strip() for x in re.split(r"\n\s*\n", open(os.path.join(ROOT, "hal_original.txt")).read())
           if x.strip()]

    print("== the paragraph ¶238 names ==")
    target = words(T[NAMED["chapter"] - 1])
    src = words(hal[NAMED["source"] - 1])
    print("  ¶238 quotes: %r"
          % T[237][T[237].index('"') + 1:T[237].rindex('"')])
    print("  chapter ¶%d  first words: %s" % (NAMED["chapter"], " ".join(target[:6])))
    print("  source  ¶%d  first words: %s" % (NAMED["source"], " ".join(src[:6])))
    print("  -> the I is the initial of ¶%d (hal ¶%d), the paragraph interleaved inside the reprint,"
          % (NAMED["chapter"], NAMED["source"]))
    print("     not the initial of the three lead-ins.")

    print("\n== boundary tokens of every candidate I paragraph ==")
    rows = [token_row(T, LEADIN[k], "lead-in " + k) for k in LEADIN]
    rows.append(token_row(T, NAMED["chapter"], "interleaved (named by ¶238)"))
    for r in rows:
        print("  %-32s ¶%-4d first=%-3s last=%-12s (…%s)  chars=%-4d words=%d"
              % (r["label"], r["para"], r["first"], r["last"], r["last_letter"],
                 r["chars"], r["words"]))
    print("  last letters in order ¶4,¶92,¶167,¶234: %s"
          % "".join(r["last_letter"] for r in rows))
    print("  all four initial letters: %s"
          % "".join(words(T[r["para"] - 1])[0][0].upper() for r in rows))

    print("\n== quad vs pentad ==")
    print("  quad  (4 paras): initials F F W W, finals s t n m -> 'stnm' in every window")
    for k, ps in PENTADS.items():
        ini = "".join(words(T[p - 1])[0][0].upper() for p in ps)
        fin = "".join(words(T[p - 1])[-1][-1] for p in ps)
        print("  pentad %-3s (5 paras): initials %s, finals %s" % (k, ini, fin))
    print("  only the letters 'Istnm' are invariant across the three windows; the pentad finals"
          " differ (nstnm / wstnm / sstnm).")

    print("\n== the author's own pairing remark (¶240) ==")
    print("  STNM pair-reversed -> TS|MN = 'TSMN'; the certified answer prefix contains 'TS mN'.")

    print("\n== the two edits in the same block ==")
    print("  spelling   hal_original ¶5: %r   chapter ¶234: %r"
          % (re.findall(r"found Bitcoin \w+", hal[NAMED["source"] - 1]),
             re.findall(r"found Bitcoin \w+", T[NAMED["chapter"] - 1])))
    print("  identity   ¶222 (verbatim quote): %r   ¶243 (instruction fragment): %r"
          % (re.findall(r"Satoshi's \w+ identity", T[221]),
             re.findall(r"Satoshi's \w+ identity", T[242])))
    print("             ¶246 states the message as %r" % re.findall(r"Satoshi's \w+ identity", T[245]))
    titles = [p["title"] for p in json.load(open(os.path.join(ROOT, "wparts.json")))["parts"]]
    print("             post titles in the corpus containing 'Real Identity': %s"
          % [t for t in titles if "Real Identity" in t])

    print("\n== the demonstrated extraction, ¶242-¶246 ==")
    for n in (242, 243, 244, 245, 246):
        print("  ¶%-4d %s" % (n, T[n - 1]))

    json.dump({"tokens": rows, "named": NAMED,
               "pentads": {k: {"initials": "".join(words(T[p - 1])[0][0].upper() for p in ps),
                               "finals": "".join(words(T[p - 1])[-1][-1] for p in ps)}
                           for k, ps in PENTADS.items()}},
              open(os.path.join(HERE, "i_anchor_audit_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
