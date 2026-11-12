#!/usr/bin/env python3
"""br_layer_probe.py - the intra-paragraph break layer, found while auditing the word rung.

Ten paragraphs of the live part carry a `<br>` inside them. `wp_paras.json` (and therefore every
candidate this hunt has ever hashed) flattens those breaks with NO replacement, so the text contains
`already?""Of course` and `"THOMAS".Satoshi` with two words glued. Wattpad's p-id agrees with that
glued form, but a p-id is a tag-stripping dedup hash: it certifies what the *platform* computes, not
what the author typed.

So for ten paragraphs the hashed form is one of at least four renderings, and every candidate so far
has used the least human of them.

  renderings: "" (current), " ", "\\n", "\\r\\n"
  block seps: "\\n\\n", "\\r\\n\\r\\n"
  plus the two strongest marking rules crossed with the two plausible renderings
"""
import json, re, sys, html
sys.path.insert(0, "harness")
import btc

TARGET = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
INDICES = [0, 1, 2, 5, 6, 7, 44, 76, 77]
RAW = open("../live_chapter.txt", encoding="utf-8", errors="replace").read()
LIVE = [(pid, t) for pid, t in re.findall(r'<p[^>]*data-p-id="([^"]+)"[^>]*>(.*?)</p>', RAW, re.S)]
BASE = [t for _, t in json.load(open("wp_paras.json"))]
BR = {i for i, (_, t) in enumerate(LIVE, 1) if "<br" in t.lower()}
SIGN = "ITASM"


def render(br):
    """rebuild the 273 paragraph texts with <br> rendered as `br`"""
    out = list(BASE)
    for i in BR:
        t = LIVE[i - 1][1]
        t = re.sub(r"<br\s*/?>", br.replace("\n", "\x00").replace("\r", "\x01"), t)
        t = re.sub(r"<[^>]+>", "", t)
        t = html.unescape(t).replace("\x00", "\n").replace("\x01", "\r")
        out[i - 1] = t
    return out


def first_sentence(t):
    for i, c in enumerate(t):
        if c in ".?!":
            return t[: i + 1]
    return t


def fa(t, end=None):
    end = len(t) if end is None else end
    return next((i for i in range(end) if t[i].isalpha()), None)


def la(t, end):
    return next((i for i in range(end - 1, -1, -1) if t[i].isalpha()), None)


def mark_both(t):
    o = list(t)
    j = fa(t)
    if j is not None:
        o[j] = o[j].lower()
    k = la(t, len(first_sentence(t)))
    if k is not None:
        o[k] = o[k].upper()
    return "".join(o)


def sel(kind, paras):
    if kind == "S1":
        return {i for i, t in enumerate(paras, 1) if t[:1].isalpha() and t[:1].upper() in SIGN}
    if kind == "S3":
        return {i for i, t in enumerate(paras, 1) if "recognize the signs" in t.lower()}
    if kind == "S4":
        return {5, 6, 7, 8, 93, 94, 95, 96, 168, 169, 170, 171}
    raise ValueError(kind)


def addrs(h):
    k, c = btc.master_key(btc.mnemonic_seed(btc.entropy_to_mnemonic(bytes.fromhex(h))))
    for d in (44 + btc.H, 0 + btc.H, 0 + btc.H, 0):
        k, c = btc.ckd_priv(k, c, d)
    return {i: btc.p2pkh(btc.pubkey(btc.ckd_priv(k, c, i)[0])) for i in INDICES}


def run(rows, tag, paras, sep, trail=False, marking=None):
    if marking:
        m = set(sel(marking, paras))
        paras = [mark_both(t) if i in m else t for i, t in enumerate(paras, 1)]
    text = sep.join(paras) + (sep if trail else "")
    h = btc.md5_hex(text)
    a = addrs(h)
    hit = [i for i, v in a.items() if v == TARGET]
    rows.append({"tag": tag, "md5": h, "addr0": a[0], "hits": hit})
    print(f"{tag:52s} md5={h} addr0={a[0]}" + ("  *** HIT ***" if hit else ""), flush=True)


def main():
    print("paragraphs carrying an intra-paragraph break:", sorted(BR))
    rows = []
    for br, bname in (("", "none"), (" ", "space"), ("\n", "LF"), ("\r\n", "CRLF")):
        paras = render(br)
        for sep, sname in (("\n\n", "LFsep"), ("\r\n\r\n", "CRLFsep")):
            run(rows, f"BR={bname}/{sname}", paras, sep)
    for br, bname in ((" ", "space"), ("\n", "LF"), ("\r\n", "CRLF")):
        paras = render(br)
        for kind in ("S1", "S3", "S4"):
            run(rows, f"BR={bname}/LFsep/{kind}/both", paras, "\n\n", False, kind)
    json.dump(rows, open("br_layer_probe_results.json", "w"), indent=1)
    print(f"\nderivations: {len(rows)}  distinct md5: {len({r['md5'] for r in rows})}"
          f"  hits: {sum(1 for r in rows if r['hits'])}")


if __name__ == "__main__":
    main()
