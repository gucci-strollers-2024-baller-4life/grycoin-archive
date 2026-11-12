"""Edge-class census of the 273-paragraph chapter, and the closure it implies.

Purpose: turn the four-window result from a sampled negative into a whole-corpus
closure, or show that it cannot be one.

Argument under test
-------------------
A site of the signature (initials reading FFWW in order, finals reading stnm in
order) consumes, at its second member, a paragraph that starts with F and ends
with t (`F...t`). If the chapter contains exactly four `F...t` paragraphs and all
four sit inside the four known windows, then no fifth site and no disjoint
"octave" can exist anywhere in the chapter, because there is no stray `F...t`
left to place in the second slot.

This script computes, from the text alone:
  1. the edge-class census (initial x final pairs) over all 273 paragraphs
  2. every `F...t` paragraph, and which known window consumes it
  3. an exhaustive search for sites under both readings of the signature:
       contiguous   - four consecutive paragraphs
       Hal-form     - four of five consecutive, one paragraph skipped
       loose span   - any four of up to eight consecutive
     each requiring initials (order-free) FFWW and finals (in order) stnm
  4. the W4 provenance check and the `Fast forward` count
  5. the ¶229 scoping test: {I,T,A,S,M} exclusion applied at 16-paragraph scope
     (hal_original.txt) and at section/16-window scope over the chapter

Reads:  ../wp_paras_br.json
Writes: ../ft_closure_results.json
"""
import json, os, re, sys, time, hashlib
import itertools
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SIG_INI = "FFWW"
SIG_FIN = "stnm"
WINDOWS = {
    "W1": (5, 6, 7, 8),
    "W2": (93, 94, 95, 96),
    "W3": (168, 169, 170, 171),
    "W4": (231, 232, 233, 235),   # Hal-form: ¶234 (I...) skipped
}
ITASM = set("ITASM")


def load():
    d = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    return [("\n".join(x) if isinstance(x, list) else x) for x in ps]


def ini(p):
    c = next((c for c in p if c.isalpha()), "")
    return c.upper()


def fin(p):
    c = next((c for c in reversed(p) if c.isalpha()), "")
    return c.lower()


def first_word(p):
    m = re.search(r"[A-Za-z']+", p)
    return m.group(0) if m else ""


def last_word(p):
    m = re.findall(r"[A-Za-z']+", p)
    return m[-1] if m else ""


def main():
    paras = load()
    n = len(paras)
    assert n == 273, f"expected 273 paragraphs, got {n}"
    I = [ini(p) for p in paras]
    F = [fin(p) for p in paras]
    out = {"paragraphs": n}

    # ---- 1. edge-class census -------------------------------------------------
    pairs = Counter(zip(I, F))
    census = [{"initial": a, "final": b, "count": c,
               "positions": [i + 1 for i in range(n) if I[i] == a and F[i] == b]}
              for (a, b), c in sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0]))]
    out["edge_census"] = census
    out["initial_counts"] = dict(Counter(I).most_common())
    out["final_counts"] = dict(Counter(F).most_common())

    # ---- 2. the F...t class and who consumes it -------------------------------
    ft = [i + 1 for i in range(n) if I[i] == "F" and F[i] == "t"]
    consumed = {}
    for name, w in WINDOWS.items():
        for p in w:
            if p in ft:
                consumed[p] = name
    out["Ft_positions"] = ft
    out["Ft_count"] = len(ft)
    out["Ft_consumed_by"] = consumed
    out["Ft_unconsumed"] = [p for p in ft if p not in consumed]
    out["Ft_detail"] = [{"pos": p, "first_word": first_word(paras[p - 1]),
                         "last_word": last_word(paras[p - 1]),
                         "chars": len(paras[p - 1]),
                         "window": consumed.get(p)} for p in ft]

    # ---- 3. exhaustive site search under three readings -----------------------
    def is_site(idx):
        return ("".join(sorted(I[j] for j in idx)) == SIG_INI
                and "".join(F[j] for j in idx) == SIG_FIN)

    sites = {"contiguous4": [], "hal_form5": [], "span_upto8": []}
    for i in range(n - 3):
        if is_site(range(i, i + 4)):
            sites["contiguous4"].append([j + 1 for j in range(i, i + 4)])
    for i in range(n - 4):
        for skip in range(5):
            idx = [i + k for k in range(5) if k != skip]
            if is_site(idx):
                sites["hal_form5"].append([j + 1 for j in idx])
    for L in range(4, 9):
        for i in range(n - L + 1):
            span = list(range(i, i + L))
            for combo in itertools.combinations(span, 4):
                if "".join(F[j] for j in combo) == SIG_FIN:
                    if "".join(sorted(I[j] for j in combo)) == SIG_INI:
                        sites["span_upto8"].append([j + 1 for j in combo])
    # dedupe while keeping order, for the report
    for k in sites:
        seen, uniq = set(), []
        for s in sites[k]:
            t = tuple(s)
            if t not in seen:
                seen.add(t)
                uniq.append(s)
        sites[k] = uniq
    out["sites"] = {k: {"count": len(v), "list": v} for k, v in sites.items()}

    # does any site exist outside the four known windows?
    known = set()
    for w in WINDOWS.values():
        known.update(w)
    out["sites_outside_known_windows"] = {
        k: [s for s in v if set(s) - known] for k, v in sites.items() if
        [s for s in v if set(s) - known]
    }

    # ---- 3b. exact enumeration of every site at unbounded span ----------------
    # finals must read s,t,n,m in order and initials must be two F and two W, so
    # the second member is necessarily an F...t paragraph. Only four exist.
    def cls(a, b):
        return [i + 1 for i in range(n) if I[i] == a and F[i] == b]
    Fs, Ft, Wn, Wm = cls("F", "s"), cls("F", "t"), cls("W", "n"), cls("W", "m")
    loose, anchor_tally = [], {}
    for a in Ft:
        A = [p for p in Fs if p < a]
        Wn_a = [p for p in Wn if p > a]
        Wm_a = [p for p in Wm if p > a]
        cnt = 0
        for x in A:
            for y in Wn_a:
                for z in Wm_a:
                    if y < z:
                        loose.append([x, a, y, z])
                        cnt += 1
        anchor_tally[a] = {"F_s_before": len(A), "W_n_after": len(Wn_a),
                           "W_m_after": len(Wm_a), "sites": cnt}
    out["loose_sites"] = {"classes": {"F_s": Fs, "F_t": Ft, "W_n": Wn, "W_m": Wm},
                          "count": len(loose), "anchor_tally": anchor_tally,
                          "list": loose}
    out["loose_sites_outside_known_windows"] = [
        s for s in loose if set(s) - known]
    out["loose_sites_fully_inside_known"] = [
        s for s in loose if not (set(s) - known)]

    # ---- 3c. derive every loose site: the closure, settled by exhaustion ------
    import sys as _s
    _s.path.insert(0, HERE)
    import sixteen_matrix as sm
    t0 = time.time()
    hits, ntexts = [], 0
    for site in loose:
        quad0 = [p - 1 for p in site]
        marked = sm.mark(paras, quad0)
        for blob, tag in sm.serialisations(marked):
            ntexts += 1
            h = hashlib.md5(blob).hexdigest()
            for i, a in sm.addrs(h).items():
                if a == sm.ESCROW:
                    hits.append({"site": site, "serialisation": tag,
                                 "md5": h, "index": i})
    out["loose_site_sweep"] = {
        "sites": len(loose), "texts": ntexts,
        "derivations": ntexts * len(sm.IDX), "elapsed_s": round(time.time() - t0, 2),
        "escrow": sm.ESCROW, "indices": list(sm.IDX), "hits": hits,
    }

    # ---- 3d. the ¶238 adjacency reading: windows plus their I anchors --------
    # In hal_original.txt the I paragraph sits inside the four (¶5, between ¶4
    # and ¶6). In the chapter's three novel windows it sits immediately before.
    ANCHOR = {"W1": 4, "W2": 92, "W3": 167, "W4": 234}
    penta = {name: sorted(list(w) + [ANCHOR[name]]) for name, w in WINDOWS.items()}
    sels = set()
    for name, pen in penta.items():
        for r in range(1, len(pen) + 1):
            for combo in itertools.combinations(pen, r):
                sels.add(combo)
        w = WINDOWS[name]
        for drop in w:            # anchor substituted for each window member
            sels.add(tuple(sorted([ANCHOR[name]] + [x for x in w if x != drop])))
    names = list(WINDOWS)
    for r in (2, 3, 4):           # unions of whole pentads
        for combo in itertools.combinations(names, r):
            u = []
            for nm in combo:
                u += penta[nm]
            sels.add(tuple(sorted(set(u))))
    sels = sorted(sels, key=lambda t: (len(t), t))
    t0 = time.time()
    phits, ptexts = [], 0
    for sel in sels:
        marked = sm.mark(paras, [q - 1 for q in sel])
        for blob, tag in sm.serialisations(marked):
            ptexts += 1
            h = hashlib.md5(blob).hexdigest()
            for i, a in sm.addrs(h).items():
                if a == sm.ESCROW:
                    phits.append({"selection": list(sel), "serialisation": tag,
                                  "md5": h, "index": i})
    out["pentad"] = {
        "anchors": ANCHOR,
        "pentads": {k: v for k, v in penta.items()},
        "anchor_finals": {str(a): {"first": I[a - 1], "final": F[a - 1],
                                   "final_word": last_word(paras[a - 1]),
                                   "chars": len(paras[a - 1])} for a in ANCHOR.values()},
        "selections": len(sels), "texts": ptexts,
        "derivations": ptexts * len(sm.IDX),
        "elapsed_s": round(time.time() - t0, 2), "hits": phits,
    }

    # ---- 3e. what the terminal letters actually are ---------------------------
    lw = [(re.findall(r"[A-Za-z']+", p) or [""])[-1].lower() for p in paras]
    out["terminal_words"] = {
        name: {"last_words": [lw[q - 1] for q in w],
               "last_letters": "".join(F[q - 1] for q in w)}
        for name, w in WINDOWS.items()}
    out["them_paragraphs"] = [i + 1 for i, w in enumerate(lw) if w == "them"]
    out["them_starting_W"] = [i + 1 for i, w in enumerate(lw)
                              if w == "them" and I[i] == "W"]

    # ---- 4. window certification, W4 provenance, Fast forward -----------------
    win = {}
    for name, w in WINDOWS.items():
        win[name] = {
            "paragraphs": list(w),
            "initials": "".join(I[p - 1] for p in w),
            "finals": "".join(F[p - 1] for p in w),
            "first_words": [first_word(paras[p - 1]) for p in w],
            "last_words": [last_word(paras[p - 1]) for p in w],
            "chars": [len(paras[p - 1]) for p in w],
        }
    out["windows"] = win
    ff = [i + 1 for i, p in enumerate(paras) if "fast forward" in p.lower()]
    out["fast_forward_positions"] = ff
    out["fast_forward_count"] = len(ff)

    # ---- 5. the ITASM exclusion scope test -----------------------------------
    def nonitasm(idx):
        return [j + 1 for j in idx if I[j] not in ITASM]

    hal = open(os.path.join(ROOT, "hal_original.txt"), encoding="utf-8").read()
    hal_paras = [p.strip() for p in re.split(r"\n\s*\n", hal) if p.strip()]
    hal_hits = [i + 1 for i, p in enumerate(hal_paras) if ini(p) not in ITASM]
    out["itasm_scope"] = {
        "hal_paragraphs": len(hal_paras),
        "hal_nonitasm": hal_hits,
        "hal_nonitasm_initials": "".join(ini(hal_paras[i - 1]) for i in hal_hits),
        "hal_nonitasm_finals": "".join(fin(hal_paras[i - 1]) for i in hal_hits),
    }
    # 16-paragraph scope slid across the chapter
    counts16 = Counter()
    for i in range(n - 15):
        counts16[len(nonitasm(range(i, i + 16)))] += 1
    # section scope: paragraph clusters separated by the chapter's own headers,
    # if any exist; otherwise the whole chapter counts as one section
    sec_counts = {"whole_chapter": len(nonitasm(range(n)))}
    out["itasm_scope"].update({
        "chapter_nonitasm_total": len(nonitasm(range(n))),
        "chapter_nonitasm_positions_count": len(nonitasm(range(n))),
        "sliding16_range": [min(counts16), max(counts16)],
        "sliding16_histogram": dict(sorted(counts16.items())),
        "sliding16_windows_with_exactly_four": sum(
            1 for i in range(n - 15) if len(nonitasm(range(i, i + 16))) == 4),
        "whole_chapter_as_one_scope": sec_counts,
    })
    # do any 16-windows reproduce {2,3,4,6}-style behaviour, i.e. four non-ITASM
    # paragraphs spelling FFWW with finals stnm?
    hits16 = []
    for i in range(n - 15):
        sel = nonitasm(range(i, i + 16))
        if len(sel) >= 4:
            for combo in itertools.combinations(sel, 4):
                if is_site([j - 1 for j in combo]):
                    hits16.append({"window_start": i + 1, "selection": list(combo)})
                    break
    out["itasm_scope"]["16w_sites"] = {"count": len(hits16), "list": hits16}

    # ---- 6. the four I-anchors named in ¶238 ---------------------------------
    anchors = [4, 92, 167, 234]
    out["I_anchors"] = [{
        "pos": a,
        "first_letter": I[a - 1],
        "first_word": first_word(paras[a - 1]),
        "final_letter": F[a - 1],
        "final_word": last_word(paras[a - 1]),
        "chars": len(paras[a - 1]),
        "words": len(re.findall(r"[A-Za-z']+", paras[a - 1])),
        "opens_next_window": next((k for k, w in WINDOWS.items() if min(w) - 1 == a), None),
        "is_inside_window": next((k for k, w in WINDOWS.items() if a in w), None),
        "text_head": paras[a - 1][:120],
    } for a in anchors]

    json.dump(out, open(os.path.join(ROOT, "ft_closure_results.json"), "w"),
              indent=1)

    # ---- report --------------------------------------------------------------
    print(f"paragraphs {n}")
    print(f"F...t paragraphs: {out['Ft_count']} at {ft}")
    print(f"  consumed by: {consumed}")
    print(f"  unconsumed: {out['Ft_unconsumed']}")
    for k, v in out["sites"].items():
        print(f"sites[{k}] = {v['count']}  {v['list']}")
    print(f"outside known windows: {out['sites_outside_known_windows']}")
    print(f"'fast forward' appears {out['fast_forward_count']}x at {ff}")
    print(f"chapter non-ITASM paragraphs: {out['itasm_scope']['chapter_nonitasm_total']}")
    print(f"hal_original: {len(hal_paras)} paras, non-ITASM {hal_hits} "
          f"{out['itasm_scope']['hal_nonitasm_initials']}/{out['itasm_scope']['hal_nonitasm_finals']}")
    print(f"sliding 16-window non-ITASM count range: {out['itasm_scope']['sliding16_range']}"
          f" histogram {out['itasm_scope']['sliding16_histogram']}")
    print(f"16-windows with exactly 4 non-ITASM: {out['itasm_scope']['sliding16_windows_with_exactly_four']}")
    print(f"16-window sites reproducing the signature: {out['itasm_scope']['16w_sites']['count']}")
    ls = out["loose_sites"]
    print(f"loose sites (unbounded span, initials order-free): {ls['count']} {ls['classes']}")
    print(f"  anchored per F..t: {ls['anchor_tally']}")
    print(f"  mixing in paragraphs outside the windows: {len(out['loose_sites_outside_known_windows'])}")
    sw = out["loose_site_sweep"]
    print(f"  derived all {sw['sites']} sites: {sw['texts']} texts, {sw['derivations']} "
          f"derivations, {sw['elapsed_s']}s, hits={len(sw['hits'])}")
    pe = out["pentad"]
    print(f"pentad family: {pe['selections']} selections, {pe['texts']} texts, "
          f"{pe['derivations']} derivations, {pe['elapsed_s']}s, hits={len(pe['hits'])}")
    print(f"  anchors {pe['anchors']} finals {pe['anchor_finals']}")
    print(f"  'them' paragraphs {out['them_paragraphs']} (starting W: {out['them_starting_W']})")
    print(f"  window last words: " + "; ".join(
        f"{k}={v['last_words']}" for k, v in out['terminal_words'].items()))
    print("\nI anchors:")
    for a in out["I_anchors"]:
        print(f"  ¶{a['pos']}: {a['first_letter']}|{a['final_letter']} "
              f"last_word={a['final_word']!r} chars={a['chars']} words={a['words']} "
              f"opens={a['opens_next_window']} inside={a['is_inside_window']}")


if __name__ == "__main__":
    main()
