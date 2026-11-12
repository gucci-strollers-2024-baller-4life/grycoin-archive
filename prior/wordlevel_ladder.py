#!/usr/bin/env python3
"""wordlevel_ladder.py - the word-level rung from STRUCTURAL_BLUEPRINT_2026-10-31.md section 4.

Unit of analysis moves from paragraph to word edge, inside the designated structural windows.
Every candidate is a named hypothesis. No positional enumeration.

  W1  raise the final letter of the 12 terminal words of the three FFWW windows
      (keys/that/again/them, purposes/budget/emission/them, this/object/Dorian/them).
      This is the letter that spells STNM, made visible in case.
  W2  W1 plus paragraph-initial lowering in the same 12 paragraphs (the demo's two-edge pair,
      applied at the window).
  W3  same as W1 over the 12 "recognize the signs" paragraphs (S3).
  W4  same as W1 over para 222 + the Finney reprint 231-235 (S5).
  W5  the word the rule actually names: para 222's first four and last four words (the operands of
      para 242). Raise the final letter of each of the 8 words.
  W6  the sign letters themselves, at word edges: inside each window paragraph, uppercase every
      word-edge occurrence of that paragraph's STNM letter (s, t, n, m).
  W7  signs are recognized by initial letter and LOWERED (the demo's direction, I -> i), applied at
      word level inside the selection set: every word beginning with {I,T,A,S,M} is lowered.
      W7a windows, W7b S3, W7c S5.

Serializations: \\n\\n and \\r\\n\\r\\n, each with and without trailing separator.
Indices: 0, 1, 2, 5, 6, 7, 44, 76, 77.  Target: 14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W (live only).
"""
import json, sys, re, hashlib
sys.path.insert(0, "harness")
import btc

PARAS = [t for _, t in json.load(open("wp_paras.json"))]
SIGN = "ITASM"
TARGET = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
RETIRED = {
    "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC": "rbb_old_refunded",
    "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi": "demo_drained",
}
INDICES = [0, 1, 2, 5, 6, 7, 44, 76, 77]
SEPS = [("\n\n", "LF"), ("\r\n\r\n", "CRLF")]

WIN = {5: "s", 6: "t", 7: "n", 8: "m",
       93: "s", 94: "t", 95: "n", 96: "m",
       168: "s", 169: "t", 170: "n", 171: "m"}
S3 = {20, 42, 220, 222, 223, 225, 226, 230, 236, 244, 246, 273}
S5 = {222, 231, 232, 233, 234, 235}


def last_alpha(t):
    for i in range(len(t) - 1, -1, -1):
        if t[i].isalpha():
            return i
    return None


def first_alpha(t):
    for i, c in enumerate(t):
        if c.isalpha():
            return i
    return None


def words_with_spans(t):
    return [(m.group(0), m.start(), m.end()) for m in re.finditer(r"[A-Za-z']+", t)]


def w1(t):
    """raise final letter of the paragraph's last word"""
    out = list(t)
    k = last_alpha(t)
    if k is not None:
        out[k] = out[k].upper()
    return "".join(out)


def w1_plus_init_down(t):
    out = list(w1(t))
    j = first_alpha(t)
    if j is not None:
        out[j] = out[j].lower()
    return "".join(out)


def w6(t, letter):
    """uppercase word-edge occurrences of `letter` in this paragraph"""
    out = list(t)
    for word, a, b in words_with_spans(t):
        if word[0].lower() == letter:
            out[a] = word[0].upper()
        if word[-1].lower() == letter:
            out[b - 1] = word[-1].upper()
    return "".join(out)


def w7(t):
    """lower every word-initial sign letter"""
    out = list(t)
    for word, a, b in words_with_spans(t):
        j = first_alpha(word)
        if j is not None and word[j].upper() in SIGN:
            out[a + j] = out[a + j].lower()
    return "".join(out)


def para222_operands():
    """indices of the 8 operand words: first four and last four words of para 222"""
    t = PARAS[221]
    spans = words_with_spans(t)
    return [spans[:4], spans[-4:]]


def build(sep, trail, edits):
    out = list(PARAS)
    for i, fn in edits.items():
        out[i - 1] = fn(PARAS[i - 1])
    return sep.join(out) + (sep if trail else "")


def addrs_for(md5hex):
    ent = bytes.fromhex(md5hex)
    m = btc.entropy_to_mnemonic(ent)
    k, c = btc.master_key(btc.mnemonic_seed(m))
    for depth in (44 + btc.H, 0 + btc.H, 0 + btc.H, 0):
        k, c = btc.ckd_priv(k, c, depth)
    return {i: btc.p2pkh(btc.pubkey(btc.ckd_priv(k, c, i)[0])) for i in INDICES}


def main():
    variants = []
    variants.append(("W1/windows-final-up", {i: w1 for i in WIN}))
    variants.append(("W2/windows-final-up+init-down", {i: w1_plus_init_down for i in WIN}))
    variants.append(("W3/signs-paras-final-up", {i: w1 for i in S3}))
    variants.append(("W4/reprint-final-up", {i: w1 for i in S5}))
    for name, sel, fn in (("W7a/windows", set(WIN), w7), ("W7b/S3", S3, w7), ("W7c/S5", S5, w7)):
        variants.append((name, {i: fn for i in sel}))

    # W5: the 8 operand words of para 222, final letter raised
    spans_rows = para222_operands()
    pos = {a + j for row in spans_rows for _, a, b in row for j in (b - a - 1,)}

    def w5_fn(t):
        out = list(t)
        for p in pos:
            out[p] = out[p].upper()
        return "".join(out)

    variants.append(("W5/para222-operand-words-final-up", {222: w5_fn}))

    # W6: word-edge occurrences of each window paragraph's own STNM letter
    variants.append(("W6/windows-STNM-letter-at-word-edges",
                     {i: (lambda t, L=L: w6(t, L)) for i, L in WIN.items()}))

    base_md5 = {}
    for sep, name in SEPS:
        for trail in (False, True):
            base_md5[name + ("+t" if trail else "")] = btc.md5_hex(sep.join(PARAS) + (sep if trail else ""))

    rows, hits = [], []
    for tag, edits in variants:
        for sep, sname in SEPS:
            for trail in (False, True):
                text = build(sep, trail, edits)
                h = btc.md5_hex(text)
                a = addrs_for(h)
                found = [k for i, v in a.items() if v == TARGET for k in [f"index {i}"]]
                dead = [(i, RETIRED[v]) for i, v in a.items() if v in RETIRED]
                noop = (h == base_md5[sname + ("+t" if trail else "")])
                lab = f"{tag}/{sname}{'+t' if trail else ''}"
                rows.append({"tag": lab, "md5": h, "addr0": a[0], "hits": found,
                             "retired_hits": dead, "noop": noop})
                print(f"{lab:44s} md5={h} addr0={a[0]}"
                      + ("  [no-op: equals base]" if noop else ""), flush=True)
                if found:
                    hits.append(rows[-1])
                    print("  *** HIT ***", found)

    json.dump(rows, open("wordlevel_ladder_results.json", "w"), indent=1)
    print(f"\nderivations: {len(rows)}  distinct md5: {len({r['md5'] for r in rows})}"
          f"  hits: {len(hits)}  no-ops: {sum(r['noop'] for r in rows)}")


if __name__ == "__main__":
    main()
