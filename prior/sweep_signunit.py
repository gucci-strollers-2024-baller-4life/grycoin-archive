#!/usr/bin/env python3
"""Sign sets that para 229 licenses but no earlier sweep has used.

Para 229: "All paragraphs except for four, which start with F F and W W."
Hal's post realises it as F,F,W,W at paras 2,3,4,6, with the I-paragraph 5 between
the two W's; those four paragraphs are exactly the certified stage-one flips.

sign_unit_scan.py finds every span of the chapter whose only non-{I,T,A,S,M} openers
are four F/W paragraphs. It returns the three known windows plus three SHIFTED
quadruples that mix window and non-window paragraphs:

    {94,95,96,100}    F W W F
    {95,96,100,102}   W W F F
    {232,233,235,236} F W W W

The three windows are closed. The shifted quadruples are not, and they are the reading
that makes "two F and two W" order-free. This sweep covers every non-empty subset of
{94,95,96,100,102,232,233,234,235,236} that contains at least one paragraph no window
sweep ever touched (100, 102, 236), so no candidate repeats closed ground.

Harness: rbb_probe (coincurve). Certified self-tests run first and abort on failure.
Usage: python3 sweep_signunit.py
"""
import itertools
import json
import sys

import rbb_probe as R

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

NEW = {100, 102, 236}
POOL = [94, 95, 96, 100, 102, 232, 233, 234, 235, 236]
IDX = (0, 1, 2, 44, 76, 77)

# (label, act_on_first, case_for_first, act_on_last, case_for_last)
MODES = [
    ("first_lo+last_up", True, "lo", True, "up"),
    ("first_up+last_lo", True, "up", True, "lo"),
    ("first_lo", True, "lo", False, None),
    ("last_up", False, None, True, "up"),
    ("first_up", True, "up", False, None),
    ("last_lo", False, None, True, "lo"),
]


def load(path):
    """Paragraph texts exactly as certified: internal <br> joins become \n and the
    13 significant trailing spaces are NOT stripped."""
    raw = json.load(open(path, encoding="utf-8"))
    return ["\n".join(p) if isinstance(p, list) else p for p in raw]


def edge_index(text, forward=True):
    rng = range(len(text)) if forward else range(len(text) - 1, -1, -1)
    return next((j for j in rng if text[j].isalpha()), None)


def mutate(text, mode):
    _, fa, fc, la, lc = mode
    s = list(text)
    if fa:
        i = edge_index(s, True)
        if i is not None:
            s[i] = s[i].lower() if fc == "lo" else s[i].upper()
    if la:
        i = edge_index(s, False)
        if i is not None:
            s[i] = s[i].lower() if lc == "lo" else s[i].upper()
    return "".join(s)


def main():
    stage1 = R.addr_at(bytes.fromhex("9dd2efb9bc976c2095bd534d7b8d431c"), 0)
    if stage1 != R.STAGE1:
        sys.exit("stage-one selftest FAILED: %s" % stage1)
    print("stage-one selftest PASS", flush=True)

    sets = [s for k in range(1, len(POOL) + 1)
            for s in itertools.combinations(POOL, k) if NEW & set(s)]
    print("sign sets with new ground:", len(sets), flush=True)

    CERT = {
        ("wp_paras_br.json", "crlf2"): "bd07e6ee209c5ab65d874bbbcfccda18",
        ("wp_paras_br.json", "lf2"): "46a308c279540a33e977ea1f660e8458",
        ("chapter_paras_exact.json", "crlf2"): "f74e8e0122e114fe13c89a3bba25294a",
        ("chapter_paras_exact.json", "lf2"): "48d318202691ffb873e00b63196eaf36",
    }
    bases = []
    for fname in ("wp_paras_br.json", "chapter_paras_exact.json"):
        paras = load(fname)
        for jname, join in (("crlf2", "\r\n\r\n"), ("lf2", "\n\n")):
            bases.append((fname, jname, join, paras))
    for fname, jname, join, paras in bases:
        got = R.md5b(join.join(paras)).hex()
        want = CERT[(fname, jname)]
        if got != want:
            sys.exit("base certification FAILED %s/%s: %s != %s" % (fname, jname, got, want))
    print("base certification PASS for all four serialisations", flush=True)

    seen = {}
    for fname, jname, join, paras in bases:
        for st in sets:
            for mode in MODES:
                out = list(paras)
                for p in st:
                    out[p - 1] = mutate(out[p - 1], mode)
                text = join.join(out)
                h = R.md5b(text)
                seen.setdefault(h, (fname, jname, st, mode[0]))
    print("unique preimages:", len(seen), "derivations:", len(seen) * len(IDX), flush=True)

    hits = []
    for n, (h, meta) in enumerate(seen.items(), 1):
        for i in IDX:
            got = R.addr_at(h, i)
            if got in (R.LIVE, R.OLD):
                print("HIT!!", meta, "idx", i, got, h.hex(), flush=True)
                hits.append({"meta": [meta[0], meta[1], list(meta[2]), meta[3]],
                             "idx": i, "addr": got, "md5": h.hex()})
        if n % 5000 == 0:
            print("  %d/%d preimages, %d derivations, hits=%d"
                  % (n, len(seen), n * len(IDX), len(hits)), flush=True)

    print("DERIVATIONS:", len(seen) * len(IDX), "HITS:", len(hits), "DONE", flush=True)
    json.dump(hits, open("sweep_signunit_hits.json", "w"), indent=1)


if __name__ == "__main__":
    main()
