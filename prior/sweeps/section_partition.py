"""Section partition audit: do the chapter's natural sections yield a four-anomaly partition?

Sections are the 18 structural headings of the chapter (I/II/III acts and their numbered
sections). Each heading opens a section that runs to the paragraph before the next heading.
Headings themselves are excluded from the count, so a section title cannot be counted as one of
its own anomalies.

Two alphabets, since `fb3cb47` established that `{A,I,M,O,S,T}` is the minimal set giving exactly
four anomalies on both the Finney post and the grycoin demo, while `{A,I,M,O,S,T,H}` gives the
92-paragraph anomaly pool some notes quote:

    AIMOST   169 carriers / 103 anomalies (+ ¶15, letterless)
    AIMOSTH  180 carriers / 92 anomalies

Every section with exactly four prose anomalies is then derived under the certified transport
(first letter down, last letter up), four serialisations, indices 0/1/2/44/76/77.

Reads:  ../wp_paras_br.json
Writes: ../section_partition_results.json
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import sixteen_matrix as sm

HEADS = {1: "Second", 2: "I. Second Life", 3: "1. Second Coming", 54: "2. Running",
         71: "3. Reverse Turing Test", 88: "II. Second Layer", 89: "Abstract",
         91: "1. Purpose of Grycoin", 115: "2. Bitcoin With Two Changes", 130: "3. Incentives",
         152: "4. Why Blockchain?", 157: "5. What Grycoin can do for Bitcoin",
         161: "6. Conclusion", 163: "III. Second Identity", 164: "1. My Identity",
         175: "2. The Satoshi Code", 176: "a) Satoshi's birthday", 182: "b) THOMAS and Satoshi",
         209: "c) BITcoin is actually AHScoin", 215: "d) Outing himself on Bitcointalk",
         247: "3. Other evidence", 250: "a) ALS Condition", 252: "b) Previous Experience",
         254: "c) Mail Conversation With Himself", 256: "d) Not Citing RPOW", 258: "e) Coding Style",
         260: "f) Overheating Computer", 265: "4. What Does it Mean?"}
ALPHABETS = {"AIMOST": set("AIMOST"), "AIMOSTH": set("AIMOSTH")}


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


def mark(ps, sel):
    out, moved = list(ps), 0
    for n in sel:
        s = out[n - 1]
        a, b = first_i(s), last_i(s)
        if a is None or a == b or not (s[a].isupper() and s[b].islower()):
            continue
        q = list(s)
        q[a] = q[a].lower()
        q[b] = q[b].upper()
        out[n - 1] = "".join(q)
        moved += 1
    return out, moved


def serialisations(ps):
    for join, tag in ((b"\n\n", "LF"), (b"\r\n\r\n", "CRLF")):
        for trail in (False, True):
            yield join.join(p.encode() for p in ps) + (join if trail else b""), \
                tag + ("+t" if trail else "")


def main():
    sm.validate()
    ps = load()
    N = len(ps)
    ini = [(p[first_i(p)] if first_i(p) is not None else "").upper() for p in ps]
    fin = [(p[last_i(p)] if last_i(p) is not None else "").lower() for p in ps]
    starts = sorted(HEADS)
    out = {"escrow": sm.ESCROW, "indices": list(sm.IDX) if hasattr(sm, "IDX") else [0, 1, 2, 44, 76, 77]}
    idx = out["indices"]

    results = {}
    for name, alpha in ALPHABETS.items():
        rows, four = [], []
        for k, s in enumerate(starts):
            e = (starts[k + 1] - 1) if k + 1 < len(starts) else N
            prose = list(range(s + 1, e + 1))
            an = [i for i in prose if ini[i - 1] and ini[i - 1] not in alpha]
            rows.append({"section": HEADS[s], "start": s, "end": e, "prose": len(prose),
                         "anomalies": an,
                         "initials": "".join(ini[i - 1] for i in an),
                         "finals": "".join(fin[i - 1] for i in an)})
            if len(an) == 4:
                four.append(rows[-1])
        print(f"\n=== {name}: {len(four)} sections with exactly four prose anomalies ===")
        for r in four:
            print(f"  ¶{r['start']}-{r['end']} {r['section'][:30]:32s} {r['anomalies']} "
                  f"initials {r['initials']} finals {r['finals']}")
            marked, moved = mark(ps, r["anomalies"])
            derivs, hits = [], []
            for blob, tag in serialisations(marked):
                md5 = hashlib.md5(blob).hexdigest()
                for i, a in sm.addrs(md5).items():
                    derivs.append({"serialisation": tag, "md5": md5, "index": i, "addr": a})
                    if a == sm.ESCROW:
                        hits.append({"section": r["section"], "serialisation": tag,
                                     "md5": md5, "index": i})
            r["units_moved"] = moved
            r["derivations"] = len(derivs)
            print(f"      moved {moved}, {len(derivs)} derivations, {len(hits)} hits")
        results[name] = {"sections": rows, "four_anomaly_sections": four}
    out["by_alphabet"] = results
    json.dump(out, open(os.path.join(ROOT, "section_partition_results.json"), "w"), indent=1)
    print("\nwrote section_partition_results.json")


if __name__ == "__main__":
    main()
