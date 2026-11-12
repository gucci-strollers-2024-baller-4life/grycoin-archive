"""Block 76/77 indexing against corpus.json, plus the "Aa" edge-pair census.

Three questions:
  1. how the 33 parts are ordered, and whether they form a partition at all
  2. where 76 and 77 land under each reading of the modulus
  3. whether any part carries exactly four anomalies under {A,I,M,O,S,T}, and whether the
     landings do

The author's reply in the block 77 stage-one thread names "the Aa in the genesis block address" as
the thing that hinted at the solution, so the chapter is also censused for paragraphs whose first
and last letters are the same letter in different case, which is the edge pair she describes.

Reads:  ../corpus.json, ../wp_paras_br.json
Writes: ../part_index_results.json
"""
import collections, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ALPHA = set("AIMOST")


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


def main():
    d = json.load(open(os.path.join(ROOT, "corpus.json"), encoding="utf-8"))
    keys = list(d)
    out = {"parts": [], "landings": {}, "overlap": {}, "four_anomaly_parts": []}

    owner = collections.defaultdict(set)
    instances = 0
    for i, k in enumerate(keys):
        paras = [("\n".join(p) if isinstance(p, list) else p) for p in d[k]["paras"]]
        an = [n for n, p in enumerate(paras, 1)
              if first_i(p) is not None and p[first_i(p)].upper() not in ALPHA]
        ini = "".join(paras[n - 1][first_i(paras[n - 1])].upper() for n in an)
        fin = "".join(paras[n - 1][last_i(paras[n - 1])].lower() for n in an)
        for p in paras:
            t = p.strip()
            if len(t) < 40:
                continue
            instances += 1
            owner[hashlib.md5(t.encode()).hexdigest()].add(i)
        row = {"ordinal": i, "post_id": k, "title": d[k]["title"],
               "paragraphs": len(paras), "anomalies": an, "initials": ini, "finals": fin}
        out["parts"].append(row)
        if len(an) == 4:
            out["four_anomaly_parts"].append(row)
        print(f"{i:3d} {k:>10} {d[k]['title'][:36]:38s} ¶{len(paras):4d} anom {len(an):4d} "
              f"{ini[:16]}({fin[:16]})")

    dup = sum(1 for h, s in owner.items() if len(s) > 1)
    out["overlap"] = {"instances": instances, "distinct": len(owner),
                      "duplicate_instances": instances - len(owner),
                      "shared_paragraphs": dup}
    print(f"\nparagraph instances {instances}, distinct {len(owner)}, "
          f"duplicates {instances - len(owner)}, shared {dup}")

    print("\nmodulo landings")
    for N in (76, 77):
        r = N % 33
        r2 = (N - 1) % 33
        land = {"N mod 33, 0-based": (r, d[keys[r]]["title"]),
                "N mod 33, 1-based": (r - 1, d[keys[r - 1]]["title"]),
                "(N-1) mod 33, 0-based": (r2, d[keys[r2]]["title"]),
                "(N-1) mod 33, 1-based": (r2 - 1, d[keys[r2 - 1]]["title"])}
        out["landings"][N] = {k: {"ordinal": v[0], "title": v[1]} for k, v in land.items()}
        print(f"  {N}:")
        for k, v in land.items():
            an = len(out["parts"][v[0]]["anomalies"])
            print(f"    {k:24s} ord {v[0]:2d} {v[1][:34]:36s} anomalies {an}")

    # the "Aa" edge-pair census on the chapter
    ch = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = ch if isinstance(ch, list) else (ch.get("paras") or list(ch.values())[0])
    ps = [("\n".join(x) if isinstance(x, list) else x) for x in ps]
    pairs, same = [], []
    for n, p in enumerate(ps, 1):
        a, b = first_i(p), last_i(p)
        if a is None or a == b:
            continue
        fa, lb = p[a], p[b]
        if fa.lower() == lb.lower() and fa != lb:
            pairs.append({"para": n, "edge": fa + lb})
            if fa.isupper() and lb.islower():
                same.append(n)
    out["edge_pairs"] = {"different_case_same_letter": pairs, "head_upper_tail_lower": same}
    print(f"\nparagraphs whose first and last letter are the same letter in different case: "
          f"{len(pairs)}")
    for r in pairs:
        print(f"  ¶{r['para']:3d} {r['edge']}  {ps[r['para'] - 1][:60]!r}")
    print(f"  of those, head-upper/tail-lower (the genesis 'Aa' shape): {same}")

    json.dump(out, open(os.path.join(ROOT, "part_index_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
