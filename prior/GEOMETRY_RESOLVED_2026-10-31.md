# The up-mark geometry: the binary is false

**Date:** 2026-10-31

## Both facts are as stated

Stage one, four marked paragraphs, three candidate positions each:

| ¶ | marked | paragraph-final word | first-sentence final |
|---|---|---|---|
| 2 | `s`->`S` | activities | `y` ("...I'm Hal Finney.") |
| 3 | `t`->`T` | it | `n` ("...the announcement of Bitcoin.") |
| 4 | `n`->`N` | reaction | `t` ("...a skeptical reception at best.") |
| 6 | `m`->`M` | them | `y` ("...I grabbed it right away.") |

Demo ¶5: marked `f`->`F` of "himself", which closes sentence 1; the paragraph closes on the `l` of
"detail". So the paragraph-final and first-sentence-final hypotheses are genuinely different here, and
in stage one they are different at every paragraph too.

## But "paragraph-final" cannot be tested against "sentence-final" on stage-one data

A paragraph's final letter is, by definition, the final letter of its last sentence. So the hypothesis
"the up-mark is the last letter of a *sentence-final word*" **implies** "the up-mark is the
paragraph-final letter" whenever the sign word sits in the paragraph's last sentence — which it does in
all four stage-one paragraphs. Stage one therefore cannot distinguish the two rules; it is consistent
with both, and its four marks are the paragraph-final letter *because* they are sentence-final letters
of the final sentence.

Only the demo discriminates, and the demo's ¶5 mark lands on "himself". So:

- **H1 (paragraph-final)** is *refuted* by the demo: the mark is not on the `l` of "detail".
- **H2 (sentence-final word)** is consistent with stage one (4/4) and with the demo (1/1), and with
  block 29's "voice" (which closes "A pleasant female voice."). That is 5/5 on every certified tail mark
  in the corpus.

H2 wins on consistency alone. Choosing H1 requires declaring the demo wrong; choosing H2 requires
declaring nothing wrong. "Production code beats tutorial prose" is a reasonable prior, but here the
production code does not actually disagree — it is silent on the distinction, and the tutorial is the
only witness that speaks to it.

## What the resolution predicts, and what it cost to test

The resolved rule: **down-mark = the paragraph's first letter; up-mark = the last letter of the
sentence-final word that carries the sign.** In stage one the sign is in the paragraph's last sentence;
in the demo it is in the first. Nothing is inconsistent; only the sign's location moves.

Tested the consequence on the chapter — all 4,096 subsets of the twelve "the signs" paragraphs, head
down plus the last letter of the sign-bearing sentence up, both joins:

| texts | escrow hits | time |
|---|---|---|
| 8,192 | **0** | 44 s |

Named four-unit candidates under the same geometry also nil, e.g. {222,236,244,246} -> `bbc3c7d4…` LF /
`156794a6…` CRLF, {220,222,244,273} -> `a7fb8a4b…` / `73299a9b…`.

## So the geometry is not the blocker

Both geometries are now closed on the demo (18,432 and 8,192 texts respectively, escrow-checked), and
the resolved geometry is closed on the chapter's sign pool. The live unknown is unchanged and is not
geometric: **which sentences carry signs, and how many.** The receipt says four units; nothing yet says
which four sentences in a 273-paragraph chapter those are.
