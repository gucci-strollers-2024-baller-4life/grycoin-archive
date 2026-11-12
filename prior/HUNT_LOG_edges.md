# Edge-flip hunt, 2026-10-29 (demo exhausted, new chapter signature)

## Demo (block cleczc): literature-following reading tested exhaustively

Base certified first: `demo_base.txt`, paragraphs stripped, `\n\n` join, no trailing newline
-> MD5 `7759227d7406` = author-confirmed question hash. All tests derive BIP39/BIP44 addresses
(`demo_oracle.py`, selftest passes) and compare against the demo escrow `1tzieU...`.

| candidate family | count | result |
|---|---|---|
| demo text unchanged | 1 | addr 16PM6yVZ... no |
| every subset of the 8 `I` and 2 `himself` occurrences flipped (I->i, himself->himselF) | 1,023 | none |
| every paragraph-edge combination, per paragraph {none, first-down, last-up, both} | 1,048,576 | 256 hit the `3c6` prefix, none derive the escrow |
| author's stated pair (I->i + himselF) across 70 derivation paths (idx 0-59, m/0'/0'/i, m/44'/0'/0', .../1/0) | 504 | none |

So "write back the two example flips" is dead, and so is every paragraph-edge-only reading of
the demo question. The demo must contain word-internal flips beyond the two named.

## New chapter structure: the STNM signature repeats

The stage-one certified signature is: a run of 4 paragraphs whose first letters are F,F,W,W and
whose last letters are s,t,n,m. It occurs in the chapter exactly three times:

| window | firsts | lasts | delta to next |
|---|---|---|---|
| paras 5-8 | F,F,W,W | s,t,n,m | 88 = 2x44 |
| paras 93-96 | F,F,W,W | s,t,n,m | 75 |
| paras 168-171 | F,F,W,W | s,t,n,m | - |

`L` (last letters) = `degnstnm...` so the signature starts at paragraph 5; no other 4-window
matches. The middle window opens with **the only 44-character paragraph in the chapter**:

    93 (44 chars): For starters, define the project's purposes.

That is the "44" marker: a 44-char paragraph at index 93 = 5 + 88 = 5 + 2x44.

## Chapter sweeps against the live prize address

Each candidate text is hashed and derived, then compared to `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`.

| family | count | result |
|---|---|---|
| selections {all, ITASM, not-ITASM, last-STNM, not-last-STNM, finney4, finney5, paras containing "I", stride-44 offsets 0-43} x 5 edge modes x 6 joins | 1,560 | none |
| the three signature windows flipped (fd/lu/both) x 4 joins | 12 | none |
| signature-table selections {pairs exact, pairs not, firsts-FW, lasts-STNM, both, either, windows, not-windows, window boundaries} x 5 edge modes x 4 joins | 180 | none |

Plain chapter reference: `\n\n` join -> MD5 48d31820 -> 14isnRimk9qAzpm85qwiFgLjzxL1387TXL.
