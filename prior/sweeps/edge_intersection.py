"""Structural-edge rule: the demo's asymmetric pair ported to the chapter's own syntax.

Demo, paragraph 5: paragraph-initial lowercased ('I' -> 'i') AND the final letter of the last
word of the FIRST SENTENCE capitalised ('himself' -> 'himselF'). One mark at the macro edge
(paragraph start), one at the micro edge (first-sentence close).

Measured on the chapter: macro-edge anomalies (lowercase initial) = 10 paragraphs, all of them
enumerators a) b) c) ... ; micro-edge anomalies (first-sentence final letter already capital) =
12 paragraphs, all of them acronyms/initials; their intersection is empty. This script tests the
structural classes anyway, in every mode direction, both certified bases.
"""
import hashlib, itertools, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import fast2

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)

LIVE_H, OLD_H = fast2.h160(fast2.LIVE), fast2.h160(fast2.OLD)
IDX = (0, 1, 2)
SEGS = json.load(open(os.path.join(HERE, "wp_paras_br.json")))
CERT = {"lf": "46a308c279540a33e977ea1f660e8458", "mixed": "bd07e6ee209c5ab65d874bbbcfccda18"}


def base(kind):
    join, ibr = ("\n\n", "\n") if kind == "lf" else ("\r\n\r\n", "\n")
    text = join.join(ibr.join(p) for p in SEGS)
    b = text.encode()
    assert hashlib.md5(b).hexdigest() == CERT[kind]
    return b, text


def context(kind):
    b, txt = base(kind)
    spans, pos = [], 0
    step = 4 if kind == "mixed" else 2
    for p in SEGS:
        t = "\n".join(p)
        spans.append((pos, pos + len(t)))
        pos += len(t) + step
    return b, txt, spans


def letters(txt, a, b):
    return [i for i in range(a, b) if txt[i].isalpha()]


def s1_end(txt, spans, n):
    s, e = spans[n - 1]
    seg = txt[s:e]
    m = re.search(r"[.!?](?=\s|$)", seg)
    cut = s + (m.end() if m else len(seg))
    ls = letters(txt, s, cut)
    return ls[-1] if ls else None


def para_first(txt, spans, n):
    s, e = spans[n - 1]
    ls = letters(txt, s, e)
    return ls[0] if ls else None


A = [176, 182, 209, 215, 250, 252, 254, 256, 258, 260]
Bset = [2, 88, 163, 183, 184, 194, 195, 211, 229, 237, 239, 245]
CAPS1 = [184, 194, 195, 211, 229, 237, 239]
LISTS = {"list_ad": [176, 182, 209, 215], "list_af": [250, 252, 254, 256, 258, 260]}
allp = set(range(1, 274))
SETS = {"A_initlower": A, "B_finup": Bset, "D_pool": sorted(set(A) | set(Bset)),
        "CAPS1": CAPS1, "notA": sorted(allp - set(A)), "notB": sorted(allp - set(Bset)),
        "notD": sorted(allp - set(A) - set(Bset)), **LISTS}

MODES = {
    "init_down": ("d", None), "init_up": ("u", None),
    "fin_up": (None, "u"), "fin_down": (None, "d"),
    "down_up": ("d", "u"), "down_down": ("d", "d"),
    "up_down": ("u", "d"), "up_up": ("u", "u"),
}


def apply(txt, spans, paras, imode, fmode):
    out = []
    for n in paras:
        if imode:
            q = para_first(txt, spans, n)
            if q is not None and ((imode == "d" and txt[q].isupper()) or
                                  (imode == "u" and txt[q].islower())):
                out.append(q)
        if fmode:
            q = s1_end(txt, spans, n)
            if q is not None and ((fmode == "u" and txt[q].islower()) or
                                  (fmode == "d" and txt[q].isupper())):
                out.append(q)
    return out


def main():
    hits = n = 0
    for kind in ("mixed", "lf"):
        b, txt, spans = context(kind)
        for name, paras in SETS.items():
            for mname, (im, fm) in MODES.items():
                for tag, plist in ((name, paras), ("singles", None)):
                    if plist is None:
                        continue
                    toggles = apply(txt, spans, plist, im, fm)
                    if not toggles:
                        continue
                    a = bytearray(b)
                    for q in toggles:
                        a[q] ^= 32
                    h = hashlib.md5(bytes(a)).digest()
                    for idx in IDX:
                        n += 1
                        addr = fast2.addr_from_key(fast2.key_at(fast2.seed_from(h), idx))
                        if fast2.h160(addr) in (LIVE_H, OLD_H):
                            hits += 1
                            print("*** HIT", name, mname, kind, idx, h.hex(), addr, flush=True)
        for para in sorted(set(A) | set(Bset)):
            for mname, (im, fm) in MODES.items():
                toggles = apply(txt, spans, [para], im, fm)
                if not toggles:
                    continue
                a = bytearray(b)
                for q in toggles:
                    a[q] ^= 32
                h = hashlib.md5(bytes(a)).digest()
                for idx in IDX:
                    n += 1
                    addr = fast2.addr_from_key(fast2.key_at(fast2.seed_from(h), idx))
                    if fast2.h160(addr) in (LIVE_H, OLD_H):
                        hits += 1
                        print("*** HIT", para, mname, kind, idx, h.hex(), addr, flush=True)
    print(f"derivations={n} hits={hits}")


if __name__ == "__main__":
    main()
