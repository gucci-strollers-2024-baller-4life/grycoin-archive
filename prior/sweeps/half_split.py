"""The two-halves device: one marked unit per half of the chapter.

The author's own worked example splits the genesis address at its central letter and puts one
ciphertext item in each half (Wattpad 761570746, paragraphs 114, 116, 138). Every chapter sweep so
far has treated the 273 paragraphs as a single object with one four-unit selection. This tests the
bipartite reading instead: split the chapter, take one item from each side.

Pools:
  live  the four live uses of "recognize the signs"  20, 42, 220, 273
  ends  every paragraph carrying a sign/signs sentence  18 distinct paragraphs

Splits: the three act markers, the physical midpoint, and the four window starts.
Transport: certified (first letter down, last letter up), four serialisations, six indices.

Reads:  ../wp_paras_br.json
Writes: ../half_split_results.json
"""
import hashlib, itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import sixteen_matrix as sm

LIVE = [20, 42, 220, 273]
ENDS = [20, 42, 206, 220, 222, 223, 225, 226, 227, 228, 230, 236, 240, 244, 246, 273]
SPLITS = {"act I|II ¶88": 88, "midpoint ¶137": 137, "act II|III ¶163": 163,
          "W1 ¶5": 5, "W2 ¶93": 93, "W3 ¶168": 168, "W4 ¶231": 231}


def load():
    d = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    return [("\n".join(x) if isinstance(x, list) else x) for x in ps]


def first_i(s):
    for i, c in enumerate(s):
        if c.isalpha(): return i
    return None


def last_i(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i].isalpha(): return i
    return None


def mark(ps, sel):
    out, moved = list(ps), 0
    for n in sel:
        s, a, b = out[n - 1], first_i(out[n - 1]), last_i(out[n - 1])
        if a is None or a == b or not (s[a].isupper() and s[b].islower()): continue
        q = list(s); q[a] = q[a].lower(); q[b] = q[b].upper()
        out[n - 1] = "".join(q); moved += 1
    return out, moved


def serialise(ps):
    for join, tag in ((b"\n\n", "LF"), (b"\r\n\r\n", "CRLF")):
        for trail in (False, True):
            yield join.join(p.encode() for p in ps) + (join if trail else b""), tag + ("+t" if trail else "")


def run(ps, pool, splits):
    rows, hits, derivs = [], [], 0
    for name, sp in splits.items():
        left = [p for p in pool if p < sp]
        right = [p for p in pool if p >= sp]
        if not left or not right: continue
        for pair in itertools.product(left, right):
            sel = sorted(pair)
            marked, moved = mark(ps, sel)
            d0 = 0
            for blob, tag in serialise(marked):
                md5 = hashlib.md5(blob).hexdigest()
                for i, a in sm.addrs(md5).items():
                    d0 += 1
                    if a == sm.ESCROW:
                        hits.append({"split": name, "set": sel, "serialisation": tag, "md5": md5, "index": i})
            derivs += d0
            rows.append({"split": name, "set": sel, "moved": moved, "derivations": d0})
    return rows, derivs, hits


def main():
    sm.validate()
    ps = load()
    out = {"escrow": sm.ESCROW, "indices": list(sm.IDX)}
    total = 0
    for pool_name, pool, splits in (("live", LIVE, SPLITS),
                                    ("ends", ENDS, {"act I|II ¶88": 88, "midpoint ¶137": 137,
                                                    "act II|III ¶163": 163, "W4 ¶231": 231})):
        rows, derivs, hits = run(ps, pool, splits)
        total += derivs
        print(f"\npool {pool_name}: {len(rows)} sets, {derivs} derivations, {len(hits)} hits")
        for r in rows[:6]:
            print(f"  {r['split']:18s} {str(r['set']):16s} moved {r['moved']}")
        out[pool_name] = {"sets": rows, "derivations": derivs, "hits": hits}
    out["total_derivations"] = total
    json.dump(out, open(os.path.join(ROOT, "half_split_results.json"), "w"), indent=1)
    print(f"\ntotal {total} derivations, 0 hits" if not (out['live']['hits'] or out['ends']['hits']) else "HIT")


if __name__ == "__main__":
    main()
