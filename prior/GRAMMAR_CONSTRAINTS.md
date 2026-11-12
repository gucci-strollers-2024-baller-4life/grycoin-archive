# The demo read as a specification: five constraints, and what they exclude

Reading `cleczc` (grycoin block 2) grammatically — as BTCxanter's 2026-10-27 reply asks, *"It should
demonstrate an example that is the reverse Turing test"* — the text fixes five independent things.
Numbering follows the ten paragraphs of the certified base (md5 `7759227d…`).

| # | constraint, in the author's words | formal content |
|---|---|---|
| C1 | *"if the letter "n" at the end of the last paragraph was part of the solution, you would be expected to change it to "N" and write "capitalizatioN""* | the letter `n` ending **paragraph 2** (`…in their capitalization.`) is the paragraph-final letter of that block; changing it is the worked example of the *style* |
| C2 | *"that "n" is not part of the solution"* | **C1's letter must remain lower case in the answer** |
| C3 | *"if you were able to recognize the signs and thought that the "I" at the beginning of the previous paragraph was one of them, you would be expected to change that "I" as well to a "i""* | paragraph 5's **first letter** is lowered |
| C4 | *"you would end up changing "I" to "i" and "himself" to "himselF""* | the **final letter of paragraph 5's first sentence** is raised |
| C5 | *"Which would be the solution, once you do that for all the paragraphs where you recognize the signs"* | the rule is applied per paragraph, to a set larger than one |

## What the constraints exclude

- **Sentence-initial sign set {I,T,A,S,M}** (WORDPLAY_RULES_CATALOG §5.1). Paragraph 2 begins with `As`,
  so its single sentence is selected, and the rule raises the letter before its full stop — the `n` of
  `capitalization`. That is exactly what C2 forbids. **The formalisation in §5.1 is falsified by the
  demo's own text**, not merely negative against the oracle. This is why it never produced `3c6`.
- **Paragraph-initial sign set.** Same paragraph, same `n`. Falsified by C2.
- **Sentence-final raising in general.** C2 rules it out wherever the paragraph's last sentence ends the
  paragraph, which in this text is most of them.
- **Edge-flip families as a whole.** C3 pairs a *paragraph-first* letter with a *first-sentence-final*
  letter. The corpus tested paragraph-first with paragraph-final, and sentence-first with sentence-final,
  but never that pairing. Tested now (`sweeps/first_sentence_last_variant.py`): every subset of the ten
  demo paragraphs, both joins, oracle `3c6` — **no survivor at all**, so no `3c6` prefix exists in that
  family; chapter sets at six indices — negative.

## What the constraints allow

The selection must **exclude paragraph 2 and include paragraph 5**. The only discriminator in the text
that does both without special pleading is the phrase itself: paragraphs that *say* "recognize the
signs" — 4, 5, 6 and 8. That set, with C3+C4, gives eight changed letters
(`f`…`S`, `i`…`F`, `o`…`I`, `w`…`S`) and hashes to neither `3c6` nor the escrow; it is one of the
1,024 subsets enumerated in the same sweep.

So the demo's answer contains changes that are **not at sentence or paragraph edges**: the constraints
fix two edge letters and the text says more are present. The remaining degrees of freedom are word-internal
letters, which is where R1 (`messaGe`, `vOIce`) lives — and R1's own constraint, never used, is that every
marked letter sits at a **word edge** (`a`→`A` initial, `messaGe` final, `You` initial, `oN` final).

That family is now enumerated for the chapter (`sweeps/name_marking_word_edges.py`): every in-order chain
of word-edge occurrences per paragraph for ten names, plus the seed-anchored chain at the chapter's one
planted interior capital (`ppM`, paragraph 73). **728,072 derivations at indices 0/1/2/76, zero hits.**

## The surviving-capitals reading (tested, negative on the demo, and it is the only reading that explains C3)

Stage two's own hint says the signs are read *off the paragraph initials* ("The letters I, T, A, S, and M
as first letters of each paragraph of this post"), and block 29's answer marks the name **AOI** by case.
The demo's ten paragraph initials are `IAFFIOWWIA` — and they contain `A`, `O`, `I` **in order** at
paragraphs **2, 6 and 9**. So the reading is: lower every paragraph's initial *except* the ones that spell
the name, so the surviving capitals spell it.

Why this reading matters even though it fails the oracle: it is the only one that explains C3 without
special pleading. C3 lowers paragraph 5's initial `I` — under a sign-set rule that is arbitrary (the `I`
of `IAFFIOWWIA` at paragraph 1 and paragraph 9 are signs too, and paragraph 2's `A` is a sign, which is
exactly what makes the sign-set reading contradict C2). Under the surviving-capitals rule, paragraph 5's
`I` is lowered *because it is not part of the name*, and it is the only `I` in the text that the rule
singles out. C2 is respected too, since only initials move.

Tested on the certified demo base, both joins, oracle `3c6`: keep-only, keep + first-sentence-final
raise, keep + paragraph-final raise, and the inverted selection. **No `3c6` survivor at all**, so no
member of this family is the demo's answer.

Caveat that cuts both ways: the rule touches seven initials in the demo, which fits "keep the rest
completely unchanged" but strains "change only a couple of letters". On the chapter the same rule needs an
enumeration of every embedding of the name in the 273-initial string (AOI alone has thousands), which is
the one part of this pass left unfinished.

## Chapter side of the surviving-capitals reading (run 2026-10-31)

`sweeps/surviving_capitals_chapter.py`, repaired harness, indices 0/1/2/76, repaired base (br-crlf).
Paragraph initials are the sign channel the chapter itself names, so the rule was applied to that channel:

| variant | what it lowers | meanings |
|---|---|---|
| V1 dense | every paragraph initial except the embedding | 3,045 (AOI) + 46 (STNM) + 18 (AOIN) + 9,945 (THOMAS) + 8,120 (NAKAMOTO) + 15,329 (SATO) |
| V2 sparse | only initials equal to a name letter but outside the embedding — the variant that honours "change only a couple of letters", and in the demo it lowers four initials including the one C3 names | same embeddings |

**292,024 derivations, zero hits.** The chapter's initials are `SISIFFWW…IA` (273 characters); FINNEY,
HAL, SECOND and GRYCOIN have no embedding at all in that channel, which is itself a result: the initials
cannot spell any of those, so if the channel is the initials the name is one of the six above and it is
not marked this way.

## Word-level inheritance of the demo's two exemplars (closed)

If the demo's format is inherited by *token* rather than by position, the chapter's own occurrences of the
two exemplified strings are the sites: `himself` → `himselF` (C4) and a paragraph-opening `I` → `i` (C3).
The chapter carries 7 lowercase `himself` tokens (paras 126, 205, 215, 218, 218, 219, 248) and 27
paragraphs opening on the word `I`. All 2^7 subsets of the `himself` sites, each with and without the
27 `I` openings lowered, on three bases, indices 0/1/2/76: **1,560 derivations, zero hits.**

Note also that the chapter's `himself` sites are the *argument's* prose ("Hal maybe didn't know himself",
"Outing himself as Satoshi", "Mail Conversation With Himself") — the same semantic dilution that killed the
`SMITH` reading of the internal-capital words in `FINDINGS_MARKS_2026-10-31.md`. The token channel is not
where a deliberately sparse mark set would live.

## Short marks: SN, EU (requested), and their Atbash foldovers — 2026-10-31

Atbash is not a foreign device here: round-two block 30's answer is `EU IQ KO` with TOMI
`Atbash foldover`, so `EU` is a token her own corpus treats as folded. Under the foldover
A↔Z, B↔Y, …: **SN → HM**, **EU → VF**. Both directions were tested, plus the reversals NS, UE, MH, FV.

### A structural exclusion, not a sweep result

| channel | units | letters available |
|---|---|---|
| paragraph initials | 273 | no **U** at all |
| sentence initials | 621 | S 40, N 16, H 21, M 13, E 7, **U 0** |

So **EU and UE cannot be surviving-capitals marks in either initials channel** — there is no `U` to keep.
Any reading that needs EU has to live in the word-edge channel or outside the case mechanism entirely.
(The chapter mentions Atbash twice, in the PGP/address discussion; the strings `EU IQ KO`, `EUIQKO` and
their foldover `VFRJPL` do not occur in the text.)

### What was swept

| channel | marks | readings | derivations |
|---|---|---|---|
| paragraph initials | SN, NS, HM, MH, VF, FV (EU, UE impossible) | dense and sparse surviving-capitals | 3,816 |
| sentence initials | SN 192 embeddings, NS 448, HM 139, MH 134, VF 39, FV 24 | dense and sparse | ≈ 12,000 |
| word edges per paragraph (block-2 constraint) | all eight marks, incl. EU 730 and UE 617 embeddings | marked up and marked down | 234,608 |

Three bases (br-crlf, br-lf, ex-crlf), indices 0/1/2/76, repaired harness: **250,424 derivations, zero
hits** in addition to the paragraph-initial run. The short-mark family is closed on every case channel
the chapter has.

## 2026-10-31 evening pass: the initials carry TWO exactly at the anchor, and R1:29's device runs on this chapter but is not the answer

**R1:29's device, applied to the chapter.** R1:29's answer is the chapter draft with `voice`→`vOIce`:
AOI marked across an article `A` and a later word carrying `o` then `i`. That shape is present in this
chapter — paragraph 11 mentions a pleasant female voice — so the device was enumerated over every
sentence: 156 (article, oi-word) pairs, marked with the article and without it, both joins, four indices.
**624 derivations, zero hits.**

**The three windows already contain STNM, unflipped.** Reading the last letters of paragraphs 5-8,
92-95 and 167-170 gives `s,t,n,m` in all three — the certified stage-one signature, latent, three times
over. That is a calibration result rather than a lead: the answer's flips would be exactly what
capitalises those, and that family is closed.

**New: the initials spell TWO at paragraphs 77, 78, 79.** Skipping the opening quotation mark, those
three paragraphs begin `T`, `W`, `O`:

| para | initial | text |
|---|---|---|
| 77 | T | "There are two ways to make sure of adoption. I will use the opportunity to do a reverse Turing test." |
| 78 | W | "What?" |
| 79 | O | "Of course you know what a Turing test is. …" |

This is the only acrostic in the chapter that lands exactly on the puzzle's own anchor pair, and the
paragraph it starts in says "two ways" — the word is self-declaring there. Split by channel, it is
dialogue-only (index 49 of the 63 dialogue initials); the narration channel carries none. So if the
initials are a channel at all, its live site is the block-77 dialogue, not the signature windows.

**TOMI-infix appendix forms with the recovered b76 key.** Round two's documented format is
`[solution] TOMI [TOMI] [link]`, and b76's key is now known, so the infix forms were tested where the
earlier appendix pass used bare separators: chapter + `" TOMI "`/`" TOMI omit TOMI "`/`" TOMI Omit TOMI "`
+ b76 WIF / its last 7 / last 3 / nothing, with no flips, the windows flipped, and the non-ITASM set
flipped: **72 derivations, zero hits.**

## Numbers as positional selectors (2026-10-31, closed)

The chapter states 23 distinct numeric tokens, and the number motif is over-determined in this text: `350 ppm`
sits in paragraph 73 and `ppM` inside it is the chapter's only planted interior capital, while 350 mod 273 = 77,
which lands exactly on the second `"What?"` anchor. That coincidence had never been used as a *selector*.

Selector family: every numeric token mapped three ways (mod 273, complement mod 273, digit sum mod 273), each
with offsets -1/0/+1 in paragraph space, three edge modes (first down, last up, both), both joins, indices
0/1/2/76. **4,440 derivations, zero hits.**

So the numbers locate the anchor but they do not select the marks. What the coincidence does establish is that
the anchor pair is where the puzzle's own arithmetic points, which is where the `T-W-O` acrostic also sits
(paragraphs 77-79), and both readings are now closed as selectors.

## Paragraph 78's pid is not an md5 of any text in the story (closed 2026-10-31)

BTCxanter's claim was that paragraph 78's `data-p-id` (`8b71bade9685d3388452bc4755b06a0d`) does not match
`"What?"` and therefore the author edited the text, leaving a substituted paragraph in the base. If that were
true the original line would be some text whose md5 is that pid, and since the line is dialogue it would almost
certainly be a line from this story.

Tested: **20,282 candidate strings** — every paragraph of the certified 273 (as published, stripped, with
trailing CRLF/LF/space, with and without straight and curly quotes), every paragraph as split by its internal
break, every sentence of the chapter, every paragraph and sentence of all 33 parts (2,066 paragraphs, 3,871
sentences, HTML-stripped and entity-unescaped), and every quote-style variant of `What?`/`what?`. **No string
in that set hashes to `8b71bade…`.**

That settles the asymmetry the corpus had only inferred: paragraph 34's pid *is* the md5 of its text
(`184826be0ea6837abb5851807f7a9e2b`, identical to our `"What?"`), and paragraph 78, the exact duplicate, carries
a pid that is not a content hash at all. The pair is produced by Wattpad assigning a fresh non-content pid to a
duplicated paragraph, not by an edit. The base text at 34/78 is original, and the substitution reading is dead.
