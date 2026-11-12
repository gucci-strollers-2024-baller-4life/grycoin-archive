# Block 29 as template: what it actually teaches, and the exhaustive closure it does not survive

**Date:** 2026-10-31
**Scripts:** inline runs against `harness/btc.py`; no new files. Base: `demo_base.txt` (md5 `7759227d7406`,
confirmed by the author in the thread as the unedited question hash).

## 1. Block 29's device, stated exactly

The published, MD5-verified answer to round-1 block 29 is its own 1,360-character input with two characters
changed:

    "A pleasant female vOIce."        capitals: A · O · I

The sentence-initial `A` is already capital and is one of the three letters. The two interior capitals are
added. The capitals spell **AOI**, the author's name. That is the device: keep the text, change a couple of
letters, and the capitals spell the name, with the sentence's own initial free.

## 2. But the actual Rosetta stone for block 77 is stage one, not block 29

`safudev_stage1.txt` in this repo **is** the certified stage-one preimage: md5 `9dd2efb9bc976c2095bd534d7b8d431c`,
the 32-hex that derives to `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`. It differs from `hal_original.txt` by exactly
**eight bytes**, and here they are with paragraph positions (16 paragraphs, joined `\n\n`):

| byte | para | offset | change | context |
|---|---|---|---|---|
| 85 | 2 | 0 | `F` → `f` | ¶ initial, "**F**or those who don't know me" |
| 480 | 2 | 395 | `s` → `S` | ¶ final, "other activitie**s**" |
| 484 | 3 | 0 | `F` → `f` | ¶ initial, "**F**ast forward to late 2008" |
| 713 | 3 | 229 | `t` → `T` | ¶ final, "the paradox of i**t**" |
| 717 | 4 | 0 | `W` → `w` | ¶ initial, "**W**hen Satoshi announced" |
| 924 | 4 | 207 | `n` → `N` | ¶ final, "a knee jerk reactio**n**" |
| 1299 | 6 | 0 | `W` → `w` | ¶ initial, "**W**hen Satoshi announced" |
| 1691 | 6 | 392 | `m` → `M` | ¶ final, "him fixing the**m**" |

The paragraph initials of the post are `I F F W I W T A T S M A T I A T` and the finals are
`e s t n g m s s s g t n s n o y`. The four selected paragraphs are 2, 3, 4, 6 — exactly the paragraphs
whose initial is **not** in `{I,T,A,S,M}`, which in this post is exactly the paragraphs starting with
**F** or **W**. Every selected paragraph gets **first letter down, last letter up**.

Two corrections to how this repo has been describing stage one:

1. `FFWW` and `stnm` are the **output** of the edit, not the signs to be recognised. In the source those
   positions read `F…s`, `F…t`, `W…n`, `W…m`. After the answer they read `f…S`, `f…T`, `w…N`, `w…M`.
   The "signature window" language has been treating the answer as if it were the question.
2. The rule is **paragraph** granularity, one edit at each edge of the paragraph, and the edit is a pair
   (down at the start, up at the end). Nothing here is interior, and nothing here spells a name.

## 3. Why block 29 is not the template for block 77

Block 29 and stage one are different devices, and the RBB is the second stage of **block 77**:

| | selection | edit | what the marks spell |
|---|---|---|---|
| block 29 | one sentence, where the name fits | 2 interior capitals | a name (AOI) |
| block 77 stage one | paragraphs whose initial ∈ {F,W} | first↓ + last↑, 8 characters | nothing; F,F,W,W become f,f,w,w |
| demo (round-2 block 2) | "the paragraphs where you recognise the signs" | "a couple of letters" | ? |

Block 29 is the *precedent* the demo cites for "keep the whole text and change a couple of letters". It is
not the same operation, and treating it as the template imports an interior-spelling model into a
paragraph-edge problem.

## 4. The spelling goal is degenerate on a 1,549-character text, and that is decisive

Applied as a spelling constraint, "the capitals must spell a name" does not select anything. Minimal-cost
markings of candidate names on the demo base, computed exactly (DP over positions, a letter already capital
costs 0):

| name | cheapest marking cost | name | cheapest marking cost |
|---|---|---|---|
| AOI | **0** | SATOSHI | 4 |
| HAL | 2 | SECOND | 4 |
| FINNEY | 2 | SATOMMI | 4 |
| TOMI | 2 | NAKAMOTO | 5 |
| STNM | 3 | GRYCOIN | 5 |
| THOMAS | 3 | SATOSHINAKAMOTO | 10 |
| HALFINNEY | 4 | | |

`AOI` costs **zero**: the demo's capitals already spell A‑O‑I at ¶2 ("**A**s is already clear"), ¶6
("**O**n the other hand") and ¶9 ("**I** think this easy example"). Every plausible name can be spelled for
four or five edits out of 1,197 positions. So "the capitals spell the name" is satisfied by hundreds of
distinct texts and cannot be the selecting rule. A 44-character sentence constrains a spelling; a
1,549-character chapter does not.

## 5. Exhaustive closure of the orthographic selection family on the demo

The demo's paragraph initials are `I A F F I O W W I A`, five distinct letters. Its 15 sentence initials
give seven distinct letters. So the whole family "select by first-letter class, then edit the edges" is
finite and small, and it was enumerated in full rather than sampled:

| run | candidates | `3c6` matches |
|---|---|---|
| all 31 non-empty paragraph initial classes × first↓+last↑ × 4 serializations | 124 | 0 |
| all 127 non-empty sentence initial classes × first↓+last↑ × 4 serializations | 508 | 0 |
| all 31 paragraph classes × {paragraph-final, first-sentence-final} × 4 serializations | 248 | 0 |
| named sets: stage-one positions 2/3/4/6, ±4 offset, FFWW initials, not-ITASM, all ten, F/W+A/O × 3 modes × 4 serializations | 72 | 0 |
| minimal name markings for 13 names × 4 serializations | 52 | 0 |
| greedy R1 name marking, 9 names, both directions, 4 serializations | 72 | 0 |
| **total** | **1,076** | **0** |

**No first-letter class can be the demo's sign set.** That is now exhaustive, not sampled: every one of the
31 paragraph classes and every one of the 127 sentence classes has been tried in every serialization.

## 6. What the FFWW observation is worth

The demo does carry the same channel as the post: its initials contain `F F` at ¶3‑¶4 and `W W` at ¶7‑¶8,
four paragraphs, the same count as stage one's four. Two of those paragraphs' finals are **already capital
in the posted text**, because the author quotes his own worked examples in them: ¶3 ends `"capitalizatioN"`
and ¶7 ends `"himselF"`. That is the strongest structural echo of the post anywhere in the demo, and it is
the reason the FFWW reading (`18` candidates across modes and serializations, best hash `a992f7a1…`) was
worth running first. It is negative, and it is now closed with the rest of the family.

## 7. Where that leaves the demo, precisely

Three things are now excluded by enumeration rather than by argument:

1. the answer is not any text within two case edits of the base (2,868,016 texts);
2. the answer is not a paragraph or sentence edge-edit selected by any first-letter class (all 31 and all
   127, four serializations, two geometries);
3. the answer is not a minimal spelling of any of the thirteen names the corpus proposes.

What is left is narrower than anything stated before: **the demo's edits are neither edge-aligned nor
initial-selected**, which points at interior, content-selected changes, and the "signs" are semantic. Two
concrete next candidates, both reading tasks:

- The demo names its own worked examples twice (`capitalizatioN`, `himselF`) and says the first is *not*
  part of the solution. Those two quoted forms are the only places in the demo where the author demonstrates
  a mark. A rule that is consistent with rejecting `capitalizatioN` while accepting `himselF` is a real
  constraint that no sweep has used.
- Block 29's `vOIce` and the demo's `himselF` are both **word-internal**. If the demo's device is
  word-internal marking (block 29's, not stage one's), then the search space is word-interior positions,
  which is 1,197 positions but only ~60 words per paragraph, and `himselF` names the word it lives in.
