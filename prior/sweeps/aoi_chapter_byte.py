"""AOI-in-one-sentence family, byte-exact, on the published chapter.

The family (block-29 'vOIce' mechanic): inside one sentence of the chapter, mark the three letters
spelling AOI by uppercasing every occurrence of A, O and I in that sentence, in the order
A < O < I. One candidate per (sentence, a, o, i) triple. MD5 -> BIP39 -> m/44'/0'/0'/0/{0,1,2}.

This replaces aoi_chapter.py, which swept `wp_paras.json[1]` (the chapter_paras_exact object: ten
characters short of the published text) and applied character offsets to encoded bytes. Neither its
53,787 candidates nor its "no match" were about the RBB base.

Every offset here is a byte offset, the base digest is asserted before the loop, and the guard runs
first.

Usage:  python3 sweeps/aoi_chapter_byte.py [budget_seconds]
        budget 0 or absent = run to completion
"""
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "harness"))

from guard import install as _guard_install                # noqa: E402

_guard_install(__file__)

import corpus                                             # noqa: E402
import fast2                                              # noqa: E402

LIVE_H = fast2.h160(fast2.LIVE)
OLD_H = fast2.h160(fast2.OLD)
PROG = os.path.join(HERE, "aoi_byte_progress.json")
HITS = os.path.join(HERE, "aoi_byte_hits.txt")
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
KINDS = ("mixed", "lf")
SENT = re.compile(rb"[^.!?]+")


def candidates(b, spans):
    """(sentence_index, (a, o, i)) in byte space, A < O < I, one per triple"""
    out = []
    for si, (s, e) in enumerate(spans):
        chunk = b[s:e]
        pa = [s + m for m, c in enumerate(chunk) if c in b"Aa"]
        po = [s + m for m, c in enumerate(chunk) if c in b"Oo"]
        pi = [s + m for m, c in enumerate(chunk) if c in b"Ii"]
        if not (pa and po and pi):
            continue
        for a in pa:
            for o in po:
                if o <= a:
                    continue
                for i in pi:
                    if i > o:
                        out.append((si, (a, o, i)))
    return out


def mark(b, tri):
    a = bytearray(b)
    for x in tri:
        c = a[x]
        if not corpus.is_letter(c):
            raise AssertionError(f"byte {x} is {bytes([c])!r}, not a letter")
        if 0x61 <= c <= 0x7A:               # only lowercase needs the flip
            a[x] = c - 0x20
    return bytes(a)


def main():
    t0 = time.time()
    prog = json.load(open(PROG)) if os.path.exists(PROG) else {"kind": 0, "cand": 0, "done": 0}
    for ki in range(prog["kind"], len(KINDS)):
        kind = KINDS[ki]
        b, spans = corpus.chapter(kind)
        # sentence spans in the same byte space as the base
        sspans = [(m.start(), m.end()) for m in SENT.finditer(b)]
        cands = candidates(b, sspans)
        start = prog["cand"] if ki == prog["kind"] else 0
        print(f"{kind}: {len(b)} bytes, {len(sspans)} sentence spans, {len(cands)} candidates, "
              f"starting at {start}", flush=True)
        for ci in range(start, len(cands)):
            si, tri = cands[ci]
            h = hashlib.md5(mark(b, tri)).digest()
            for idx in (0, 1, 2):
                addr = fast2.addr_from_key(fast2.key_at(fast2.seed_from(h), idx))
                ah = fast2.h160(addr)
                if ah in (LIVE_H, OLD_H):
                    which = "LIVE" if ah == LIVE_H else "OLD"
                    rec = (f"HIT kind={kind} sentence={si} pos={tri} idx={idx} {which} "
                           f"md5={h.hex()} addr={addr}\n")
                    open(HITS, "a").write(rec)
                    print("!!!!!! SOLVED " + rec, flush=True)
                    json.dump({**prog, "kind": ki, "cand": ci, "done": prog["done"] + 1},
                              open(PROG, "w"))
                    return 0
            prog["done"] += 1
            if BUDGET and time.time() - t0 > BUDGET:
                json.dump({"kind": ki, "cand": ci + 1, "done": prog["done"]}, open(PROG, "w"))
                print(f"PAUSED at {kind} candidate {ci+1}/{len(cands)}, "
                      f"{prog['done']} tested, {time.time()-t0:.0f}s", flush=True)
                return 2
        prog["kind"] = ki + 1
        prog["cand"] = 0
        json.dump(prog, open(PROG, "w"))
    secs = time.time() - t0
    print(f"DONE {prog['done']} candidates, {prog['done']*3} derivations, {secs:.0f}s, 0 hits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
