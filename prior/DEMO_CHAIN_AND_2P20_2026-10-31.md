# The demo escrow is real and was swept on August 3, and the whole endpoint family fails on it

**Date:** 2026-10-31

## 1. The demo escrow on chain

`1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi`, from blockstream:

| | |
|---|---|
| funded | block 588,035, 2019-08-01T03:04:38Z, **700,000 sats**, out of a 77,690,300-sat transaction from `1CemUGFXwTVv…` |
| swept | block 588,406, 2019-08-03T11:22:10Z, 689,594 sats to `129jw1GUGwiJ…`, fee ~10,406 |
| tx count | 2 |

So the demo's prize was real and was moved **three days after funding, on the same date as the "Block 77
solved … shutting down" announcement**. That is the strongest candidate explanation for the August tweet:
it was the demo, not stage two.

It is not decisive on its own, though. The block-77 escrow was also swept by the author when he wound the
experiment down, so a sweep three days after funding is equally consistent with (a) a solver claiming the
demo, or (b) the author reclaiming it while closing up. If (a), the demo is a certified solved instance of
the stage-two mechanic and the rule must work somewhere. If (b), the demo proves nothing and may be as
unreachable as the chapter.

## 2. Exhaustive endpoint sweep on the demo

The demo's 10 paragraphs give 20 endpoint characters (the head and the last alphabetic character of each).
Flipping any *subset* of those 20, at every cardinality, is 2^20 - 1 = 1,048,575 candidates — the whole
endpoint family, not only the "both ends of selected paragraphs" shape the chapter sweeps used.

| join | text chars | begin `3c6` | derive to the demo escrow, index 0 |
|---|---|---|---|
| LF (`\n\n`) | 1,549 | 257 (chance ≈ 256) | **0** |
| CRLF (`\r\n\r\n`, the author's stated separator) | 1,567 | 261 | **0** |

Both joins, both exhausted. With the earlier closures — 717,003 arbitrary one- and two-character flips, the
1,023 both-ends paragraph subsets, indices 0 through 2 — the demo is not reachable by any endpoint-casing
reading of its own text.

## 3. Boundary trims on the chapter

The demo's one explicit hashing instruction is a *boundary* instruction: "Start with the first `I` and stop
with the period after `method`", with no leading or trailing whitespace included. That reading had never
been applied to the chapter, so:

- every prefix truncation, drop the first k paragraphs for k = 1…272: 272 candidates
- every suffix truncation, drop the last k: 272 candidates
- strip leading/trailing whitespace, drop the final period, drop the title and strip: 5 candidates

**551 candidates at index 0, zero hits.** Paragraph-granularity boundaries are closed. Sentence-granularity
boundaries (~2,000 single trims) remain open and are cheap.

## 4. What this does not license

"Formal decoy" is a conclusion about intent that the evidence does not support. What is established is
narrower and stranger: the published rule does not reproduce the published example, at every cardinality
and both joins. That is at least as likely to be our modelling error — the slice, the join, or which
characters count as endpoints — as a deliberate trap. The one thing that is certain is that the family has
**no certified stage-two instance**: stage one is certified, but it is the Hal-post mechanism, and both
stage-two-shaped objects we hold are unresolved.

## 3. k=3 at word edges: closed (2026-11-08)

`demo_k3_edge.c` — every 3-letter case flip over the demo's 546 word-edge positions:
27,277,796 derivations, 6,551 md5 hits beginning `3c6` (chance 27.3M/4096 ≈ 6,659),
each derived at index 0 via `check_hits.py`. **None lands on the demo escrow.**

## 4. The author says he lost the solution

`corpus.json` part 762380140 ("Starting Up", 2019-07-23), ¶12:

> "The real big block will stay in the background. No hints for that one until further notice.
> As a consequence of getting shut down and starting up again, I have lost any information on
> the solution of that one. Tragic boating accident variation."

That is why no hint and no hash digits were ever published for stage two, and it means no
living party can confirm a solve except by deriving the address.

## 5. Reprint restore: closed (2026-11-08)

Each of ¶231–¶235 offered four readings — chapter form, certified stage-one paragraph with
its quotation marks, the bare stage-one paragraph, and the chapter paragraph with only its
two endpoint cases reversed — across all 4^5 = 1,024 combinations, derived at index 0.
**Zero hits.** The reprint is not the edit, in any mix, including the exact stage-one bytes.

The diffs are exact: ¶232/¶233/¶235 differ from the certified text only by both endpoint cases
being reversed (`f…T`→`F…t`, `w…N`→`W…n`, `w…M`→`W…m`), ¶231 by its tail (`S`→`s`), ¶234 by
Hal's `facinating` corrected to `fascinating`, and each by an added pair of quotation marks.

## 6. Index space and 44-boundary extracts (2026-11-11)

- Certified base measured in UTF-8 bytes: **45,456** (45,450 characters + six two-byte NBSPs).
  The md5 was always taken over those bytes, so no substrate change is implied.
- Index sweep 0–2047 on the unedited base at `m/44'/0'/0'/0/i`: **no hit**.
- 44-boundary and palimpsest extracts at index 0 (first 44, last 44, both, middle ¶45–229,
  ¶44+¶230, ¶34+¶78, S-I-S-I ¶1–4, Block-29 quotes ¶11–12, the FFWW quad, ¶229–235,
  ¶242–246, ¶1–44+¶242–246): **no hit**.
- Full k=3 sweep over all 1,197 alphabetic positions of `demo_base.txt` completed:
  285,129,390 triples, **69,424** md5 hits beginning `3c6` against a chance expectation of
  69,600. Derivation of all hits against the demo escrow is running.

## 7. TOMI-suffix hypothesis for 3c6 (2026-11-11)

- The certified demo hash `7759227d…` is the **LF** join: 1,549 chars. The CRLF join is
  1,567 chars and hashes to `e9970079…`. The author's "13 10 13 10" remark therefore describes
  Reddit's storage, not his hash input, and the LF base stands.
- Suffix search: three bases (CRLF with ¶5 flipped, LF with ¶5 flipped, LF raw) × 4,630-word
  dictionary (corpus + BIP39) × {Grycoin, grycoin} × four suffix shapes including a
  `\r\n\r\nTOMI …` variant: 111,120 candidates, **28** beginning `3c6` against a chance
  expectation of 27, and none deriving to the demo escrow. The 3c6 gap is not a two-word
  TOMI field.

## 8. Structural read (2026-11-11)

Wattpad's `data-p-id` is minted at creation and left stale on edit; 272 of 273 paragraphs
reconcile, so **only ¶78 has ever been edited**. The part was created 2019-04-17 and last
modified 2019-07-23T23:12:04Z, so 272 paragraphs are April text and exactly one paragraph is
the July change. The escrow was funded 2019-07-30, after that edit, so the current ¶78 is the
one in the preimage; the original ¶78 is a curiosity, not the answer.

Also negative this round: the stage-one editorial marker appended to the chapter
(`\n[edited slightly]` and five variants), 72 pipeline variants on the certified md5
(entropy as raw 16 bytes vs the 32-byte hex string; salt `mnemonic` vs empty; passphrases
`''`/`grycoin`/`Second`; paths `m/44'/0'/0'/0/0`, `m/0'/0/0`, `m/44'/0'/0'`; compressed and
uncompressed P2PKH), and a hunt for the pre-edit ¶78 among every paragraph, sentence and
quoted variant in the chapter and in Hal's post (no match for `8b71bade…`).
