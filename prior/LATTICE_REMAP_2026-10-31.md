# Relattice: reading the chapter as a text, then rebuilding the search lattice from it

Session 2026-10-31, fifth pass. This document does two things: it reads paragraphs 220-246 as prose
rather than as a rule statement, and it rebuilds the constraint lattice from what the prose actually
says. One earlier family is voided by the reading, not merely closed.

## 1. The chapter says what "all paragraphs except for four" means, and it is not this chapter

Read in order, paragraphs 220-230 are a single argument about **Hal Finney's bitcointalk post**:

- 220: "Once you know about the anagram above, you will expect it to have some hidden meaning. And it
  will become very easy to recognize the signs." The antecedent of "it" is *that post*.
- 228: "The letters I, T, A, S, and M as first letters of each paragraph **of this post**."
- 229: "All paragraphs except for four, which start with F F and W W."
- 230: "Those paragraphs are (with one paragraph starting with I in between)."

So the sentence is a **description of the stage-one base**: in the Finney post every paragraph begins
with I, T, A, S or M except four that begin F, F, W, W, and those four carry an I-paragraph between
them. It is narration of a solved mechanism, not an instruction about the 273-paragraph chapter.

**Consequence.** The family tested as "flip every chapter paragraph except four" (269 paragraphs,
`test_four_exception.py`, 264 derivations) and its variants are void, not merely negative: the
instruction was never addressed to this text. The same applies to any future reading that treats the
sentence as a prescription. This is the mechanical reason that whole family produced a typographically
impossible document (262 of 273 paragraphs open uppercase): it was applying a sentence about a
16-paragraph forum post to a 273-paragraph novel.

## 2. The four are one quotation block, not structural seams

The four paragraphs are printed in the chapter as what they are:

| para | first letter | what it says |
|---|---|---|
| 222 | T | the full Finney paragraph: "Today, Satoshi's true identity has become a mystery… so I recognize the signs." |
| 231 | F | "For those who don't know me, I'm Hal Finney…" |
| 232 | F | "Fast forward to late 2008 and the announcement of Bitcoin…" |
| 233 | W | "When Satoshi announced Bitcoin on the cryptography mailing list…" |
| 234 | I | "I was more positive…" — the I-paragraph the narrator says sits between them |
| 235 | W | "When Satoshi announced the first release of the software…" |

231-235 is the stage-one quotation; 234 is the interpolated I. Their paragraph-final letters are the
STNM signature the narrator then reads out at 236-237. 243 ("Today, Satoshi's real identity") and 244
("I recognize the signs.") are the narrator's own four-word fragments, used at 245-246 to demonstrate
the confirmation device. None of the six is a seam, a spacer, an editorial insertion or a payload
boundary: they are a quotation and its worked example.

## 3. The chapter plants three decoys of the same signature

Three windows of four consecutive **original** paragraphs also start F, F, W, W and end in the same
tail pattern: **5-8**, **93-96**, **168-171**. They are the chapter's own prose (the brain-wallet
opening, the Grycoin purpose section, the anonymity discussion), not quotations. A solver who "looks
for the signs" finds these three, which is exactly why they are there. Every subset of those windows
is already closed (2^16 over the 17 window paragraphs, negative at indices 0, 1, 76).

## 4. The device the chapter states for itself

- 236: read the **last** letter of each anomalous paragraph, because "recognize the signs" comes last
  in the paragraph. That yields STNM.
- 240: "Nm ST" is the genesis-block signature; same signature.
- 242: "The first four and last four words of the paragraph hinting at the solution."
- 245-246: "Today, I" / "Satoshi's real identity, recognize the signs".

So the chapter states two devices, both of which it demonstrates on itself: a paragraph-tail read, and
a first-four/last-four-words read applied to *the paragraph that hints at the solution*. The second
has only ever been applied to a handful of hand-picked paragraphs (21 candidates, `WORDPLAY_RULES`
§8), never per paragraph across the chapter.

## 5. The lattice, rebuilt

Axes: **corpus** (exact / repaired / tagged / single-line) × **join** (CRLFCRLF / LFLF / none) ×
**unit** (chapter / paragraph / sentence / word / letter) × **selection** (positional, lexical,
structural, grammatical) × **direction** (first-down-last-up certified, inverse, split) × **extent**
(case only, per her own wording) × **index** (0, 1, 2, 44, 76, 77).

Closed and byte-verified: ~5.45M candidates across every documented rule R1-R8, the 2^16 window
closure, the 2^20 mechanism closure, the 14 "signs" paragraphs, the three decoy windows, name marking
on 19 names, positional keys 7 and 44, numeric/Fibonacci/draft channels, spans as whole preimages.

Three cells are genuinely open, in ascending cost:

1. **Demo answer space.** The demo's source text is certified (`demo_source_exact.txt`, 1,549 bytes,
   md5 `7759227d7406d8230d7e3a8f7b9846d7`) and its escrow is unspent. Singles and pairs of arbitrary
   case flips are closed (716,710). **Arbitrary triples have never been enumerated**: 285,129,390
   texts, filtered by the published 12-bit prefix `3c6`, survivors derived at indices 0/1/2. This is
   the only cell with an independent oracle, and it converts the chapter's unknown rule into a known
   plaintext diff.
2. **Sentence-granularity pairs of marks.** 651 sentence openings and closings, ~847k ordered pairs,
   never run correctly (`WORDPLAY_RULES` §31).
3. **Word-edge letter pairs on the chapter**, 121M, ~49h, not affordable here.

## 6. What the reading changes about the target

The phrase that generated the last four sessions of exclusions is a description of someone else's post.
The chapter's own instruction is narrower and stranger: find the paragraph that hints at the solution,
take its first four and last four words. That is a **selection** rule pointing at a single paragraph,
not at 269. The next cheap test is therefore not another subset sweep but the per-paragraph
first-four/last-four-word preimage family the chapter itself names.
