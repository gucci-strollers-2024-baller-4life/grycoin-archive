# The documentary pull on `3c6`

**Date:** 2026-10-31 **Source:** `grycoin_posts.json`, all 91 posts, `title` + `selftext`, literal search.

## Result: one occurrence, in the demo's own post

`3c6` appears **exactly once** in the whole corpus, in `t3_cleczc` ("Grycoin Block 2"), in the same
paragraph that defines the hash boundary:

> "…Start with the first 'I' and stop with the period after 'method', with no spaces or line breaks
> before or after that included in the hash. **First three digits of MD5 hash are 3c6.**"

It is not attached to the Finney post, to stage one's residue, or to any other artefact in her
writings. There is no second mention to compare against, so the "attached to a different file in the
corpus" hypothesis has nothing to stand on.

## What the corpus does show: the prefix is hand-typed, and she has got it wrong before

Nearly every block publishes its prefix the same way, with an annotation saying whether she copied it:

- "(copypasted)" appears on blocks 61, 63, 64, 71, 72, 73, 74, 75, 76 — the ones where she trusts the value
- block 53: "FIrst three digits of MD5 hash (**not MP5**, spelled correctly this time) are 4c1."
- block 52: "FIrst three digits of **MP5** hash are 21b."
- **block 59 is the decisive one:** *"Sorry everyone. Another mistake in this block. When typing the
  first three digits of the MD5 hash, I got the last one wrong. Should have copypasted that."*

So a published prefix that does not match the answer is a **documented author failure mode**, with a
named instance. That is the only explanation for `3c6` that does not require a missing answer: the
demo's true digest may begin `3c_` or `_c6`, and the last digit is exactly the digit she admits getting
wrong elsewhere.

## But the prefix is not the binding oracle, so it does not matter

The gate was never `3c6`; it is the escrow. Re-ran the demo's full positional space **with no prefix
filter at all** — 9 mark modes (head; head + paragraph-tail; head + first-sentence-tail; head +
sign-sentence-tail; head + every-sentence-tail; paragraph-tail; first-sentence-tail; sign-sentence-tail;
every-sentence-tail) x all 1,024 paragraph subsets x 2 joins = **18,432 texts, every one derived at
indices 0/1/2**.

| texts | begin `3c6` | escrow hits |
|---|---|---|
| 18,432 | 2 | **0** |

So: if `3c6` is a typo, the typo is not hiding an answer in this family, because the family was checked
against the address rather than the prefix. The demo's answer is not a paragraph-edge case-edit under
any of the nine modes.

## Two premises in the request that do not survive the text

1. The disavowal is of the `n` at the end of the paragraph **before** ¶3 — that is ¶2's
   "capitalization." — not of ¶3's own terminal letter. ¶3 is the hypothetical example, not the object.
2. ¶3 and ¶7 are not "FFWW blocks." The F/F/W/W initials are ¶3-¶4 and ¶7-¶8; ¶3 and ¶7 are the
   *instructions about* the marks ("you would be expected to change…", "you would end up changing…").
   The exclusion covers a paragraph's terminal letter, not a block class.

## What is left

`3c6` is a single, hand-typed, unverifiable digit in a corpus where the author has already admitted
getting such a digit wrong once. It is not evidence about where the answer lives. The escrow
`1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` is the only oracle in the demo that cannot be mistyped, and it has
now been checked against 18,432 structurally valid texts with no prefix gate.
