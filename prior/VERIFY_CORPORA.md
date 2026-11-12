# Block inputs verified against every available corpus

153 inputs (quiz1 blocks 1-77 SHA-256, quiz2 blocks 1-77 MD5) checked against both texts in the
workspace with the same engine: 12-character anchor index, each anchor extended exactly both ways
(true longest common substring), plus sentence presence and 6-word-gram overlap.

| corpus | size | embedded (LCS >= 200) | LCS >= 15 |
|---|---|---|---|
| chapter "Second" (`wp_paras.json`) | 273 paras / 45,149 chars | 2 | 17 |
| author guide / quizchain intro (`part_*_paras.json`) | 315 paras / 54,435 chars | 1 | 24 |

## Chapter (unchanged from the earlier pass)

- **q1 b29** LCS 444 (paras 11-29, question side, one flip: vOIce)
- **q2 b77** LCS 1200 (stage-one solution, chapter copy 231-235, flips F/F/W/W down + s/t/n/m up)
- q2 b66 65 (one sentence of para 29), q1 b23 41, q1 b32 35, q1 b9 29, q2 b27 27, q1 b17/b48 26,
  q1 b13 25, q2 b67 24, q1 b11 20, q2 b75 19, q1 b49 18 - all single-phrase reuse.
- 119 inputs share not even 12 consecutive characters.

## Author guide (new)

- **q1 b63** - byte-identical to a whole guide paragraph, coverage **1.00**:
  `The Rt Hon Alistair Darling MP TOMI If you don't get this, sorry, it is hard L4GWDy9Ld3ZydGCtFaHaaDEJe4YL5hAiSLsLgGzdEVQkNWgZUqu3`
  The same guide paragraph set explains the answer: "the correct way to address Alistair Darling in
  2009 ... 'The Rt hon Alistair Darling MP'". So this is the author publishing a solved block as a
  worked format example, not an unsolved question. Note the literal `TOMI` token inside a solution
  string and the long trailing code.
- q2 b67 coverage 0.69 (`Thomas TOMI Harold Thomas Finney II` plus name tokens).
- Term-level only: genesis address `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` (q1 b46), "artificial
  intelligence" (q1 b29/b32), "He who must not be named" (q1 b60), "Thank you for playing" (q1 b54),
  "Book of Swindles" (q1 b43), "private Internet cash" (q1 b1/b21), "mine with your mind" (q2 b37),
  "Japanese ancestry" (q2 b66/b77).
- **No block matches any guide paragraph case-only**, so the guide supplies no further certified
  flip examples beyond block 29 and stage one.

## Conclusion

Coverage of the 153 published inputs is now complete against both corpora. There are exactly three
embedded texts in the whole material: block 29 (question), stage one / block 77 (solution), and
block 63 (a solved example the author quotes). Nothing new is available to harvest for the flip
grammar from the block set.
