"""Sentence-level census of the sign vocabulary, by narrative act, over prose paragraphs only.

Prose basis: 273 paragraphs minus 18 structural headings, 10 list labels `a)`..`f)`, and ¶15
(`"2020."`, no letters) = 244 prose paragraphs.

Acts, split at the four window starts:
    I   ¶1-92     II  ¶93-167     III ¶168-230    IV ¶231-273

Counts three classes of sentence:
    strict  the token `sign` or `signs` as a word
    stem    sign, signs, signature, signal, signed, signing, signify, significance
    recog   the phrase "recognize/recognized/recognizing the signs"

Also classifies each `sign` sentence as a live use of the instruction (narrator or dialogue), a
quotation, or the author's own analysis of it, and censuses case-odd tokens by act, since the
two channels turn out not to co-occur.

Reads:  ../wp_paras_br.json
Writes: ../sign_census_results.json
"""
import json, os, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

LABELS = {176, 182, 209, 215, 250, 252, 254, 256, 258, 260}
HEADS = {1, 2, 3, 54, 71, 88, 89, 91, 115, 130, 152, 157, 161, 163, 164, 175, 247, 265}
LETTERLESS = {15}
EXCLUDED = LABELS | HEADS | LETTERLESS

ACTS = [("I", 1, 92), ("II", 93, 167), ("III", 168, 230), ("IV", 231, 273)]

SENT = re.compile(r"[^.!?]*[.!?]+[\"\u201d]?|[^.!?]+$")
STRICT = re.compile(r"\b(sign|signs|Sign|Signs)\b")
STEM = re.compile(r"\b(sign|signs|signature|signatures|signal|signals|signed|signing|"
                  r"signify|significance)\b", re.I)
RECOG = re.compile(r"recogni[sz]\w*\s+the\s+signs?", re.I)
TOKEN = re.compile(r"[A-Za-z][A-Za-z']*")

# every `sign` sentence in the chapter, hand-classified. Paraphrase risk is nil: each is quoted in
# the census doc with its paragraph number.
CLASS = {
    206: "false-positive",   # "dollar sign" twice
    240: "false-positive",   # the verb, "a way used to sign"
    222: "quotation",        # hal's post, ¶7
    244: "quotation",        # the quoted line on its own
    223: "analysis", 225: "analysis", 226: "analysis", 227: "analysis",
    228: "analysis", 230: "analysis", 236: "analysis", 246: "analysis",
    20: "live", 42: "live", 220: "live", 273: "live",
}


def load():
    d = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    return [("\n".join(x) if isinstance(x, list) else x) for x in ps]


def act_of(i):
    for n, s, e in ACTS:
        if s <= i <= e:
            return n
    return "?"


def case_odd(t):
    if not t.isalpha() or len(t) < 2:
        return False
    return not (t.islower() or t.isupper() or (t[0].isupper() and t[1:].islower()))


def main():
    ps = load()
    assert len(ps) == 273
    rows = {n: {"paras": 0, "sentences": 0, "strict": [], "stem": [], "recog": []}
            for n, _, _ in ACTS}
    odd = collections.defaultdict(list)
    for i, p in enumerate(ps, 1):
        a = act_of(i)
        if i in EXCLUDED:
            continue
        rows[a]["paras"] += 1
        for s in (x.strip() for x in SENT.findall(p)):
            if not s:
                continue
            rows[a]["sentences"] += 1
            if STRICT.search(s):
                rows[a]["strict"].append({"para": i, "sentence": s, "class": CLASS.get(i, "?")})
            if STEM.search(s):
                rows[a]["stem"].append(i)
            if RECOG.search(s):
                rows[a]["recog"].append(i)
        for t in TOKEN.findall(p):
            if case_odd(t):
                odd[t].append(i)

    tot = {k: sum(len(rows[n][k]) for n, _, _ in ACTS) for k in ("strict", "stem", "recog")}
    tot["paras"] = sum(rows[n]["paras"] for n, _, _ in ACTS)
    tot["sentences"] = sum(rows[n]["sentences"] for n, _, _ in ACTS)
    print(f"prose paragraphs {tot['paras']}  sentences {tot['sentences']}")
    print(f"{'act':4s}{'paras':>7s}{'sents':>8s}{'sign':>7s}{'stem':>7s}{'recog':>7s}")
    for n, _, _ in ACTS:
        r = rows[n]
        print(f"{n:4s}{r['paras']:7d}{r['sentences']:8d}{len(r['strict']):7d}"
              f"{len(r['stem']):7d}{len(r['recog']):7d}")
    print(f"{'':4s}{tot['paras']:7d}{tot['sentences']:8d}{tot['strict']:7d}"
          f"{tot['stem']:7d}{tot['recog']:7d}")
    live = [(r["para"]) for n, _, _ in ACTS for r in rows[n]["strict"] if r["class"] == "live"]
    print(f"\nlive uses of the instruction: {sorted(live)}")
    print("sign-sentence classes:",
          dict(collections.Counter(r["class"] for n, _, _ in ACTS for r in rows[n]["strict"])))
    print("\ncase-odd tokens by act:")
    by_act = collections.Counter()
    for t, where in odd.items():
        acts = sorted({act_of(i) for i in where})
        print(f"  {t:28s} x{len(where):<2d} ¶{where[:6]} acts {''.join(acts)}")
        for i in where:
            by_act[act_of(i)] += 1
    print(f"  occurrences: {sum(len(w) for w in odd.values())} in {len(odd)} distinct tokens; "
          f"per act {dict(sorted(by_act.items()))}")

    json.dump({"prose_paragraphs": tot["paras"], "sentences": tot["sentences"],
               "acts": {n: {k: (len(v) if isinstance(v, list) else v) for k, v in rows[n].items()}
                        for n, _, _ in ACTS},
               "sentences_by_act": {n: rows[n]["strict"] for n, _, _ in ACTS},
               "live_uses": sorted(live),
               "case_odd": {t: where for t, where in odd.items()},
               "totals": tot},
              open(os.path.join(ROOT, "sign_census_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
