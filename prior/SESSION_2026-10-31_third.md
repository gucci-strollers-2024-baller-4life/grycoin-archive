# Session 2026-10-31 (third): class-3 slips closed, paste bases closed

Fresh sandbox. Nothing carried over from the previous sessions except this repo, so the first
job was to rebuild the harness and re-certify the base before any new claim. Then the two
families `SLIP_PATTERNS.md` §8.2-8.3 named as never enumerated.

## 0. Harness rebuilt and certified from scratch

| check | result |
|---|---|
| `harness/btc.py` pure-python pipeline, md5 `9dd2efb9…` @ 0 | `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` ✔ |
| `python3 build_base.py` | LF `46a308c2…`, CRLF `db11a7fd…`, mixed `bd07e6ee…` — all three reproduce ✔ |
| Wattpad length arithmetic (44,896 + 10 breaks + 544 separators + 1) | 45,451 = stored `length` ✔ |
| `h160(14zMkT…)` | `2bc16867479a8d01179a6452651abe14a65eb61a` ✔ |
| new `harness/fast2.py` (coincurve 21.0, local wordlist, own base58, h160 compare) | 1,000-word list self-check passes ✔ |

Throughput in this sandbox: **560-580 address-verified derivations/second**, one core
(`hashlib.pbkdf2_hmac` dominates; the EC step is negligible). That matches the ~450/s figure in
`STATE_OF_HUNT.md` and sets the budget for everything below.

## 1. Class-3 slips — the family §8.2 named, now swept and closed

Her documented error on the answer's own layer is a wrong-direction flip or a stray capital
(R2 b12, "solution was grycoin, not Grycoin … first mistake of this round"). Ported to stage two
that means: take an accepted sign set, then

- **tier A**: invert the flip direction of exactly one paragraph in the set;
- **tier B**: apply the set normally and add exactly one stray case toggle, kept inside the set's
  own paragraphs (where a typo would land).

Script `sweeps/class3_slips.py`. Bases: the two certified serialisations. Sets: the four FFWW
windows (`230-234`, `231-235` both readings), the three windows together, all four windows
together. Modes A (first↓ last↑, the certified stage-one direction) and B (the inverse). Indices
0, 1, 2, 76, 77. Both escrows compared on hash160.

| tier | candidates | derivations | hits |
|---|---|---|---|
| A, one paragraph inverted | 155 | 775 | 0 |
| B, one stray capital inside the set | 23,907 | 119,535 | 0 |

## 2. The same slip, widened to every accepted set, plus the claimer's paste (§8.3)

Script `sweeps/slip_extension.py`. Same inversion logic, applied to twelve sets: `non_ITASM`
(147 by first *non-space* char), `ITASM`, `non_SATOI`, the 14 "signs" paragraphs, the
trailing-space paragraphs (17 segment-bearing, 13 by the docs' count), the lowercase-initial
paragraphs, the 63 quoted paragraphs, the narrative complement (210), and the four windows.
Bases: certified LF, certified CRLF-mixed, plus the two "claimer's paste" builds — trailing
spaces dropped per paragraph, and every trailing whitespace character dropped — because §8.3
asks whether she hashed the text as a browser copy hands it back rather than as wattpad stores
it. Indices 0, 1, 2, 44, 76, 77.

**5,628 candidates, 33,768 derivations, 0 hits, 60 s.**

## 3. Why this is outside the earlier closures

Every previous set sweep applied **one** edge mode to a whole set; the `2^20` mechanism closure
enumerated arbitrary paragraph *subsets* under a fixed mode. A per-paragraph direction (one
paragraph the wrong way, the rest the right way) is not a member of that closure, which is why
§8.2 called it out. It is now closed on every set the corpus has ever proposed, in both
directions, on four bases, at six indices.

## 4. Totals

**154,078 address-verified derivations this session, 0 hits.** Cumulative index coverage for the
chapter battery stays 0, 1, 2, 3, 4, 5, 6, 7, 44, 76, 77.

## 5. Primary-source check: the demo thread (as_cleczc, 13 comments)

Re-read in full; nothing contradicts the corpus, and two quotes are worth pinning because they
bound the demo's search:

- Aoi, 2019-08-02: *"I am saying copy paste and do not change anything with the line breaks,
  change only the capitalization of letters in solution."* — no edits other than case, and the
  line breaks are whatever her paste produced. The `3c6` solution hash therefore has to come
  from `demo_base.txt` bytes with case changes only.
- Aoi, 2019-08-03: the swing at the answer ("the first seven digits of that MD5 hash are
  7759227") **confirms the question hash she hashed was our LF2 base**, and she repeats that the
  letter choice is obvious from the stage-one solution while the claim step is not.

Also on the record and already known: `puzzleponky` asked for the un-edited question hash
because a non-Windows copy produces `\n` breaks only — the same paste hazard the chapter base
was repaired for (§1 above).

## 6. What is left, and what it costs

1. **The demo (block 2) as calibration.** Its answer needs ≥5 case flips (k≤4 anywhere is
   closed by the GPU hunt), and the 12-bit `3c6` oracle only costs an md5. Feasible shapes are
   structured ones — a mark set derived from the demo's own words — not blind subsets.
2. **The chapter's claim step.** Index, path and the two-hop password-manager chain are swept on
   the accepted sets. What has *not* been swept is a hop applied to the class-3 slip variants
   (this session's 24k states); at two PBKDF2 builds per candidate that is ~4 h for the tier-B
   space on one core, which is the most expensive remaining shape that is not blind.
3. **Blind spaces** are out of reach here: the 31.8M non-adjacent deletion space alone is ~15 h
   at this sandbox's rate, and the author forbids deletions anyway ("change only the
   capitalization of letters").
