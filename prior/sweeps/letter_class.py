"""Letter-class masks: flip the case of EVERY occurrence of a letter subset.

Why this family: her phrase for the format is "change only a couple of letters in their
capitalization" (demo, paragraph 2). The corpus read that as a couple of *positions* (and closed
every space up to four arbitrary positions). The other reading is a couple of *letter symbols*,
applied to every occurrence, which changes hundreds of characters while still being "a couple of
letters". CLUES_CANONICAL 12.4 tested only the letter sets of candidate names (THOMAS, FINNEY,
NAKAMOTO, SATOSHI, STNM, GRYCOIN, SECOND ...); arbitrary alphabet subsets were never enumerated.

Three modes:
  swap  every occurrence toggles case
  down  every uppercase occurrence is lowered
  up    every lowercase occurrence is capitalised

Cost: the chapter has no MD5 prefix oracle, so every candidate needs a full address derivation.

Usage: python3 sweeps/letter_class.py [swaplte4|all|count] [--max-min N]
"""
import itertools, json, sys, time, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import fast2
# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)

LIVE_H, OLD_H = fast2.h160(fast2.LIVE), fast2.h160(fast2.OLD)
IDX = (0, 1, 2, 76, 77)
ALPHA = "abcdefghijklmnopqrstuvwxyz"
CERT = {"lf": "46a308c279540a33e977ea1f660e8458", "mixed": "bd07e6ee209c5ab65d874bbbcfccda18"}


def build(kind):
    import hashlib
    segs = json.load(open(os.path.join(HERE, "wp_paras_br.json")))
    join, ibr = ("\n\n", "\n") if kind == "lf" else ("\r\n\r\n", "\n")
    text = join.join(ibr.join(p) for p in segs)
    b = text.encode()
    assert hashlib.md5(b).hexdigest() == CERT[kind], kind
    return b


def index_letters(b):
    up, low = {}, {}
    for i, c in enumerate(b):
        if 65 <= c <= 90:
            up.setdefault(chr(c + 32), []).append(i)
        elif 97 <= c <= 122:
            low.setdefault(chr(c), []).append(i)
    return up, low


def run(mode, kmax, cap=None, bases=("mixed","lf")):
    t0 = time.time()
    stats = dict(cands=0, derivs=0, hits=[])
    for kind in bases:
        b = build(kind)
        up, low = index_letters(b)
        for k in range(1, kmax + 1):
            for combo in itertools.combinations(ALPHA, k):
                a = bytearray(b)
                for ch in combo:
                    if mode in ("swap", "down"):
                        for i in up.get(ch, ()):
                            a[i] = ord(ch)
                    if mode in ("swap", "up"):
                        for i in low.get(ch, ()):
                            a[i] = ord(ch) - 32
                import hashlib
                h = hashlib.md5(bytes(a)).digest()
                for idx in IDX:
                    addr = fast2.addr_from_key(fast2.key_at(fast2.seed_from(h), idx))
                    stats["derivs"] += 1
                    ah = fast2.h160(addr)
                    if ah in (LIVE_H, OLD_H):
                        which = "LIVE" if ah == LIVE_H else "OLD"
                        stats["hits"].append((kind, mode, "".join(combo), idx,
                                              h.hex(), addr, which))
                        print("*** HIT", stats["hits"][-1], flush=True)
                stats["cands"] += 1
                if stats["cands"] % 500 == 0:
                    el = time.time() - t0
                    print(f"  {kind} {mode} k<={k} combo={''.join(combo)} "
                          f"cands={stats['cands']} derivs={stats['derivs']} "
                          f"{stats['derivs']/el:.0f}/s", flush=True)
                    if cap and el > cap:
                        stats["stop"] = "time"
                        return stats
    stats["secs"] = round(time.time() - t0, 1)
    return stats


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "swaplte4"
    cap = None
    if "--max-min" in sys.argv:
        cap = 60 * float(sys.argv[sys.argv.index("--max-min") + 1])
    if what == "count":
        for mode, k in (("swap", 4), ("down", 3), ("up", 3)):
            n = sum(1 for i in range(1, k + 1) for _ in itertools.combinations(ALPHA, i))
            print(f"mode {mode} k<={k}: {n} subsets -> {n*2*len(IDX)} derivations, "
                  f"~{n*2*len(IDX)/580/60:.1f} min")
        sys.exit()
    bases = ("mixed", "lf")
    if "--base" in sys.argv:
        bases = (sys.argv[sys.argv.index("--base") + 1],)
    if what == "swaplte4":
        r = run("swap", 4, cap, bases)
    elif what == "down":
        r = run("down", 3, cap, bases)
    elif what == "up":
        r = run("up", 3, cap, bases)
    else:
        r = run("swap", 4, cap, bases)
    print(json.dumps({k: v for k, v in r.items() if k != "hits"}), "hits:", r["hits"])
