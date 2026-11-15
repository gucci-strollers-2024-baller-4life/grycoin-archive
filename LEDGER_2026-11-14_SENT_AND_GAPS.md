# Two new lanes, 2026-11-14 15:20 UTC

## Why: the demo marks inside a paragraph

The author's own format demo (cleczc, "Grycoin Block 2") says the answer changes the
"I" at the beginning of a paragraph to "i" **and** "himself" to "himselF". In the text
he actually posted, "himself" sits at a sentence end *inside* that paragraph
("...outing himself. Even after I explained the method used and the result in detail.").
A paragraph-edge rule cannot produce that mark. Every sweep in this hunt marks paragraph
edges, so the unit of marking was never controlled.

Note: the demo answer itself remains uncomputable from the post text. Marking the
Question text at sentence granularity (2^15 subsets x 3 mutation modes x 3 joins) yields
54 candidates whose md5 starts 3c6; none derives to `1tzieUf...` at BIP44 indices 0-77.
The demo is used here only as evidence about the *unit*, not as an address oracle.

## LANE 1: GAPS (`ci/gaps.py`, run 43609600805)

Both certified lanes pin one selector/mutation pairing: CLASS selects by paragraph
initial and mutates both ends, TAIL selects by paragraph final and mutates the tail only.
Paragraph 236 ("we are directed to look at the last letter of each of these") licenses
separating the two, so three pairings had never been hashed:

| lane | selection | mutation | masks |
|---|---|---|---|
| L1 | paragraph initial, 21 axes | tail only | 2^21 |
| L2 | paragraph initial, 21 axes | head only | 2^21 |
| L3 | paragraph final, 18 axes | head only | 2^18 |

28,311,552 derivations, both joins, indices 0-2, both escrows. Gate reproduces all three
certified digests and proves each lane's construction byte-identical at four probes.

## LANE 2: SENT (`ci/sent.py`, run 43609896672)

The certified mechanic applied to **sentences**: 670 units, 22 distinct initials
(ABCDEFGHIJKLMNOPRSTVWY), 2^22 masks, mark when the sentence initial is outside the
class, lower its first alphabetic and raise its last. Both joins, indices 0-2, both
escrows, 25,165,824 derivations. The identity mask reproduces 46a308c2 and bd07e6ee
byte-exactly, and the sentence space strictly contains the paragraph-edge class space
(the first and last sentence of every paragraph carry its head and tail).

## Status of the earlier queue

Mega run 43578710933 (viol 2^25 on the as-is base, class family on six cleaned base
variants, tail-only) still has 15 of 20 shards in progress at 15:25 UTC. Shard 8's
violator lane is a certified negative: 1,677,721 masks, indices 0, zero hits, 1,429
derivations/s.

## Run accounting, corrected (accepted)

Valid, gated coverage of the 2^25 violator lane is **46,137,344 derivations**, not
88,207,360:

- `43570563558` (fix commit's own run): 2^25 masks at index 0, CRLF only, because the LF
  join prints "skip duplicate join under V1" = 33,554,432 derivations.
- `43574235865`: 4,194,304 masks x indices 0,1,2 = 12,582,912 derivations.
- `43567789115` and `43568736664` are **void**: the splice bug
  `flip[vm] if (mask >> vm) & 1 else norm[i]` appends the wrong paragraph whenever a bit
  is set, and neither calls `gate(P)`. Their 33,554,400 + 16,777,216 come off the books.
- K2 (`43576012943`) is cancelled, 20/20, no coverage.

The index point stands as the user states it: the harness increments `n` before the index
loop, so `n` counts masks and the printed rate is masks/s. A shard at 330 masks/s with
three indices is 990 derivations/s, consistent with the 917-954 derivation/s the violator
lanes measure; at index 0 alone the same wall clock would have shown ~950 masks/s.

## Local content-and-word families, 15:35-15:45 UTC (all zero, both escrows)

The chapter was swept along the axis no arithmetic sweep touches: which paragraphs you
would *recognise* as carrying the sign. Every family below was derived at indices 0-2 on
LF, CRLF2 and single-CRLF, comparing against `14zMk` and `1EFojcAo`.

| family | selection rule | documents | derivations |
|---|---|---|---|
| words | set of paragraphs containing a given word (1,704 distinct sets, with complements) x 3 mark modes x 3 joins | 15,336 | 46,008 |
| phrases | paragraphs containing a given bigram (1,016 sets, with complements) | 9,144 | 27,432 |
| names | every occurrence of each letter of AOI, YANG, FINNEY, HAL, SATOSHI, NAKAMOTO, AOINAKAMOTO, HALFINNEY, GRYCOIN, SATOMI, THOMAS, STNM, AOIN, OI, GREEN, FOWLER, upper and normalised | 102 | 306 |
| features | 27 structural predicates (ends with ? ! or "; opens with a quote; digits; colons; length <60, >600, ==44; contains Satoshi, Finney, identity, sign, crypt, hash, letter, name, proof, Grycoin, ellipsis, quote mark) x in/out x 3 modes | 432 | 1,296 |
| word marks | for each of 1,493 word types, upper the last letter / upper the first / upper the first occurrence only (the block-29 shape: "change the o and i in 'voice'") | 13,434 | 40,302 |
| sentence content | 1,444 word types selecting sentences inside the 670-sentence parse, 3 modes | 8,664 | 25,992 |
| word windows | first and last k=1..5 words of each paragraph (paragraph 242's "first four and last four words"), heads/tails/both, plus the four FFWW windows, plus the chapter's own first and last four words | 192 | 576 |
| hint paragraphs | the two paragraphs that end "recognize the signs" (222, 273), 244, 241, the 14 signs paragraphs, each with 3 modes and the 4-word window | 126 | 378 |

Total 47,430 documents, 142,290 derivations, zero hits.

Reading: the marks are neither an arithmetic class (closed earlier) nor a content keyword,
a word-shape, a name's own letters, a punctuation feature, a length class, or the paragraph
242 word window. Those are the only selection rules the chapter's own text licenses, so the
selection is judgement, not a rule, and no further structured sweep on this text is going to
find it.

## Name lane 4030e56: case direction and what a demo hit would transfer

**Case direction, confirmed from the committed source.** `mark()` is
`b[p] = c - 32 if 97 <= c <= 122 else c` and nothing else: it rewrites a lowercase letter
to its uppercase form at each chosen position. There is no lowering branch anywhere in the
file, and a chosen position that is already uppercase is a no-op, leaving the document
byte-identical to the base at that offset. So 4030e56 tests **lowercase → uppercase only**;
the demo's own worked example (`I` → `i`, lowercased, plus `f` → `F`) is a two-direction
rule and is **not** covered by this lane. Those two directions are covered elsewhere and
separately: the paragraph-edge and sentence-edge families lower the first alphabetic of a
selected unit and raise the last, and the local word-mark family ran `first` (lower) as well
as `last` (upper) over all 1,493 word types at every occurrence. What this lane adds is the
block-2/29 device specifically: a name spelled by uppercasing one occurrence of each of its
letters, with nothing lowered.

**Expectation on a cleczc hit.** FINNEY on this 1,549-byte demo has 92,104,718 in-order
embeddings; the same name on the 45,450-byte chapter has on the order of 1e14, so the demo
result alone does not transfer. It transfers only if the winning placement is structurally
tight, because a tight placement is a rule that can be re-run on the chapter while a
scattered one is an arbitrary offset. Every hit therefore prints a containment report:
paragraphs, distinct words, distinct sentences, the span, the spread, the largest gap, and
`all_one_word` / `all_one_sentence`. Probes on the demo come out scattered
(`paragraphs=4 words=6 sentences=4 span=47..1084 spread=1037`), which is the shape that
would *not* transfer; the shape that would is `words=1` or `sentences=1` with a small span.

The three runs already dispatched (`43611136238` NFINNEY, `43611141897` NTHOMAS,
`43611146983` NGRYCOIN) are pinned to 4030e56 and predate this diagnostic, but each hit
writes its full text to `HIT_NAME_<name>_<ordinal>_<join>_<idx>.txt`, so the same report
can be recomputed from the artifact after the fact.

No further work is stacked on the queue, per instruction. The eight runs in flight or
queued are the mega, GAPS, SENT, SENTT, CLWS, NFINNEY, NTHOMAS, NGRYCOIN and MSG.

## The demo, three new closures (2019 thread evidence + derived)

The demo's own thread supplies a sentence the hunt had not used. Asked what letters the
demo changes, the author wrote on 2019-08-03: "The question of what letters to change in
capitalization is obvious if you know the solution to Satoshi's bitcointalk puzzle, which I
revealed already. The question of how to go from that to claiming the prize is not, not even
to me." So the mark *choice* is the revealed puzzle solution (the FFWW / STNM signature) and
the author himself never had the derivation path. That reframes the demo as a known-answer
instance for the letters only.

1. **The literal illustration is dead at any index.** `I`→`i` at ¶5's head plus
   `himself`→`himselF` at its tail, four serializations (LF, CRLF2, and each with a trailing
   newline), derived at **indices 0 through 4,999**: 20,000 derivations, zero hits on
   `1tzieUf…`. The earlier note had only reached index 5. So the demo answer is not the two
   flips the demo describes, at any plausible derivation index, in any of the four byte forms.

2. **STNM cannot be spelled by the demo's paragraph tails at all.** The demo's ten paragraph
   tails are `T N N S L I F D E D` and its heads `I A F F I O W W I A`. There is no T after the
   S, so "STNM" has **zero** in-order embeddings at paragraph granularity. That is why every
   demo sweep built on paragraph-edge selection is structurally empty for this message, and it
   is independent evidence that the demo's unit is not the paragraph.

3. **Letters-level STNM is negative.** Uppercasing one in-order occurrence each of S, T, N, M
   anywhere in the demo (694,082 embeddings), in two variants (plain, and with the head of every
   paragraph containing a mark lowered to the certified mechanic's shape), on LF and CRLF2:
   2,776,328 documents, 10,833 at `3c`, 684 at `3c6` (chance is 678), 32,499 derivations at
   indices 0-2, **zero** hits. So the demo's marks are not "one in-order occurrence of the
   signature anywhere in the text" either.

Together with the earlier closures (all 1,024 paragraph subsets x 9 modes, all 32 sign-set
subsets x first/last/both, 717,003 one- and two-character flips screened on the prefix), the
demo now has no reading left that this hunt can test without the derivation path that the
author says he never had.

## The author's numbered posts in r/real_big_block_discussion (never mined before)

Fifteen comments by the author in that thread, numbered by him "for later reference". Two matter
directly:

- **1.** "When I posted the real big block at the Wattpad site, I added extra line breaks between
  paragraphs. This information is needed to solve the block."
- **7.** "I took back the prize for a moment and sent it again to a new address, hashing with a
  slightly different solution… It has multiple paragraphs and **two line breaks between each of
  them**." Clarified when asked what that looks like in ASCII: "Hit enter twice. This displays in
  Ascii as 13 10 13 10."

So **CRLF2 (`\r\n\r\n`, i.e. 13 10 13 10) is the authoritative answer serialization**, stated by the
author twice, and the second escrow differs from the first by that serialization alone, with the
mark set unchanged. That is exactly the V1/LIVE split the target map already encodes
(`1EFojcAo` single 13 10, `14zMk` 13 10 13 10), and it means a hit on either escrow confirms the same
marks. Every lane that runs both joins is aligned with his own description; LF-only lanes are not.

Also from the stage-one thread, on how the selection is hinted: "Actually there is a hint on how to
solve this right in the post by Hal. Much like the Aa in the genesis block address hinted at the
solution." So the class of hint is a *visible case anomaly* in the text.

## Case-anomaly repair reading (new family, zero)

Scanning the chapter for the analogous anomalies turns up exactly twelve mixed-case tokens, the only
places in 45,450 bytes where a capital sits inside a word after a lowercase or before one:

| ¶ | token |
|---|---|
| 73 | `ppM` |
| 106, 112 | `WorldWideAbsoluteCarbonBudget` |
| 107 | `FUCKFuckFUCKFuckFUCKFuckFUCKX`, `AndrewYangForPresident`, `oXXX` |
| 126 | `abcdefghijkLmnopqruvwxyz`, `abcdefghijkLmnopqrstuvwxyz` |
| 128 | `VIrgin` |
| 136 | `BItcoin` |
| 209 | `BITcoin`, `AHScoin` |

Note ¶126's *first* alphabet example omits exactly **s** and **t** (`…pqruvwxyz`), the two letters of
the signature's tail, and the second repeats the same capital `L`.

Tested: every one of the 256 subsets of those twelve paragraphs with their internal capitals
lowercased (the repair reading, the opposite direction from every previous sweep), on LF and CRLF2,
at indices 0-2: 512 documents, **zero** hits. So the answer is not "repair the anomalies", and the
anomalies are therefore ordinary authoring artefacts rather than the signs themselves.

## Overnight audit: all eight queued runs settled, 921.6M documents, zero hits

Pulled every shard log rather than trusting the run conclusions. Per run: documents counted from the
harness's own `n` (which counts documents, both joins), hits from `***HIT` lines, gate line from the raw
log.

| run | lane | documents | derivations | gate | hits |
|---|---|---|---|---|---|
| 43578710933 | mega, 20 shards | 96,468,992 | (masks) | OK, 20/20 | 0 |
| 43609600805 | GAPS L1/L2/L3 | 8,912,896 | — | OK | 0 |
| 43609896672 | SENT | 8,388,608 | — | OK | 0 |
| 43610061023 | SENTT | 4,194,304 | — | OK | 0 |
| 43610745382 | CLWS, single-CRLF base | 2,097,152 | — | OK | 0 |
| 43611136238 | NFINNEY | 184,209,436 | 2,162,712 | OK | 0 |
| 43611141897 | NTHOMAS | 354,117,806 | 4,150,410 | OK | 0 |
| 43611146983 | NGRYCOIN | 247,121,970 | 2,894,514 | OK | 0 |
| 43611493228 | MSG | 16,777,216 | 50,331,648 | OK | 0 |

Total 921,607,380 documents, zero hits. The name lanes are exhaustive: FINNEY 92,104,718 x 2 joins =
184,209,436, THOMAS 177,058,903 x 2 = 354,117,806, GRYCOIN 123,560,985 x 2 = 247,121,970. So the demo's
block-2/29 name-marking device is closed for all three large names at every in-order placement, both
joins, indices 0-2, under the 3c* filter: 9,207,636 derivations in total.

**One real coverage gap found in MSG.** The gate line reports 363 messages and 8,743,576 embeddings
(the dispatch ran with the default length 2..6, not the 2..5 I sized the grid for), while the 2^23 grid
reaches only 8,388,608. Uncovered: the last 207,437 embeddings of `SYSTEM`, plus `THEORY`, `THINGS`,
`TITLED`, `TRYING`, `WISHES`, `WONDER`, `WRITES` entirely. Dispatched **43684830750** (`MSG2`, commit
`2b5a1be`, space_bits 19 with a 2^23 offset) to close exactly that tail: 354,968 ordinals, 709,936
documents, ~2.1M derivations, about four minutes.

## Re-read of the chapter's own walkthrough (¶228-246): the algorithm in the author's words

Stage one's rule is stated outright in "Second", not inferred:

- **¶228** "Turns out, there are some signs we recognize from the Satoshi anagram. The letters I, T, A, S
  and M as first letters of each paragraph of this post."
- **¶230** "Having seen the signs before, we are directed to look at those four paragraphs, the only ones
  where we don't recognize the signs."
- **¶236** "We are directed to look at the last letter of each of these. Because we are directed by the
  fact that the 'recognize the signs' instruction comes last in the paragraph."
- **¶240** "And it dovetails nicely with 'Nm ST' as a way used to sign in the genesis block. Exactly the
  same signature."

So the selection is: paragraphs whose first letter is **not** in the sign class {I,T,A,S,M}; mark = lower
the first, raise the last. That is the certified 8-flip calibration exactly.

**Arithmetic now kills the transfer of that rule to the chapter, independently of any sweep.** The
chapter has 273 paragraphs over **21 distinct initials** (A36 B11 C4 D3 E3 F14 G6 H11 I47 K1 L1 M2 N5
O15 P3 R2 S19 T50 V3 W27 Y9). For the analogue of stage one to hold, the marked set would have to be
exactly 4 paragraphs, which requires the sign class to contain the initials of the other 269, i.e. at
least 17 letters. A 5-letter class cannot. Concretely, {I,T,A,S,M} selects **118 of 273** paragraphs, not
4. So no initial-class sign set of stage one's size can produce a "couple of letters" on the chapter, and
the whole class lane is dead by counting rather than by having missed a subset.

That leaves "signs" as a **per-paragraph property** (what the paragraph does or contains), which is
exactly the family the name lane and the message-first lanes test. Full verification of the message list:
`STNM` and `FFWW` are both among the 363 messages, so the signature-as-message reading is covered on tails
(run 43611493228 + 43684830750, exhaustive, zero) and is running now on heads (43685708179).

## Whole-word case changes and the demo's letter-level signature (all zero)

Two families closed locally, both cheap and both plausible readings of the manual's block-29 shape
("just change the o and i in 'voice'"):

- **Every occurrence of one word type re-cased.** All 1,482 word types of the chapter, four modes
  each (all letters uppercased, all lowercased, inner letters only, final letter only), both joins,
  indices 0-2: 11,856 documents, 35,568 derivations, zero. So the answer is not "one word of the
  chapter uniformly re-cased", which is the naive generalisation of block 29.
- **The demo at letter level for the signature's own spellings.** In-order placements, both joins,
  deriving only the 3c6-prefixed candidates: `YANG` 130,203 placements (59 at 3c6), `FFWW` 20,033
  (10), `WWFF` 13,468 (3), `UUUU` 58,905 (33), `NMST` 360,876 (146), `TNMS` 887,678 (474). Together
  260,406 + 1.5M documents, zero hits against `1tzieUf…`. Together with the earlier `STNM` closure
  (694,082 placements), every spelling of the certified signature is now negative on the demo at
  letter level, which is the unit its author points at ("obvious if you know the solution to
  Satoshi's bitcointalk puzzle").

Two new lanes dispatched from this: **K3** (43685930762, exhaustive three-paragraph reading,
C(273,3) = 3,353,896 selections, certified mechanic, both joins, targets LIVE+V1) and **DMSG**
(demo letter level over all 56 words of its own vocabulary of length 2..4, 35,522,273 in-order
placements, filtered at 3c with pfx3c6 counted, against the demo escrow).
