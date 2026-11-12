"""The sign-letter selection, swept at whole-chapter scale.

The argument under test (from the 15:29 read of §9/§13.2): the sign alphabet is not the chapter's
stated {I,T,A,S,M} but the letters of SATOSHI, and the marked set is therefore the ~179 paragraphs that
*do* carry a sign letter, marked by transport (capital off the unit head, on to the unit tail), rather
than the four-window paragraphs marked first-down/last-up.

What this script does:
  1. validates the fast lane (coincurve) against harness/btc.py, as required before any run
  2. calibrates the two candidate alphabets against BOTH documents the author demonstrates on:
     hal_original.txt (16 paragraphs) and the grycoin block-2 format example (demo_base.txt, 10)
  3. builds the carrier and anomaly sets under each alphabet
  4. marks each set by transport, with two tail definitions:
       - first-sentence tail  (the demo's own worked example, demo ¶5 bytes 535 / 652)
       - paragraph tail       (the stage-one certified edit)
     across four serialisations, and derives every text at indices 0-77
  5. reports live-edit counts, so a set that is mostly no-ops is visible as such

Reads:  ../wp_paras_br.json, ../hal_original.txt, ../demo_base.txt
Writes: ../sign_letter_results.json
"""
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import sixteen_matrix as sm                      # noqa: E402  (validated fast lane)

ITASM = set("ITASM")
SATOSHI = set("SATOSHI")
UNION = ITASM | SATOSHI                 # == the letters of THOMAS plus I: {A,H,I,M,O,S,T}
MINIMAL = set("AIMOST")                 # smallest fixed alphabet that reproduces four on BOTH docs


def load_chapter():
    d = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    out = [("\n".join(x) if isinstance(x, list) else x) for x in ps]
    assert len(out) == 273, len(out)
    return out


def load_hal():
    t = open(os.path.join(ROOT, "hal_original.txt")).read()
    return [x.strip() for x in re.split(r"\n\s*\n", t) if x.strip()]


def load_demo():
    t = open(os.path.join(ROOT, "demo_base.txt"), encoding="utf-8").read()
    return [x.strip() for x in t.split("\n\n") if x.strip()]


def ini(p):
    c = next((c for c in p if c.isalpha()), "")
    return c.upper()


def anomalies(doc, alpha):
    return [i + 1 for i, p in enumerate(doc) if ini(p) not in alpha]


def show_calibration():
    hal, demo = load_hal(), load_demo()
    print("== calibration: which alphabet reproduces 'exactly four' on each demonstrated document ==")
    rows = {}
    for name, alpha in (("{I,T,A,S,M}", ITASM), ("{S,A,T,O,H,I}", SATOSHI),
                        ("THOMAS+I {A,H,I,M,O,S,T}", UNION),
                        ("minimal {A,I,M,O,S,T}", MINIMAL)):
        h, d = anomalies(hal, alpha), anomalies(demo, alpha)
        rows[name] = {"hal": h, "demo": d}
        print("  %-22s hal anomalies %-2d %-18s demo anomalies %-2d %s"
              % (name, len(h), h, len(d), d))
        print("  %-22s hal initials outside: %-10s demo initials outside: %s"
              % ("", "".join(ini(hal[i - 1]) for i in h), "".join(ini(demo[i - 1]) for i in d)))
    assert len(anomalies(hal, ITASM)) == 4 and len(anomalies(demo, SATOSHI)) == 4
    return rows


def first_sentence_tail(p):
    """Last letter of the last word of the FIRST sentence — the demo's demonstrated tail."""
    m = re.split(r"(?<=[.!?])\s", p.strip(), maxsplit=1)
    s = m[0]
    ws = re.findall(r"[A-Za-z']+", s)
    return (ws[-1][-1] if ws else "") or next((c for c in reversed(p) if c.isalpha()), "")


def mark(paras, sel, tail):
    """Transport: lowercase the unit head, uppercase the unit tail. Returns text + live-edit count."""
    out = list(paras)
    live = 0
    for i in sel:
        p = out[i]
        if not any(ch.isalpha() for ch in p):
            continue                       # ¶15 is '2020.' — no letters to transport
        a = next(j for j, ch in enumerate(p) if ch.isalpha())
        if tail == "first_sentence":
            ch = first_sentence_tail(p)
            k = p.rfind(ch) if ch else -1
        else:
            k = next(j for j in range(len(p) - 1, -1, -1) if p[j].isalpha())
        q = list(p)
        if p[a].isupper():
            q[a] = p[a].lower()
            live += 1
        if 0 <= k < len(p) and p[k].islower():
            q[k] = p[k].upper()
            live += 1
        out[i] = "".join(q)
    return out, live


def serialisations(paras):
    for join, tag in ((b"\n\n", "LF"), (b"\r\n\r\n", "CRLF")):
        for trail in (False, True):
            yield join.join(p.encode() for p in paras) + (join if trail else b""), tag + ("+t" if trail else "")


def main():
    sm.validate()
    paras = load_chapter()
    cal = show_calibration()

    print("\n== sets ==")
    sets = {}
    print("\n== minimality: drop one letter at a time ==")
    for L in sorted(MINIMAL):
        a = MINIMAL - {L}
        h, d = anomalies(load_hal(), a), anomalies(load_demo(), a)
        ok = len(h) == 4 and len(d) == 4
        print("  without %s: hal %-2d %-10s  demo %-2d %-10s  %s"
              % (L, len(h), "".join(ini(load_hal()[i - 1]) for i in h),
                 len(d), "".join(ini(load_demo()[i - 1]) for i in d),
                 "STILL FOUR" if ok else "breaks"))
    for name, alpha in (("ITASM", ITASM), ("SATOSHI", SATOSHI), ("MINIMAL", MINIMAL),
                        ("UNION", UNION)):
        car = [i for i, p in enumerate(paras) if ini(p) in alpha]
        ano = [i for i, p in enumerate(paras) if ini(p) not in alpha]
        sets[name] = {"carrier": car, "anomaly": ano}
        print("  %-8s carrier %-3d  anomaly %-3d  (anomaly with letters: %d)"
              % (name, len(car), len(ano),
                 sum(1 for i in ano if any(c.isalpha() for c in paras[i]))))
    letterless = [i + 1 for i, p in enumerate(paras) if not any(c.isalpha() for c in p)]
    print("  paragraphs with no letters at all: %s" % letterless)

    print("\n== strict mass conservation: only units where both moves are real ==")
    for name in ("SATOSHI", "MINIMAL"):
        car = sets[name]["carrier"]
        keep = []
        for i in car:
            p = paras[i]
            if not any(c.isalpha() for c in p):
                continue
            a = next(j for j, ch in enumerate(p) if ch.isalpha())
            k = next(j for j in range(len(p) - 1, -1, -1) if p[j].isalpha())
            if p[a].isupper() and p[k].islower():
                keep.append(i)
        print("  %-8s carrier strict (paragraph tail): %d of %d" % (name, len(keep), len(car)))

    print("\n== transport sweeps ==")
    hits, n, t0 = [], 0, time.time()
    log = []
    for name in ("ITASM", "SATOSHI", "MINIMAL", "UNION"):
        for which in ("carrier", "anomaly"):
            sel = sets[name][which]
            for tail in ("first_sentence", "paragraph"):
                marked, live = mark(paras, sel, tail)
                for blob, tag in serialisations(marked):
                    n += 1
                    h = hashlib.md5(blob).hexdigest()
                    res = sm.addrs(h)
                    rec = {"alphabet": name, "set": which, "n": len(sel), "tail": tail,
                           "join": tag, "md5": h, "live_edits": live,
                           "idx0": res[0]}
                    log.append(rec)
                    for i, a in res.items():
                        if a == sm.ESCROW:
                            hits.append((name, which, tail, tag, h, i))
                print("  %-8s %-8s n=%-3d tail=%-14s live-edits=%d md5=%s idx0=%s"
                      % (name, which, len(sel), tail, live,
                         log[-1]["md5"] if tail == "paragraph" else "", rec["idx0"]))
    print("\n  texts=%d derivations=%d elapsed=%.1fs hits=%d"
          % (n, n * len(sm.IDX), time.time() - t0, len(hits)))
    for x in hits:
        print("  HIT", x)
    if not hits:
        print("  ALL NEGATIVE — no text in this family reproduces the escrow %s" % sm.ESCROW)

    json.dump({"calibration": cal,
               "sizes": {k: {w: len(v) for w, v in d.items()} for k, d in sets.items()},
               "letterless": letterless, "runs": log, "hits": hits},
              open(os.path.join(HERE, "..", "sign_letter_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
