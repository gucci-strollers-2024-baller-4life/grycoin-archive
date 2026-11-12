# Can the escrow private key be reverse-derived? (2026-10-31)

Live escrow: `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` (777 mbtc)
Earlier escrow: `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC` (prize withdrawn, re-sent)

## 1. On-chain audit

| address | txs | state | signatures by its own key |
|---|---|---|---|
| LIVE 14zMk… | 1 | funded 2019-07-31 from `3E7gTGXp4EcKhcLo69Utw3vae4Axj5ZPh7` in block 587833, **never spent** | none |
| OLD 1EFoj… | 2 | funded 2019-07-22 from `1FtU2GwV9ww3AxisPQYz1AMGu5JnoZ1iUV`, spent 2019-07-31 to `36nwcMJwoy99xyENeRcCCQmA3FZibji3Un` | one, pubkey `0228e8f9d2c8addd9e84…` |

The prize is still at the LIVE address. Its key has **never produced a signature**, so its public key
is not even exposed on chain.

## 2. The one shortcut that exists, and why it does not apply

The only way to recover an ECDSA private key without solving the preimage is nonce reuse: two
signatures made with the same `k`, which share an `r` value and yield the key algebraically. Checked:

- signatures parsed from raw transactions: 2 (one from the funding wallet `036444c8…`, one from the
  OLD escrow key `0228e8f9…`);
- distinct `r` values: 2; reused: **none**.

And even if a reuse existed somewhere in her wallet, it could only expose the key that signed, which
is the OLD key. The current escrow key has signed nothing and cannot leak this way unless she spends,
which would end the puzzle.

Conclusion: **the escrow private key is not reverse-derivable.** It is a pure preimage problem:
md5(flipped chapter) -> BIP39 entropy -> m/44'/0'/0'/0/0. No chain data, no weak-key shortcut, no
shortcut through the OLD address.

## 3. Semantic reread of the hints, with the one real contradiction resolved

Hint 1: "I added extra line breaks between paragraphs. This information is needed to solve the block."
Hint 7: "hashing with a slightly different solution… It has multiple paragraphs and two line breaks
between each of them", clarified on 08-01 as "I mean the second one. Hit enter twice. This displays
in Ascii as 13 10 13 10".

The 07-28 answer in the same thread ("the solution you need to hash with has only one line break
between paragraphs… one 13 and one 10") predates the re-escrow. So the two statements are not in
conflict: the *first* solution used one break, and the *currently escrowed* solution uses two, i.e.
`13 10 13 10` between paragraphs. That is the CRLF paragraph separator, and it is exactly the
certified base `bd07e6ee…` (CRLF between paragraphs, LF inside the ten internal breaks).

Hint 4: "the 7th private key in the list for this wallet contains the number 7 three times… But the
first one also has some amazing properties." The prize address itself carries the answer to that
curiosity: `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` contains **44** at the end of its run, which is the
BIP44 envelope of the derivation path. So "the first one" is the first key of the list, index 0 of the
external chain, and the hint is a self-referential confirmation of the path, not a new clue.

Hint 6: "Once someone figures out the format for the first stage, they will also have a big hint for
the format of this second stage." Stage one's format is: take the paragraphs whose first letters fall
outside the signature, lower their first letter, raise their last. Second stage = same operation on
the chapter. That is the operation the corpus has swept.

Hint 2: an internal odd capital is "just a mistake, not a hint for the solution" — closes the
case-mark reading, per `FINDINGS_MARKS_2026-10-31.md`.

## 4. What this leaves

Every remaining route is the preimage, and the search space is the flip set. The clue set constrains
it to: her narrative paragraphs only (the signs live in her voice, 39% of them violate ITASM), the
four signature windows (5-8, 93-96, 168-171, 231-235), paragraphs split by 13 10 13 10, first letter
down and last letter up. All of that is swept and negative.
