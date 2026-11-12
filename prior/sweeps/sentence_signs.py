"""The sentence-unit reading: calibrated on the author's own worked example, then swept on the chapter.

CLUES_CANONICAL §13.4: the demo's worked example is sentence-level, not paragraph-level. "I expected…"
is the first sentence of demo ¶5 and "himself" is that sentence's last word, so head-down / tail-up on a
single sentence reproduces both quoted changes exactly. This script:

  1. reproduces that pair from demo_base.txt as a hard assertion (the calibration the repo requires)
  2. applies the same unit to the chapter: sentence heads and sentence tails
  3. selects sentences by sign alphabet, in class and out of class
  4. runs the three mixed units the chapter has never been swept with:
        sentence head + sentence tail   (the demo's own unit)
        paragraph head + sentence tail  (what "first sentence's last word" becomes at chapter scale)
        sentence head + paragraph tail
  5. derives every text at indices 0, 1, 2, 5, 6, 7, 44, 76, 77 against the escrow

Reads:  ../wp_paras_br.json, ../demo_base.txt
Writes: ../sentence_signs_results.json
"""
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import sixteen_matrix as sm                      # noqa: E402  (validated fast lane)

ALPHABETS = {
    "ITASM": set("ITASM"),
    "SATOSHI": set("SATOSHI"),
    "AIMOST": set("AIMOST"),
    "THOMAS": set("THOMAS"),
    "THOMAS+I": set("THOMASI"),
}
SPLIT = re.compile(r'(?<=[.!?"])\s+(?=["\u201cA-Z0-9])')


def sents(p):
    return [s for s in SPLIT.split(p.strip()) if s.strip()]


def first_alpha(s):
    for j, c in enumerate(s):
        if c.isalpha():
            return j
    return -1


def last_alpha(s):
    for j in range(len(s) - 1, -1, -1):
        if s[j].isalpha():
            return j
    return -1


def head_tail_up(s, head_j, tail_j):
    """Return s with the head lowered and the tail raised, skipping no-ops. Count real moves."""
    q, moves = list(s), 0
    if head_j >= 0 and s[head_j].isupper():
        q[head_j] = s[head_j].lower()
        moves += 1
    if tail_j >= 0 and s[tail_j].islower():
        q[tail_j] = s[tail_j].upper()
        moves += 1
    return "".join(q), moves


def calibrate():
    """The author's own worked example must fall out of the sentence unit."""
    demo = [x.strip() for x in open(os.path.join(ROOT, "demo_base.txt"), encoding="utf-8").read().split("\n\n") if x.strip()]
    assert len(demo) == 10, len(demo)
    p5 = demo[4]
    s1 = sents(p5)[0]
    assert s1.startswith("I expected"), s1[:40]
    marked, moves = head_tail_up(s1, first_alpha(s1), last_alpha(s1))
    assert marked.startswith("i expected"), marked[:40]
    assert marked.rstrip(".").endswith("himselF"), marked[-40:]
    print("  calibration: demo ¶5 sentence 1 -> %r … %r  (%d moves)"
          % (marked[:12], marked[-12:], moves))
    assert moves == 2
    return "ok"


def load_chapter():
    d = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    out = [("\n".join(x) if isinstance(x, list) else x) for x in ps]
    assert len(out) == 273, len(out)
    return out


def serialisations(paras):
    for join, tag in ((b"\n\n", "LF"), (b"\r\n\r\n", "CRLF")):
        for trail in (False, True):
            yield join.join(p.encode() for p in paras) + (join if trail else b""), tag + ("+t" if trail else "")


def apply_unit(paras, mode, sel_sent, sel_para):
    """mode: st / pt_st / st_pt.  sel_sent: set of (para, sent) indices.  sel_para: set of para indices."""
    out = list(paras)
    moves = 0
    for i, p in enumerate(paras):
        if mode == "st" or mode == "st_pt":
            if i not in sel_para and mode == "st_pt":
                continue
        ss = sents(p)
        if not ss:
            continue
        new = list(ss)
        for k, s in enumerate(ss):
            if (i, k) not in sel_sent:
                continue
            hj, tj = first_alpha(s), last_alpha(s)
            new[k], m = head_tail_up(s, hj, tj)
            moves += m
        out[i] = " ".join(new)
    if mode == "pt_st":
        for i, p in enumerate(paras):
            if i not in sel_para:
                continue
            ss = sents(p)
            if not ss:
                continue
            hj = first_alpha(p)
            new = list(ss)
            new[-1] = p[last_alpha(p)] if False else new[-1]
            # paragraph head down, first sentence tail up
            ph, m = head_tail_up(p, hj, -1)
            moves += m
            tj = last_alpha(new[0])
            q2, m2 = head_tail_up(new[0], -1, tj)
            moves += m2
            new[0] = q2
            body = " ".join(new)
            # carry the paragraph-level head edit over
            q = list(body)
            if hj >= 0 and p[hj].isupper():
                q[hj] = p[hj].lower()
            out[i] = "".join(q)
    return out, moves


def main():
    sm.validate()
    print("\n== calibration on the author's worked example ==")
    calibrate()

    paras = load_chapter()
    sent_index = [(i, k) for i, p in enumerate(paras) for k, _ in enumerate(sents(p))]
    print("\n== the chapter at sentence scale ==")
    print("  paragraphs 273, sentences %d, mean %.2f per paragraph" % (len(sent_index), len(sent_index) / 273))
    print("  a free 'which sentences' selection is 2^%d, so only a rule is sweeppable"
          % len(sent_index))

    print("\n== sentence-initial sign letters ==")
    sets = {}
    for name, alpha in ALPHABETS.items():
        ins, outs = [], []
        for i, p in enumerate(paras):
            for k, s in enumerate(sents(p)):
                j = first_alpha(s)
                (ins if j >= 0 and s[j].upper() in alpha else outs).append((i, k))
        sets[name] = {"in": ins, "out": outs}
        print("  %-9s in-class sentences %-4d out-class %-4d" % (name, len(ins), len(outs)))

    print("\n== sweeps ==")
    hits, n, t0 = [], 0, time.time()
    rows = []
    for name in ALPHABETS:
        for which in ("in", "out"):
            sel_sent = set(sets[name][which])
            sel_para = {i for i, k in sel_sent}
            for mode in ("st", "pt_st", "st_pt"):
                marked, moves = apply_unit(paras, mode, sel_sent, sel_para)
                for blob, tag in serialisations(marked):
                    n += 1
                    h = hashlib.md5(blob).hexdigest()
                    res = sm.addrs(h)
                    rows.append({"alphabet": name, "set": which, "mode": mode, "join": tag,
                                 "md5": h, "moves": moves, "idx0": res[0]})
                    for i, a in res.items():
                        if a == sm.ESCROW:
                            hits.append((name, which, mode, tag, h, i))
                print("  %-9s %-4s %-6s sentences=%-4d moves=%-4d md5=%s idx0=%s"
                      % (name, which, mode, len(sel_sent), moves, rows[-1]["md5"], rows[-1]["idx0"]))
    print("\n  texts=%d derivations=%d elapsed=%.1fs hits=%d"
          % (n, n * len(sm.IDX), time.time() - t0, len(hits)))
    print("  ALL NEGATIVE" if not hits else "  HIT")
    for x in hits:
        print("  HIT", x)

    json.dump({"sentences": len(sent_index),
               "sizes": {k: {w: len(v) for w, v in d.items()} for k, d in sets.items()},
               "runs": rows, "hits": hits},
              open(os.path.join(ROOT, "sentence_signs_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
