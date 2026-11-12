# The 16-paragraph boundary table of `hal_original.txt`, screened for `Xx` in six scopes

**Date:** 2026-10-31
**Source:** `hal_original.txt`, 5,363 bytes, 16 paragraphs, **0 non-ASCII bytes throughout**, so raw-byte
and case-folded identities agree everywhere and folding introduces no edge case.

## 1. The table

| ¶ | Initial Char | Initial Word | Terminal Word | Terminal Char | Self-Matching (Xx)? |
|---|---|---|---|---|---|
| 1 | I | I | me | e | no |
| 2 | F | For | activities | s | no |
| 3 | F | Fast | it | t | no |
| 4 | W | When | reaction | n | no |
| 5 | I | I | facinating | g | no |
| 6 | W | When | them | m | no |
| 7 | T | Today | signs | s | no |
| 8 | A | After | things | s | no |
| 9 | T | The | heirs | s | no |
| 10 | S | Speaking | wrong | g | no |
| 11 | M | My | it | t | no |
| 12 | A | ALS | progression | n | no |
| 13 | T | Today | eyes | s | no |
| 14 | I | It | documentation | n | no |
| 15 | A | And | go | o | no |
| 16 | T | That's | slightly | y | no |

Heads: `I F F W I W T A T S M A T I A T`. Tails: `e s t n g m s s s g t n s n o y`.

**Self-matching paragraphs: none.** Not one of the 16 opens and closes on the same letter in either case
direction. The four stage-one marks and the interleaved paragraph are `F…s`, `F…t`, `W…n`, `I…g`, `W…m`
— no internal pairing among them either.

Expected count under chance is 0.88, using the post's own head-letter frequencies (s appears 5 times as a
tail and S heads one paragraph, t twice against four T heads, m once against one M head). Observing 0 is
unremarkable: P(0) ≈ 0.42.

## 2. The other five scopes

**Global endpoints.** The post opens on `I` (*"I thought I'd write…"*) and closes on `y` (*"…comfortable
with my legacy."*); the final character of the file is `]`, from the tag `[edited slightly]`. `I…y` is not
a pair. Contrast the genesis address, where the `A` at position 2 and the `a` at position 36 are the only
occurrences of that letter in either case in the entire string — that uniqueness is what makes the pair
announce itself. Hal's post has no such device at its ends.

**Adjacent, head(¶i) → tail(¶i+1).** All fifteen checked: `Is`, `Ft`, `Fn`, `Wg`, `Im`, `Ws`, `Ts`, `As`,
`Tg`, `St`, `Mn`, `As`, `Tn`, `Io`, `Ay`. **Zero matches**, against 0.88 expected.

**Adjacent, tail(¶i) → head(¶i+1).** One match in fifteen: **¶9 tail `s` → ¶10 head `S`**. Expected 0.75,
so one is exactly chance.

**Bookend mirror, head(¶i) → tail(¶17−i).** Zero matches in eight. Expected 0.13.

**Bookend mirror, tail(¶i) → head(¶17−i).** Two matches in eight: **¶6 tail `m` → ¶11 head `M`** and
**¶7 tail `s` → ¶10 head `S`**. Expected 0.50, so this is a 4× excess with P(X≥2) ≈ 0.09 — the only place
in any scope where a mirror signal appears at all, and it survives nothing once the six scopes are
counted (0.09 × 6 ≈ 0.54). Worth recording because ¶6 is one of the four anomalies, so three of the four
anomalous tails do point at heads: `s`→¶10, `t`→¶7/9/13/16, `m`→¶11, with `n` pointing nowhere.

## 3. The answer to the request

The table shows **no `Xx` anywhere**: not within a paragraph, not at the document's ends, not between
adjacent paragraphs, and not across the bookend mirror. The one structural asymmetry that survives is the
head/tail one, and it runs the wrong way for the `Aa` model: **no paragraph in the post ends on `f` or
`w`, so the four anomalous heads are dead ends**, while three of the four anomalous tails do resolve to
paragraph heads. A symmetric edge-pairing marker is not present.

So the `Aa` analogy does not transfer as a matching pair. What it transfers is **polarity**: the genesis
pair is capital head / lowercase tail, the four anomalies are exactly that shape, and the certified
operation inverts both ends and touches nothing else. Verified by diff against `safudev_stage1.txt`: eight
single-character replacements at offsets 85, 480, 484, 713, 717, 924, 1299 and 1691, plus one deleted
newline at 5362.

| ¶ | base | certified |
|---|---|---|
| 2 | `F…s` | `f…S` |
| 3 | `F…t` | `f…T` |
| 4 | `W…n` | `w…N` |
| 6 | `W…m` | `w…M` |

That is the visible, non-enumerable cue: four paragraphs whose ends carry case in the wrong direction for
their neighbours, and flipping them is what makes `STNM` legible.

## 4. Two texts, not one

`hal_original.txt` carries two orthographic slips that the chapter's reprint does not: `facinating` at
¶5's tail and `moter` at ¶12, against `fascinating` and `motor` in the chapter's ¶231–235, which keeps the
same edge geometry. `hal_original.txt` is the certified stage-one base (its flipped form hashes to
`9dd2efb9` → `19TbyN5`); the reprint is a different byte stream. Do not substitute one for the other in a
sweep.

## 5. Index

`corpus.json` ¶714–715 ("the second private key … because this was block 2") is a 0-based `block − 1`
rule, so block 77 is **index 76**; index 77 is the weaker reading. This constrains nothing further in
practice: both indices are already in this repo's standard set, and the raw chapter and raw post were
swept at every index 0–79 with 0 hits (`PATHWAY_B_AUDIT_2026-10-31.md` §4).

No derivations were run this pass: the boundary table is a text measurement, and there is no candidate
plaintext to put on the two paths.

## 6. State

| scope | expected | observed |
|---|---|---|
| self-matching `Xx` within a paragraph | 0.88 | **0** |
| global endpoints | — | **no** (`I…y`) |
| adjacent head→tail | 0.88 | **0** |
| adjacent tail→head | 0.75 | 1 (¶9→¶10) |
| mirror head→tail | 0.13 | **0** |
| mirror tail→head | 0.50 | 2 (¶6→¶11, ¶7→¶10) |

No `Aa`-style marker exists in `hal_original.txt` in any of the six scopes. The hint in the post is the
case geometry itself, not an edge pair.
