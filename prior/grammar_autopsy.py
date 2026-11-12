#!/usr/bin/env python3
"""grammar_autopsy.py - the three syntactic layers of "Second", counted.

1. mood: every imperative, sentence-initial or buried in narrative
2. modality: modal auxiliary density per paragraph and per part, and the conditional inventory
3. internal punctuation: colons, semicolons, dashes, as potential syntactic equalisers

Plus the calibration gate: each syntactic feature is computed on the ten demo paragraphs
(where the selected set {4,5,6,8} is certified by the author's own text) before it is
allowed to touch the chapter.  A feature that does not return {4,5,6,8} on the demo is not
the selection mechanism, whatever it looks like on the chapter.
"""
import json, re, collections

PARAS = [t for _, t in json.load(open("wp_paras.json"))]
DEMO = [p.strip() for p in open("demo_base.txt").read().split("\n\n") if p.strip()]
MODALS = ("can could shall should will would may might must").split()
DEMO_SELECTED = {4, 5, 6, 8}          # GRAMMAR_CONSTRAINTS.md, C1-C5


def sents(p):
    out, s = [], 0
    for m in re.finditer(r'[.!?]+["\u201d]?(?=\s|$)', p):
        out.append((s, m.end()))
        s = m.end()
    if s < len(p):
        out.append((s, len(p)))
    return out


def alpha_first(s):
    return next((c for c in s if c.isalpha()), "")


def alpha_last(s):
    return next((c for c in reversed(s) if c.isalpha()), "")


# ---------------------------------------------------------------- 1. mood
# sentence-initial imperative: first alphabetic word is a base-form verb and carries no subject.
# The detector is deliberately narrow and every hit is printed for inspection.
VERB_LEMMAS = set("""take look note remember consider see try imagine read add change remove keep start show
tell want let check go come give find think know use put make set turn follow count write combine subtract
join reverse ask forget ignore compare align focus hear listen watch stop begin continue expect suppose assume
say speak open close move place hold carry bring send call answer apply select choose pick mark capitalize
raise lower flip scroll reveal""".split())
# narrative-buried imperative: an infinitival or coordinated command whose subject is suppressed
BURIED = re.compile(r'\b(?:just|simply)\s+(\w+)|\b(?:and|then)\s+(?:you\s+get|take|spell|count|look|read|remove|join|add)\b'
                    r'|what you get if you (\w+)|if you (\w+?)\b', re.I)


def mood_report():
    out = {"initial": [], "buried": [], "let": []}
    for i, p in enumerate(PARAS, 1):
        for a, b in sents(p):
            s = p[a:b]
            w = re.match(r'\s*["\u201c(\[]*([A-Za-z\']+)', s)
            if w and w.group(1).lower() in VERB_LEMMAS and w.group(1)[0].isupper():
                out["initial"].append((i, w.group(1), s.strip()))
        for m in re.finditer(r"\blet(?:'s| us)\b", p, re.I):
            out["let"].append((i, p[max(0, m.start() - 50):m.end() + 60]))
        for m in BURIED.finditer(p):
            if m.group(0).lower().startswith("if you"):
                continue
            out["buried"].append((i, m.group(0), p[max(0, m.start() - 60):m.end() + 70]))
    return out


# ---------------------------------------------------------------- 2. modality
def modality_report():
    per = collections.defaultdict(list)
    for i, p in enumerate(PARAS, 1):
        ms = re.findall(r"\b(" + "|".join(MODALS) + r")\b", p)
        per[i] = ms
    inventory = collections.Counter(m for v in per.values() for m in v)
    words = {i: len(p.split()) for i, p in enumerate(PARAS, 1)}
    parts = {"I": range(2, 88), "II": range(88, 163), "III": range(163, 274)}
    bypart = {}
    for k, rng in parts.items():
        n = sum(len(per[i]) for i in rng)
        w = sum(words[i] for i in rng)
        bypart[k] = (n, w, round(1000 * n / w, 1))
    return per, inventory, words, bypart


CONSEQ = re.compile(r"\b(would|could|might|will|shall|should|must|then)\b", re.I)
IMPERATIVE_CONSEQ = re.compile(r',\s*(?:just\s+)?(?:recognize|keep|take|look|add|remove|change|use|count)\b', re.I)


def conditional_report():
    rows = []
    for i, p in enumerate(PARAS, 1):
        for a, b in sents(p):
            s = p[a:b]
            m = re.search(r"\b(if|unless|once|when)\b", s, re.I)
            if not m or m.group(1).lower() in ("once", "when"):
                continue
            rest = s[m.start():]
            if CONSEQ.search(rest):
                kind = "modal consequent"
            elif IMPERATIVE_CONSEQ.search(rest):
                kind = "IMPERATIVE consequent"
            elif s.rstrip().endswith("..."):
                kind = "TRUNCATED (no consequent)"
            elif re.search(r"^\W*(i wonder|see if|what happens|show me|guess what)", s, re.I) or " if " in s[max(0, m.start()-30):m.start()].lower():
                kind = "interrogative / embedded"
            else:
                kind = "bare consequent"
            rows.append((i, kind, s.strip()))
    return rows


# ---------------------------------------------------------------- 3. punctuation
def punct_report():
    out = {}
    for name, ch in (("colon", ":"), ("semicolon", ";"), ("emdash", "\u2014"),
                     ("endash", "\u2013"), ("hyphen", "-"), ("paren_open", "("),
                     ("paren_close", ")"), ("ellipsis", "...")):
        out[name] = sum(p.count(ch) for p in PARAS)
    sites = []
    for i, p in enumerate(PARAS, 1):
        for m in re.finditer(r"[:;]", p):
            before = p[max(0, m.start() - 45):m.start()]
            after = p[m.end():m.end() + 55]
            sites.append((i, p[m.start()], before.strip()[-30:], after.strip()[:45]))
    return out, sites


def interior_capitals():
    tok = re.compile(r"[A-Za-z]{2,}")
    out = []
    for i, p in enumerate(PARAS, 1):
        for m in tok.finditer(p):
            w = m.group(0)
            if w[0].isupper() and not any(c.isupper() for c in w[1:]):
                continue          # ordinary Capitalised word
            if not (any(c.isupper() for c in w[1:]) and any(c.islower() for c in w[1:])):
                continue          # all-caps acronym: no interior case boundary
            before = p[max(0, m.start() - 45):m.start()]
            after = p[m.end():m.end() + 25]
            out.append((i, w, before[-45:], after[:25]))
    return out


# ---------------------------------------------------------------- the gate
def demo_features():
    feats = collections.OrderedDict()
    def add(name, fn, text):
        feats.setdefault(name, set())
        if fn(text):
            feats[name].add(DEMO.index(text) + 1)
    for p in DEMO:
        add("lexical 'recognize the signs'", lambda t: "recognize the signs" in t.lower(), p)
        add("lexical 'signs'", lambda t: "sign" in t.lower(), p)
        add("modal present", lambda t: bool(re.search(r"\b(" + "|".join(MODALS) + r")\b", t)), p)
        add("conditional (if/when/once)", lambda t: bool(re.search(r"\b(if|when|once|unless)\b", t, re.I)), p)
        add("second person you/your", lambda t: bool(re.search(r"\byou\b|\byour\b", t, re.I)), p)
        add("quotation marks", lambda t: '"' in t, p)
        add("internal punctuation (: ; - )", lambda t: bool(re.search(r"[:;\u2014\u2013-]", t)), p)
        add("imperative sentence", lambda t: any(
            (re.match(r'["\u201c(\[]*([A-Za-z]+)', s) or [None, ""])[1].lower() in VERB_LEMMAS
            for s in [t[a:b] for a, b in sents(t)]), p)
        add("negation", lambda t: bool(re.search(r"\bnot\b|\bn't\b|n't", t, re.I)), p)
        add("more than one sentence", lambda t: len(sents(t)) > 1, p)
    return feats


if __name__ == "__main__":
    mood = mood_report()
    print("=== 1. MOOD ===")
    print(f"sentence-initial imperatives: {len(mood['initial'])}")
    for i, w, s in mood["initial"]:
        print(f"  P{i:3d} {w:8s} {s[:100]}")
    print(f"\n'let us / let me': {len(mood['let'])}")
    for i, s in mood["let"]:
        print(f"  P{i:3d} ...{s}")
    print(f"\nburied command shapes: {len(mood['buried'])}")
    for i, w, s in mood["buried"]:
        print(f"  P{i:3d} [{w}] ...{s}")

    per, inv, words, bypart = modality_report()
    tot = sum(len(v) for v in per.values())
    tw = sum(words.values())
    print("\n=== 2. MODALITY ===")
    print(f"modal tokens {tot} / {tw} words = {1000*tot/tw:.1f} per 1000")
    print("inventory", inv.most_common())
    print("per part (modals, words, rate/1000):", bypart)
    print("paragraphs with zero modals:", sum(1 for i in range(1, 274) if not per[i]))
    print("histogram:", sorted(collections.Counter(len(v) for v in per.values()).items()))

    cond = conditional_report()
    print(f"\nconditionals: {len(cond)}")
    print(collections.Counter(k for _, k, _ in cond).most_common())
    for i, k, s in cond:
        print(f"  P{i:3d} {k:26s} {s[:110]}")

    pu, sites = punct_report()
    print("\n=== 3. PUNCTUATION ===")
    print(pu)
    for i, ch, before, after in sites:
        print(f"  P{i:3d} {ch!r:3s} ...{before}  ||  {after}")

    print("\n=== interior capitals ===")
    for i, w, before, after in interior_capitals():
        print(f"  P{i:3d} {w:34s} ...{before}  <<  {after}")

    print("\n=== GATE: syntactic features on the demo, target {4,5,6,8} ===")
    for name, sel in demo_features().items():
        mark = "MATCH" if sel == DEMO_SELECTED else ""
        print(f"  {name:32s} -> {sorted(sel)} {mark}")
