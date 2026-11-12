# The August 3 sweep was the author consolidating his own escrows, not a solve

**Date:** 2026-10-31

## The trace

The demo escrow `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` paid out on 2019-08-03 at 11:22:10 UTC to
`129jw1GUGwiJbf4rL7qEANPbxvSRC5zfHN`. That destination is a **consolidation wallet**:

    funded_txo_count 30   funded 42,153,481 sats
    spent_txo_count  30   spent  42,153,481 sats
    tx_count         31

Thirty separate escrow-sized payouts (~0.0060-0.0077 BTC each) arrived there, and on 2019-08-15 all thirty
were spent in a single transaction into `1KRHsErvfPDu48sfz2zK…`.

Two of its inputs are decisive:

| time (unix) | from | value |
|---|---|---|
| 1564841397 | `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` | 7,700,000 sats |
| 1564840930 | `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` (the demo) | 700,000 sats |

`19TbyN5…` is the **certified stage-one escrow** — the address the `9dd2efb9` preimage derives. It paid into
the same wallet **467 seconds before** the demo did.

## What that means

A single destination receiving payouts from the stage-one escrow and the demo escrow within eight minutes
can only be one entity controlling both: **the author**, sweeping his own unclaimed prize pots as he wound
the experiment down on the day of the "shutting down" announcement.

So:

1. **No Grycoin escrow in this family was ever claimed by anyone.** Thirty of them were swept at once into
   one wallet, including the stage-one pot, which is the one pot we know had a certified public solution.
2. **The demo's 2019-08-03 sweep is not evidence that the demo mechanism was operational or solved.** It is
   the author cleaning up.
3. **The inference "our endpoint model is a modelling error because the demo was solved" is withdrawn.**
   There is no solved demo to model. The demo joins the chapter as an unresolved instance, and the
   contradiction between the published `3c6` and the published instruction stands unexplained.
4. The August 2019 tweet is best read as an exit, not a solve announcement.

## The byte audit the failure was being blamed on

`demo_base.txt` is clean, so no serialization artifact is available to explain the `3c6` gap:

| check | result |
|---|---|
| bytes | 1,549 |
| BOM | none |
| carriage returns | none |
| non-ASCII | none |
| double spaces | none |
| leading / trailing whitespace | none (`I thought I ` … `only method.`) |
| paragraph separators | `\n\n`, 10 paragraphs |

It is also exactly `selftext[778:2327]` of the Reddit source, i.e. the first `I` to the period after the last
"method", byte for byte.

## How the flip was defined

Head = character 0 of the paragraph. Tail = the last character whose `isalpha()` is true, so the trailing
period and any quote are skipped. Case swapped by ±32, join `\n\n`, no trailing newline.

For ¶5 both conventions select exactly the two characters the author names in ¶7 — the `I` at offset 0 and
the `f` of "himself" — so **no indexing convention can change the result**. The author did not describe an
algorithm there, he described the output string. That string hashes to `731aee6b…`.

Alternative slices were also screened: to the period after the first "method", to the end of the metadata
block (2,108), and to the end of the post (3,004), each under LF and CRLF, raw and with the ¶5 flip. None
begins `3c6`; the closest is the 2,108-char slice with the ¶5 flip at `3cbad5e5…`.
