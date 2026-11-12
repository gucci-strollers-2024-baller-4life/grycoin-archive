# The ¶232 reprint — full analysis

Chapter ¶231-235 quotes Hal Finney's bitcointalk post. This is the only place
in the entire corpus where the author shows a transform working on text he
did not write. Measured character by character.

## The diff, exact

Source: `hal_original.txt` ¶2-6 (1,608 chars, LF-joined)
Reprint: `base_chapter_lf.txt` ¶231-235 (1,611 chars, LF-joined)

Three differences. All three are **insertions**. Nothing is deleted or moved.

| # | Type | Hal | Chapter | Offset in 45,450-char base | Paragraph |
|---|---|---|---|---|---|
| 1 | insert `"` | — | opening quote | 38358 | ¶231 |
| 2 | insert `s` | `facinating` | `fascinating` | 39562 | ¶234 |
| 3 | insert `"` | — | closing quote | 39968 | ¶235 |

Net +3 characters. The reprint is a superset of Hal's text, not a variant of it.

## What this establishes

**One. It cannot be a copy-paste.** A paste preserves spelling. He repaired
Hal's misspelling, which means he retyped or re-edited the passage. That matters
because the author's own instruction is "copy paste and do not change anything
with the line breaks, change only the capitalization of letters." In the one
place where he demonstrates the method, he broke his own transcription rule.

**Two. It forecloses a whole family arithmetically.** Because the reprint is
three characters longer, no sequence of case flips applied to it can ever
reproduce `safudev_stage1.txt`. Not "has not" — cannot. The families that
assume the reprint equals stage one's question are dead by length alone,
independent of their empirical 0 hits.

**Three. The quotation boundary is not arbitrary.** Hal's 16 paragraphs have
initials `I,F,F,W,I,W` then `T,A,T,S,M,A,T,I,A,T`. Every anomaly, every
paragraph the rule can fire on, sits in ¶2-6. The second half has none. He
quoted exactly the operative half and dropped the inert one, then lifted the
trigger sentence out of the dropped half and gave it its own paragraph:

> Hal ¶7: "…so I recognize the signs."
> Chapter ¶20: "I recognize the signs."

So the quote is bounded by the rule, and the one line he needed from the other
half he kept as a separate paragraph.

## What it does not establish

A selector. Every reading at this site is closed:

- the `himself` → `himselF` variant the demo names, on all six paragraphs
  containing "himself", first-sentence form and whole-paragraph form
- the `fascinating` variants: `faScinating`, `fascinatinG`, `Fascinating`,
  dropping the inserted `s`, and dropping it together with the Finney four
- the Finney four ¶231, 232, 233, 235 alone, with and without ¶234

760 derivations, both joins, indices 0-9, zero hits on 14zMkTga.

## The structural conclusion

The author said stage one's solution becomes stage two's **question**. He then
reprinted stage one's question inside stage two's text. So the reprint is the
question restated, and a text cannot be both the question and the answer. That
is why applying the signature to it can only regenerate `19TbyN5`, the address
that was already solved.

The reprint's value is diagnostic, not cryptographic. It proves the author
adapted rather than copied, and it shows what adaptation looked like when he did
it in front of us: he repaired a spelling, he added delimiters, and he cut the
passage at the exact boundary where the rule stops being able to fire.

That is the shape of the adaptation still required. It is not a lookup.
