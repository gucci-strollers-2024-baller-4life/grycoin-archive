#!/usr/bin/env python3
"""unit_topology.py - the transport operator applied at every unit the prose licenses.

The conservation law (one capital leaves a unit's head, one lands on its tail; total unchanged)
turns the search into a *deterministic* construction: once the unit and the selector are named, the
answer text is fixed. There is nothing to permute. So the whole question is the one the chapter
cannot answer for you: what is the unit?

Everything tested here is balanced by construction, so every candidate obeys the invariant.
Units: paragraph (273), sentence (641), part (3), window (the three FFWW quads + the Finney reprint).
Selectors: all / the sign paragraphs / F-W initials / non-ITASM initials / per window / per part.
Anchor modes: 'unit'  -> head down + tail up inside each selected unit
              'demo'  -> paragraph head down + sign-sentence tail up (the demo ¶5 asymmetry)
"""
import json, re, sys, hashlib
sys.path.insert(0, "harness")
import fast2

LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
IDX = [0, 1, 2, 5, 6, 7, 44, 76, 77]
P = [t for _, t in json.load(open("wp_paras.json"))]
KEY = "recognize the signs"


def addrs(h):
    e = bytes.fromhex(h)
    return {i: fast2.addr_from_key(fast2.key_at(fast2.seed_from(e), i)) for i in IDX}


assert addrs("9dd2efb9bc976c2095bd534d7b8d431c")[0] == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"


def sents(p):
    out, s = [], 0
    for m in re.finditer(r'[.!?]+["\u201d]?(?=\s|$)', p):
        out.append((s, m.end()))
        s = m.end()
    if s < len(p):
        out.append((s, len(p)))
    return out


def head(p, a, b):
    return next((j for j in range(a, b) if p[j].isalpha()), None)


def tail(p, a, b):
    return next((j for j in range(b - 1, a - 1, -1) if p[j].isalpha()), None)


def apply_units(paras, unit, sel):
    """one down at each unit head, one up at each unit tail"""
    edits = {}          # para index (1-based) -> list of (offset, 'down'|'up')
    def add(i, j, d):
        if j is not None:
            edits.setdefault(i, []).append((j, d))
    for i, p in enumerate(paras, 1):
        if not sel(i, p):
            continue
        if unit == "paragraph":
            add(i, head(p, 0, len(p)), "down"); add(i, tail(p, 0, len(p)), "up")
        elif unit == "sentence":
            for a, b in sents(p):
                add(i, head(p, a, b), "down"); add(i, tail(p, a, b), "up")
        elif unit == "word":
            for m in re.finditer(r"[A-Za-z']+", p):
                add(i, head(p, m.start(), m.end()), "down"); add(i, tail(p, m.start(), m.end()), "up")
    out = list(paras)
    for i, ops in edits.items():
        t = list(out[i - 1])
        for j, d in ops:
            if d == "down" and t[j].isupper():
                t[j] = t[j].lower()
            elif d == "up" and t[j].islower():
                t[j] = t[j].upper()
        out[i - 1] = "".join(t)
    return out


def apply_demo(paras, sel):
    """paragraph head down + the sign sentence's tail up, per selected paragraph"""
    out = list(paras)
    for i, p in enumerate(paras, 1):
        if not sel(i, p):
            continue
        t = list(p)
        j = head(p, 0, len(p))
        if j is not None and t[j].isupper():
            t[j] = t[j].lower()
        sp = next(((a, b) for a, b in sents(p) if KEY in p[a:b].lower()), None)
        if sp:
            k = tail(p, *sp)
            if k is not None and t[k].islower():
                t[k] = t[k].upper()
        out[i - 1] = "".join(t)
    return out


W1, W2, W3 = [5, 6, 7, 8], [93, 94, 95, 96], [168, 169, 170, 171]
REP = [231, 232, 233, 235]
ALL = range(1, len(P) + 1)

SELECTORS = [
    ("all", lambda i, p: True),
    ("sign", lambda i, p: KEY in p.lower()),
    ("FWinit", lambda i, p: re.match(r'\s*["\u201c(\[]*[FW]', p) is not None),
    ("nonITASM", lambda i, p: (head(p, 0, len(p)) is not None and
                               p[head(p, 0, len(p))].upper() not in "ITASM")),
    ("ITASM", lambda i, p: (head(p, 0, len(p)) is not None and
                            p[head(p, 0, len(p))].upper() in "ITASM")),
    ("W1", lambda i, p: i in W1),
    ("W2", lambda i, p: i in W2),
    ("W3", lambda i, p: i in W3),
    ("REP", lambda i, p: i in REP),
    ("partI", lambda i, p: 2 <= i <= 87),
    ("partII", lambda i, p: 88 <= i <= 162),
    ("partIII", lambda i, p: 163 <= i <= 273),
]

CAND = []
for unit in ("paragraph", "sentence", "word"):
    for name, sel in SELECTORS:
        CAND.append((f"{unit}/{name}", unit, name, sel))
CAND.append(("demo-shape/all", "demo", "all", SELECTORS[0][1]))
CAND.append(("demo-shape/sign", "demo", "sign", SELECTORS[1][1]))
CAND.append(("demo-shape/nonITASM", "demo", "nonITASM", SELECTORS[3][1]))

rows, hits = [], 0
for label, unit, sname, sel in CAND:
    paras = apply_demo(P, sel) if unit == "demo" else apply_units(P, unit, sel)
    for sep, jn in (("\n\n", "LF"), ("\r\n\r\n", "CRLF")):
        text = sep.join(paras)
        h = hashlib.md5(text.encode("utf-8")).hexdigest()
        a = addrs(h)
        hit = [k for k, v in a.items() if v in (LIVE, OLD)]
        bal = sum(x.isupper() for x in text) - sum(x.isupper() for x in sep.join(P))
        rows.append({"label": label, "join": jn, "md5": h, "addr0": a[0], "hits": hit, "d_caps": bal})
        if hit:
            hits += 1
            print("  *** HIT", label, jn, h, hit, flush=True)
        print(f"  {label:26s} {jn:4s} caps{bal:+4d} {h} {a[0]}", flush=True)

json.dump(rows, open("unit_topology_results.json", "w"), indent=1)
print(f"\n{len(rows)} texts, {len(rows)*len(IDX)} derivations, {hits} hits, "
      f"all balanced: {all(r['d_caps'] == 0 for r in rows)}")
