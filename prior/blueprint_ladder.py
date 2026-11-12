#!/usr/bin/env python3
"""blueprint_ladder.py - five-derivation ladder from STRUCTURAL_BLUEPRINT_2026-10-31.md.

No sweeps. Each derivation is one hypothesis named in the blueprint:

  serializations  sep in {"\\n\\n", "\\r\\n\\r\\n"} x trailing-newline {no, yes}
  S1  in-class initials {I,T,A,S,M}, first character          (demo paras 5-8, literal)
  S2  in-class initials {I,T,A,S,M}, first alphabetic char    (dialogue-tolerant variant)
  S3  paragraphs that say "recognize the signs"               (demo allow-set logic)
  S4  the three FFWW windows 5-8, 93-96, 168-171              (STNM markers)
  S5  para 222 + the Finney reprint 231-235                   (rulebook-adjacent container)

  modes  both      paragraph-initial down + first-sentence-final up   [author's geometry]
         down      paragraph-initial down only
         up        first-sentence-final up only
         both_para paragraph-initial down + paragraph-final up        [falsified control]

Pipeline: text -> MD5 -> BIP39-12 -> PBKDF2 -> m/44'/0'/0'/0/i -> P2PKH, i in the hunt's index set.
"""
import json, sys
sys.path.insert(0, "harness")
import btc

PARAS = [t for _, t in json.load(open("wp_paras.json"))]
SIGN = "ITASM"

ORACLES = {
    "rbb_live": "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W",
    "rbb_old_refunded": "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC",
    "demo": "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi",
}
INDICES = [0, 1, 2, 5, 6, 7, 44, 76, 77]
SEPS = [("\n\n", "LF"), ("\r\n\r\n", "CRLF")]
WINDOWS = {5, 6, 7, 8, 93, 94, 95, 96, 168, 169, 170, 171}
REPRINT = {222, 231, 232, 233, 234, 235}
STOP = ".?!"


def first_sentence(t):
    for i, ch in enumerate(t):
        if ch in STOP:
            return t[: i + 1]
    return t


def first_alpha(t, end=None):
    end = len(t) if end is None else end
    for i in range(end):
        if t[i].isalpha():
            return i
    return None


def last_alpha(t, end):
    for i in range(end - 1, -1, -1):
        if t[i].isalpha():
            return i
    return None


def mark_para(t, up_target):
    """up_target: 'sent' | 'para' | None"""
    out = list(t)
    j = first_alpha(t)
    if j is not None:
        out[j] = out[j].lower()
    if up_target:
        end = len(t) if up_target == "para" else len(first_sentence(t))
        k = last_alpha(t, end)
        if k is not None:
            out[k] = out[k].upper()
    return "".join(out)


def mark_up_only(t):
    out = list(t)
    k = last_alpha(t, len(first_sentence(t)))
    if k is not None:
        out[k] = out[k].upper()
    return "".join(out)


def select(kind):
    if kind == "S1":
        return {i for i, t in enumerate(PARAS, 1) if t[:1].isalpha() and t[:1].upper() in SIGN}
    if kind == "S2":
        return {i for i, t in enumerate(PARAS, 1)
                if (j := first_alpha(t)) is not None and t[j].upper() in SIGN}
    if kind == "S3":
        return {i for i, t in enumerate(PARAS, 1) if "recognize the signs" in t.lower()}
    if kind == "S4":
        return set(WINDOWS)
    if kind == "S5":
        return set(REPRINT)
    raise ValueError(kind)


def build(sep, trail, sel, mode):
    out = []
    for i, t in enumerate(PARAS, 1):
        if i not in sel:
            out.append(t)
        elif mode == "down":
            out.append(mark_para(t, None))
        elif mode == "up":
            out.append(mark_up_only(t))
        elif mode == "both":
            out.append(mark_para(t, "sent"))
        elif mode == "both_para":
            out.append(mark_para(t, "para"))
        else:
            raise ValueError(mode)
    return sep.join(out) + (sep if trail else "")


def addrs_for(md5hex):
    ent = bytes.fromhex(md5hex)
    m = btc.entropy_to_mnemonic(ent)
    seed = btc.mnemonic_seed(m)
    acct = btc.derive_path(seed, (44 + btc.H, 0 + btc.H, 0 + btc.H, 0))
    # recover account chain code by replaying the path
    k, c = btc.master_key(seed)
    for depth in (44 + btc.H, 0 + btc.H, 0 + btc.H, 0):
        k, c = btc.ckd_priv(k, c, depth)
    assert k == acct
    res = {}
    for i in INDICES:
        ki, _ = btc.ckd_priv(acct, c, i)
        res[i] = btc.p2pkh(btc.pubkey(ki))
    return m, res


def main():
    rows, hits = [], []

    for sep, name in SEPS:
        for trail in (False, True):
            base = sep.join(PARAS) + (sep if trail else "")
            h = btc.md5_hex(base)
            m, a = addrs_for(h)
            found = [(i, k) for i, v in a.items() for k, ov in ORACLES.items() if v == ov]
            rows.append({"tag": f"BASE-{name}{'+t' if trail else ''}", "n": 273, "set": "-",
                         "md5": h, "addrs": {str(k): v for k, v in a.items()}, "hits": found})
            print(f"BASE-{name}{'+t' if trail else '':4s} md5={h} addr@0={a[0]} hits={found}", flush=True)
            if found:
                hits.append(rows[-1])

    for sel_kind in ("S1", "S2", "S3", "S4", "S5"):
        sel = select(sel_kind)
        for mode in ("both", "down", "up", "both_para"):
            for sep, name in SEPS:
                for trail in (False, True):
                    text = build(sep, trail, sel, mode)
                    h = btc.md5_hex(text)
                    m, a = addrs_for(h)
                    found = [(i, k) for i, v in a.items() for k, ov in ORACLES.items() if v == ov]
                    tag = f"{sel_kind}/{mode}/{name}{'+t' if trail else ''}"
                    rows.append({"tag": tag, "n": len(sel), "set": sel_kind, "md5": h,
                                 "addrs": {str(k): v for k, v in a.items()}, "hits": found})
                    print(f"{tag:26s} n={len(sel):3d} md5={h}", flush=True)
                    if found:
                        hits.append(rows[-1])
                        print("  *** HIT ***", found)
    json.dump(rows, open("blueprint_ladder_results.json", "w"), indent=1)
    print(f"\nderivations: {len(rows)}  hits: {len(hits)}")
    for h in hits:
        print("HIT", h["tag"], h["hits"])


if __name__ == "__main__":
    main()
