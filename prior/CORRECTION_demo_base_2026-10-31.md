# Correction, and the correction of the correction: the demo's hashed object is settled

**Date:** 2026-10-31
**Source:** `grycoin_posts.json`, `t3_cleczc` ("Grycoin Block 2"), `selftext`, verbatim.

## What the author actually wrote

> "I added the extra line breaks between paragraphs necessary for correct display in Reddit before
> hashing. And for the record, each of these resolves to the combination of the ASCII codes 13 and 10,
> for 13 10 13 10 meaning two line breaks, or `\r\n \r\n` as another way of saying the same thing.
> Anyway, there should be no problem if you just copypaste everything in the Question from this Reddit
> post. **Start with the first "I" and stop with the period after "method"**, with no spaces or line
> breaks before or after that included in the hash.
>
> First three digits of MD5 hash are `3c6`."

## The three "method" occurrences, and which one the instruction means

| offset in Question | next char | context |
|---|---|---|
| 719 | space | "I explained the **method** used and the result in detail." |
| 1549 | `.` | "faster to solve by the thinking only **method**." |
| 2107 | space | "the **method** used" — inside the metadata paragraph, past the boundary |

Only the second is followed by a period. "The period after 'method'" therefore resolves to the end of
**"…the thinking only method."**, and the slice is:

| reading | chars | paragraphs | md5 |
|---|---|---|---|
| to the period ending the sentence containing the **first** `method` | 719 | 5 | `63f78215ca645670e2980c03567284cc` |
| **to the period immediately after the last `method`** | **1,549** | **10** | **`7759227d7406d8230d7e3a8f7b9846d7`** |
| to "…included in the hash." (whole Question + Format line + metadata) | 2,108 | 12 | `e40eac5d286a4f49aa56af27ee1b3c71` |

The middle one is byte-identical to `demo_base.txt`, whose md5 `7759227d…` is the value the repo
already recorded independently as "the demo's source text".

## Verdict

**`CLUES_CANONICAL.md` §6 is correct and §14.1 is wrong.** `demo_base.txt` *is* the author's slice: first
`I` of the Question to the period after the last `method`. The 10 paragraphs are all inside the hash
boundary, including ¶7's instruction sentence.

`§14.1`'s numbers cannot be reproduced by any literal reading. Its "1,456 characters" matches nothing;
its "12 blank-line-separated blocks" is the 2,108-character reading, which overshoots the stated stop
by two paragraphs; and its stated ending, "…the result in detail.", is at character 719, not 1,456.

## Consequence for this session

The retraction in the previous version of this file is itself withdrawn. Every demo number produced in
this conversation was computed on `demo_base.txt`, and that file is now confirmed by primary source and
by the independent md5 as the correct hashed object:

- 12,288 positional readings (6 mark modes x 1,024 paragraph subsets x 2 joins): 2 chance `3c6`, 0 escrow
- 2,048 sentence-scale readings: 0 begin `3c6`
- the {4,5,6,8} transport: `13082a45…` (LF) / `0f69c8ea…` (CRLF)

`DEMO_PARADOX_2026-10-31.md` stands as written. The repo's independent 9.8M sweep on the same object
agrees with it.

## One loose thread the source raises

She says the paragraph breaks "resolve to … 13 10 13 10 … or `\r\n \r\n`", i.e. CRLF CRLF, and that
this is what she hashed. The recorded source md5 `7759227d…` is the **LF** variant; the CRLF variant is
`e997007971f6f17c8775d83f30edb4c6` (1,567 chars). Both joins are covered in the sweeps, so nothing is
lost, but "the source text has md5 7759227d" and "she hashed CRLF CRLF" cannot both be true of the same
byte string. The LF value is the one that reproduces the author's own boundary arithmetic.
