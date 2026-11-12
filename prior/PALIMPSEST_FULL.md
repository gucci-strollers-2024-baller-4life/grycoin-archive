# The palimpsest index, built across all 33 parts and 91 posts

Corpus: every Wattpad part of the story (33 fetched, 1,297 paragraphs) plus the 91 r/Grycoin posts, split
into 2,988 sentences of 45+ characters. Each of the 273 chapter paragraphs matched against all of them at
25-character anchors, then extended both ways.

## Result: 24 paragraphs have a verbatim source of 70+ characters

| source | paragraphs | where |
|---|---|---|
| THOMAS and SATOSHI | 17 | 183-207 |
| Second Life | 3 | 14, 17, 25 |
| r/Grycoin block 77 Stage One post | 3 | 222, 234, 271 |
| r/Grycoin block 57 post | 1 | 160 |

Everything else is original to this part, including the whole Grycoin paper (88-162).

## Two facts that came out of building it

1. **The reprint is exact.** Word-by-word diff of chapter 183-207 against the source part: zero case-only
   differences. Nothing is hidden in the copying.
2. **No block question is reused.** 66 posts carry an explicit `Question:` line; none matches any chapter
   paragraph at 40 characters. The reuse is prose about the method, not questions. So the palimpsest reading
   is correct about *what* was copied but the copies are explanatory, not puzzles.

## Negatives this pass

- `satommi` I/M readings (M->m, I->i, MI->mi, both, all-case) x 2 joins x 6 indices: 168, none
- I/M nonce readings (all capital I, all capital M, both, IBM) x 4 joins x 6 indices: 144, none
- combined embedded-rule application: vOIce at 12, Finney flips at 231-235, quote flips at 222 and 271,
  all 16 subsets x 2 joins x 3 indices: 96, none
