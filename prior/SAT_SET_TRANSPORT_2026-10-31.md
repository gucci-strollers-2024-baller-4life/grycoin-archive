# The in-class transport sweep: two alphabets, 432 derivations, 0 hits, plus two structural findings

**Date:** 2026-10-31
**Script:** `sweeps/sat_set_transport.py` (results in `sat_set_transport_results_SATOSHI.json`
and `sat_set_transport_results_AIMOST.json`)
**Derivations:** 432 across the two alphabets. Nothing here interacts with any earlier negative.

## 1. The sets, and the two paragraphs that are not prose

Under the letters of SATOSHI `{S,A,T,O,H,I}` the chapter splits 178 in-class / 94 out-of-class.
The split is not 179/94 because **¶15 is `"2020."`** and carries no letters at all, so it can be
neither marked nor excluded.

The out-class 94 is contaminated by formatting. Ten paragraphs are list labels `a)` through `f)`
in two sections: ¶176, 182, 209, 215, 250, 252, 254, 256, 258, 260. Eight of them fall in the
out-class set, because `B C D E` are not SATOSHI letters, and the other two, `a)` and `f)`, fall
in-class because `A` and `F` are. Under `{I,T,A,S,M}` all ten are out-class, so **ten of the 118
non-ITASM paragraphs are subheadings** rather than prose.

True prose sets:

| letter test | all | minus subheadings |
|---|---|---|
| SATOSHI in-class | 178 | 176 |
| SATOSHI out-class | 94 | **86** |
| ITASM out-class | 118 | **108** |

Every sweep in the corpus to date used the unreduced sets.

## 1b. The second alphabet

`fb3cb47` established that SATOSHI's six letters do not reproduce the Finney post: ¶11 opens on `M`,
which SATOSHI excludes, so that test leaves five anomalies there. The minimal fixed alphabet that
gives exactly four on both the Finney post and the demo is `{A,I,M,O,S,T}`. Both alphabets are
therefore run in full, since the chapter split differs:

| alphabet | in-class | out-class | in-class minus subheadings | out-class minus subheadings |
|---|---|---|---|---|
| `SATOSHI` = AIHOST | 178 | 94 | 176 | 86 |
| `AIMOST` | 169 | 103 | 167 | 95 |

## 2. The ledger

Transport = move the capital from the unit's first letter to its last letter (first down, last up),
the certified stage-one edit. Strict means only units that actually can move, first uppercase and
last lowercase, are moved; forced applies it regardless. Four serialisations (`\n\n` and `\r\n\r\n`,
with and without a trailing join), indices 0, 1, 2, 44, 76, 77, screened against `14zMkTga…`.

Each lane is one marked set, so each contributes 4 texts and 24 derivations.

| lane | marked SATOSHI | moved | marked AIMOST | moved | capitals | hits |
|---|---|---|---|---|---|---|
| L1 in-class, paragraph, strict | 178 | 168 | 169 | 159 | 1344 → 1344 | 0 |
| L2 in-class, paragraph, forced | 178 | 178 | 169 | 169 | 1344 → 1338 | 0 |
| L3a out-class, paragraph, strict | 94 | 85 | 103 | 94 | 1344 → 1344 | 0 |
| L3b out-class, paragraph, forced | 94 | 94 | 103 | 103 | 1344 → 1351 | 0 |
| L4 in-class, sentence, strict | 178 | 413 | 169 | 395 | 1344 → 1344 | 0 |
| L5 in-class, paragraph, inverted | 178 | **0** | 169 | **0** | 1344 → 1344 | 0 |
| L6 in-class minus reprint, strict | 177 | 167 | 168 | 158 | 1344 → 1344 | 0 |
| L7 in-class minus subheadings, strict | 176 | 168 | 167 | 159 | 1344 → 1344 | 0 |
| L8 out-class minus subheadings, strict | 86 | 85 | 95 | 94 | 1344 → 1344 | 0 |

## 3. Two findings that outlive the negative

**The inverted transport is a structural no-op.** L5 moves zero units under either alphabet: **no paragraph in the
chapter starts on a lowercase letter and ends on an uppercase one.** The strict lanes conserve the
capital count exactly (1344), so they are the faithful edit; the forced lanes leak, +6 and +7, which
is the diagnostic that marks them as the wrong reading rather than an alternative one.

**The 94-set was never the anomaly set it was called.** Eight of its members are typographic labels,
and the same holds for ten members of the 118. This does not rescue any earlier family, it retires
the set description: every "non-ITASM" figure in the corpus over-counts prose anomalies by ten.

## 4. Overlap with existing work, stated plainly

`CLUES_CANONICAL` §13.3 already swept sign-letter families, including SATOSHI, across
first-letter in/out, last-letter in/out, eight edge modes, both joins and two derivation paths,
1,408 derivations at index 0. This pass overlaps that axis and extends it in two dimensions only:
indices 44, 76 and 77, and the trailing-join serialisations, plus the sentence-level reading and
the sub-set variants in L6–L8. It is a wider negative on the same hypothesis, not a new hypothesis.

## 5. What this does not close

The open variable is *which* units carry signs, and how many. That is `CLUES_CANONICAL` **§9, open
leads, lead 1**: *"The only open variable is which paragraphs get flipped."* This paragraph previously
cited a `§13.9`, which does not exist (§13 runs 13.1 to 13.5), so it has been re-anchored to §9, which
is the corpus's actual open-leads list. A single marked set per lane cannot reach that variable, and
4-unit selection from 178 paragraphs is C(178,4) = 40,432,700 before serialisation, which is a day and
a half of this machine. At sentence scale the chapter has 664 units, so the free-count reading is
2^664 and is not a sweep at all. If that space is to be entered it needs a rule that names the units,
not a sweep.
