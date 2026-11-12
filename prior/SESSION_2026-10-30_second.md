# Session 2026-10-30 (second pass) — post-repair re-validation, two base corrections, 715k candidates

Harness: `/tmp/fast.py` (coincurve, 1,185 derivations/s), validated this session against the solved
stage-one escrow (`9dd2efb9…` → `19TbyN5…`) before any sweep. Indices 0, 1, 2, 44, 76, 77 (the author's
own "Nth private key for block N" convention); escrows `14zMkTga…` (live) and `1EFojcAo…` (refunded).

## 1. Closures that were produced before the base58 repair, re-run

The base58 leading-zero bug (commit `5060d61`) made every address-string comparison fail, so every
negative produced before that fix is void. Re-run here on the repaired harness:

| family | candidates | hits |
|---|---|---|
| contiguous run of paragraphs as the **entire** preimage, every run 1..273, three bases, six indices | 674,370 | 0 |
| sign-letter families {ITASM, SATOSHI, THOMAS, NAKAMOTO, FINNEY, HALFINNEY, STNM, AOI, SATOMI, SH, OH} × first/last membership × 8 edge modes, three bases, indices 0/1/2/76 | 8,304 | 0 |
| 44-lattice families and all 2⁶−1 subsets of {34,78,122,166,210,254}, three bases | 8,304 (shared run) | 0 |
| R1 name marking, seed-anchored and greedy chains, 22 name orders, three bases | 2,064 | 0 |
| demo name marking FINNEY / THOMAS / GRYCOIN, every `3c6` survivor re-derived (fixed harness, indices 0/1/2/76) | 81,600 derivations over 81,528 survivors | 0 |

## 2. New families applied this pass (all negative)

| family | candidates |
|---|---|
| **paragraph-selected × sentence-flipped** — choose paragraphs by a sign test, then flip at *sentence* edges inside them (the demo's device is sentence-level, stage one's selection is paragraph-level; the two had never been combined) | 3,564 |
| **keyword sign sets** — paragraphs selected by the hint's own words (sign/signs, recognize, identity, today, real, and the union of the instruction's five words) plus complements | 2,754 |
| **stride keys as case EDITS for the strides §20 never used** — 2,3,4,5,11,21,22,37,77,88 at word granularity with every offset and four directions, plus letter granularity at 4,7,11,22,44 | 22,608 |

§20 had applied strides 7 and 44 only; the rest of the stride family is now closed as a case selector.

## 3. Two base corrections

**3.1 The demo's certified base is the ten-paragraph Question block, and the "slice" reading is falsified.**
`demo_base.txt` (ten paragraphs, LF-LF) hashes to `7759227d7406…`, the value the author published
("first seven digits of that MD5 hash are 7759227"). `demo_post_lf.txt` — the 1,456-character "slice" of
`CLUES_CANONICAL.md` §14.1 — hashes to `2bc61c2e…`, because it starts at the post's preamble
("I still have not completely given up…") instead of at the Question block's first word. So the slice is
**not** the author's preimage, and the §14.1 conclusion ("either it flips four or more letters or the
slice boundaries differ") resolves to the first branch: the boundaries are settled, the demo flips four
or more letters. Every sweep run on `demo_post_*.txt` tested a preimage the author never hashed.

**3.2 The chapter repair does not touch the letter stream.** `wp_paras_br.json` stores each paragraph as a
list of lines; joining lines with a single break and paragraphs with the double break changes only the
paragraph boundaries and the 10 internal breaks, never a letter's case. So all case-edit families are
unaffected by the repair except through paragraph selection, which is why the br-crlf and br-lf bases are
swept alongside `chapter_paras_exact.json` in every run above.

## 4. Where this leaves §25's decision

The extraction shape has now had fragments (4,806), reversals (15,283), boustrophedon (144),
edge extraction (253), and — this session — **every contiguous run** as the whole preimage (674,370).
The whole-text shape has had every sign set, the lattice, the name markings, positional keys, and the two
granularity combinations (3,564). Both shapes are negative on the repaired harness at six indices.

The one axis that remains unexhausted is not mechanical: which letters she edited, which she took with her.
