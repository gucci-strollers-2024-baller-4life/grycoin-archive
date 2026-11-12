# Remaining discrepancies: blocks vs chapter, forensic read

## 1. Block 29 vs chapter 11-29: ten word-level substitutions, no insertions or deletions

Word-level alignment gives **10 replace ops, 0 insert, 0 delete** over the same scene. The chapter is
block 29's text with exactly these swaps (block -> chapter):

| # | block 29 | chapter | type |
|---|---|---|---|
| 1 | `vOIce.` | `voice.` | the only certified flip, removed |
| 2 | `"Still 21st Century".` | `"2020."` | number rewritten as a date |
| 3 | `one hundred` (years) | `ten` | number shrunk |
| 4 | `Third most` (popular) | `A` ... | ordinal dropped |
| 5 | `girls` | `girls."` | punctuation/quotation repaired |
| 6 | `right` | `I` | attribution repaired |
| 7 | `now."` | `recognize the signs.` | phrase replaced |
| 8 | `Overlord` | `Omnipotent` | name of Aoi's agency changed |
| 9 | `second` (rate) | `third` (rate) | ordinal shifted +1 |
| 10 | `zff` | `The scenery changes again. Now she is a young woman of Japanese ancestry who is very smart and sincere. She is dressed in a running outfit...` | block code removed, closing rewritten |

Pattern: **the author swapped numbers and ordinals** (21st Century->2020, 100->10, third->a, second->third)
and one name. That is the same "shift by one" business the Satoshi Code toolkit describes (HAL=IBM,
BIT=AHS). The one flip in the block (`OI`) is absent from the chapter, so the chapter keeps the
**question** form of this scene.

## 2. Stage one (q2 b77) vs chapter: only 28% of the post is there

The block is the full 16-paragraph Finney post (5,331 chars). The chapter contains **1,504 chars of it
(0.28)**, in five paragraphs (231-235). 12 of the 17 block paragraphs are absent entirely (ALS, heirs,
paralysis, the 2010 emails). So the chapter holds only the four flipped paragraphs plus one context
paragraph, not the post.

But the block's opening line is echoed: block `I thought I'd write about the last four years, an
eventful time for Bitcoin and me.` vs chapter para 4 `I thought I'd write about my second coming, an
unusual event some people might be interested in.` The chapter's opening is a rewrite of the post's
opening, so the chapter is a **re- authored story built on top of the post**, not a copy of it.

## 3. Block 66: a later block quotes the chapter's own addition

`q2 b66` = `A young woman of Japanese ancestry who is very smart and sincere.` It is present in chapter
para 29 and **absent from block 29's text** - it is exactly one of the clauses the chapter added when it
rewrote the block-29 scene (row 10 above). So at least one block was authored from the chapter's new
material. The layering runs chapter -> later blocks, not blocks -> chapter.

## 4. The 3-character codes are not checksums - and that has a consequence

48 of the 153 inputs end in a 3-character token (41 after a space: `Thank you KPb`, `... zF3`;
7 glued after a full stop: `...cash.Pzd`, `...death.HwX`). 105 inputs carry no token. Twelve
derivations of that token from the preceding text were tested (MD5/SHA-256 first and last 3 hex chars,
base58 prefixes of both digests, text length) - **zero hits**. The code is independent puzzle metadata,
not a function of the input text.

Consequence for the chapter: block 63's published answer is
`The Rt Hon Alistair Darling MP TOMI If you don't get this, sorry, it is hard L4GWDy9...` - a solution
string carrying a literal `TOMI` token plus a long code. If the RBB chapter's answer likewise carries a
token or code, then **every bare-chapter sweep, ours included, is testing text that cannot match**.
That single fact would explain the entire certified-negative wall on the chapter.

## 5. Candidates built from these discrepancies (all negative)

Five chapter texts derived from the swaps above were hashed and derived against both escrows
(`14zMk...` prize, `1tzieU...` demo), 4 joins each (20 derivations):

- chapter plain
- chapter with `vOIce` restored
- chapter with the numbers restored (`2020`->`Still 21st Century`)
- chapter with the whole rewritten span replaced by block 29's text
- same, with paragraph-edge flips applied to the spliced block-29 lines

None match. Reference values: chapter `\n\n` -> MD5 `48d31820` -> `14isnRimk9qAzpm85qwiFgLjzxL1387TXL`.

## 6. Paragraph 243 is not a verbatim extract of paragraph 222: `true` became `real`

The chapter's rulebook states the extraction device in word terms, not letter terms:

- 242: *"The first four and last four words of the paragraph hinting at the solution."*
- 243: `"Today, Satoshi's real identity"`
- 244: `"I recognize the signs."`
- 245-246 gloss them: *"Take the first words of that together and you get 'Today, I' ... Take the next
  three words together and you get 'Satoshi's real identity, recognize the signs'."*

Paragraph 222 is 51 words and its first four are `Today, Satoshi's true identity`; its last four are
`I, recognize, the, signs.` So 244 is exact and 243 **is not**: the chapter's own hint paragraph
(222) and Hal's post (`hal_original.txt`) both read *true identity*, and `real identity` occurs
neither in 222 nor anywhere in the post. The worked example silently substitutes one word.

Consequences for any preimage built from her quoted strings:

1. A string assembled as `Today, Satoshi's real identity ...` cannot reproduce her bytes; the
   chapter's own word is `true`.
2. This is the same substitution class as §1 (numbers and ordinals swapped by one, `Overlord` to
   `Omnipotent`): the author paraphrases when she quotes herself, so quotes are evidence of intent,
   never of bytes.
3. The unit in 242 is the **word**, not the letter. Every case-flip sweep in the corpus works at the
   letter/edge level; the only word-level rule the author states outright sits on the paragraph she
   then demonstrates.

## 7. The four "quoted non-voice" paragraphs are all Hal's words, and the doublet is a gloss

222 and 231 are verbatim Finney (`true identity`, `I recognize the signs`, the post's opening all
verify against `hal_original.txt`); 243 and 244 are her extraction from 222. So the four are one
document layer, which is why the voice census isolates exactly them, and why they cannot be a
switch set: 243/244 are not text from the story at all, they are the author reading paragraph 222.

Rhythm check after the doublet, for the record: paragraphs 218-242 average 13.4 words per sentence
with 4.4 commas per 100 words; 245-260 average 12.3 with 3.2. There is no staccato break, no
register shift, and 247 is a section heading (`3. Other evidence`). Nothing begins payload-like after
243/244; the doublet is followed by her own two-sentence gloss and then the next section.

## 8. Measured: the four "quoted non-voice" paragraphs as a corpus

Counts, punctuation stripped (script: none, arithmetic below is reproducible):

| paragraph | chars | letters | words |
|---|---|---|---|
| 222 | 275 | 215 | 51 |
| 231 | 398 | 315 | 70 |
| 243 | 32 | 25 | 4 |
| 244 | 24 | 18 | 4 |
| concatenated | 729 | 573 | 129 |

None of 9, 26, 37, 44, 63, 77 or 273 appears in that table, so the four-paragraph block is not
carrying a count constant.

**The one place 44 does appear is her own gloss.** Paragraphs 243+244 are the eight words
`Today Satoshi's real identity I recognize the signs`, word lengths 5,9,4,8,1,9,3,5: **44 typographic
characters including the apostrophe, 43 letters, 8 words, 4+4**. The chapter's signature stride is 44
(the 34/78 anchor pair sits 44 apart). So the demonstrated extraction is 44 characters long, which is
either the author's thumb on the scale or a coincidence; it is recorded here, not claimed.

**The flatness hypothesis fails.** Index of coincidence: 222 = 0.061, 231 = 0.060, 243 = 0.063,
244 = 0.059, concatenation 0.062, whole chapter 0.065, English prose 0.0667. Chi-square per alphabet
letter against English: 0.7 to 3.7 for the four paragraphs, 24 for the chapter. The four are *closer*
to textbook English than the chapter is, which is the opposite of a constructed inscription. They are
prose by Hal Finney, which is what they are.

**Anagram and multiset tests have no power here.** At 573 letters, `HALFINNEY`, `AOINAKAMOTO`,
`SATOSHINAKAMOTO`, `ANDREWYANG`, `NAKAMOTO` and `STNM` are all "contained". Any name of that length is.
Containment at this n is vacuous and must not be read as a signal.

**Targeted probe (285 derivations, negative).** If the rule in 242 is the word-level extraction, the
preimage may be an extracted string rather than the edited chapter. Built first-four, last-four and
first-four-plus-last-four word strings from paragraphs 222, 229, 231, 237, 238, 239, 240, 241, 242,
245, 246 in three joiner forms, plus the two gloss phrases, using the chapter's own `true` (never her
paraphrased `real`), at indices 0, 1, 2, 76, 77 against both escrows: **0 hits.**

## 9. The "four exceptions" are the quotation layer, and the worked example carries no case mask

**Provenance of the four** (CORRECTED 2026-10-31, fifth pass): 222 is verbatim Hal and 244 is its last
four words. The five-paragraph reprint at 231-235 is **also** verbatim: token-level diff against
`hal_original.txt` paragraphs H2-H6 gives 81/48/38/70/79 tokens on both sides with **exactly one
change in the whole span**, `facinating` -> `fascinating` (234). An earlier substring test in this
note reported only three verbatim paragraphs; that test was faulty and the token diff supersedes it.
243 remains the paraphrase. So the four exceptions are the quotation layer, which the voice census
isolated, not a coordinate.

**The worked example contains zero case anomalies.** Capitals in 243 sit only at letter positions
0 (`T`) and 5 (`S`); in 244 only at position 0 (`I`). That is ordinary sentence capitalisation. There
is no deviant capital anywhere in the pair, so there is no mask to reverse-engineer: the mask is the
identity.

**Input and declared output are the same eight words, reordered.** Her own gloss (245-246):

- in: `Today, Satoshi's real identity` + `I recognize the signs.`
- out: `Today, I` then `Satoshi's real identity, recognize the signs`

positions of the output words in the input: `1,5,2,3,4,6,7,8`. The device demonstrated is a reading
order (take the first word of each line together, then the rest), not a case pattern. Applying that
"mask" cyclically to 273 paragraphs applies nothing.

**44 cannot be the modulus that selects the exceptions.** Paragraph indices mod 44: 222→2, 231→11,
243→23, 244→24. First-character offsets mod 44: 31, 10, 33, 25. No shared residue, no ladder. Mod 9
gives 6, 6, 0, 1; mod 13 gives 1, 10, 9, 10. The 44 lattice as sign sets was already swept (1,056
derivations, negative) and the stride is real in the chapter's *placement* (34 and 78 sit 44 apart),
but the four exceptions do not lie on it.

**Structural note on "extract a key":** the certified pipeline is one hash over the text
(md5(text) -> BIP39 -> address, verified end to end on stage one at 19TbyN5). A keyword lifted from
the prose has no slot to enter; the only object that touches the wallet is the chapter's own bytes.
The single open variable remains *which letters carry a capital*, which is why the demo (block 2,
md5 prefix `3c6`, cheap oracle) is the one object that can still supply the rule.
