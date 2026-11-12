#!/usr/bin/env python3
"""demo_two_edit_closure.py - exhaustive closure of the demo at the author's own stated edit count.

She says the answer is made by keeping the whole text and changing "only a couple of letters in their
capitalization". Every prior demo sweep varied WHICH units were selected but always constrained the
edits to structural edges (paragraph, sentence, word). The exhaustive dictionaries of those families are
closed: 3^15 sentences, 4^10 paragraphs, 2^15 sentence pairs.

What has never been enumerated is the author's literal statement taken as a bound on the EDIT COUNT
rather than on the unit: two case flips, anywhere in the text, edges or interiors. That is not a hash
space, it is a complete enumeration of every text that satisfies her sentence:

    C(1160, 2) x 4 direction combinations + 1160 single edits + the unedited base  =  2,691,381 texts
    x 4 serializations (CRLF / LF join, trailing separator or not)

Screened by the published oracle (md5 begins `3c6`, 1 in 4096), survivors derived at
m/44'/0'/0'/0/{0,1,2} against 1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi.
"""
import hashlib, re, sys, time
sys.path.insert(0, "harness")
import btc

ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
PREFIX = "3c6"
txt = open("demo_base.txt", encoding="utf-8", newline="").read()
PARAS = [p for p in re.split(r"\r?\n\r?\n", txt.strip()) if p.strip()]
assert len(PARAS) == 10


def derive3(md5hex):
    k, c = btc.master_key(btc.mnemonic_seed(btc.entropy_to_mnemonic(bytes.fromhex(md5hex))))
    for d in (44 + btc.H, 0 + btc.H, 0 + btc.H, 0):
        k, c = btc.ckd_priv(k, c, d)
    out = {}
    for i in (0, 1, 2):
        out[i] = btc.p2pkh(btc.pubkey(btc.ckd_priv(k, c, i)[0]))
    return out


def sweep(base, label):
    raw = base.encode()
    n = len(raw)
    positions = [p for p in range(n) if chr(raw[p]).isalpha()]
    flips = {p: (chr(raw[p]).swapcase()).encode() for p in positions}
    survivors = []
    t0 = time.time()
    count = 0

    # base, single edits
    cand = [raw]
    for p in positions:
        cand.append(raw[:p] + flips[p] + raw[p + 1:])
    for text in cand:
        count += 1
        m = hashlib.md5(text).hexdigest()
        if m.startswith(PREFIX):
            survivors.append((m, text))

    # pairs
    np_ = len(positions)
    for a in range(np_):
        p = positions[a]
        head = raw[:p] + flips[p]
        for b in range(a + 1, np_):
            q = positions[b]
            m = hashlib.md5(head + raw[p + 1:q] + flips[q] + raw[q + 1:]).hexdigest()
            count += 1
            if m.startswith(PREFIX):
                survivors.append((m, head + raw[p + 1:q] + flips[q] + raw[q + 1:]))
    dt = time.time() - t0
    print(f"{label}: positions={np_} candidates={count} in {dt:.1f}s ({count/dt/1000:.0f}k/s) "
          f"survivors={len(survivors)}", flush=True)
    return survivors


def main():
    allhits = 0
    for join, jname in (("\r\n\r\n", "CRLF"), ("\n\n", "LF")):
        for trail in (False, True):
            base = join.join(PARAS) + (join if trail else "")
            surv = sweep(base, f"{jname}{'+t' if trail else ''}")
            seen = set()
            for m, text in surv:
                if m in seen:
                    continue
                seen.add(m)
                for i, a in derive3(m).items():
                    if a == ESCROW:
                        allhits += 1
                        print("   *** ESCROW MATCH ***", jname, trail, m, "index", i, flush=True)
                        open("demo_two_edit_MATCH.txt", "wb").write(text)
            print(f"   derived {len(seen)} distinct survivors at indices 0/1/2", flush=True)
    print(f"\nescrow matches: {allhits}")


if __name__ == "__main__":
    main()
