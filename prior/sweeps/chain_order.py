#!/usr/bin/env python3
"""sweeps/chain_order.py - the lead BLOCK29_ANCHOR_CENSUS §6/§7 produced, run to closure.

The demo's four marked paragraphs carry anchor -> mark pairs

    P4  F -> S      P5  I -> F      P6  O -> I      P8  W -> S

and two raised letters are the *next* paragraph's lowered anchor (P5 raises F = P4's anchor,
P6 raises I = P5's anchor).  Read as a handoff the order is 6 -> 5 -> 4, ending on the same S
that P8 also terminates on.  Every earlier sweep in the repo marks a *set* of paragraphs in
text order and never re-orders the paragraphs before serialising.  That is the gap.

Geometry used, per paragraph: lower the first letter; raise the last letter of the FIRST
sentence.  On single-sentence paragraphs (P4, P6) that is the paragraph-final; on two-sentence
paragraphs (P5, P8) it is not.  This is geometry (ii) of DISCRIMINATOR_2026-10-31 §1, the one
the author's decoy `capitalizatioN` does not flag, and it is asserted against the census letters.

Families
  A  every ordering of the ten paragraphs (10! = 3,628,800) x 4 serializations, marks applied
     to their own paragraphs.  Strictly contains the chain orders 6-5-4-8 and 6-5-4, and also
     contains every "process the marks in this order" reading, because applying case edits is
     commutative: order can only matter if the *answer text* is re-ordered, which is what this
     enumerates.
  B  the four marked paragraphs permuted among their own slots (24) x all 16 subsets of the
     four marks x 4 serializations = 1,536.

Usage:
    python3 sweeps/chain_order.py screen    # writes chain_order_survivors.json
    python3 sweeps/chain_order.py derive    # derives every survivor at 9 indices
    python3 sweeps/chain_order.py both
"""
import hashlib
import itertools
import json
import re
import sys

sys.path.insert(0, "harness")
import btc

ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
PREFIX = "3c6"
INDICES = (0, 1, 2, 5, 6, 7, 44, 76, 77)
OUT = "chain_order_survivors.json"

RAW = open("demo_base.txt", encoding="utf-8", newline="").read()
PARAS = [p for p in re.split(r"\r?\n\r?\n", RAW.strip()) if p.strip()]
assert len(PARAS) == 10
assert hashlib.md5(RAW.encode()).hexdigest().startswith("7759227d7406"), "base is not certified"

MARKED = (3, 4, 5, 7)  # 0-based: P4 P5 P6 P8
PLAIN = tuple(i for i in range(10) if i not in MARKED)


def first_sentence_end(para: str) -> int:
    m = re.search(r'[.!?]+["\u201d]?\s', para)
    return m.end() if m else len(para)


def mark_para(idx: int, anchor: bool, mark: bool) -> bytes:
    para = PARAS[idx]
    b = bytearray(para.encode())
    if anchor:
        i = next(i for i, c in enumerate(b) if chr(c).isalpha())
        b[i] = ord(chr(b[i]).lower())
    if mark:
        end = first_sentence_end(para)
        j = next(i for i in range(end - 1, -1, -1) if chr(b[i]).isalpha())
        b[j] = ord(chr(b[j]).upper())
    return bytes(b)


# --- certify the geometry against the census letters before anything runs ---
for idx, anchor, letter in ((3, "F", "S"), (4, "I", "F"), (5, "O", "I"), (7, "W", "S")):
    assert PARAS[idx][0] == anchor
    end = first_sentence_end(PARAS[idx])
    j = next(i for i in range(end - 1, -1, -1) if PARAS[idx][i].isalpha())
    assert PARAS[idx][j].upper() == letter, (idx, PARAS[idx][j], letter)

# unmarked text, and the same text with the four recognised paragraphs marked.  The other
# six paragraphs are untouched: only the recognised ones carry marks.
BARE = [mark_para(i, False, False) for i in range(10)]
FULL = [mark_para(i, True, True) if i in MARKED else BARE[i] for i in range(10)]


def serializations():
    for join, jtag in ((b"\r\n\r\n", "CRLF"), (b"\n\n", "LF")):
        for trail in (False, True):
            yield join, trail, jtag + ("+t" if trail else "")


def screen():
    hits = []
    seen = 0
    for join, trail, tag in serializations():
        tail = join if trail else b""
        n = 0
        for perm in itertools.permutations(range(10)):
            body = join.join([FULL[i] for i in perm]) + tail
            h = hashlib.md5(body).hexdigest()
            n += 1
            if h.startswith(PREFIX):
                hits.append({"family": "A", "ser": tag,
                             "order": "".join("%d" % (i + 1) for i in perm), "md5": h})
        seen += n
        print(f"  A {tag}: {n} candidates, running survivors {len(hits)}", flush=True)

    for join, trail, tag in serializations():
        tail = join if trail else b""
        n = 0
        for perm in itertools.permutations(MARKED):
            for mask in range(16):
                chunks = [None] * 10
                for i in PLAIN:
                    chunks[i] = BARE[i]
                for bit, slot in enumerate(perm):
                    chunks[slot] = mark_para(slot, bool(mask >> bit & 1), bool(mask >> bit & 1))
                h = hashlib.md5(join.join(chunks) + tail).hexdigest()
                n += 1
                if h.startswith(PREFIX):
                    hits.append({"family": "B", "ser": tag,
                                 "order": "".join("%d" % (i + 1) for i in perm),
                                 "mask": mask, "md5": h})
        seen += n
        print(f"  B {tag}: {n} candidates, running survivors {len(hits)}", flush=True)

    json.dump(hits, open(OUT, "w"), indent=1)
    print(f"\ncandidates={seen}  3c6 survivors={len(hits)}  -> {OUT}", flush=True)
    return hits


def derive(hits):
    """one PBKDF2 per survivor, then the nine indices off the same parent"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("fast2", "harness/fast2.py")
    f2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(f2)
    target = f2.h160(ESCROW)
    assert f2.addr_md5hex("9dd2efb9bc976c2095bd534d7b8d431c") == "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"
    matches = 0
    for k, rec in enumerate(hits, 1):
        ent = bytes.fromhex(rec["md5"])
        k0, c0 = f2.parent(f2.seed_from(ent))
        for i in INDICES:
            ki, _ = f2.ckd(k0, c0, i)
            if f2.pubhash(ki) == target:
                matches += 1
                print("  *** ESCROW MATCH ***", rec, "index", i, flush=True)
        if k % 1000 == 0:
            print(f"  derived {k}/{len(hits)}", flush=True)
    print(f"\nderived {len(hits)} survivors x {len(INDICES)} indices   escrow matches={matches}",
          flush=True)
    return matches


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    surv = screen() if mode in ("screen", "both") else json.load(open(OUT))
    if mode in ("derive", "both"):
        derive(surv)
