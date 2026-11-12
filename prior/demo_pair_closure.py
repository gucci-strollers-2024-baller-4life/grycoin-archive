#!/usr/bin/env python3
"""demo_pair_closure.py - the one demo family that was never enumerated.

The demo is the only object in this hunt with two published oracles at once:
  * md5 of the answer begins `3c6`  (1-in-4096 filter, microseconds per candidate)
  * the answer's address is 1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi

The demo's worked example applies BOTH edges to the SAME sentence:

    "I expected ... outing himself."  ->  "i expected ... outing himselF."

Prior sweeps gave each sentence of the base three states (unchanged / first down / last up):
3^15 = 14,348,907 candidates, exhaustive, 201 prefix survivors, 0 escrow matches.
Paragraph granularity with four states was closed too (4^10).

What was never run is the pair family at sentence granularity: for each sentence, either
leave it alone or apply BOTH edges to it. That is 2^15 = 32,768 candidates, and it is the
family the author's own example demonstrates. Both joins, trailing separator or not.

Reports every `3c6` survivor and derives each at m/44'/0'/0'/0/i for i in 0..77.
"""
import hashlib, itertools, re, sys
sys.path.insert(0, "harness")
import btc

ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
PREFIX = "3c6"

txt = open("demo_base.txt", encoding="utf-8", newline="").read()
paras = [p for p in re.split(r"\r?\n\r?\n", txt.strip()) if p.strip()]
assert len(paras) == 10, len(paras)


def sentences(base):
    spans, start = [], 0
    for m in re.finditer(r'[.!?]+["\u201d]?\s+', base):
        e = m.end()
        while e > start and base[e - 1].isspace():
            e -= 1
        spans.append((start, e))
        start = m.end()
    if start < len(base):
        spans.append((start, len(base)))
    return spans


def edits_for(base, a, b):
    """the pair of character edits the worked example performs on one sentence"""
    out = []
    fi = next((i for i in range(a, b) if base[i].isalpha()), None)
    li = next((i for i in range(b - 1, a - 1, -1) if base[i].isalpha()), None)
    if fi is not None and base[fi].isupper():
        out.append((fi, base[fi].lower()))
    if li is not None and base[li].islower():
        out.append((li, base[li].upper()))
    return out


def run(base, label, trail):
    sp = sentences(base)
    per = [edits_for(base, a, b) for a, b in sp]
    print(f"{label}: sentences={len(sp)} edits/sentence={[len(e) for e in per]} candidates={2**len(sp)}", flush=True)
    ba = bytearray(base.encode())
    body = bytes(ba)
    found = []
    seen = 0
    for mask in range(1 << len(sp)):
        touched = []
        for k in range(len(sp)):
            if mask >> k & 1:
                for i, c in per[k]:
                    ba[i] = ord(c)
                    touched.append(i)
        m = hashlib.md5(bytes(ba)).hexdigest()
        seen += 1
        if m.startswith(PREFIX):
            found.append((mask, m, bytes(ba)))
        for i in touched:
            ba[i] = body[i]
    print(f"  candidates={seen}  {PREFIX} survivors={len(found)}", flush=True)
    return found


def main():
    total_c, total_s, hits = 0, 0, 0
    for join, jname in (("\r\n\r\n", "CRLF"), ("\n\n", "LF")):
        for trail in (False, True):
            base = join.join(paras) + (join if trail else "")
            label = f"{jname}{'+t' if trail else ''}"
            for mask, m, data in run(base, label, trail):
                total_s += 1
                print(f"   survivor mask={mask:05d} md5={m}", flush=True)
                k, c = btc.master_key(btc.mnemonic_seed(btc.entropy_to_mnemonic(bytes.fromhex(m))))
                for d in (44 + btc.H, 0 + btc.H, 0 + btc.H, 0):
                    k, c = btc.ckd_priv(k, c, d)
                for i in range(78):
                    ki, _ = btc.ckd_priv(k, c, i)
                    if btc.p2pkh(btc.pubkey(ki)) == ESCROW:
                        hits += 1
                        print("   *** ESCROW MATCH ***", label, mask, m, "index", i, flush=True)
    print(f"\ntotal survivors derived: {total_s}  escrow matches: {hits}")


if __name__ == "__main__":
    main()
