"""Quantitative sign census by narrative act: prose paragraphs, sentences, `sign*` directives,
and case-odd tokens, on the 273-paragraph chapter.

Definitions, stated so they can be argued with:
  prose paragraph   a paragraph that is not a heading, not an a)-f) list label, and not one of the
                    two bare `STNM` lines
  heading           the `Second` / `I.` / `1.` style lines and the one-word section titles
  sentence          split on a terminal mark (. ! ? ") followed by whitespace and a capital, digit or
                    opening quote; a conservative variant that never splits before a quote is reported
                    alongside, because the two differ by 37 sentences
  sign directive    a token whose stem is `sign` (signs, sign, signed, signing, signals excluded)
  case-odd token    a word token that is neither lower case, nor upper case, nor Capitalised:
                    internal capitals such as `VIrgin`, `BItcoin`, `ppM`

Act boundaries are the four used in the request: 1-92, 93-167, 168-230, 231-273. They are NOT the
author's own headings (`I. Second Life` at ¶2, `III. Second Identity` at ¶163), which split the text
into three parts, not four. Both are reported.

Reads:  ../wp_paras_br.json
Writes: ../act_census_results.json
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

ACTS = [("I", 1, 92), ("II", 93, 167), ("III", 168, 230), ("IV", 231, 273)]

HEAD = re.compile(r'^(Second|Abstract|STNM\.?|I{1,3}\.\s|[1-9]\.\s|[a-f]\)\s)')
SPLIT_Q = re.compile(r'(?<=[.!?"])\s+(?=["\u201cA-Z0-9])')
SPLIT_C = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9])')
TOKEN = re.compile(r"[A-Za-z][A-Za-z'\-]*")
SIGN = re.compile(r"\bsign(s|ed|ing)?\b", re.I)


def load():
    d = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    out = [("\n".join(x) if isinstance(x, list) else x) for x in ps]
    assert len(out) == 273, len(out)
    return out


def is_prose(p):
    s = p.strip()
    if not s:
        return False
    if s == "STNM" or s == "STNM.":
        return False
    if HEAD.match(s) and len(s) < 60:
        return False
    return True


def case_odd(tok):
    """Neither lower, nor upper, nor Capitalised."""
    if tok.islower() or tok.isupper():
        return False
    if tok[0].isupper() and tok[1:].islower():
        return False
    return True


def main():
    T = load()
    prose = [i + 1 for i, p in enumerate(T) if is_prose(p)]
    print("prose paragraphs: %d of 273 (non-prose %d)" % (len(prose), 273 - len(prose)))

    rows, res = [], {"acts": {}, "prose_total": len(prose)}
    for name, a, b in ACTS:
        idx = [n for n in prose if a <= n <= b]
        chars = sum(len(T[n - 1]) for n in idx)
        sq = sum(len([s for s in SPLIT_Q.split(T[n - 1].strip()) if s.strip()]) for n in idx)
        sc = sum(len([s for s in SPLIT_C.split(T[n - 1].strip()) if s.strip()]) for n in idx)
        signs = [(n, m.group(0)) for n in idx for m in SIGN.finditer(T[n - 1])]
        odd = []
        for n in idx:
            for m in TOKEN.finditer(T[n - 1]):
                if case_odd(m.group(0)):
                    odd.append((n, m.group(0)))
        rows.append({"act": name, "range": [a, b], "prose": len(idx), "chars": chars,
                     "sent_quote": sq, "sent_plain": sc,
                     "sign": len(signs), "sign_paras": sorted({n for n, _ in signs}),
                     "case_odd": len(odd), "odd_paras": sorted({n for n, _ in odd})})
        res["acts"][name] = {"range": [a, b], "prose": idx, "signs": signs, "odd": odd}

    hdr = "%-4s %-9s %5s %7s %6s %6s %6s %6s" % ("act", "range", "prose", "chars", "sentQ", "sentP", "sign", "odd")
    print(hdr)
    for r in rows:
        print("%-4s %-9s %5d %7d %6d %6d %6d %6d"
              % (r["act"], "%d-%d" % tuple(r["range"]), r["prose"], r["chars"],
                 r["sent_quote"], r["sent_plain"], r["sign"], r["case_odd"]))
    print("%-4s %-9s %5d %7d %6d %6d %6d %6d" % ("sum", "", sum(r["prose"] for r in rows),
          sum(r["chars"] for r in rows), sum(r["sent_quote"] for r in rows),
          sum(r["sent_plain"] for r in rows), sum(r["sign"] for r in rows), sum(r["case_odd"] for r in rows)))

    print("\nsign tokens by paragraph")
    for r in rows:
        if r["sign"]:
            print("  %-4s %s" % (r["act"], res["acts"][r["act"]]["signs"]))
    print("\ncase-odd tokens by paragraph")
    for r in rows:
        if r["case_odd"]:
            print("  %-4s %s" % (r["act"], res["acts"][r["act"]]["odd"]))

    print("\nboundary carriers")
    for n in (73, 128, 136):
        p = T[n - 1]
        first = next((c for c in p if c.isalpha()), "")
        last = next((c for c in reversed(p) if c.isalpha()), "")
        print("  ¶%-4d init=%s term=%s  %r" % (n, first, last, p[:70]))

    json.dump(res, open(os.path.join(ROOT, "act_census_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
