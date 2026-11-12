# Systematic verification: all 153 quizchain block inputs vs the 273-paragraph chapter

Inputs: 153 (quiz1 1-77 SHA-256, quiz2 1-77 MD5).
Method: whitespace-normalised, casefolded; 12-character anchors indexed over the chapter, each anchor
extended exactly in both directions to give the true longest common substring (LCS), plus sentence
presence and 6-word-gram overlap as independent checks.

| class | rule | count |
|---|---|---|
| EMBEDDED | LCS >= 200 chars | 2 |
| SENTENCE | LCS 60-199 | 1 |
| PHRASE | LCS 25-59 | 7 |
| TERM | LCS 15-24 | 7 |
| GENERIC | LCS 12-14 (ordinary English) | 17 |
| NONE | LCS < 12 chars | 119 |

**119 of 153 inputs share not even 12 consecutive characters with the chapter.**

## Fully embedded (question text reproduced in the chapter)

- **q1 b29** - LCS 444 chars at para 20: ` "Fine with me. Pleased to meet you, Aoi. Care to explain the meaning?" "Artificial Omnipotent Intelligence, obviously." Yes. That`
- **q2 b66** - LCS 65 chars at para 29: `a young woman of Japanese ancestry who is very smart and sincere.`
- **q2 b77** - LCS 1200 chars at para 230: `For those who don't know me, I'm Hal Finney. I got my start in crypto working on an early version of PGP, working closely with Phi`

## Distinctive phrases and terms borrowed from the chapter (LCS 15-59)

| input | LCS | para | fragment |
|---|---|---|---|
| q1 b23 | 41 | 47 | `climate emergency episode on this planet.` |
| q1 b32 | 35 | 17 | ` artificial intelligence explosion ` |
| q1 b9 | 29 | 27 | `You will torture me to death.` |
| q2 b27 | 27 | 125 | ` unspent transaction output` |
| q1 b17 | 26 | 107 | `AndrewYangForPresident2o2o` |
| q1 b48 | 26 | 107 | `AndrewYangForPresident2o2o` |
| q1 b13 | 25 | 3 | ` Second Coming I thought ` |
| q2 b67 | 24 | 183 | ` Harold Thomas Finney II` |
| q1 b11 | 20 | 43 | ` the solution with a` |
| q2 b75 | 19 | 71 | `Reverse Turing Test` |
| q1 b49 | 18 | 154 | ` good luck with th` |
| q1 b60 | 18 | 200 | `Tom Marvolo Riddle` |
| q1 b1 | 16 | 208 | `Satoshi is an an` |
| q1 b21 | 16 | 208 | `Satoshi is an an` |

## Ordinary-English coincidences (LCS 12-14, not borrowings)

| input | LCS | fragment |
|---|---|---|
| q1 b22 | 14 | ` intelligence ` |
| q1 b36 | 14 | ` Only one way ` |
| q2 b24 | 14 | ` proof of work` |
| q2 b42 | 14 | `e solution to ` |
| q2 b73 | 14 | `carbon budget ` |
| q1 b76 | 13 | ` Second Life ` |
| q2 b25 | 13 | `l number of b` |
| q2 b34 | 13 | ` to the right` |
| q2 b59 | 13 | ` to the right` |
| q1 b2 | 12 | `lar message ` |
| q1 b7 | 12 | ` without the` |
| q1 b53 | 12 | ` You like th` |
| q1 b65 | 12 | ` blockchain ` |
| q1 b77 | 12 | `m Hal Finney` |
| q2 b20 | 12 | `burn address` |
| q2 b56 | 12 | ` to have an ` |
| q2 b63 | 12 | ` Omnipotent ` |

## Appendix: every input

| input | input len | LCS | para | class |
|---|---|---|---|---|
| q1 b1 | 97 | 16 | 208 | TERM |
| q1 b2 | 97 | 12 | 107 | GENERIC |
| q1 b3 | 6 | 0 | - | NONE |
| q1 b4 | 13 | 0 | - | NONE |
| q1 b5 | 37 | 0 | - | NONE |
| q1 b6 | 13 | 0 | - | NONE |
| q1 b7 | 34 | 12 | 171 | GENERIC |
| q1 b8 | 9 | 0 | - | NONE |
| q1 b9 | 32 | 29 | 27 | PHRASE |
| q1 b10 | 30 | 0 | - | NONE |
| q1 b11 | 64 | 20 | 43 | TERM |
| q1 b12 | 14 | 0 | - | NONE |
| q1 b13 | 46 | 25 | 3 | PHRASE |
| q1 b14 | 20 | 0 | - | NONE |
| q1 b15 | 75 | 0 | - | NONE |
| q1 b16 | 11 | 0 | - | NONE |
| q1 b17 | 37 | 26 | 107 | PHRASE |
| q1 b18 | 14 | 0 | - | NONE |
| q1 b19 | 10 | 0 | - | NONE |
| q1 b20 | 11 | 0 | - | NONE |
| q1 b21 | 99 | 16 | 208 | TERM |
| q1 b22 | 36 | 14 | 17 | GENERIC |
| q1 b23 | 45 | 41 | 47 | PHRASE |
| q1 b24 | 6 | 0 | - | NONE |
| q1 b25 | 5 | 0 | - | NONE |
| q1 b26 | 5 | 0 | - | NONE |
| q1 b27 | 14 | 0 | - | NONE |
| q1 b28 | 27 | 0 | - | NONE |
| q1 b29 | 1360 | 444 | 20 | EMBEDDED |
| q1 b30 | 36 | 0 | - | NONE |
| q1 b31 | 19 | 0 | - | NONE |
| q1 b32 | 55 | 35 | 17 | PHRASE |
| q1 b33 | 30 | 0 | - | NONE |
| q1 b34 | 48 | 0 | - | NONE |
| q1 b35 | 17 | 0 | - | NONE |
| q1 b36 | 23 | 14 | 173 | GENERIC |
| q1 b37 | 15 | 0 | - | NONE |
| q1 b38 | 22 | 0 | - | NONE |
| q1 b39 | 18 | 0 | - | NONE |
| q1 b40 | 16 | 0 | - | NONE |
| q1 b41 | 24 | 0 | - | NONE |
| q1 b42 | 29 | 0 | - | NONE |
| q1 b43 | 30 | 0 | - | NONE |
| q1 b44 | 28 | 0 | - | NONE |
| q1 b45 | 45 | 0 | - | NONE |
| q1 b46 | 68 | 0 | - | NONE |
| q1 b47 | 24 | 0 | - | NONE |
| q1 b48 | 117 | 26 | 107 | PHRASE |
| q1 b49 | 50 | 18 | 154 | TERM |
| q1 b50 | 30 | 0 | - | NONE |
| q1 b51 | 34 | 0 | - | NONE |
| q1 b52 | 70 | 0 | - | NONE |
| q1 b53 | 56 | 12 | 19 | GENERIC |
| q1 b54 | 55 | 0 | - | NONE |
| q1 b55 | 51 | 0 | - | NONE |
| q1 b56 | 31 | 0 | - | NONE |
| q1 b57 | 29 | 0 | - | NONE |
| q1 b58 | 23 | 0 | - | NONE |
| q1 b59 | 70 | 0 | - | NONE |
| q1 b60 | 101 | 18 | 200 | TERM |
| q1 b61 | 24 | 0 | - | NONE |
| q1 b62 | 71 | 0 | - | NONE |
| q1 b63 | 129 | 0 | - | NONE |
| q1 b64 | 68 | 0 | - | NONE |
| q1 b65 | 86 | 12 | 136 | GENERIC |
| q1 b66 | 84 | 0 | - | NONE |
| q1 b67 | 103 | 0 | - | NONE |
| q1 b68 | 108 | 0 | - | NONE |
| q1 b69 | 70 | 0 | - | NONE |
| q1 b70 | 126 | 0 | - | NONE |
| q1 b71 | 72 | 0 | - | NONE |
| q1 b72 | 73 | 0 | - | NONE |
| q1 b73 | 78 | 0 | - | NONE |
| q1 b74 | 72 | 0 | - | NONE |
| q1 b75 | 77 | 0 | - | NONE |
| q1 b76 | 76 | 13 | 2 | GENERIC |
| q1 b77 | 112 | 12 | 231 | GENERIC |
| q2 b1 | 72 | 0 | - | NONE |
| q2 b2 | 52 | 0 | - | NONE |
| q2 b3 | 74 | 0 | - | NONE |
| q2 b4 | 36 | 0 | - | NONE |
| q2 b5 | 19 | 0 | - | NONE |
| q2 b6 | 37 | 0 | - | NONE |
| q2 b7 | 32 | 0 | - | NONE |
| q2 b8 | 110 | 0 | - | NONE |
| q2 b9 | 19 | 0 | - | NONE |
| q2 b10 | 34 | 0 | - | NONE |
| q2 b11 | 15 | 0 | - | NONE |
| q2 b12 | 29 | 0 | - | NONE |
| q2 b13 | 25 | 0 | - | NONE |
| q2 b14 | 14 | 0 | - | NONE |
| q2 b15 | 4 | 0 | - | NONE |
| q2 b16 | 24 | 0 | - | NONE |
| q2 b17 | 17 | 0 | - | NONE |
| q2 b18 | 19 | 0 | - | NONE |
| q2 b19 | 11 | 0 | - | NONE |
| q2 b20 | 12 | 12 | 105 | GENERIC |
| q2 b21 | 34 | 0 | - | NONE |
| q2 b22 | 19 | 0 | - | NONE |
| q2 b23 | 26 | 0 | - | NONE |
| q2 b24 | 23 | 14 | 153 | GENERIC |
| q2 b25 | 35 | 13 | 216 | GENERIC |
| q2 b26 | 52 | 0 | - | NONE |
| q2 b27 | 36 | 27 | 125 | PHRASE |
| q2 b28 | 43 | 0 | - | NONE |
| q2 b29 | 21 | 0 | - | NONE |
| q2 b30 | 29 | 0 | - | NONE |
| q2 b31 | 36 | 0 | - | NONE |
| q2 b32 | 24 | 0 | - | NONE |
| q2 b33 | 26 | 0 | - | NONE |
| q2 b34 | 43 | 13 | 189 | GENERIC |
| q2 b35 | 30 | 0 | - | NONE |
| q2 b36 | 26 | 0 | - | NONE |
| q2 b37 | 41 | 0 | - | NONE |
| q2 b38 | 38 | 0 | - | NONE |
| q2 b39 | 44 | 0 | - | NONE |
| q2 b40 | 14 | 0 | - | NONE |
| q2 b41 | 52 | 0 | - | NONE |
| q2 b42 | 58 | 14 | 134 | GENERIC |
| q2 b43 | 37 | 0 | - | NONE |
| q2 b44 | 13 | 0 | - | NONE |
| q2 b45 | 25 | 0 | - | NONE |
| q2 b46 | 52 | 0 | - | NONE |
| q2 b47 | 17 | 0 | - | NONE |
| q2 b48 | 33 | 0 | - | NONE |
| q2 b49 | 32 | 0 | - | NONE |
| q2 b51 | 17 | 0 | - | NONE |
| q2 b52 | 23 | 0 | - | NONE |
| q2 b53 | 58 | 0 | - | NONE |
| q2 b54 | 23 | 0 | - | NONE |
| q2 b55 | 29 | 0 | - | NONE |
| q2 b56 | 72 | 12 | 99 | GENERIC |
| q2 b57 | 51 | 0 | - | NONE |
| q2 b58 | 38 | 0 | - | NONE |
| q2 b59 | 40 | 13 | 189 | GENERIC |
| q2 b60 | 14 | 0 | - | NONE |
| q2 b61 | 13 | 0 | - | NONE |
| q2 b62 | 8 | 0 | - | NONE |
| q2 b63 | 19 | 12 | 22 | GENERIC |
| q2 b64 | 20 | 0 | - | NONE |
| q2 b65 | 18 | 0 | - | NONE |
| q2 b66 | 65 | 65 | 29 | SENTENCE |
| q2 b67 | 35 | 24 | 183 | TERM |
| q2 b68 | 25 | 0 | - | NONE |
| q2 b69 | 21 | 0 | - | NONE |
| q2 b70 | 15 | 0 | - | NONE |
| q2 b71 | 28 | 0 | - | NONE |
| q2 b72 | 23 | 0 | - | NONE |
| q2 b73 | 35 | 14 | 95 | GENERIC |
| q2 b74 | 25 | 0 | - | NONE |
| q2 b75 | 19 | 19 | 71 | TERM |
| q2 b76 | 11 | 0 | - | NONE |
| q2 b77 | 5347 | 1200 | 230 | EMBEDDED |

## What this establishes

1. The chapter reproduces exactly two block inputs as real text: q1 b29 (the scene at paras 11-29) and
   q2 b77 (the stage-one solution, whose chapter copy is 231-235). Everything else is short reuse.
2. The block set was authored *around* the chapter: proper nouns and technical terms (Hal Finney,
   Tom Marvolo Riddle, Reverse Turing Test, unspent transaction output, burn address, proof of work,
   carbon budget, the vanity key) are lifted verbatim, but never a whole question.
3. No further embedded questions exist to harvest. Any flip grammar has to come from the two pairs
   plus the author's comments, not from a wider palimpsest scan.
