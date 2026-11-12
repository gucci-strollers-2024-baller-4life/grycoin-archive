#!/usr/bin/env python3
"""container_probe.py - the container question: is the hashed object a division rather than the document?

STRUCTURE_MAP.md gives the divisions; the live part gives their exact heading paragraphs (28 of them,
each wrapped in <b> in the published HTML). Every heading-to-heading span is a candidate container,
under two boundary conventions:

  body   heading+1 .. next(heading)-1     a human copying the section copies this
  head   heading   .. next(heading)-1     the document's own serialization, heading included

Marking rules, applied only to paragraphs inside the container:

  plain   no case changes  (the container hypothesis proper)
  geom    the validated geometry: paragraph-initial down + first-sentence-final up, on paragraphs
          whose first letter is a recognized sign {I,T,A,S,M}
  win     raise the final letter of the terminal words of the three FFWW windows that fall inside
          the container (the STNM letters made visible)

Serializations: \\n\\n and \\r\\n\\r\\n, each with and without a trailing separator.
Indices: 0, 1, 2, 5, 6, 7, 44, 76, 77.  Target: 14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W.
"""
import json, re, sys
sys.path.insert(0, "harness")
import btc

TARGET = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
DEMO = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
INDICES = [0, 1, 2, 5, 6, 7, 44, 76, 77]
SEPS = [("\n\n", "LF"), ("\r\n\r\n", "CRLF")]
SIGN = "ITASM"
WIN = {5, 6, 7, 8, 93, 94, 95, 96, 168, 169, 170, 171}

P = [t for _, t in json.load(open("wp_paras.json"))]
HEAD = [1, 2, 3, 54, 71, 88, 89, 91, 115, 130, 152, 157, 161, 163, 164, 175, 176,
        182, 209, 215, 247, 250, 252, 254, 256, 258, 260, 265]
N = len(P)


def fa(t):
    return next((i for i, c in enumerate(t) if c.isalpha()), None)


def first_sentence(t):
    for i, c in enumerate(t):
        if c in ".?!":
            return t[: i + 1]
    return t


def geom(t):
    o = list(t)
    j = fa(t)
    if j is not None:
        o[j] = o[j].lower()
    end = len(first_sentence(t))
    k = next((i for i in range(end - 1, -1, -1) if t[i].isalpha()), None)
    if k is not None:
        o[k] = o[k].upper()
    return "".join(o)


def winmark(t):
    o = list(t)
    k = next((i for i in range(len(t) - 1, -1, -1) if t[i].isalpha()), None)
    if k is not None:
        o[k] = o[k].upper()
    return "".join(o)


def body(lo, hi, rule):
    out = []
    for i in range(lo, hi + 1):
        t = P[i - 1]
        if rule == "plain":
            out.append(t)
        elif rule == "geom":
            j = fa(t)
            out.append(geom(t) if (j is not None and t[j].upper() in SIGN) else t)
        elif rule == "win":
            out.append(winmark(t) if i in WIN else t)
    return out


def addrs(h):
    k, c = btc.master_key(btc.mnemonic_seed(btc.entropy_to_mnemonic(bytes.fromhex(h))))
    for d in (44 + btc.H, 0 + btc.H, 0 + btc.H, 0):
        k, c = btc.ckd_priv(k, c, d)
    return {i: btc.p2pkh(btc.pubkey(btc.ckd_priv(k, c, i)[0])) for i in INDICES}


def spans():
    out = [("WHOLE", 1, N)]
    for idx, h in enumerate(HEAD):
        nxt = HEAD[idx + 1] if idx + 1 < len(HEAD) else N + 1
        name = re.sub(r"[^A-Za-z0-9]+", "-", P[h - 1]).strip("-")[:34]
        out.append((f"body/{h}/{name}", h + 1, nxt - 1))
        out.append((f"head/{h}/{name}", h, nxt - 1))
    # part-level and composite spans from STRUCTURE_MAP.md, which heading-to-heading cannot express
    out += [
        ("PART-I", 2, 87), ("PART-I/body", 3, 87),
        ("PART-II", 88, 162), ("PART-II/body", 89, 162),
        ("PART-III", 163, 273), ("PART-III/body", 164, 273),
        ("III-2/Satoshi-Code", 175, 246), ("III-2/Satoshi-Code/body", 176, 246),
        ("III-2d/Outing", 215, 246), ("III-2d/Outing/body", 216, 246),
        ("WHOLE/no-title", 2, 273),
    ]
    return [(t, a, b) for t, a, b in out if a <= b]


def main():
    rows, hits = [], []
    for tag, lo, hi in spans():
        for rule in ("plain", "geom", "win"):
            for sep, sname in SEPS:
                for trail in (False, True):
                    txt = sep.join(body(lo, hi, rule)) + (sep if trail else "")
                    h = btc.md5_hex(txt)
                    a = addrs(h)
                    hit = [(i, "live") for i, v in a.items() if v == TARGET] + \
                          [(i, "old") for i, v in a.items() if v == OLD] + \
                          [(i, "demo") for i, v in a.items() if v == DEMO]
                    rows.append({"tag": tag, "lo": lo, "hi": hi, "n": hi - lo + 1, "rule": rule,
                                 "ser": f"{sname}{'+t' if trail else ''}", "md5": h,
                                 "addr0": a[0], "hits": hit})
                    if hit:
                        hits.append(rows[-1])
                        print("*** HIT ***", rows[-1]["tag"], rule, rows[-1]["ser"], hit, flush=True)
        print(f"  {tag:44s} {lo:3d}-{hi:3d} done", flush=True)
    json.dump(rows, open("container_probe_results.json", "w"), indent=1)
    print(f"\nderivations: {len(rows)}  distinct md5: {len({r['md5'] for r in rows})}"
          f"  hits: {len(hits)}")


if __name__ == "__main__":
    main()
