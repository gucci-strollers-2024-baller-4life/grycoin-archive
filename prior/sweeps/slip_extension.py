"""Slip extension: one-inverted-paragraph variants on every accepted set, plus the
claimer's-paste bases (SLIP_PATTERNS.md sec.8.2-8.3).

Why this is not inside an earlier closure: every previous sweep applied ONE edge mode to a
whole set (2^20 closure = arbitrary paragraph *subsets* under a fixed mode). A per-paragraph
direction (one paragraph flipped the wrong way, the rest the right way) is outside that
closure, and it is exactly her documented error class (R2 b12 warning).

Sets: non-ITASM, ITASM, non-SATOI, the 14 "signs" paragraphs, the 13 trailing-space
paragraphs, the 10 lowercase-initial paragraphs, the 63 quoted paragraphs, the narrative
complement, and the four FFWW windows. Modes A/B, with every single paragraph inverted in
turn. Paste variants (trailing space dropped per paragraph / all trailing whitespace
dropped) are applied to the accepted window sets.

Usage: python3 sweeps/slip_extension.py
"""
import hashlib, json, sys, time, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import fast2

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)

LIVE_H, OLD_H = fast2.h160(fast2.LIVE), fast2.h160(fast2.OLD)
IDX = (0, 1, 2, 44, 76, 77)
CERT = {"lf": "46a308c279540a33e977ea1f660e8458", "mixed": "bd07e6ee209c5ab65d874bbbcfccda18"}
SIGNS = set("ITASM")
SATOI = set("SATOI")


def segs():
    return json.load(open(os.path.join(HERE, "wp_paras_br.json")))


def build(kind, paste=0):
    """paste 0: certified base. 1: trailing spaces dropped per paragraph.
    2: trailing spaces dropped and 10 internal breaks kept (same), 3: every trailing
    whitespace char in the whole text dropped."""
    S = segs()
    if paste == 1:
        S = [[seg.rstrip(" ") for seg in p] for p in S]
    join, ibr = ("\r\n\r\n", "\n") if kind != "lf" else ("\n\n", "\n")
    text = join.join(ibr.join(s) for s in S)
    if paste == 3:
        text = text.replace(" \n", "\n")
    b = text.encode()
    if paste == 0:
        assert hashlib.md5(b).hexdigest() == CERT[kind], kind
    # offsets of each paragraph in the *same* text that was built
    offs, pos = [], 0
    for p in S:
        para = ibr.join(p)
        if paste == 3:
            para = para.replace(" \n", "\n")
        offs.append((pos, pos + len(para.encode())))
        pos += len(para.encode()) + len(join)
    return b, offs


def text_of(p):
    return " ".join(p)


def sets_of(S):
    first = [(i + 1, " ".join(p).lstrip()[:1]) for i, p in enumerate(S)]
    txt = [text_of(p) for p in S]
    out = {}
    out["non_ITASM"] = [n for n, f in first if f and f.upper() not in SIGNS]
    out["ITASM"] = [n for n, f in first if f and f.upper() in SIGNS]
    out["non_SATOI"] = [n for n, f in first if f and f.upper() not in SATOI]
    out["signs14"] = [n for n, t in zip(range(1, len(S) + 1), txt) if "signs" in t.lower()]
    out["trail13"] = [i + 1 for i, p in enumerate(S) if any(s != s.rstrip(" ") for s in p)]
    out["lower10"] = [n for n, f in first if f and f.islower()]
    out["quoted63"] = [n for n, t in zip(range(1, len(S) + 1), txt) if t.lstrip().startswith('"')]
    q = set(out["quoted63"])
    out["narrative"] = [n for n in range(1, len(S) + 1) if n not in q]
    out["W1_5-8"] = [5, 6, 7, 8]
    out["W2_93-96"] = [93, 94, 95, 96]
    out["W3_168-171"] = [168, 169, 170, 171]
    out["W4_230-234"] = [230, 231, 232, 234]
    return out


def is_lower(c):
    return 97 <= c <= 122


def edges(b, span, mode):
    s, e = span
    ls = [i for i in range(s, e) if 65 <= b[i] <= 90 or 97 <= b[i] <= 122]
    if not ls:
        return []
    f, l = ls[0], ls[-1]
    out = []
    if mode == "A":
        if not is_lower(b[f]):
            out.append(f)
        if is_lower(b[l]):
            out.append(l)
    else:
        if is_lower(b[f]):
            out.append(f)
        if not is_lower(b[l]):
            out.append(l)
    return out


def toggle(b, ps):
    a = bytearray(b)
    for p in ps:
        c = a[p]
        a[p] = c + 32 if 65 <= c <= 90 else c - 32
    return bytes(a)


def main():
    t0 = time.time()
    stats = dict(cands=0, derivs=0, hits=[])
    S = segs()
    names = sets_of(S)
    for name, paras in sorted(names.items()):
        print(f"{name}: {len(paras)} paragraphs", flush=True)
    for kind, paste in (("mixed", 0), ("lf", 0), ("mixed", 1), ("mixed", 3)):
        b, offs = build(kind, paste)
        for name, paras in names.items():
            for mode in ("A", "B"):
                pos, pp = [], {}
                for p in paras:
                    e = edges(b, offs[p - 1], mode)
                    pp[p] = e
                    pos += e
                if not pos:
                    continue
                variants = [("plain", pos)]
                for p in paras:
                    inv = edges(b, offs[p - 1], "B" if mode == "A" else "A")
                    variants.append((f"inv{p}", [x for x in pos if x not in pp[p]] + inv))
                for tag, ps in variants:
                    h = hashlib.md5(toggle(b, ps)).digest()
                    for idx in IDX:
                        a = fast2.addr_from_key(fast2.key_at(fast2.seed_from(h), idx))
                        stats["derivs"] += 1
                        ah = fast2.h160(a)
                        if ah in (LIVE_H, OLD_H):
                            which = "LIVE" if ah == LIVE_H else "OLD"
                            stats["hits"].append((kind, paste, name, mode, tag, idx,
                                                  h.hex(), a, which))
                            print("*** HIT", stats["hits"][-1], flush=True)
                    stats["cands"] += 1
        print(f"  done {kind}/paste{paste}: cands={stats['cands']} derivs={stats['derivs']} "
              f"{stats['derivs']/(time.time()-t0):.0f}/s", flush=True)
    stats["secs"] = round(time.time() - t0, 1)
    print(json.dumps({k: v for k, v in stats.items() if k != "hits"}))
    print("hits:", stats["hits"])


if __name__ == "__main__":
    main()
