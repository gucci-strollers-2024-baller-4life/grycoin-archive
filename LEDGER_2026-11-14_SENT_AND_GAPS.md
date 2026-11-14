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
