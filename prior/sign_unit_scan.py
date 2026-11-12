#!/usr/bin/env python3
"""Sign-unit scan: does the chapter carry the stage-one sign structure anywhere?

Stage one (Hal Finney's "Bitcoin and me", 16 paragraphs) is certified:
every paragraph starts with one of I,T,A,S,M except four, which start
F,F,W,W (paras 2,3,4,6), with one I-paragraph (5) sitting between the two W's.
Those four paragraphs are exactly the certified flips.

This script asks the same question of the RBB chapter (part 720888559, 273
paragraphs, base wp_paras_br.json):

  1. chapter-wide violator count for {I,T,A,S,M}
  2. per-section violator counts
  3. every contiguous span whose ONLY violators are four F/W-initial paragraphs
  4. replicas of the stage-one shape F,F,W,[I],W

Run: python3 sign_unit_scan.py
"""
import json
import re

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

BASE = "wp_paras_br.json"
SIGNS = set("ITASM")


def load_paras(path=BASE):
    raw = json.load(open(path))
    return ["".join(p) if isinstance(p, list) else p for p in raw]


def initials(paras):
    out = []
    for t in paras:
        m = re.search(r"[A-Za-z]", t)
        out.append(m.group(0) if m else "")
    return out


SECTIONS = {
    "title+I 1-87": (1, 87),
    "II 88-162": (88, 162),
    "III 163-273": (163, 273),
    "1 Second Coming 3-53": (3, 53),
    "2 Running 54-70": (54, 70),
    "3 Reverse Turing 71-87": (71, 87),
    "Abstract 89-90": (89, 90),
    "1 Purpose 91-114": (91, 114),
    "2 Two Changes 115-129": (115, 129),
    "3 Incentives 130-151": (130, 151),
    "4 Why Blockchain 152-156": (152, 156),
    "5 What Grycoin 157-160": (157, 160),
    "6 Conclusion 161-162": (161, 162),
    "1 My Identity 164-174": (164, 174),
    "2 The Satoshi Code 175-246": (175, 246),
    "2a birthday 176-181": (176, 181),
    "2b THOMAS and Satoshi 182-208": (182, 208),
    "2c BITcoin is AHScoin 209-214": (209, 214),
    "2d outing 215-246": (215, 246),
    "3 Other evidence 247-264": (247, 264),
    "4 What does it mean 265-273": (265, 273),
    "rulebook 228-246": (228, 246),
    "Finney reprint 231-235": (231, 235),
}


def main():
    paras = load_paras()
    ini = initials(paras)
    n = len(paras)
    viol = [i + 1 for i, c in enumerate(ini) if c not in SIGNS]

    print(f"paragraphs: {n}")
    print(f"violators of {''.join(sorted(SIGNS))}: {len(viol)}")
    print(f"violator paragraphs: {viol}")
    print()

    print("per-section (1-indexed):")
    for name, (a, b) in SECTIONS.items():
        v = [x for x in viol if a <= x <= b]
        flag = "  <== exactly four" if len(v) == 4 else ""
        print(f"  {name:32s} n={b - a + 1:3d}  viol={len(v):3d}{flag}")
    print()

    print("spans whose only violators are four F/W-initial paragraphs:")
    hits = []
    for a in range(n):
        v = []
        for b in range(a, n):
            if ini[b] not in SIGNS:
                v.append(b + 1)
            if len(v) > 4:
                break
            if len(v) == 4 and all(ini[x - 1] in "FW" for x in v):
                hits.append((a + 1, b + 1, tuple(v)))
    distinct = {}
    for a, b, v in hits:
        distinct.setdefault(v, []).append((a, b))
    print(f"  {len(hits)} spans, {len(distinct)} distinct violator sets:")
    for v, spans in distinct.items():
        letters = "".join(ini[x - 1] for x in v)
        widest = max(spans, key=lambda s: s[1] - s[0])
        print(f"    {v} initials={letters} widest span {widest[0]}-{widest[1]}"
              f" ({widest[1] - widest[0] + 1} paras)")
    print()

    print("replicas of the stage-one shape (F,F,W,[I],W):")
    for i in range(n - 4):
        w = ini[i:i + 5]
        if w[0] == "F" and w[1] == "F" and w[2] == "W" and w[3] in SIGNS and w[4] == "W":
            print(f"    paras {i + 1}-{i + 5}: {''.join(w)}")


if __name__ == "__main__":
    main()
