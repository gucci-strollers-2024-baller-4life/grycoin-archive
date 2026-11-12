"""The read-out hypothesis: do the three novel windows' boundary words carry a seed?

Tests the three operational models proposed after the case-inversion spaces were exhausted:

  M1  tri-coordinate extraction — 12 paragraph-initial words + 12 paragraph-final words across
      W1, W2, W3, checked against the BIP39 English list, plus the acrostics.
  M2  the window deltas (88, 75, 63) as offsets.
  M3  not testable here (external payload); noted in the report only.

Also reconciles the out-of-class initial-letter count under every reasonable convention, since
118 and 121 were both quoted.

Reads the certified base through harness/corpus.py. No key derivation.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "harness"))
from guard import install                       # noqa: E402
install(__file__)
import corpus                                   # noqa: E402

WINDOWS = {"W1": (5, 6, 7, 8), "W2": (93, 94, 95, 96), "W3": (168, 169, 170, 171)}
LEADIN = {"W1": 4, "W2": 92, "W3": 167}
CLASS = set("ITASM")
BIP = {w.strip() for w in open(os.path.join(ROOT, "harness", "bip39_english.txt"))}


def paras():
    out = ["\n".join(s) if isinstance(s, list) else s for s in corpus.seeds()]
    assert len(out) == 273
    return out


def boundary_words(t):
    ws = re.findall(r"[A-Za-z']+", t)
    return ws[0], ws[-1]


def m1(T):
    init, term, rows = [], [], []
    for k, ps in WINDOWS.items():
        for p in ps:
            a, b = boundary_words(T[p - 1])
            init.append(a)
            term.append(b)
            rows.append((k, p, a, a.lower() in BIP, b, b.lower() in BIP))
    acc_i = "".join(w[0].upper() for w in init)
    acc_t = "".join(w[-1] for w in term)
    hits = sum(w.lower() in BIP for w in init + term)
    return {"rows": rows, "init": init, "term": term, "acc_init": acc_i, "acc_term": acc_t,
            "bip_init": sum(w.lower() in BIP for w in init),
            "bip_term": sum(w.lower() in BIP for w in term),
            "bip_all": hits, "valid_mnemonic_length": len(init + term) in (12, 15, 18, 21, 24)}


def m2(T):
    starts = [min(p) for p in WINDOWS.values()]
    deltas = [b - a for a, b in zip(starts, starts[1:])]
    to_reprint = 231 - starts[-1]
    b, _ = corpus.chapter("lf")
    text = b.decode()
    return {"starts": starts, "deltas": deltas, "delta_to_reprint": to_reprint,
            "offsets": {d: text[max(0, d - 12):d + 12] for d in deltas + [to_reprint]}}


def leadins(T):
    out = []
    for k, p in LEADIN.items():
        ws = re.findall(r"[A-Za-z']+", T[p - 1])
        out.append((k, p, ws[0], ws[-1], re.match(r"[^A-Za-z]*([A-Za-z])", T[p - 1]).group(1).upper()))
    return out


def position_words(T):
    """The closing word at each of the four positions, across the three windows and the source."""
    rows = {}
    for pos in range(4):
        rows[pos + 1] = [boundary_words(T[ps[pos] - 1])[1] for ps in WINDOWS.values()]
    return rows


def count_reconciliation(T):
    def c(f):
        return sum(1 for t in T if f(t) not in CLASS)
    alpha_upper = c(lambda t: (re.match(r"[^A-Za-z]*([A-Za-z])", t) or [None, "?"])[1].upper()
                    if re.match(r"[^A-Za-z]*([A-Za-z])", t) else "?")
    alpha_raw = c(lambda t: (re.match(r"[^A-Za-z]*([A-Za-z])", t).group(1))
                  if re.match(r"[^A-Za-z]*([A-Za-z])", t) else "?")
    raw0 = c(lambda t: t[0] if t else "?")
    return {"first_alpha_uppercased": alpha_upper, "first_alpha_raw_case": alpha_raw,
            "raw_index_0": raw0}


def main():
    corpus.self_check()
    T = paras()

    r1 = m1(T)
    print("== M1: boundary words ==")
    for k, p, a, ai, b, bi in r1["rows"]:
        print("  %-3s ¶%-4d INIT %-8s bip39=%-5s  TERM %-10s bip39=%s" % (k, p, a, ai, b, bi))
    print("  initials  : %s" % " ".join(r1["init"]))
    print("  terminals : %s" % " ".join(r1["term"]))
    print("  acrostic init=%s  term=%s" % (r1["acc_init"], r1["acc_term"]))
    print("  BIP39 %d/12 initial, %d/12 terminal, %d/24 combined"
          % (r1["bip_init"], r1["bip_term"], r1["bip_all"]))
    print("  forms a legal mnemonic length: %s" % r1["valid_mnemonic_length"])

    print("\n== closing word at each of the four positions ==")
    hal = [x.strip() for x in open(os.path.join(ROOT, "hal_original.txt")).read().split("\n\n")]
    hal = [x for x in hal if x]
    SRC = (2, 3, 4, 6)          # hal ¶2, ¶3, ¶4, ¶6 — ¶5 is the interleaved I paragraph
    for pos, ws in position_words(T).items():
        print("  pos %d: %-40s source(¶%d)=%s"
              % (pos, ws, SRC[pos - 1], boundary_words(hal[SRC[pos - 1] - 1])[1]))

    print("\n== M2: deltas ==")
    r2 = m2(T)
    print("  window starts: %s" % r2["starts"])
    print("  intervals between the three novel windows: %s" % r2["deltas"])
    print("  third number counting to the reprint (¶231): %d" % r2["delta_to_reprint"])
    for d, ctx in r2["offsets"].items():
        print("  offset %-3d -> %r" % (d, ctx))

    print("\n== lead-in paragraphs ==")
    for k, p, first, last, ini in leadins(T):
        print("  %-3s ¶%-4d initial=%-2s first=%-4s last=%-8s" % (k, p, ini, first, last))

    print("\n== out-of-class initial count, by convention ==")
    for k, v in count_reconciliation(T).items():
        print("  %-24s %d" % (k, v))

    json.dump({"m1": r1, "m2": r2, "leadins": leadins(T),
               "positions": position_words(T), "counts": count_reconciliation(T)},
              open(os.path.join(HERE, "boundary_readout_results.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
