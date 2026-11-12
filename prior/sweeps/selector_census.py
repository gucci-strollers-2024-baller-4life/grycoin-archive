"""The two candidate selectors for "which four paragraphs", both taken to the end of the corpus.

Context: sixteen_matrix.py proved that no 4-subset of the four FFWW/stnm windows produces the
escrow address, across four serialisations and nine indices. That kills the windows as mark
carriers, not the question. The question left open was: what names four paragraphs anywhere in 273?

This script closes the two selectors proposed as answers, and then closes the selector the chapter
itself states in ¶229-¶230.

Scan A  lexical openers. Does any non-window set of four paragraphs open with Fast / For / When and
        spell F,F,W,W? (The "narrative echo" hypothesis.)

Scan B  terminal directives. Which paragraphs END on meta-commentary about signs, letters, marks,
        instructions? (The ¶236 anchor taken as a locator.)

Scan C  edge-class census. Every paragraph classified by (first letter, last letter). This is the
        decisive one: it is the whole chapter, not a 16-paragraph sample.

Scan D  the exception rule of ¶229: "All paragraphs except for four, which start with F F and W W."
        Verified verbatim on hal_original.txt, then applied to every post and every post-section in
        the corpus, because that is where a fifth FFWW site could hide.

Nothing here derives a key. It is a text-structure census.
"""
import hashlib
import itertools
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "harness"))
from guard import install                       # noqa: E402
install(__file__)
import corpus                                   # noqa: E402

WINDOWS = {"W1": (5, 6, 7, 8), "W2": (93, 94, 95, 96),
           "W3": (168, 169, 170, 171), "W4": (231, 232, 233, 235)}
WIN = {p for w in WINDOWS.values() for p in w}
TEMPLATE_TAILS = "stnm"

DIRECTIVE = (r"\b(sign|signs|signal|signature|mark|marked|marks|note|noted|notice|"
             r"recogni[sz]e|instruct[a-z]*|letter|letters)\b")


def paragraphs():
    """The 273 paragraphs of the certified base, in document order, 1-indexed below."""
    out = []
    for seg in corpus.seeds():
        out.append("\n".join(seg) if isinstance(seg, list) else seg)
    assert len(out) == 273, len(out)
    return out


def edges(t):
    """(first letter upper, last letter) — non-letters at either end are skipped."""
    m = re.match(r"[^A-Za-z]*([A-Za-z])", t)
    f = m.group(1).upper() if m else "?"
    m2 = re.search(r"([A-Za-z])\W*$", t)
    l = m2.group(1) if m2 else "?"
    return f, l


def sentences(t):
    return [s for s in re.split(r'(?<=[.!?"])\s+', t) if s.strip()]


def scan_a(paras):
    openers = {}
    for i, t in enumerate(paras):
        m = re.match(r"[^A-Za-z]*([A-Za-z]+)", t)
        w = m.group(1) if m else "?"
        openers.setdefault(w, []).append(i + 1)
    interesting = {w: v for w, v in openers.items()
                   if w.lower() in ("fast", "for", "forgive", "first", "face", "fairly",
                                    "from", "finally", "when", "while", "whatever", "with")}
    # every paragraph whose FIRST LETTER is F or W, outside the windows, in document order
    fw_out = [(i + 1, edges(t)[0]) for i, t in enumerate(paras)
              if edges(t)[0] in ("F", "W") and (i + 1) not in WIN]
    # does any 4 of them spell F,F,W,W in document order?
    seq = [p for p, ch in fw_out]
    ffww = []
    Fs = [p for p in seq if edges(paras[p - 1])[0] == "F"]
    Ws = [p for p in seq if edges(paras[p - 1])[0] == "W"]
    for a, b in itertools.combinations(Fs, 2):
        for c, d in itertools.combinations(Ws, 2):
            if a < b < c < d:
                ffww.append((a, b, c, d))
    return {"openers": interesting, "nonwindow_FW_initials": fw_out,
            "nonwindow_FFWW_in_order": ffww}


def scan_b(paras):
    any_hit, final_hit, signs_final = [], [], []
    for i, t in enumerate(paras):
        ss = sentences(t)
        if not ss:
            continue
        if re.search(DIRECTIVE, t, re.I):
            any_hit.append(i + 1)
        if re.search(DIRECTIVE, ss[-1], re.I):
            final_hit.append((i + 1, ss[-1]))
        if re.search(r"\bsigns?\b", ss[-1], re.I):
            signs_final.append(i + 1)
    return {"any": any_hit, "final_sentence": final_hit, "final_sentence_sign": signs_final}


def scan_c(paras):
    FL = [edges(t) for t in paras]
    cls = {}
    for want in (("F", "s"), ("F", "t"), ("W", "n"), ("W", "m")):
        hit = [i + 1 for i, v in enumerate(FL) if v == want]
        cls[want] = {"all": hit, "windows": [p for p in hit if p in WIN],
                     "outside": [p for p in hit if p not in WIN]}
    return {"classes": cls, "initials": Counter(f for f, l in FL)}


def _html_blocks(path):
    """[(heading or '(head)', [paragraph, ...]), ...] with bold-only paragraphs as headings."""
    h = open(path, encoding="utf-8", errors="replace").read()
    blocks, cur = [], []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", h, re.S):
        inner = m.group(1)
        bold = bool(re.fullmatch(r"\s*<b>.*</b>\s*", inner, re.S))
        t = re.sub(r"<[^>]+>", " ", inner)
        t = re.sub(r"&nbsp;", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        if not t:
            continue
        if bold:
            blocks.append((t, cur))
            cur = []
        else:
            cur.append(t)
    blocks.append(("(tail)", cur))
    return blocks


def _exception_quad(doc):
    """Best F,F,W,W quartet whose removal leaves the smallest initial-letter alphabet."""
    FL = [edges(t) for t in doc]
    Fs = [i for i, v in enumerate(FL) if v[0] == "F"]
    Ws = [i for i, v in enumerate(FL) if v[0] == "W"]
    if len(Fs) > 4 or len(Ws) > 4:
        return None                      # the four cannot be the only non-alphabet paragraphs
    best = None
    for a, b in itertools.combinations(Fs, 2):
        for c, d in itertools.combinations(Ws, 2):
            for q in itertools.permutations((a, b, c, d)):
                if list(q) != sorted(q):
                    continue
                comp = sorted({v[0] for i, v in enumerate(FL) if i not in q})
                if best is None or len(comp) < len(best[0]):
                    best = (comp, q, "".join(FL[i][1] for i in q))
    return best


def scan_d():
    """The ¶229 rule: all paragraphs from a small alphabet except four that start F F W W."""
    rows = []
    hal = [x.strip() for x in re.split(r"\n\s*\n",
                                       open(os.path.join(ROOT, "hal_original.txt")).read()) if x.strip()]
    best = _exception_quad(hal)
    fl = [edges(t) for t in hal]
    rows.append({"doc": "hal_original.txt", "n": len(hal),
                 "initials": "".join(f for f, l in fl),
                 "quad": [i + 1 for i in best[1]], "tails": best[2],
                 "complement_alphabet": "".join(best[0])})
    meta = json.load(open(os.path.join(ROOT, "wparts.json")))["parts"]
    for p in meta:
        fp = os.path.join(ROOT, "wparts", "%d.txt" % p["id"])
        if not os.path.exists(fp):
            continue
        for name, doc in _html_blocks(fp):
            if len(doc) < 8:
                continue
            r = _exception_quad(doc)
            if r is None or len(r[0]) > 6:
                continue
            rows.append({"doc": p["title"], "section": name, "n": len(doc),
                         "quad": [i + 1 for i in r[1]], "tails": r[2],
                         "complement_alphabet": "".join(r[0])})
    return rows


def main():
    corpus.self_check()
    paras = paragraphs()

    a = scan_a(paras)
    print("\n== Scan A: lexical openers ==")
    for w in sorted(a["openers"]):
        print("  %-8s %s" % (w, a["openers"][w]))
    print("  non-window F/W-initial paragraphs: %d" % len(a["nonwindow_FW_initials"]))
    print("  non-window F,F,W,W quartets in document order: %d" % len(a["nonwindow_FFWW_in_order"]))

    b = scan_b(paras)
    print("\n== Scan B: terminal directives ==")
    print("  paragraphs with directive vocabulary anywhere: %d" % len(b["any"]))
    print("  paragraphs whose FINAL SENTENCE carries it:    %d %s"
          % (len(b["final_sentence"]), [p for p, s in b["final_sentence"]]))
    print("  paragraphs ending on the word sign/signs:      %d %s"
          % (len(b["final_sentence_sign"]), b["final_sentence_sign"]))

    c = scan_c(paras)
    print("\n== Scan C: edge-class census over all 273 ==")
    for k, v in c["classes"].items():
        print("  %s..%s  total %2d  in windows %d  outside %d %s"
              % (k[0], k[1], len(v["all"]), len(v["windows"]), len(v["outside"]),
                 v["outside"]))
    feasible = all(v["outside"] for v in c["classes"].values())
    print("  a fifth FFWW/stnm site anywhere in the chapter: %s"
          % ("possible" if feasible else "IMPOSSIBLE (a tail class outside the windows is empty)"))

    d = scan_d()
    print("\n== Scan D: the exception rule of ¶229 ==")
    for r in d:
        print("  %-10s %-32s n=%-3d quad=%-22s tails=%-5s complement alphabet=%s"
              % (r["doc"][:10], (r.get("section") or "")[:32], r["n"], r["quad"],
                 r["tails"], r["complement_alphabet"]))
    hits = [r for r in d if r["tails"] == TEMPLATE_TAILS]
    print("  documents where the exception quartet's tails spell %r: %d" % (TEMPLATE_TAILS, len(hits)))
    for r in hits:
        print("    %s / %s  quad=%s" % (r["doc"], r.get("section"), r["quad"]))

    c_json = {"classes": {"%s..%s" % k: v for k, v in c["classes"].items()},
              "initials": dict(c["initials"])}
    json.dump({"a": {"nonwindow_FW_initials": a["nonwindow_FW_initials"],
                     "nonwindow_FFWW_in_order": a["nonwindow_FFWW_in_order"]},
               "b": {"final_sentence": [p for p, s in b["final_sentence"]],
                     "final_sentence_sign": b["final_sentence_sign"]},
               "c": c_json, "d": d},
              open(os.path.join(HERE, "selector_census_results.json"), "w"), indent=1, default=str)
    print("\nwrote sweeps/selector_census_results.json")


if __name__ == "__main__":
    main()
