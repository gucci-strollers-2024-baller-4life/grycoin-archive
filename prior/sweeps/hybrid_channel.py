"""The hybrid channel: four marks drawn from two disjoint channels, one per act.

Acts I, III and IV carry the sign vocabulary; Act II carries the planted orthography and no sign
vocabulary at all. If the four marked units are one per act, Act II's member can only come from the
case-odd inventory, and the two prose-internal candidates there are

    ¶128  VIrgin   capital injected at index 1, the letter I
    ¶136  BItcoin  capital injected at index 1, the letter I

Both inject `I`, the lead-in letter of every window and of the `Nm ST` signature.

Selection: {¶20 or ¶42} x {¶128 or ¶136} x {¶220 or ¶222} x {¶273} = 8 sets.
Three modes per set, because the Act II mark may be the injected capital itself rather than a
paragraph edge:

    edge    certified transport (first letter down, last letter up) on all four members
    repair  normalise the Act II anomaly to its plain spelling, transport the other three
    clean   normalise the Act II anomaly only, no transport anywhere

Reads:  ../wp_paras_br.json
Writes: ../hybrid_channel_results.json
"""
import hashlib, itertools, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import sixteen_matrix as sm

IDX = (0, 1, 2, 44, 76, 77)
REPAIR = {"VIrgin": "Virgin", "BItcoin": "Bitcoin"}


def load():
    d = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    return [("\n".join(x) if isinstance(x, list) else x) for x in ps]


def first_i(s):
    for i, c in enumerate(s):
        if c.isalpha():
            return i
    return None


def last_i(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i].isalpha():
            return i
    return None


def transport(s):
    a, b = first_i(s), last_i(s)
    if a is None or a == b or not (s[a].isupper() and s[b].islower()):
        return s, False
    q = list(s)
    q[a] = q[a].lower()
    q[b] = q[b].upper()
    return "".join(q), True


def repair(s):
    out, changed = s, False
    for bad, good in REPAIR.items():
        if bad in out:
            out = out.replace(bad, good)
            changed = True
    return out, changed


def apply(ps, sel, mode):
    out, moved = list(ps), 0
    for n in sel:
        s = out[n - 1]
        if mode == "repair" and n in (128, 136):
            out[n - 1], _ = repair(s)
            continue
        if mode == "clean":
            out[n - 1], ch = repair(s)
            moved += ch
            continue
        out[n - 1], ch = transport(s)
        moved += ch
    return out, moved


def serialisations(ps):
    for join, tag in ((b"\n\n", "LF"), (b"\r\n\r\n", "CRLF")):
        for trail in (False, True):
            yield join.join(p.encode() for p in ps) + (join if trail else b""), \
                tag + ("+t" if trail else "")


def main():
    sm.validate()
    ps = load()
    ini = lambda p: (p[first_i(p)] if first_i(p) is not None else "")
    fin = lambda p: (p[last_i(p)] if last_i(p) is not None else "")
    print("candidate letters")
    for n in (20, 42, 128, 136, 220, 222, 273):
        p = ps[n - 1]
        lw = p.split()[-1] if p.split() else ""
        print(f"  ¶{n:3d}  initial {ini(p)!r} final {fin(p)!r} characters {len(p):3d} "
              f"words {len(p.split()):3d} last word {lw!r}  {p[:48]!r}")
        print(f"        transport eligible: {p[first_i(p)].isupper() and p[last_i(p)].islower()}")

    combos = list(itertools.product((20, 42), (128, 136), (220, 222), (273,)))
    rows, hits, texts = [], [], 0
    for sel in combos:
        for mode in ("edge", "repair", "clean"):
            marked, moved = apply(ps, list(sel), mode)
            derivs = 0
            for blob, tag in serialisations(marked):
                texts += 1
                md5 = hashlib.md5(blob).hexdigest()
                for i, a in sm.addrs(md5).items():
                    derivs += 1
                    if a == sm.ESCROW:
                        hits.append({"set": list(sel), "mode": mode, "serialisation": tag,
                                     "md5": md5, "index": i})
            rows.append({"set": list(sel), "mode": mode, "moved": moved,
                         "initials": "".join(ini(ps[n - 1]) for n in sel),
                         "finals": "".join(fin(ps[n - 1]) for n in sel),
                         "derivations": derivs})
            print(f"  {str(sel):24s} {mode:7s} initials {rows[-1]['initials']} "
                  f"finals {rows[-1]['finals']} moved {moved} derivs {derivs} hits 0")

    out = {"escrow": sm.ESCROW, "indices": list(IDX), "combinations": len(combos),
           "texts": texts, "derivations": sum(r["derivations"] for r in rows),
           "hits": hits, "rows": rows}
    json.dump(out, open(os.path.join(ROOT, "hybrid_channel_results.json"), "w"), indent=1)
    print(f"\n{len(combos)} sets x 3 modes: {texts} texts, {out['derivations']} derivations, "
          f"{len(hits)} hits")


if __name__ == "__main__":
    main()
