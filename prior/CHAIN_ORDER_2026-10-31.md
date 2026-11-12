# The chain-order family, closed; and the provenance/metadata planes, audited

**Date:** 2026-10-31
**Script:** `sweeps/chain_order.py`
**Ledger:** `chain_order_survivors.json`
**Total this pass:** 14,516,736 candidates, 3,628 `3c6` survivors, 3,628 x 9 indices derived, **0 escrow hits**.

## 1. The family, and why it was the one open shape

`BLOCK29_ANCHOR_CENSUS_2026-10-31.md` §6 left exactly one testable lead: the demo's four marked paragraphs
carry anchor -> mark pairs

| ¶ | anchor (lowered) | mark (raised) |
|---|---|---|
| 4 | F | S (`signs`) |
| 5 | I | F (`himself`) |
| 6 | O | I (`"i"`) |
| 8 | W | S (`signs` in the trigger sentence, not the paragraph-final `unchanged`) |

and two raised letters are the *next* paragraph's lowered anchor (¶5 raises `F`, which is ¶4's anchor;
¶6 raises `I`, which is ¶5's anchor). Read as a handoff the order is 6 -> 5 -> 4, terminating on the same
`S` that ¶8 also terminates on.

**Case edits commute.** Applying the four marks in the order 6,5,4,8 produces exactly the same bytes as
applying them in text order. So "process the marks in chain order" can only change the answer if the
*paragraphs themselves are re-ordered in the text that gets hashed*. That is the family, and no sweep in
this repo had ever permuted paragraphs before serialising (every previous family selects a set and
serialises it in text order).

## 2. Implementation certification, before any result was read

The geometry is: lower the paragraph's first letter; raise the last letter of the paragraph's **first
sentence**. On the single-sentence paragraphs ¶4 and ¶6 that is the paragraph-final; on the two-sentence
¶5 and ¶8 it is not. This is geometry (ii) of `DISCRIMINATOR_2026-10-31.md` §1, the one the author's own
decoy `capitalizatioN` does not flag, and it is asserted in code against the census letters (`S,F,I,S`).

Checks the script runs and passes:

| check | result |
|---|---|
| bare serialisation reproduces the certified question hash | `7759227d7406` |
| eight-change text, `\n\n` | `13082a45` (matches `GRAMMAR_AUTOPSY` §6) |
| eight-change text, `\r\n\r\n` | `0f69c8ea` (matches) |
| edit count | exactly 8, at `F->f`/`s->S` ¶4, `I->i`/`f->F` ¶5, `O->o`/`i->I` ¶6, `W->w`/`s->S` ¶8 |

**A false start worth recording.** The first build applied anchor+mark to all ten paragraphs instead of the
four recognised ones: 18 edits, `\n\n` digest `cc907621`. It reproduced the certified *base* and therefore
looked healthy, and it produced a plausible-looking negative on a family that was not the intended one. The
digest cross-check against `13082a45`/`0f69c8ea` is what caught it. Any future script that marks paragraphs
should assert the two published eight-change digests before it runs, for the same reason the base digest is
asserted.

## 3. The runs

**Family A — every ordering of the ten paragraphs**, marks applied to their own paragraphs, four
serialisations (LF / CRLF, with and without trailing separator), 10! x 4 = 14,515,200 texts. This strictly
contains the chain orders 6-5-4-8 and 6-5-4.

* 3,628 candidates passed the `3c6` screen.
* All 3,628 derived at `m/44'/0'/0'/0/i`, i in {0, 1, 2, 5, 6, 7, 44, 76, 77}: **0 matches** against
  `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi`.

Expected survivors under a uniform hash: 14,515,200 / 4096 = 3,543, sd 60. Observed 3,628 is +1.4 sd, i.e.
chance. The chain orders themselves did not survive the prefix, and neither did any of their neighbours.

**Family B — the four marked paragraphs permuted among their own slots** (24) x every subset of the four
marks (16) x 4 serialisations = 1,536 texts. **0 survivors**, so nothing was owed a derivation. This covers
"the marks are a chain, so perhaps only a chain-closed subset of them is applied".

## 4. What the closure means

The chain is a property of the **marking process**, not of the **answer text**. Re-ordering paragraphs is
the only way a process order can reach the hash, and it is now exhausted at both the full-permutation and
the in-place level. The residue the census identified is real as an observation (the raised letters do hand
off to the next lowered anchor) but it is not an encoding channel. Nothing about ¶6 -> ¶5 -> ¶4 should be
carried forward as a live lead.

## 5. The provenance and metadata planes, audited (same pass)

Recorded together because both were proposed as alternatives to further search and both are now answerable
rather than open.

**(a) On-chain metadata: empty.** All three escrows' funding transactions are vanilla single-input P2PKH
with `nLockTime = 0` and no `OP_RETURN`:

| address | funding tx | locktime | size | outputs | OP_RETURN |
|---|---|---|---|---|---|
| LIVE `14zMk…` | `a1916e7e…` | 0 | 251 | 77,700,000 + 463,539,695 change | none |
| OLD `1EFoj…` | see `ESCROW_KEY_AUDIT` | 0 | - | - | none |
| stage one `19Tby…` | `ccf5ad64…` | 0 | 226 | 7,700,000 + 3,926,125 change | none |
| demo `1tzieU…` | `f11eca99…` | 0 | 251 | 700,000 + 76,983,868 change | none |

The two funding wallets were scanned too (`3E7gTGXp…` and `1FtU2GwV…`, two transactions each): no
`OP_RETURN`, no non-standard script types anywhere in their history. There is no metadata channel on chain.
The solved-vs-unsolved comparison shows no structural difference at all, so "how she deployed it" carries
no information. `ESCROW_KEY_AUDIT` already closed the nonce-reuse route: the live escrow key has never
signed, and the one signature that exists belongs to the OLD key.

**(b) Archive snapshots: they cannot answer the open question.** The CDX index returns nothing for
`wattpad.com/720888559*` or `wattpad.com/story/184148284*` in any snapshot year (re-queried this pass;
`cdx_results.txt` from the earlier pass agrees). More decisive than the absence: **the join is not a
property of the page.** Wattpad renders paragraphs with `<p>` markup regardless, and the author's own
instruction is about what she did in a text editor ("hit enter twice... 13 10 13 10"). No snapshot of the
render can tell us what bytes were in her file, so even a perfect 2019 capture would not move the one
variable this line of enquiry is aimed at. `wp_paras.json` already certifies the paragraph *text* byte-exact
through the `data-p-id` hashes (272 direct + 1 by dedup rule).

## 6. Where this leaves the plan

Two of the four proposed planes are closed with evidence (on-chain metadata, archive provenance). The two
that carry information are the repository's own history and the search space itself, and the repository is
being worked in parallel: `origin/main` moved twice during this pass

- `e4a3a3c` — POS/punctuation pools and a C engine; the POS-filtered five-change space (**7,084,700**
  candidates, L2s) exhausted, 0 hits;
- `a971108` — 44-char string as transport operator, cross-window transport closed;
- `85f0c32` — 78 balanced transport constructions, 0 hits; word scale excluded by conservation.

So the demo's five-change space is closed **under the POS constraint** (L2s) and open only at L1
(135,360,884, non-initial up-marks) and L0 (283,701,365, unconstrained). At the measured 0.49 M/s those are
4.6 and 9.7 minutes on one core. The decision to run them is a decision about what a negative would prove,
not about compute: L1 would say the demo's up-mark must sit on a verb, adjective, adverb or function word,
which nothing certified ever does; L0 would leave only "more than five changes" or "not a case edit of this
base".
