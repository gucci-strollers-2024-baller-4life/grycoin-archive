"""Structural-edge classes and the Finney-block sign readings, BYTE-CORRECT.

BUG FIXED 2026-10-31: the chapter contains six U+00A0 characters (char positions 9084, 16922,
17272, 17780, 33411, 43301), so the encoded text is six bytes longer than the string. The earlier
version of this sweep computed flip positions on the decoded string and applied them to a
bytearray of the encoded text, which means every position after char 9084 was off by one to six
bytes: it hashed the wrong letters. This version works entirely in byte space.

Sets tested (see EDGE_INTERSECTION_2026-10-31.md for provenance of each):
  A_initlower  10 paragraphs whose first letter is lowercase (all enumerators a)-f))
  B_finup      12 paragraphs whose first sentence closes on a capital (numerals, acronyms)
  D_pool       union of the two, plus complements and the two enumerations
  finney4/5    the Finney reprint read as the sign set, with and without the I paragraph

Modes: paragraph-initial down/up x first-sentence-close up/down. Bases: CRLF paragraphs and LF
paragraphs, both certified. Indices 0, 1, 2.

Usage: python3 sweeps/edge_intersection_byte.py
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import fast2

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)

LIVE_H, OLD_H = fast2.h160(fast2.LIVE), fast2.h160(fast2.OLD)
IDX = (0, 1, 2, 76, 77)
SEGS = json.load(open(os.path.join(HERE, "wp_paras_br.json")))
CERT = {"lf": "46a308c279540a33e977ea1f660e8458", "mixed": "bd07e6ee209c5ab65d874bbbcfccda18"}
A = [176, 182, 209, 215, 250, 252, 254, 256, 258, 260]
B = [2, 88, 163, 183, 184, 194, 195, 211, 229, 237, 239, 245]
ALLP = set(range(1, 274))
SETS = {
    "A_initlower": A, "B_finup": B, "D_pool": sorted(set(A) | set(B)),
    "CAPS1": [184, 194, 195, 211, 229, 237, 239],
    "notA": sorted(ALLP - set(A)), "notB": sorted(ALLP - set(B)),
    "notD": sorted(ALLP - set(A) - set(B)),
    "list_ad": [176, 182, 209, 215], "list_af": [250, 252, 254, 256, 258, 260],
    "finney4": [231, 232, 233, 235], "finney5": [231, 232, 233, 234, 235],
    "finney5+222": [222, 231, 232, 233, 234, 235],
}
MODES = {"down_up": ("d", "u"), "down_down": ("d", "d"), "up_down": ("u", "d"),
         "up_up": ("u", "u"), "init_down": ("d", None), "init_up": ("u", None),
         "fin_up": (None, "u"), "fin_down": (None, "d")}


def context(kind):
    """byte-exact base plus byte-space paragraph spans"""
    join, ibr, step = ("\n\n", "\n", 2) if kind == "lf" else ("\r\n\r\n", "\n", 4)
    segs_b = [ibr.join(p).encode() for p in SEGS]
    b = join.encode().join(segs_b)
    assert hashlib.md5(b).hexdigest() == CERT[kind], kind
    spans, pos = [], 0
    for s in segs_b:
        spans.append((pos, pos + len(s)))
        pos += len(s) + step
    return b, spans


def is_alpha(c):
    return 65 <= c <= 90 or 97 <= c <= 122


def is_upper(c):
    return 65 <= c <= 90


def para_first(b, spans, n):
    s, e = spans[n - 1]
    for i in range(s, e):
        if is_alpha(b[i]):
            return i
    return None


SENT = re.compile(rb"[.!?](?=\s|$)")


def s1_close(b, spans, n):
    s, e = spans[n - 1]
    m = SENT.search(b, s, e)
    cut = m.end() if m else e
    last = None
    for i in range(s, cut):
        if is_alpha(b[i]):
            last = i
    return last


def toggles(b, spans, paras, imode, fmode):
    out = []
    for n in paras:
        if imode:
            q = para_first(b, spans, n)
            if q is not None and ((imode == "d" and is_upper(b[q])) or
                                  (imode == "u" and not is_upper(b[q]))):
                out.append(q)
        if fmode:
            q = s1_close(b, spans, n)
            if q is not None and ((fmode == "u" and not is_upper(b[q])) or
                                  (fmode == "d" and is_upper(b[q]))):
                out.append(q)
    return out


def main():
    n = hits = 0
    for kind in ("mixed", "lf"):
        b, spans = context(kind)
        print(f"--- {kind}: {len(b)} bytes, md5 {hashlib.md5(b).hexdigest()[:8]}", flush=True)
        for name, paras in SETS.items():
            for mname, (im, fm) in MODES.items():
                tg = toggles(b, spans, paras, im, fm)
                if not tg:
                    continue
                a = bytearray(b)
                for q in tg:
                    a[q] ^= 32
                h = hashlib.md5(bytes(a)).digest()
                for idx in IDX:
                    n += 1
                    addr = fast2.addr_from_key(fast2.key_at(fast2.seed_from(h), idx))
                    if fast2.h160(addr) in (LIVE_H, OLD_H):
                        hits += 1
                        print("*** HIT", name, mname, kind, idx, h.hex(), addr, flush=True)
        for para in sorted(set(A) | set(B)):
            for mname, (im, fm) in MODES.items():
                tg = toggles(b, spans, [para], im, fm)
                if not tg:
                    continue
                a = bytearray(b)
                for q in tg:
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
