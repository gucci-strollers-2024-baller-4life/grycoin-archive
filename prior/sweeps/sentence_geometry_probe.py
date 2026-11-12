#!/usr/bin/env python3
"""sentence_geometry_probe.py - the one geometry the syntax catalog states but no sweep has run.

WORDPLAY_RULES_CATALOG.md line 824 splits the demo's device into two *different* anchors:

    a paragraph's FIRST letter moves down          ("I" -> "i")
    the letter closing THE SENTENCE CONTAINING THE SIGN WORD moves up   ("himself" -> "himselF")

Both exemplars sit in demo paragraph 5, whose trigger sentence is its FIRST sentence, so on the
demo the two anchors are indistinguishable and every sweep so far has treated the second anchor as
"first-sentence-final". In the chapter they separate: of the twelve paragraphs that carry
"recognize the signs", twelve carry it in a sentence that is not the paragraph's first.

Four named hypotheses, per paragraph, on the twelve trigger paragraphs:
  T1  paragraph-first alpha DOWN + trigger-sentence-last alpha UP   (the catalog verbatim)
  T2  paragraph-first alpha UP   + trigger-sentence-last alpha DOWN (inverted)
  T3  trigger-sentence own edges: first DOWN + last UP
  T4  trigger-sentence-last alpha UP only
Serialisations: LF and CRLF block separators, with and without trailing separator.
Indices: 0,1,2,5,6,7,44,76,77.  Target: the live escrow.
"""
import json, re, sys
sys.path.insert(0, "harness")
import btc

TARGET = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
INDICES = [0, 1, 2, 5, 6, 7, 44, 76, 77]
P = [t for _, t in json.load(open("wp_paras.json"))]
KEY = "recognize the signs"


def sents(p):
    out, s = [], 0
    for m in re.finditer(r'[.!?]+["\u201d]?(?=\s|$)', p):
        out.append((s, m.end()))
        s = m.end()
    if s < len(p):
        out.append((s, len(p)))
    return out


def trigger_span(p):
    """the sentence that carries the instruction phrase"""
    for a, b in sents(p):
        if KEY in p[a:b].lower():
            return a, b
    return None


def idx_first(s, a, b):
    return next((j for j in range(a, b) if s[j].isalpha()), None)


def idx_last(s, a, b):
    return next((j for j in range(b - 1, a - 1, -1) if s[j].isalpha()), None)


def mark(text, ops):
    """ops: iterable of (index, 'down'|'up')"""
    t = list(text)
    for j, d in ops:
        if j is None:
            continue
        c = t[j]
        if d == "down" and c.isupper():
            t[j] = c.lower()
        if d == "up" and c.islower():
            t[j] = c.upper()
    return "".join(t)


def addrs(h):
    k, c = btc.master_key(btc.mnemonic_seed(btc.entropy_to_mnemonic(bytes.fromhex(h))))
    for d in (44 + btc.H, 0 + btc.H, 0 + btc.H, 0):
        k, c = btc.ckd_priv(k, c, d)
    return {i: btc.p2pkh(btc.pubkey(btc.ckd_priv(k, c, i)[0])) for i in INDICES}


def main():
    sel = [i for i, p in enumerate(P, 1) if KEY in p.lower()]
    print("trigger paragraphs:", sel)
    spans = {i: trigger_span(P[i - 1]) for i in sel}
    print("\nparagraph / trigger sentence position:")
    for i in sel:
        a, b = spans[i]
        ns = len(sents(P[i - 1]))
        k = next(j for j, (x, y) in enumerate(sents(P[i - 1]), 1) if x == a)
        print(f"  P{i:3d} sentence {k}/{ns}  first={P[i-1][idx_first(P[i-1],a,b)]!r}"
              f" last={P[i-1][idx_last(P[i-1],a,b)]!r}   para-first={P[i-1][idx_first(P[i-1],0,len(P[i-1]))]!r}")

    rows = []
    for mode in ("T1", "T2", "T3", "T4"):
        paras = list(P)
        for i in sel:
            a, b = spans[i]
            pf = idx_first(P[i - 1], 0, len(P[i - 1]))
            tf = idx_first(P[i - 1], a, b)
            tl = idx_last(P[i - 1], a, b)
            if mode == "T1":
                ops = [(pf, "down"), (tl, "up")]
            elif mode == "T2":
                ops = [(pf, "up"), (tl, "down")]
            elif mode == "T3":
                ops = [(tf, "down"), (tl, "up")]
            else:
                ops = [(tl, "up")]
            paras[i - 1] = mark(P[i - 1], ops)
        for sep, sn in (("\n\n", "LF"), ("\r\n\r\n", "CRLF")):
            for trail in (False, True):
                text = sep.join(paras) + (sep if trail else "")
                h = btc.md5_hex(text)
                a_ = addrs(h)
                hit = [k for k, v in a_.items() if v == TARGET]
                rows.append({"mode": mode, "sep": sn, "trail": trail, "md5": h,
                             "addr0": a_[0], "hits": hit})
                print(f"{mode}/{sn}{'+t' if trail else '':3s} md5={h} addr0={a_[0]}"
                      + ("   *** HIT ***" if hit else ""), flush=True)
    json.dump(rows, open("sentence_geometry_probe_results.json", "w"), indent=1)
    print(f"\nderivations {len(rows)*len(INDICES)}  distinct md5 {len({r['md5'] for r in rows})}"
          f"  hits {sum(1 for r in rows if r['hits'])}")


if __name__ == "__main__":
    main()
