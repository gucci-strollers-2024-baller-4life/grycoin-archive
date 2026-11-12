"""k=5 letter-class sweep, anchor mode: first letter NOT in class -> first down, last up.

The family is not a guess. The certified stage-one answer selects paragraphs by a membership test
on the first letter against a five-letter class (I,T,A,S,M), and marks the ones outside it with
first-letter-down / last-letter-up at the alphabetic token edges. This enumerates all C(26,5)
classes in that exact mode, on both certified bases, at indices 0-7, 44, 76, 77.

Phase 1 (build, fast): md5 for every class, deduplicated. Classes that differ only in letters no
paragraph starts with produce the same text, so the unique-candidate count is far below 65,780.
Phase 2 (derive, the cost): every unique md5 through BIP39 at the index set.

    python3 sweeps/k5_class_sweep.py build
    python3 sweeps/k5_class_sweep.py derive [budget_seconds]

Resumable in phase 2 via k5_progress.json.
"""
import hashlib
import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "harness"))

from guard import install as _guard_install                # noqa: E402

_guard_install(__file__)

import corpus                                             # noqa: E402
import fast2                                              # noqa: E402

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
K = 5
INDICES = (0, 1, 2, 3, 4, 5, 6, 7, 44, 76, 77)
UNIQ = os.path.join(HERE, "k5_unique.json")
PROG = os.path.join(HERE, "k5_progress.json")
HITS = os.path.join(HERE, "k5_hits.txt")
LIVE_H = fast2.h160(fast2.LIVE)
OLD_H = fast2.h160(fast2.OLD)


def edges(kind):
    """byte base + one (first_pos, last_pos, first_letter) per non-empty paragraph"""
    b, spans = corpus.chapter(kind)
    out = []
    for s, e in spans:
        L = [i for i in range(s, e) if corpus.is_letter(b[i])]
        if L:
            out.append((L[0], L[-1], chr(b[L[0]]).upper()))
    return b, out


def build():
    uniq = {}
    for kind in ("mixed", "lf"):
        b, P = edges(kind)
        present = "".join(sorted({f for _, _, f in P}))
        by_letter = {c: [(x, y) for x, y, f in P if f == c] for c in ALPHA}
        for cls in itertools.combinations(ALPHA, K):
            cs = set(cls)
            a = bytearray(b)
            sel = 0
            for c in ALPHA:
                if c in cs:
                    continue
                for x, y in by_letter[c]:
                    sel += 1
                    if 0x41 <= a[x] <= 0x5A:
                        a[x] += 32
                    if 0x61 <= a[y] <= 0x7A:
                        a[y] -= 32
            h = hashlib.md5(bytes(a)).hexdigest()
            uniq.setdefault(h, {"kind": kind, "cls": "".join(cls), "sel": sel})
        print(f"{kind}: 65780 classes, present initials {len(present)} ({present}), "
              f"unique so far {len(uniq)}", flush=True)
    json.dump(uniq, open(UNIQ, "w"))
    print(f"unique candidates: {len(uniq)}  ({len(uniq)*len(INDICES)} derivations)", flush=True)


def derive(budget=0.0):
    uniq = json.load(open(UNIQ))
    keys = list(uniq)
    prog = json.load(open(PROG)) if os.path.exists(PROG) else {"at": 0, "done": 0}
    t0 = time.time()
    for i in range(prog["at"], len(keys)):
        h = keys[i]
        hb = bytes.fromhex(h)
        for idx in INDICES:
            addr = fast2.addr_from_key(fast2.key_at(fast2.seed_from(hb), idx))
            ah = fast2.h160(addr)
            if ah in (LIVE_H, OLD_H):
                which = "LIVE" if ah == LIVE_H else "OLD"
                rec = (f"HIT md5={h} class={uniq[h]['cls']} kind={uniq[h]['kind']} "
                       f"sel={uniq[h]['sel']} idx={idx} {which} addr={addr}\n")
                open(HITS, "a").write(rec)
                print("!!!!!! SOLVED " + rec, flush=True)
                json.dump({"at": i, "done": prog["done"] + 1}, open(PROG, "w"))
                return 0
        prog["done"] += 1
        if budget and time.time() - t0 > budget:
            json.dump({"at": i + 1, "done": prog["done"]}, open(PROG, "w"))
            print(f"PAUSED {prog['done']}/{len(keys)} unique candidates, "
                  f"{prog['done']*len(INDICES)} derivations, {time.time()-t0:.0f}s", flush=True)
            return 2
    print(f"DONE {prog['done']} unique candidates, {prog['done']*len(INDICES)} derivations, "
          f"0 hits", flush=True)
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        build()
    else:
        sys.exit(derive(float(sys.argv[2]) if len(sys.argv) > 2 else 0.0))
