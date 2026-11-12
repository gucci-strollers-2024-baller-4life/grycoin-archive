# All quizchain block inputs verified against the chapter

Inputs: 153 (quiz1 blocks 1-77, SHA-256; quiz2 blocks 1-77, MD5; one number repeats/absents).
Sources: `ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py`, `quiz2_blocks.py`.
Method: whitespace normalized, casefolded both sides, `difflib` equal runs >= 20 chars kept.
`cov_in` = matched / input length, `cov_chap` = matched / length of the chapter span it touches.

## Result: 12 of 153 touch the chapter, 141 share nothing >= 20 chars

| input | cov_in | cov_chap | matched | input len | chapter paras |
|---|---|---|---|---|---|
| q1 b29 | 0.95 | 0.84 | 1292 | 1360 | 11-29 |
| q1 b9 | 0.91 | 0.94 | 29 | 32 | 27 |
| q2 b66 | 1.00 | 0.34 | 65 | 65 | 29 |
| q1 b13 | 0.54 | 0.22 | 25 | 46 | 3-4 |
| q1 b32 | 0.64 | 0.22 | 35 | 55 | 17 |
| q1 b23 | 0.91 | 0.20 | 41 | 45 | 47 |
| q1 b11 | 0.31 | 0.12 | 20 | 64 | 43 |
| q2 b67 | 0.69 | 0.09 | 24 | 35 | 183 |
| q2 b27 | 0.75 | 0.06 | 27 | 36 | 125 |
| q1 b17 | 0.70 | 0.04 | 26 | 37 | 107 |
| q1 b48 | 0.22 | 0.04 | 26 | 117 | 107 |
| q2 b77 | 0.32 | - | 1717 | 5347 | 4, 231-235, 244, 271 |

Notes per input:

- **q1 b29** - the only block whose question is a chapter span. Same scene, re-edited (18 wording
  diffs), so `cov_chap` stops at 0.84.
- **q1 b9** `You will torture me to death.HwX` - one chapter sentence, para 27.
- **q2 b66** `A young woman of Japanese ancestry who is very smart and sincere.` - mid-sentence slice
  of para 29, exactly the clause the chapter adds relative to block 29's version.
- **q1 b13** `Second Second Life Second Coming ...` - the chapter's three headings, paras 1-3.
- **q1 b32** / **q2 b27** `artificial intelligence explosion` / `UTXO TOMI unspent transaction output` -
  phrase-level borrowings, paras 17 and 125.
- **q1 b23** `climate emergency episode on this planet.` - para 47.
- **q1 b17** and **q1 b48** - the para-107 vanity key fragment `AndrewYangForPresident2o2...`.
- **q2 b67** `Thomas TOMI Harold Thomas Finney II` - para 183.
- **q2 b77** - the stage-one solution itself, see below.

## Certified pair A: block 29 (quiz 1)

Chapter 11-29 is the block-29 question. Across 1302 matched characters there is **exactly one**
case-only difference: input `A pleasant female vOIce.` vs chapter `A pleasant female voice.`
Rule confirmed: uppercase the A-O-I vowels from the second position (O, I), in the second sentence
only. Nothing else in 1302 characters is flipped, so the rule is local.

## Certified pair B: block 77 (quiz 2) = stage one

`q2 b77` is byte-identical to `safudev_stage1.txt`, MD5 `9dd2efb9bc976c2095bd534d7b8d431c`, the
certified stage-one solution (m/44'/0'/0'/0/0, WIF on file). The chapter copy at 231-235 is
**fully contained** in it (coverage 1.00) and differs in **exactly 8 characters**, all case-only,
all at paragraph edges:

| para | chapter (question) | solution | transformation |
|---|---|---|---|
| 231 | `For those who don't know me` | `for those...` | first letter down (F->f) |
| 232 | `Fast forward... other activities.` | `fast forward... other activitieS.` | first down (F->f), last up (s->S) |
| 233 | `When Satoshi... paradox of it.` | `when Satoshi... paradox of iT.` | first down (F->f / W->w), last up (t->T) |
| 234 | `When Satoshi... knee jerk reaction.` | `when Satoshi... knee jerk reactioN.` | first down (W->w), last up (n->N) |
| 235 | `When Satoshi... him fixing them.` | `when Satoshi... him fixing theM.` | first down (W->w), last up (m->M) |

Signature: firsts F,F,W,W lowered, lasts S,T,N,M raised, one pair per selected paragraph. So the
stage-one rule is **paragraph-edge flipping only**: lower the first letter, raise the last.

## Consequences

1. The chapter is not a palimpsest of block questions. Only one block (29) is embedded, plus one
   solved text (stage one) reproduced in question form at 231-235. A 90-block scan for embedded
   questions is therefore not a productive line.
2. Both certified pairs agree on the same shape: flips are local, at word or paragraph edges,
   never arbitrary word-internal picks. The demo hypothesis of 5+ word-internal flips contradicts
   every certified example we now have.
3. The para-222 hint paragraph combined with pair B gives the concrete candidate rule for the
   chapter: select paragraphs, lower their first letter and raise their last, per paragraph edge.
