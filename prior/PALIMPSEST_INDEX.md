# Palimpsest index: 77 published block inputs vs the 273-paragraph chapter

Source of ground truth: `ninjaops-puzzle-lanes/quizchain/calib/quiz1_blocks.py`
(77 `Block(number, algorithm, exact_input)` records = solved input strings).
Scripts: `palimpsest_index.py`, `pal2.py`, `pal3.py`, `pal29.py`; data `palimpsest_index.json`.

## Result

`pal3.py` matches each normalized block input against the normalized chapter and keeps
matching runs >= 20 chars (coverage = matched chars / block chars).

| block | coverage | chapter paras |
|---|---|---|
| **29** | **0.95** | **11-29** |
| 23 | 0.91 | 47 (41-char string) |
| 9 | 0.91 | 27 (29-char string) |
| 17 | 0.70 | 107 (26-char string) |
| 32 | 0.64 | 17 (35-char string) |
| 13 | 0.54 | 3-4 (25-char string) |

Every other block: no matching run >= 20 chars. So at the scale of a real text, exactly
**one** published block (29) is embedded in the chapter. The other five rows are short
phrases, not embedded questions.

## Block 29 verified against its published input

`pal29.py` aligns block 29's `exact_input` (1360 chars, 17 lines, suffix `zff`) to chapter
paragraphs 11-29: 1302 chars match, 19 diff opcodes, of which **exactly one is case-only**:

    block:   A pleasant female vOIce.
    chapter: A pleasant female voice.

Chapter [11] `"Good morning, Tom."` and [12] `A pleasant female voice.` are byte-identical to
block 29's first two lines apart from that single flip pair. The published solution therefore
uppercases **O** and **I** in the second sentence only - the vowels of A-O-I from the second
position - and nothing else in 1302 matched characters. The rule is local, not whole-text.

## Correction to the palimpsest reading

Block 29 is a *rewrite* of the same scene, not a byte copy. The remaining 18 diffs are wording
edits, for example:

- block `"Still 21st Century"` vs chapter `"2020."`
- block `Not even one hundred years have passed.` vs chapter `Not even ten years ...`
- block `Artificial Overlord Intelligence` vs chapter `Artificial Omnipotent Intelligence`
- block `second rate quiz questions` vs chapter `third rate ...`
- block `Third most popular name` vs chapter `A [most popular name]`
- the chapter's closing lines of the span (new woman, running outfit, sportswear) are absent from block 29

So "the chapter contains previous questions verbatim" holds only for [11]-[12]. The rest is a
re-edited near-duplicate, which also means flips harvested by diffing block 29 elsewhere in the
span are unreliable.

## Consequence for the next move

An index over the chapter yields n=1, so a full 90-block scan of the chapter will not produce a
catalogue of embedded questions. The 77 `exact_input` strings are ground truth for *solutions*;
extracting the flip grammar needs the corresponding *question* texts, which are not in the
chapter and not in the Reddit answer dumps (`as_*.json` are comment threads). Two usable leads:

1. 18 of 77 inputs (blocks 31-34, 37-50) carry the literal token `BFU`/`BFUB`/`BotFU`
   ("A BFUB Before B fTS", "human BFUB Before artificial intelligence explosion 3NJ",
   "Humanity First BotFU Sphinx Yang JRu"). That is a shared substitution vocabulary, not case
   flipping, and it is worth tabulating as its own layer.
2. Block 29 is currently the only certified (question -> flips) pair. Every further certified
   pair has to come from a block question page or thread, not from the chapter.
