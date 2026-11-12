# The block was never solved, and the chapter carries six non-breaking spaces

**Date:** 2026-10-31

## 1. There was no solver. The escrow is unspent.

On-chain, `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` (blockstream and mempool.space agree):

    funded_txo_count 1     funded 77,700,000 sats
    spent_txo_count  0     spent  0
    tx_count         1

The single transaction is the funding tx
`a1916e7ed9eac3fcc56a55056328cb09d06925e2694f2e6720de12b228514d1f`, paid out of
`3E7gTGXp4EcKhcLo69Utw3vae4Axj5ZPh7` (P2SH). There is no spending transaction, therefore **no redeeming
input, no public key revealed by a spend, and no OP_RETURN**. 0.777 BTC has sat there since July 2019.

The thread says the same thing in the author's own words. u/JDScreesh congratulated the solver of the
block, and u/AoiNakamoto replied:

> There was no solver, I took the funds back for a moment to send them to a new address, see update above.

So the "Block 77 solved" framing does not hold for this block's prize. Whatever the August 2019 tweet
meant, stage two of block 77 was never claimed: the address it points at has never been touched.

That removes the strongest constraint we had been reasoning under. There is no known solution, no
winner's method, and no solved instance to reverse-engineer; the block has been open for seven years.

## 2. What the 34 comments actually contain

Nothing about punctuation, curly quotes or encoding. Reading them in order:

- `silver_anth`, a mental-health jab; `[deleted]`, and Aoi's reply "When Aoi announced Grycoin, she got a
  sceptical reaction at best."
- `puzzleponky`, farewell; Aoi: "Already started up again … Still no one paying attention to the Satoshi
  Code."
- `bulleteyedk`: no idea where to start. Aoi: "The last block is supposed to be difficult … I estimate the
  probability of someone solving it at a lower value than that of humanity passing the reverse Turing
  test."
- `martypyouknowme` asks for more hash digits for 76. Aoi: "Not going to do more hash digits for 76, would
  make it too easy to script the block. But there will be hints for that one, not always declared as
  such…"; then "I will give a hint for this block on Saturday, 1 pm Japanese time."
- The one technical contribution in the entire thread, from `bulleteyedk`: **`data-p-id` on Wattpad `<p>`
  elements is the MD5 of the paragraph text**, verified against a browser save from 2019-04-15, "including
  one paragraph where the hash only matches if a trailing space is retained", plus the 2019 CSS rule
  `pre { white-space: pre-wrap; }`.
- `CathedraTessera`, then six more accounts, all asking for that April 2019 save; nobody has the July 2019
  copy of part 720888559.
- `Kaplion`: "272 of 273 paragraphs in the current chapter match", and all 33 chapters tested against the
  escrow with no match.

## 3. Straight versus typographic quotes: the chapter has none

The base text is ASCII apart from **six `U+00A0` non-breaking spaces**, and each one sits exactly where a
double space belongs:

| ¶ | site |
|---|---|
| 90 | "built on Bitcoin as a`\xa0` mechanism" |
| 125 | "With the exception of`\xa0` transactions" |
| 126 | "creating 6.25 new`\xa0` bitcoins" |
| 126 | "on the Bitcoin network`\xa0` because" |
| 196 | "in the anagram.`\xa0` What might" |
| 257 | "heard about RPOW`\xa0` in 2008" |

242 straight double quotes and 46 straight apostrophes, no `\u201c`, `\u201d`, `\u2019` or em dash. So the
smart-quote lane is closed by inspection — but the NBSP is the same hazard in a different character, and it
is the only invisible-character difference in the file.

Derivations run, all at index 0, all negative:

| variant | chars | md5 | index 0 |
|---|---|---|---|
| NBSP → space | 45,450 | `0d2c86ff43…` | `1AF2t2NN4DV7redAngZxyJ5ZyWj4xyYcHT` |
| NBSP deleted | 45,444 | `202b684590…` | `1LHhgNVZ8AHZNrfMBxGq3HXjHYqLTYhD4L` |
| NBSP → two spaces | 45,456 | `75f1eab0e1…` | `186n3g6JLDrXFjwfYGqK8N3PATADZVPCiC` |
| each of the six sites reverted alone to two spaces | 45,450 | six md5s | six addresses, none the escrow |

## 4. The reprint hypothesis, run

| variant | chars | index 0 |
|---|---|---|
| ¶231–235 replaced by the stage-one plaintext, Hal ¶2–6 raw | 45,051 | `15DfALGJ3y6darG5hRDZbkszaQJDEyqGez` |
| same, endpoints inverted to `f…S` | 45,051 | `1PSV7cqU9pAA4tsQoE2qPzeeV3cTjqVWy9` |
| "fascinating" reverted to Hal's "facinating" | 45,449 | `133V3W415JEh9oN8JA1xRtumqC3ExtF5Vf` |
| "motor" reverted to "moter" | 45,450 | unchanged — the chapter contains no "motor" |

All negative. The reprint is not a byte-level copy of the stage-one document in either direction.
