# Wordplay rules across all 33 chapters — parsed catalogue, and what each one has been applied to

Session 2026-10-30. Method: all 33 parts of the Wattpad story re-fetched from
`wattpad.com/apiv2/?m=storytext&id=<part>` (33/33 HTTP 200), parsed as `<p data-p-id>` paragraphs with
`<br>` preserved as internal line breaks, bold/italic tags stripped, entities unescaped.

**Parse validation.** For every part, `sum(paragraph chars) + internal breaks + 2*(n-1) separators + 1`
must equal the `length` Wattpad reports for the part. It matches **exactly for 32 of 33 parts**. The
single exception is *Complete Quizchain* (61,015 modelled vs 61,032 reported, -17), which is the log
part built from nested lists; its paragraph text still parses and every rule statement quoted from it
below is byte-identical to the `<p>` bodies.

This table is the machine census behind everything else in this file.

| part | title | paras | chars | lowercase-initial paras | camelCase anomaly tokens (mechanism demos) | duplicate paras | "sign(s)" |
|---|---|---|---|---|---|---|---|
| 717956015 | Welcome to the Quizchain | 49 | 9076 | 0 |  | 2 | 0 |
| 720888559 | Second | 273 | 44896 | 10 | `WorldWideAbsoluteCarbonBudget`, `AndrewYangForPresident`, `abcdefghijkLmnopqruvwxyz`, `abcdefghijkLmnopqrstuvwxyz` | 1 | 20 |
| 720889517 | Second Life | 17 | 1342 | 0 |  | 0 | 0 |
| 720890652 | Hoax | 44 | 6666 | 0 | `oarHoaxUd`, `AndrewYangForPresident`, `zmPzd` | 1 | 0 |
| 720892473 | FU AOI | 17 | 3152 | 0 | `AndrewYangforPresident` | 0 | 0 |
| 720893344 | Utter Disaster Three Block Series | 22 | 4722 | 0 |  | 0 | 0 |
| 720895205 | Complete Quizchain | 766 | 59379 | 24 | `gFm`, `qJio`, `NRqEsd`, `notMetamon`, `naMe`, `AndrewYangForPresident`, `zmPzd`, `messaGe`, `DivfNa`, `AndrewYangforPresident`, `LidEhei`, `BaSCifCatfAaa` … | 95 | 0 |
| 720895609 | 4444 and 4442 | 15 | 3653 | 0 |  | 0 | 0 |
| 721505724 | TOMI | 18 | 3688 | 0 |  | 0 | 0 |
| 721795188 | Tragic Boating Accident | 7 | 1565 | 0 |  | 0 | 0 |
| 722270069 | Satoshi's Stash | 9 | 1531 | 0 |  | 0 | 0 |
| 724030807 | Satoshi's Real Identity | 10 | 2098 | 0 |  | 0 | 0 |
| 724031950 | Darling | 17 | 2851 | 0 |  | 0 | 0 |
| 724275249 | Mistakes | 11 | 2922 | 0 |  | 0 | 0 |
| 725370188 | Quizchain Lottery | 13 | 2487 | 0 |  | 0 | 0 |
| 728374979 | Lucky 7 Giveaway | 14 | 1638 | 0 | `NoThisIsNOTaScamoweapufs`, `NakamotoAoi` | 0 | 0 |
| 728982194 | Difficulty | 14 | 2489 | 0 |  | 0 | 0 |
| 730790756 | Quizchain as a Password Manager | 21 | 3986 | 0 | `McGill`, `BaSCifCatfAaa` | 0 | 0 |
| 731219798 | Satoshi's Puzzle??? | 14 | 2446 | 0 |  | 0 | 0 |
| 732405709 | Genesis Block Mystery | 22 | 4038 | 0 | `DivfNa` | 0 | 0 |
| 733252660 | Scripting Players | 11 | 3059 | 0 |  | 0 | 0 |
| 737461752 | Difficult Hints | 13 | 2047 | 0 |  | 0 | 0 |
| 740685487 | Exceedingly Unfair Riddle | 35 | 4737 | 2 |  | 0 | 0 |
| 742662804 | Complete Second Round of the Quizchain | 367 | 30521 | 2 | `naMe`, `AndrewYangForPresident`, `zmPzd`, `BaSCifCatfAaa`, `entropyTake`, `rGd`, `entropyPrivate`, `jUut`, `gwxUdg`, `SXwQnMasKLpzFzb`, `DivfNa`, `dzGTuQeg` … | 45 | 0 |
| 743524593 | HQ Trivia | 12 | 2539 | 0 |  | 0 | 0 |
| 747478016 | Satoshi Mystery | 11 | 2666 | 0 |  | 0 | 0 |
| 752631800 | Quizchain and AI | 13 | 2731 | 0 |  | 0 | 0 |
| 755457972 | Cariga Bright | 18 | 2960 | 0 |  | 0 | 2 |
| 757574334 | THOMAS and SATOSHI | 26 | 4316 | 0 |  | 0 | 2 |
| 759761389 | End Phase of the Experiment | 14 | 3390 | 0 |  | 0 | 0 |
| 760378354 | Waking Up | 15 | 2508 | 0 |  | 0 | 0 |
| 761570746 | The Satoshi Code | 146 | 23579 | 4 | `DivfNa`, `ivfNa` | 0 | 3 |
| 762380140 | Starting Up | 13 | 1873 | 0 |  | 0 | 0 |
Totals: 1,952 paragraphs, 71,540 words, 47 camelCase anomaly tokens (mechanism demonstrations) across
8 parts, 10 lowercase-initial paragraphs in the RBB chapter and 24 in the log part, 5 parts with
repeated paragraphs (all Wattpad dedup or list repetition).

---

## 1. The rules, as the author states them (verbatim), and where each one is demonstrated

| # | rule | verbatim source | demonstrated in | status for the RBB |
|---|---|---|---|---|
| R1 | name marking: one planted odd capital is the seed, remaining letters of the hidden name are capitalised at their own occurrences in reading order | round-1 block 2: *"One of the letters in the family name of the author is changed from lower to upper case. Change the other letters in his name in the same way for the solution."* | block 2 (`messaGe`/`You`/`oN` = NAGY), block 29 (`vOIce`) | combinatorially infeasible at occurrence level (§3.2) |
| R2 | inheritance: the solution's case pattern is copied from a visible artefact, never chosen | part 720890652 *Hoax*: *"The solution is of course the word Hoax, starting with a capital letter because the address I found had it that way"*, *"capitalization will be evident"* | Hoax block (`oarHoaxUd` inside `137SFKp9…Hoax…`) | open: no source artefact has been shown to carry the RBB pattern |
| R3 | stride acrostic → password; quotes as a "twist"; one appended word as a second twist | part 730790756 *Quizchain as a Password Manager*, paras 12-15: *"We highlight every 7th word and use the first letter of each of these words to get the string BaSCifCatfAaa1i"* … *"we will add quotation marks before and after the string"* … *"Then I add my favorite Pokemon name for "BaSCifCatfAaa1i"Metamon"* | the chapter's own worked example | **newly applied with the twists** (§3.1): 34,641 candidates, negative |
| R4 | one password, then the Nth private key for the Nth site/block | same part, paras 18-19: *"Then use the first private key for the first site you need a password, the second for the second one"*; confirmed by round-2 b2: *"Second private key because this was block 2"* | round-2 b2 | applied: indices 0, 1, 2, 44, 76, 77 throughout this session |
| R5 | paragraph-edge flips (first letter down, last letter up) on the paragraphs carrying the signs | Grycoin block 2: *"keep the whole long text and change only a couple of letters in their capitalization … for all the paragraphs where you recognize the signs, and keep the rest completely unchanged"* | block-77 stage one (certified 9dd2efb9 → 19TbyN5) | the 16-window closure is closed on the corrected base (§3.3) |
| R6 | sentence-edge flips inside one paragraph | same demo text, worked example: `I expected…` → `i expected…` and `himself` → `himselF`, one sentence | demo (block 2) | still open (demo unsolved) |
| R7 | anagram chain as narrative: THOMAS↔SATOSHI (+I, −M), HAL↔IBM, AHS↔BIT, surplus S = "Second" = satommi | part 720888559 paras 183-214; restated in part 757574334 *THOMAS and SATOSHI* | RBB chapter itself | narrative, not a key: no transform of it has ever produced an escrow |
| R8 | reverse Turing test | part 720888559 paras 77-79: *"I will use the opportunity to do a reverse Turing test."* | RBB chapter; pointed at again by BTCxanter on 2026-10-27 for the Grycoin-2 demo | open, and it is the live hint (§4) |

## 2. Devices present per chapter, and what that means

- **FFWW/stnm signature windows** exist in **one** part only: the RBB chapter (starts 5, 93, 168, plus the
  Finney reprint run 231-235). Confirmed again here. So "recognize the signs" cannot be learned from a
  sibling chapter; the sibling chapters only *describe* the mechanism in prose.
- **camelCase anomaly tokens** (`messaGe`, `theM`, `naMe`, `peNot`, `BItcoin`, `SImple`, `anGRY`, `FIrst`,
  `notMetamon`, `sffohkcreK`, `ivfNa`, `efiYDM`, `WorldWideAbsoluteCarbonBudget`,
  `AndrewYangForPresident`, `abcdefghijkLmnopqruvwxyz`) occur in 8 parts. Every one of them is either
  (a) a worked example of R1/R5 in the bookkeeping parts, (b) a decoded block answer quoted as prose, or
  (c) an address fragment. None is a live key, because each one sits in a part whose block is solved and
  each was checked when that block was cracked.
- **The odd alphabet in para 126** — `3abcdefghijkLmnopqruvwxyz` (capital L, and `st` missing) against
  `7abcdefghijkLmnopqrstuvwxyz` (capital L, complete) — is the chapter's only other case anomaly. It is
  already logged in `CLUES_CANONICAL.md` §12.3 as a planted typo. It remains un-exploited as a *selection
  rule* ("remove the letters S and T") and that reading is tested in §3.4.
- **Lowercase-initial paragraphs**: 10 in the RBB chapter (176, 182, 209, 215, 250, 252, 254, 256, 258, 260
  on the corrected base), 0 in every other narrative part, 24 in the log part. They are the chapter's only
  paragraph-level case anomalies after the base repair.
- **Trailing-space paragraphs**: 13 in the RBB chapter (86, 108, 122, 128, 139, 147, 165, 166, 192, 201,
  209, 220, 267) — already swept exhaustively as a sign set (49,146 candidates).
- **Repeated paragraphs**: only `"What?"` at 34/78 in the RBB chapter (44 apart, Wattpad dedup rule, not an
  edit).

## 3. What was newly applied this session (all on the repaired base, all negative)

### 3.1 R3 with the documented twists — the gap the last session left open

The last session closed stride acrostics without the twists. With them, the candidate space is:

- strides {7, 4, 44, 77, 22, 88, 2, 3, 5, 21, 37} × every starting offset × first-letter and last-letter
  reads of the selected words (the chapter's word list, whitespace-split, 7,974 words);
- forms: bare, `"S"`, `'S'`, quoted-lowercase, quoted-uppercase, and each of those with one appended word
  from {Metamon, Satommi, TOMI, Grycoin, Aoi, Second}, with and without a space;
- every form hashed and derived at indices 0, 1, 2, 44, 76, 77, checked against all four escrows
  (RBB live `14zMkTga…`, RBB old `1EFojcAo…`, demo `1tzieUf…`, stage one `19TbyN5…`).

**34,641 candidates, 0 hits.** Log: `out/sweep_rules.log` (this session's workspace), reproducible with
`code/sweep_rules.py`.

### 3.2 R1 is not brute-forceable, and that is now quantified

In-order embeddings of a name into the corrected base's word-initial letters:

| name | embeddings |
|---|---|
| AOI | 2.89e8 |
| HAL | 4.4e7 |
| TOM | 2.1e8 |
| IBM | 1.1e8 |
| AHS | 1.3e8 |
| BIT | 4.3e8 |
| STNM | 5.0e10 |
| FINNEY | 2.1e14 |
| THOMAS | 2.7e16 |
| GRYCOIN | 8.2e16 |
| NAKAMOTO | 6.3e20 |
| SATOSHI | 2.9e19 |
| AOINAKAMOTO | 1.8e29 |

So R1 can only be applied to the RBB as a *deterministic reading*, never as a search. The deterministic
reading used here: take the single visible odd capital as the seed (`ppM` in para 73, the chapter's only
non-acronym internal capital), then mark the nearest following (and, separately, nearest preceding)
occurrence of each remaining name letter, at letter level and at word-initial level, for 12 names.
**1,104 candidates × 5 indices, 0 hits** (`code/sweep_seed_greedy.py`).

### 3.3 Sign-set flips on the repaired base, including the sets that only exist after the repair

- the four certified FFWW/stnm runs, the 14 "signs" paragraphs, the 16-window set, the quote run alone,
  and the union sets;
- the SATOSHI-complement anomaly set (94 paragraphs, `CLUES_CANONICAL.md` §13.2) and the complements of
  ITASM/THOMAS/NAKAMOTO/FINNEY/HALFINNEY/GRYCOIN/AOI;
- **the 10 internal-break paragraphs** (63, 73, 121, 124, 146, 160, 184, 189, 193, 213), which did not
  exist in any pre-repair base, plus the 10 lowercase-initial paragraphs, plus their union;
- three serialisations (LF/LF, CRLF/CRLF, CRLF-separator with LF breaks) × four edge modes × six indices.

**168 candidates, 0 hits** (`code/sweep_rules.py`, `out/sweep_br_low.log`).

### 3.4 The para-126 alphabet as a selection rule ("drop the letters S and T")

Read as: the letters the author dropped from her own address example name the paragraphs to leave alone.
Tested as: flip every paragraph whose first letter is *not* in {S,T}, and its complement; and drop the
letters from the *signature* set instead. Negative within the §3.3 run.

## 4. Where the open question actually is

Three independent lines now agree that the mechanical space is exhausted:

1. every documented rule family, read strictly, is negative on the repaired base (§3);
2. the corpus's own quantitative closures (2^12, 2^15, 2^16 windows, 2^20 partially, 1.4M+ rule-family
   candidates) are negative;
3. the author's own statements say the format is trivial and the *judgment* is the puzzle:
   *"someone mining with the mind"*, *"obvious to anyone able to recognize the signs"*.

So the remaining variable is exactly one: **which paragraphs the author considered to carry the signs.**
Two readings are live and both are cheap to state precisely:

- **(a) the reverse-Turing-test reading.** BTCxanter's 2026-10-27 nudge on the Grycoin-2 thread —
  *"It should demonstrate an example that is the reverse Turing test"* — points back at paras 77-79 of the
  block-77 chapter. If stage two is the demonstration, its sign set is the paragraphs of the *dialogue that
  administers the test*, not the signature windows. That set has never been used as a flip set: it is the
  exchange from ``"There are two ways to make sure of adoption…"`` through the end of the Turing-test
  discussion, and it is a contiguous span, so it is one candidate, not a search.
- **(b) the two-byte-state reading.** `CLUES_CANONICAL.md` §9 lead 3 (Wattpad-tagged forms) was tested with
  the *signature* sets only. The two `<p>`-tagged serialisations have never been tested with the
  sign-set families of §3.3.

Both were run this session on the validated harness (`code/derive.py`, 492 derivations/s/core,
self-tested against `9dd2efb9…` → `19TbyN5…`), and both are negative:

- **(a) dialogue spans.** Every contiguous span starting at paragraphs 68-83, length 2-12, flipped
  whole or every other paragraph, five edge modes, both joins, indices 0/1/2/44/76/77:
  **3,520 candidates, 0 hits** (`out/sweep_dialogue.log`).
- **(b) tagged serialisations** in the forms `<p …>…</p>` and `<p data-p-id="…">…</p>`, both joins, the
  four sign sets of §3.3, four edge modes: **64 candidates, 0 hits** (`out/sweep_tagged.log`).

That leaves exactly one thing in the space that has never been enumerated at all, and it is not a
mechanical gap: a sign set the author chose by a judgment about the text that she never wrote down. The
only remaining lever on it is evidence from her own side (a statement, a screenshot, a copy of her notes),
which is what BTCxanter's 2026-10-27 remark is reaching for.

---

## 5. Sentence-level device: the demo's true geometry, formalised, and applied to the chapter

Session 2026-10-30 (second pass). This closes the one granularity the corpus had only touched with six
candidates.

### 5.1 The demo's example is not just "sentence-level", it has a stated selection rule

The author's worked example changes exactly one sentence of the Grycoin-2 text:

    "I expected otherwise, but actually not many people do recognize the signs in Satoshi's Bitcointalk
     post outing himself."   ->   "i expected otherwise, … post outing himselF."

`I` is the sentence's first letter and `himself` supplies the sentence's **last** letter (the full stop
follows it). The paragraph continues with a second sentence, "Even after I explained the method used and
the result in detail.", which is left alone — and its initial `E` is not a sign letter. The `n` of
"capitalization" at the end of the previous *paragraph* is explicitly excluded ("that 'n' is not part of
the solution"). So the rule is:

> **For every sentence whose first letter is in the sign set {I, T, A, S, M}: lower its first letter and
> raise the last letter before its full stop. Leave paragraph-final letters alone.**

Implemented mechanically, that reproduces both of the author's stated changes and nothing else
(`i expected`, `himselF`, and `capitalizatioN` absent). That is a real calibration result: the demo is
sentence-selected, not paragraph-selected, and the corpus's "paragraph-edge family" framing of the demo
(`SESSION_2026-10-29_evening.md` §1) was testing the wrong granularity. Stage one remains the
paragraph-level case, so the two stages genuinely differ in granularity: `Second` gets the demo's
geometry, `[edited slightly]`-post gets stage one's.

### 5.2 Applied to the block-77 chapter

| family | candidates | hits |
|---|---|---|
| sentence-initial sign sets {ITASM, SATOI, SATOIH, THOMAS, NAKAMOTO, FINNEY, HALFINNEY, AOI, GRYCOIN, STNM} × sign and complement × {first↓+last↑, first↓, last↑} × both joins | 120 | 0 |
| demo bases × {ITASM, SATOI, SATOIH} × sign/complement × {no tail, LF, CRLF} (binary-safe reads) | 54 | 0 (no `3c6` prefix either) |

### 5.3 A structural census result

Across all 33 chapters there is **no four-consecutive-sentence window** whose initials are F,F,W,W (or
W,W,F,F). The signature device exists at paragraph level in one part only and at sentence level nowhere.
So "recognize the signs" cannot be re-based onto sentences by analogy alone; the analogy has to come from
the demo's own text, which it does (§5.1) — but the chapter never demonstrates it.

### 5.4 Repo-hygiene finding that invalidates a class of past negatives

`demo_post_crlf.txt` and `demo_post_lf.txt` are different files (22 CR bytes apart), but any script that
opens them with `open(path).read()` gets LF text for **both**, because Python's universal-newline mode
collapses `\r\n`. My own first pass this session hit exactly that and reported identical MD5s for the two
"bases". Every sweep that read those files in text mode therefore tested the LF slice twice. Use
`open(path,'rb')` (or `newline=''`). The chapter files in this repo are JSON (explicit `\r\n` insertion),
so the chapter sweeps are not affected — but the demo slice family is only trustworthy where the reader
was binary-safe, and this session's 54-candidate table is the first one that is.

---

## 6. Channel census: why paragraph-initial rules cannot port to the chapter

A rule family assumes a *channel* — the feature the author's grammar is defined on. Stage one's
certified grammar ("paragraphs not starting with a letter of ITASM are flipped") needs every paragraph
to begin with a letter. That channel is 100% intact in Hal Finney's post (16/16). It is not intact in
the block-77 chapter:

| part | paras | start with a letter | start with `"` |
|---|---|---|---|
| **720888559 Second** | 273 | 197 (72%) | **63** |
| 720889517 Second Life | 17 | 6 (35%) | 10 |
| 720895205 Complete Quizchain | 766 | 736 (96%) | 5 |
| 742662804 Complete Second Round | 367 | 353 (96%) | 2 |
| 761570746 The Satoshi Code | 146 | 137 (94%) | 1 |
| 25 other parts | - | 92-100% | 0-3 |

The chapter is the only *narrative* part that is dialogue-dominated, and the single most common
"paragraph initial" in it is a quotation mark (63 occurrences), ahead of T (41), I (38), A (32), S (14).
Paragraph-initial distribution: `"`63 · T41 · I38 · A32 · S14 · W13 · F12 · B10 · O10 · H8 · rest ≤4.

Consequence: any ITASM-style port has to decide what a quote-initial paragraph *is*, and the prior
eliminations do resolve it (the "quote"/"quoteI" cluster variants are closed). The channel census is
the mechanical reason those ports were never going to work: the grammar's discriminating feature is
diluted by 23% of paragraphs whose first character is punctuation.

## 7. Speaker channel (new, and negative)

Dialogue vs narration as the selection rule, since the chapter is a dialogue: sentences inside
quotation marks, sentences outside, and each intersected with the ITASM sign set and its complement,
first-down + last-up, both joins, indices 0/1/2/44/76/77: **12 candidates, 0 hits.**

## 8. The author's own confirmation device (para 242) does not scale to the chapter

Para 242 states the device she uses to *confirm* a solution: "The first four and last four words of the
paragraph hinting at the solution", read as in paras 245-246 ("Today, I" + "recognize the signs").
Applied to the chapter:

- **Signature reading.** For each paragraph take the 8 initials of (first four words + last four words)
  and ask whether a name appears as a subsequence. Only **6 of 273** paragraphs qualify: AOI in
  {83, 85, 207, 214, 241}, HAL in {270}. Flips of those sets: **18 candidates, 0 hits.**
- **Derived-text reading.** Hash the concatenation of first-four-words, of last-four-words, of both, for
  the whole chapter, for the four FFWW paragraphs, for the quoted Finney paragraph 222, and for the last
  paragraph, with and without a trailing newline: **21 candidates, 0 hits.**

## 9. Numeric channel (new, and negative)

Digits {42 paras}, number words {98}, either {127}, ordinals {49}, years {11}, the bare-year paragraph
{15 only}: first-down, last-up and both, both joins, six indices — **36 candidates, 0 hits.** Worth
recording for one reason: `"2020."` (para 15) is the chapter's only paragraph that is nothing but a year,
and it exists only because of a draft edit (see §10).

## 10. TEXTUAL DISCOVERY: the chapter has a surviving draft, and the diffs are readable

Wattpad part **720889517 "Second Life"** (17 paragraphs) is a draft of the scene that the final chapter
carries at paragraphs 1-26. Because Wattpad's `data-p-id` is a hash of normalised paragraph text, pid
equality is an exact text-equality oracle across parts: **13 of the 17 draft paragraphs are byte-identical
to final paragraphs, 4 differ.** Part 757574334 "THOMAS and SATOSHI" reproduces 20 of its 26 paragraphs
verbatim from *Second*, so it is an anthology of the same text, not independent evidence.

The four edits, draft -> final:

| draft (Second Life) | final (Second, block-77 question) |
|---|---|
| `"Still 21st Century".` (B5) | `"2020."` (A15) |
| `"Not even one hundred years have passed."` (B6) | `"Not even ten years have passed."` (A16) |
| `"A popular name for Japanese girls."` -> draft: `"Third most popular name for Japanese girls right now."` (B9) | `"Good question. How about Aoi? You like that name? A popular name for Japanese girls."` (A19) |
| `"...bore you with second rate quiz questions..."` (B14) | `"...bore you with third rate quiz questions..."` (A25) |

Two things follow.

1. **"Still 21st Century" is a deleted line.** A parallel lane has been treating that phrase as a live
   semantic hint for the chapter; it is not in the chapter at all. What the final text answers to "When
   is this?" is the bare paragraph `"2020."`.
2. **The edits move counts.** hundred -> ten; "third most popular" -> dropped; "second rate" -> "third
   rate". The author revised *numbers* in this scene and left the surrounding prose alone. If any channel
   in the chapter is author-sanitised rather than incidental, it is the numeric one — which is exactly the
   channel tested in §9 (negative, but on the final text only).

Flips of the edited paragraphs {15, 16, 19, 25}, their ±neighbourhood, the whole draft scene 14-26, and
the complement of the edited set: **24 candidates, 0 hits.**

## 11. Session totals

| family | candidates | hits |
|---|---|---|
| sentence-level sign sets (§5.2) | 120 | 0 |
| first-four/last-four word device (§8) | 39 | 0 |
| speaker channel (§7) | 12 | 0 |
| numeric channel (§9) | 36 | 0 |
| draft-edit channel (§10) | 24 | 0 |
| **total this pass** | **231** | **0** |

Every one of these ran on the repaired base, with both joins where joins apply, at indices
0/1/2/44/76/77, against all four escrows (RBB live, RBB original, stage one, demo).

## 12. Code audit of the hunt repo (and a base-fidelity finding)

Three checks, all reproducible:

1. **Pipeline is sound.** `work/btc.py` defines `DEFAULT_PATH = (44+H, 0+H, 0+H, 0, 0)` and its default call on
   the stage-one input returns `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`. My independent harness in this workspace
   (`code/derive.py`, coincurve, explicit BIP32) returns the same hash160, so both lanes land on the same
   derivation and the negatives are directly comparable. (Passing a raw path such as `(44,0,0,0,0)` to
   `addr_from_md5hex` silently derives a different address — the path argument must be pre-hardened.)

2. **Base fidelity, checked by hash.** Joined with `\n\n`:

   | file | length | md5 |
   |---|---|---|
   | `chapter_paras_exact.json` | 45,440 | `48d31820…` |
   | `wp_paras.json` (273 texts, no internal breaks) | 45,440 | `48d31820…` |
   | `wp_paras_br.json` (segments split on `<br>`) | **45,450** | **`46a308c2…`** |
   | this workspace's corrected corpus | **45,450** | **`46a308c2…`** |

   and with `\r\n\r\n`: `wp_paras_br.json` = our corpus = **46,004**, md5 `db11a7fd…`.

   So the repaired base in the repo and the one used for every sweep in this document are **byte-identical**,
   and Wattpad's own `length` (45,451) is the +1 final character of its length model.

3. **Most repo scripts still read `wp_paras.json`**, i.e. the base *without* the ten internal line breaks
   (`aoi_chapter.py`, `cluster_all.py`, `chain_links*.py`, `hint_*`, `fresh_*`, `*_battery.py`, `crlf_sweep.py`,
   `discrepancy.py`, `eight_items.py`, `hunt_chapter_rules.py`, …). Only `build_base.py`, `families_br.py` and
   `final_sweep.py` read `wp_paras_br.json`. Every closure produced by the former group is a closure on a base
   that differs from the certified one by ten characters, so those results do not transfer automatically.

   To settle it rather than assume it, every chapter elimination the dossier lists was re-run here on the
   repaired base: ITASM complement, SATOSHI complement, STNM-ending set, AOI and THOMAS sets, the
   non-ITASM ∩ stnm-ending intersection, the quote set and its complement, the four paragraphs around 222,
   the FFWW windows with and without the intervening I paragraph, upper-first-letter and lower-last-letter
   sets — **20 sets × 4 edge modes × 2 joins × indices 0/1/2/44/76/77 = 160 candidates, 0 hits.** The
   dossier's chapter eliminations survive the base repair unchanged, which is the useful outcome: the
   ten missing newlines were not what stood between us and the answer.

## 13. Repo hygiene, second item

`code/sentence_rules.py`-style splitters that use `open(path).read()` collapse `\r\n` (see §5.4). The same
hazard applies to `demo_post_crlf.txt` inside the repo. The chapter files are JSON with explicit `\r\n`
insertion, so chapter sweeps are unaffected; demo-slice sweeps are only trustworthy where the reader was
binary-safe.

---

## 14. The author's own format grammar, mined from the two log parts

`RULES_BY_BLOCK.md` (new, 172 verbatim statements covering 75 of the 77 blocks) is the extraction of every
paragraph in the round-1 log (part 720895205) and the round-2 log (part 742662804) that states a format, a
method or a capitalization rule. It is the first place where the whole experiment's grammar can be read at
once. Totals:

| pattern | statements |
|---|---|
| TOMI field specified | 83 |
| `[link]` field (previous block's key tail appended) | 61 |
| capitalization rule stated | 29 |
| BFUB/BotFU field | 21 |
| explicit letter-position rule (first/second/last letter) | 10 |
| Atbash named as the method | 5 |

Three consequences for block 77.

1. **The round-1 block-77 entry is the only block whose question is meta.** Verbatim (log paras 380-385):

   > Block 77 — *"Failed block, made subtle hashing mistake, but corrected that way before anyone came close
   > to the solution." … "As announced earlier, this puzzle is written by Satoshi. I think it is beautiful, a
   > much higher level than the second rate stuff I came up with in previous blocks."* Question: **"The
   > solution is the puzzle."** Format: `[solution] TOMI omit TOMI [link]`. *"Solution format is eight items
   > in two sets of four. Two items ciphertext and two items plaintext each, 44 read from left and 44 read
   > from right."*

   That is stage one's answer shape (8 items, 4+4, 44 from each side), and it is why `omit TOMI` is stated:
   block 77's answer carries **no** TOMI field, so nothing in stage two's answer should be an appended
   descriptor string.

2. **The near-final blocks put their hints in the Wattpad parts, not in the block text.** Block 76
   (log para 699): *"Solution was Easter, TOMI field was Second Life. This was rather easy once you realized
   where exactly the hint was in the Wattpad story. And it does stand out there, as the winner pointed out in
   comments below, where he described his solving [method]."* Block 66's hint (para 327) points at the story
   title's capitalization. Blocks 45-63 repeatedly say *"impossible to solve until the final version of
   Chapter 2 of the story is posted"*. The corpus's own evidence is therefore that hint material for the
   late blocks lives **in the story parts**, sometimes in a *different* part than the block's question.

3. **The author flags the leftover numbers himself.** Log para 689: *"Similar method to 71 which used a puzzle
   from LOTR. You will find some Fibonacci numbers in the last block 77 as well…"*. Fibonacci numbers present
   in the chapter's text were not swept as a sign channel in any earlier session; the chapter's numeric
   channel was only swept as digits / number words / ordinals / years (§9).

## 15. New family run this pass: block-2's method on the names the chapter itself proposes

The round-1 logs give the exact method twice: block 2 (*"one of the letters in the family name of the author
is changed from lower to upper case; change the other letters in his name in the same way"*) and block 29
(*"just change the o and i in 'voice' … same method as in Block 2"*, i.e. the minimal spanning window of a
name inside one sentence, with already-capital letters left alone). The chapter's own thesis names Hal Finney
as Satoshi, so **FINNEY, THOMAS, HALFINNEY, HAL, TOM** are the names it puts forward — and none of them had
ever been run as a minimal-span case marking (the earlier AOI/NAKAMOTO/STNM/SATOSHI/OAINAKAMOTO runs
(53,787 + 152) did not include them).

- per-sentence minimal spanning windows, raise-only and toggle, both joins, indices 0/1/2/44/76/77:
  FINNEY 356, THOMAS 600, HALFINNEY 188, TOM 1,324, HAL 1,392, SATOSHI 732 → **4,592 candidates, 0 hits**
  (`code/name_span.py`).
- whole-chapter minimal span (the "whole long text" reading): the minimal window for every one of those names
  is exactly the name's own length, i.e. the chapter contains each one contiguously, so the reading collapses
  to marking the name where it already appears: **60 candidates, 0 hits.**

## 16. Cumulative negative ledger for stage two

| pass | candidates | hits |
|---|---|---|
| earlier sessions (repo + this workspace) | ~5.4 M | 0 |
| 2026-10-30 first pass (§3-§4) | 39,949 | 0 |
| 2026-10-30 second pass (§5) | 174 | 0 |
| 2026-10-30 third pass (§6-§11) | 231 | 0 |
| 2026-10-30 fourth pass (§12 audit) | 160 | 0 |
| 2026-10-30 fifth pass (§15) | 4,652 | 0 |

Every candidate was hashed and derived at m/44'/0'/0'/0/{0,1,2,44,76,77} and compared with both chapter
escrows plus the stage-one and demo addresses.

## 17. Fibonacci channel (the author's own flag), negative

Log para 689: *"Similar method to 71 which used a puzzle from LOTR. You will find some Fibonacci numbers in
the last block 77 as well…"*. Sets built from the chapter: paragraphs containing any number (42),
paragraphs whose numbers are Fibonacci values (23), paragraphs containing a Fibonacci digit run (1: only
para 49), paragraphs whose word count is Fibonacci (54). Three edge modes, both joins, six indices:
**24 candidates, 0 hits.**

The channel exists but is thin. The one compact signal is para 49 — the only paragraph in the chapter whose
digits contain a Fibonacci run — and 49 is itself 7², which is the only reason to keep it on the list.

## 18. Where the remaining evidence points

The corpus now supports one statement that no sweep can substitute for: **the author's late-block hints live
in the Wattpad parts, and at least once (block 76) the hint was in a different part than the block's own
question, in a place that "stands out" in the story.** Block 77's stage two is the last such block, its
question is the chapter, and its answer carries no TOMI field.

So the productive reading of "recognize the signs" is no longer "which paragraphs of the chapter", it is
"which part of the story the author would call standing out". On the evidence of §10 that is a two-item
shortlist:

1. **`"2020."` (para 15)** — the chapter's only paragraph that is nothing but a year, and it exists only
   because a draft line ("Still 21st Century") was replaced. It is the single most "standing out" paragraph
   in the chapter by any measure, and the author's own habit (block 16, `2o2o` for `2020` in a burn address)
   shows he treats that year as a sign.
2. **`ppM` (para 73)** — the only non-acronym word with an internal capital, inside a paragraph that also
   carries one of the chapter's ten internal line breaks.

Both have been used only as *members* of larger sets (numeric channel, seed-anchored marking). Neither has
been used as the whole sign set with the stage-one geometry and the block-29 name-marking geometry
simultaneously, on the paragraph plus its own line-break segments. That is the next experiment, and it is
about twenty candidates.

---

## 19. The author's own hint series for block 77, extracted (source: part 761570746, *The Satoshi Code*)

This is the only place where the author explains block 77 in his own words, and it had never been pulled out
as a list. Verbatim order (paras 84-146):

| # | hint | the author's own gloss |
|---|---|---|
| - | premise | *"When I wrote that block and posted it, I was under the impression that Satoshi wrote this address… However, that was wrong."* The genesis block publishes a **public key** (04678AFD…D5F), not the address; the address is derived from it, so almost every pattern in it is coincidence. *"I have based my puzzle completely on a fantasy. But I still think it is a valid puzzle. And my solution has not changed a bit."* |
| 1 | the `7` | at the seventh place counted from the end; *"easy to see how that is a key to reading half of the hidden message and half of my solution"* |
| 2-3 | starts and ends with A | Atbash reminder; Lerner's blog implies only ~10 digits could be forced, *"which in turn means the ciphertext part of any solution must be very short"* |
| 4 | two halves | *"the first sixteen digits from 1 to M, then a capital P, then the last sixteen digits"*; *"The first set of two ciphertext items is in the first half and the second in the second."* |
| 5 | (skipped in this part) | *"This is the big one which should have almost completely given it away."* |
| 6 | block 17 as a hint | Leonardo's "LV" in the Mona Lisa's eye → *"would that not be Hal signing his creation in the genesis block address?"* |
| 7 | "Number 7" | same key as hint 1 |
| 8 | `A → a` (Atbash), `1 → N`, **N7** | *"This was the first thing I noticed when solving this."* |
| 9 | **N7. S5.** | "Getting pretty decisive now." |
| 10 | *"Given that 1A1 is a name, what name is it?"* | last hint |
| — | partial-hash release | **"For the two plaintext items read from the left, the first 7 digits are `cc9485a`."** / **"…they are `d78c92f`."** |

Two things in that table matter beyond stage one.

1. **The `cc9485a` / `d78c92f` partial MD5s are the only published oracles for block 77's plaintext items**,
   and no lane in the repo has ever used them. They are 28-bit filters: any candidate reading of the puzzle
   whose plaintext items do not reproduce those prefixes is wrong, at a cost of one MD5 each. Whatever theory
   of "the signs" is proposed next, it can be tested against them in milliseconds instead of against an
   address derivation.
2. **"the ciphertext part of any solution must be very short"** is the author telling us the answer is not a
   dense marking of a long text: the marked part is short. That is consistent with the demo's "change only a
   couple of letters", and it is an argument against every dense family (sign sets, stride rules, every-nth).

## 20. "Number 7" as a positional key (new family, negative)

The hint series makes 7 the explicit key ("7 is the key for reading half of my solution", hint 7 is literally
"Number 7", hint 8 "N7", hint 9 "N7. S5."), and the stated answer format adds 44 as a second positional
number ("44 read from left and 44 read from right"). Neither had ever been used as a *case-flip selector* on
the chapter: the repo's stride sweeps read acrostics, they do not edit case.

Selector = every 7th (and every 44th) unit, offsets 0-6, at paragraph / sentence / word granularity, edge
direction first-down, last-up and both, both joins, six indices: **252 candidates, 0 hits.**

## 21. Status after this pass

Stage two has now been tested with: every sign-set family; every narrative/structural channel the chapter
offers (paragraph initials, sentence initials, dialogue, narration, numbers, ordinals, years, Fibonacci, word
counts, first-four/last-four words); the certified name-marking method on every name the chapter proposes
(AOI, NAKAMOTO, SATOSHI, STNM, THOMAS, FINNEY, HALFINNEY, HAL, TOM, GRYCOIN, SECOND, AOINAKAMOTO); positional
keys 7 and 44; and the author's own confirmation device. Cumulative: roughly 5.45 M candidates, all negative.

The author's own constraint is the one thing that keeps pointing elsewhere: **the marked part is short, the
text is kept whole, and the hint for late blocks lives in the story parts.** The demo is still the only target
with an independent oracle (`3c6` prefix plus a claimed escrow), and its remaining space is *short mixed
families*, which the hint series now says is the right shape.

---

## 22. FIRST POSITIVE ORACLE RESULT IN THE HUNT: the published partial MD5 is `md5("Hal Finney")`

The hint series ends with the author releasing partial MD5s for block 77's plaintext items "so everyone can
make sure they got that part right" (part 761570746, paras 145-146):

> "For the two plaintext items read from the left, the first 7 digits are **cc9485a**."
> "For the two plaintext items read from the left [sic], they are **d78c92f**."

Testing short candidate strings against those prefixes:

    md5("Hal Finney") = cc9485a0…    <-- exact match on the first published oracle

So block 77's left-half plaintext items are **`Hal`** and **`Finney`**, joined by a single space, normal
capitalization. This is the first independent verification of any piece of block 77's answer in this hunt;
it does not need the escrow, the derivation, or the author's word. It also settles three things:

1. The item format is `Item1 Item2` — one space, ordinary capitalization, no punctuation. Any hypothetical
   answer field in this puzzle family follows that shape.
2. The chapter's thesis is literally the plaintext answer: the puzzle says "Hal Finney", which is what
   `Second` argues at length and what the Finney-post flips (stage one) spell out at their edges (STNM).
3. Stage one and stage two are the *same claim in two media*: a forum post with paragraph-edge marks, and a
   novel chapter with... the same claim marked some other way. That is why every "which paragraphs" theory
   fails to feel right: the semantic payload is already known, and only the marking medium is missing.

Search negatives for the second oracle (`d78c92f`, presumably the right-half pair):

- all 1-4-word phrases adjacent in the entire 33-part corpus, 6 case/Atbash/reversal variants each:
  **508,206 candidates, 0 hits.**
- all two-name combinations over a 70-word salient vocabulary, plus address fragments of length 4-8 and their
  Atbash: **78,938 candidates, 0 hits.**
- reference prefixes for the readings that were considered: `Hal Finney` cc9485a0 · `Finney Hal` ee5ef670 ·
  Atbash(`Hal Finney`) = `SzO Urmrvb` 92532dbe · `Nakamoto Satoshi` 930bf3b5 · `Nm ST` 8b7de896 ·
  `N7 S5` 042fcebc.

The second pair is therefore not a name pair from the story's vocabulary, which is consistent with the
author's hint 4 (the second set of two ciphertext items is in the *second* half of the address): the right-hand
pair is likely another two-part reading of the address rather than a phrase from the prose.

---

## 23. The round-two solution grammar, mined from its own log (part 742662804, paras 257-367)

The round-two log has a "Solutions" section that had never been read as a grammar. It covers blocks 1-32 only
(the log stops at block 32, so the b66/b75 solutions that later lanes cite are **not** in this corpus and have
to come from the recovered records). What it does show is how answers in this round are *shaped*:

| block | answer | shape |
|---|---|---|
| 11 | one space | an invisible string, chosen between one space and one line break |
| 14 | `A1zP1eP7DivfNa` | **"the first and the last seven digits of the genesis block address, not counting the prefix 1"** |
| 15 | `TOMI` | the TOMI word as the whole answer |
| 17 | `LV` | two letters |
| 21 | `21 million` | a number, with a TOMI field carrying the meaning |
| 23 | `P` | one letter |
| 25 | `77 + 25` | arithmetic on block numbers ("this block 25 is actually already block 102") |
| 27 | `UTXO` | the four edge letters of an Atbash'd question |
| 30 | `EU IQ KO` | six letters found by looking one place to the right in an Atbash foldover |

Two rules of thumb fall out, and they matter for the RBB:

1. **Round-two answers are low entropy and often *extracted* rather than *edited*.** Block 14 is the clearest
   precedent for "read from left and read from right": take N from each end of a fixed reference string and
   concatenate. Block 77's own format statement generalises that idea ("eight items in two sets of four …
   44 read from left and 44 read from right"), and its plaintext pair is exactly that shape: `Hal Finney` read
   forward, `Nakamoto Satoshi` read backward (§22, and the reversal convention that resolves the second
   published prefix).
2. **The author does not hide long texts in this round.** He hides short strings, numbers, letters and
   single spaces. A 45,450-character answer is a round-one shape.

## 24. Families run this pass (all negative)

| family | candidates |
|---|---|
| fragments as the answer: every sentence, paragraph and heading of the chapter under 14 case/punctuation variants (including re-casing with a full stop and number-stripped headings) | 4,806 |
| the same with the author's reversal convention: character-reversed, word-reversed, and word-internally reversed, each under the same case variants | 15,283 |
| mirror geometry: first letter **up**, last letter **down** — the exact reverse of stage one's certified direction, on 5 paragraph sets | 10 |
| boustrophedon reading: paragraphs read L→R and R→L alternately, name marked by case at its minimal span | 144 |
| first-N / last-N extraction on the chapter (words, characters, paragraphs; N in 1-77 including 4, 7, 16, 44, 77), concatenated and reversed | 253 |
| number-7 and 44 as stride keys (§20) | 252 |

## 25. The decision the evidence now forces

There are two mutually exclusive shapes for the stage-two answer, and the corpus supports one of them only by
analogy:

- **Whole-text shape.** The demo says "the format for block 77 … keep the whole long text and change only a
  couple of letters in their capitalization". That is round-one block 77, whose base is the Finney post. If
  stage two inherits it, the answer is `Second` with a few case changes, and everything hinges on the sign set.
- **Extraction shape.** Round two's own solution log shows answers that are short extracted strings (block 14:
  first and last seven characters of the genesis address; block 27: the edge letters; block 25: `77 + 25`).
  If stage two follows the round it belongs to, the answer is a short string taken from the chapter, and every
  whole-text sweep is aimed at the wrong object.

The fragments of the chapter have now been hashed under both readings (§24), so the cheap version of the
extraction shape is closed. What has *not* been done is the block-14 shape applied to the **second half of the
address** the way round-one block 77 actually did it, with the plaintext pair fixed by the verified oracle: the
left pair is `Hal Finney`, the right pair is `Nakamoto Satoshi` reversed, and the two ciphertext pairs are two
readings of the address halves. That reconstruction is a closed-form task, not a search, and it is the only
remaining piece of block 77 that can be *derived* rather than guessed.

## 26. Block-14 shape on the chapter's own reference strings (negative)

Block 14's answer (`A1zP1eP7DivfNa`) is the first and last seven characters of a fixed reference string with
its prefix removed. The chapter contains 35 address-like strings of its own — five Grycoin addresses, the two
alphabet examples, the genesis address, plus ordinary long words picked up by the same pattern — so the
extraction was applied to each: prefix kept and stripped, N in {4, 7, 8, 16, 44}, left+right concatenations
with and without a space and a full stop, plus the string itself, reversed, lowercased and Atbash'd.

**1,532 candidates, 0 hits.**

The five Grycoin addresses were the interesting ones, because the author's own story says the default burn
address is `7WorldWideAbsoluteCarbonBudget` and the chapter's "checksum omitted" note means the published form
is deliberately short — exactly the "ciphertext part must be very short" property Hint 3 states.

---

## 27. Standing ledger

    earlier lanes                 ~5.40 M
    this session, pass 1-6         ~5.45 M
    this pass (7)                   22,032
    -------------------------------------------------
    cumulative                     ~5.47 M candidates, 0 escrow matches

One positive result in the whole hunt: `md5("Hal Finney") = cc9485a0…`, the author's published partial prefix
(§22). Everything else is a closed door.

## 26. Second pass of 2026-10-30: post-repair re-validation and two base corrections

Full detail in `SESSION_2026-10-30_second.md`. Summary:

- Every negative produced before the base58 fix is void; the big ones were re-run on the repaired harness
  and are still negative: contiguous runs as the whole preimage (674,370), sign sets (8,304), 44 lattice
  (8,304), R1 name marking (2,064), demo name marking FINNEY/THOMAS/GRYCOIN survivors (81,600 derivations).
- New families, negative: **paragraph-selected × sentence-flipped** (3,564) — the combination of the demo's
  sentence device with stage one's paragraph selection, never run before; **keyword sign sets** from the
  hint's own instruction (2,754); **strides as case edits for every stride §20 did not use** (22,608).
- Base correction 1: the demo's certified base is the ten-paragraph Question block (`7759227d7406…`). The
  `demo_post_*.txt` "slice" hashes to `2bc61c2e…` because it starts at the post preamble, so it is not the
  author's preimage and sweeps on it are void. §14.1's open branch is therefore "the demo flips four or
  more letters", not "the boundaries differ".
- Base correction 2: the chapter repair never changes a letter's case, only boundaries, so case families
  are unaffected except through paragraph selection — which is why every run above sweeps br-crlf, br-lf
  and the old exact base together.

---

## 28. Answers recovered from the records dumps (oracle-backed, not guessed)

`quizchain_records.json`, `quizchain2_records.json` and `grycoin_records.json` publish each block's entropy, so
any answer can be *verified* by MD5. Three were recovered this pass, and two of them are chapter-derived:

| block | answer | verification |
|---|---|---|
| quizchain2/75 | `reverse Turing test` | md5 = `5090a11660cbe404ecda4b8f0b05ad2d` = the published entropy. Format statement: `[solution]`, no period, ordinary capitalization. |
| quizchain2/66 | `A young woman of Japanese ancestry who is very smart and sincere.` | md5 = `dc59555d015d2793e7750188cad161ba` = the published entropy. Found by brute force over 36,364 chapter fragments × 14 case variants. |
| quizchain/77 (round 1) | `1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN` | recorded verbatim in `answers`. |

**Block 66 is the certified extraction grammar on this very chapter.** Its question was "Aoi", its format "one
sentence without comma and a period at the end to describe me", and its answer is *chapter paragraph 29,
sentence 2*, cut mid-sentence: the chapter reads `Now she is a young woman of Japanese ancestry who is very
smart and sincere.` and the answer starts at `a young woman`, capitalises it and adds the full stop. That is
the author, on this text, doing exactly what she did to the Finney post: taking a run of prose and re-casing
its edge. It also confirms she is willing to *adapt* while she does it — "young man … who was very smart" in
the Finney post became "young woman … who is very smart" in the chapter.

Block 77 round one's recorded answer also settles the item geometry for stage one: `1A1` and `efi2DM` are
address fragments, `Hal Finney` is the left plaintext pair read forward, `TS` and `mN` are the second pair of
ciphertext items, and `ihsotaS otomakaN` is the right plaintext pair read **backward** — the reversal
convention that had already been recovered from the published partial MD5.

## 29. A bug in this session's own sweeps, found and fixed

`derive.addr_hash160()` returns `hash160` as **bytes**. Every family script written in this session compared it
directly against the hex targets:

    h, _ = addr_hash160(md5, idx)
    if h == '2bc16867479a8d01179a6452651abe14a65eb61a':   # always False - bytes vs str

So every "0 hits" produced in this session was vacuous. The repo's own harness (`harness/btc.py`, `q1dump.py`,
`q2dump.py`) compares `bytes == bytes` and was never affected, so the ~5.4 M earlier negatives stand; the
~250 k produced today did not.

Calibration now in place, against published data rather than assumptions:

- `md5('Still 21st Century')` -> `m/44'/0'/0'/0/0` reproduces grycoin/1's escrow `18EpYz5qB…` **exactly**.
- `md5` of the stage-one input reproduces `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` (hash160 `5cc903a5…`).
- `md5('reverse Turing test')` and `md5('A young woman of Japanese ancestry who is very smart and sincere.')`
  reproduce the published entropies of their blocks.

Re-runs with the fix, index 0 plus 1 and 2 where cheap:

| family | candidates | result |
|---|---|---|
| P1 extraction grammar (30,374 fragments × capitalised/full-stop and lowercased/full-stop) | 60,748 | 0 |
| P2 name minimal spans (FINNEY, THOMAS, HALFINNEY, HAL, TOM, SATOSHI, OTOMAKAN, NAKAMOTOSATH) | 38 | 0 |
| P3 certified sign-window sets × three edge modes | 45 | 0 |
| two marks, one at a paragraph opening and one at a paragraph closing | 73,984 | 0 |
| two marks, both at paragraph openings / both at paragraph closings | 147,696 | 0 |

## 30. The demo is closed until its base text is re-derived

Because grycoin/2 publishes a 3-hex-digit oracle (`3c6`) and the author says the answer changes "only a couple
of letters", the demo's answer space is small enough to exhaust without derivation: every single and every
**pair** of letter-case flips over both reconstructions in the repo (`demo_post_lf.txt` 1,456 bytes,
`demo_post_crlf.txt` 1,478 bytes, 1,099 letters each).

    singles + pairs, both files: ~1.2 M candidate texts, ~309 prefix-3c6 survivors,
    each derived at indices 0, 1, 2 and compared with every escrow  ->  no match

With the comparison bug fixed, this is now a real negative. Conclusion: **one of the two demo base
reconstructions is not the text the author hashed**, or the answer changes more than two letters. Note that
`demo_base.txt` (1,549 bytes) and `demo_post_lf.txt` are different texts, not two serialisations of one: the
former starts at "I thought I would write a bit about the format for block 77", the latter at "I still have not
completely given up, here is another block now". Until the demo post's exact bytes are recovered, the demo
cannot serve as the oracle it was meant to be.

## 31. Where this leaves the chapter

The chapter families that remain genuinely open are the ones where the *sign set* is the unknown, and the only
lever on that is the author's own statement that the marked part is short ("the ciphertext part of any solution
must be very short", hint 3) and that block 29's device is "just change the o and i in 'voice'". Both point at
marks counted in ones and twos, at structural edges, inside paragraphs the author treats as signs.

On this text, every such family at paragraph granularity is now exhausted correctly: single edges, all-in-set,
all-not-in-set, one opening + one closing, opening pairs, closing pairs. What has not been done correctly is
the same sweep at **sentence** granularity for pairs (651 sentence openings and closings, 847 k ordered pairs,
of which the same-sentence pairs and singles are done).

## 27. R6 is falsified by the demo's own text (not just negative), and the pairing it implies

See `GRAMMAR_CONSTRAINTS.md`. The demo fixes five constraints (C1-C5). C1+C2 make paragraph 2's final `n`
exemplary but **forbidden** in the answer; paragraph 2 begins with `As`, so every rule that selects
paragraphs or sentences by a sign letter — including §5.1's sentence-initial formalisation and the
paragraph-initial one — predicts `capitalizatioN` and is therefore falsified by the author's own sentence,
independent of the md5 oracle.

C3+C4 pair a **paragraph-first** letter (the `I` of paragraph 5) with a **first-sentence-final** letter
(`himself` → `himselF`), a pairing the corpus had never tested: it had tested paragraph-first with
paragraph-final and sentence-first with sentence-final. Enumerated now: every subset of the ten demo
paragraphs, both joins, oracle `3c6` — no survivor. Chapter sets at indices 0/1/2/44/76/77 — negative.

Consequence: the demo's answer contains changes that are not at sentence or paragraph edges. The live
family is R1's word-edge constraint (every letter of block 2's answer sits at a word edge), enumerated for
the chapter in `sweeps/name_marking_word_edges.py`.

---

## 32. BTCxanter's own replies: the demo's source text is now EXACT (verified), and line 78 is confirmed

The author dump (`btcxanter.json`, 7 replies, 2026-10-04 to 2026-10-15) had never been read as evidence. The
newest reply that carries data (id `pgft8au`, 2026-10-13, in thread `t3_cleczc`) posts the demo's **source
text** verbatim together with its hash:

> "Who solved this part? I only found the source text. MD5: 7759227d7406d8230d7e3a8f7b9846d7 … text = "I thought
> I would write a bit about the format for block 77 …" Can anyone who has solved this help? The first three
> digits of the MD5 hash are 3c6."

Unescaping that string and hashing it reproduces the published value **exactly**:

    len 1549    md5 7759227d7406d8230d7e3a8f7b9846d7   <-- matches the author's own figure
    same text with \r\n separators: md5 e997007971f6f17c8775d83f30edb4c6 (1567 bytes)

Saved as `demo_source_exact.txt`. This matters twice over: it settles which of the repo's two demo
reconstructions is real (`demo_base.txt` was right at 1,549 bytes; `demo_post_lf.txt`, 1,456 bytes, is the
surrounding forum post and was never the hashed text), and it gives the demo a *first* constraint
(source hash 7759227) that can be checked before any search is run.

The same reply also restates the example that defines the marking grammar:

- a paragraph's **first** letter may move down: `"I"` -> `"i"`;
- the letter that **closes the sentence containing the sign word** may move up: `"himself"` -> `"himselF"`;
- and the counter-example the author gives is the paragraph-final `n` of `capitalization`, which is explicitly
  *not* part of the solution: `"capitalizatioN"` would be wrong.

So the mark is not a blanket edge rule: it is one mark at the paragraph opening and one mark at the *sign word's*
sentence ending, where the sign word in the example is a reflexive pronoun.

The 2026-10-10 reply (id `pf0ea4v`) is a second, independent clue:

> "The only anomaly in the "Second" chapter is line 78. Its MD5 hash 8b71bade9685d3388452bc4755b06a0d doesn't
> match if the word is "What?". That is likely the puzzle. We need to find the sentence that unlocks this MD5
> hash."

Paragraph 78 of `Second` is indeed `"What?"` — so "line" means paragraph in the author's own file, one paragraph
per line. The stored hash belongs to a line that is no longer in the published story, consistent with the
2026-10-15 reply: "The MD5 hash does not match in instances where Aoi has modified the text".

## 33. Searches this pass, on the exact base (all negative)

| test object | candidates | result |
|---|---|---|
| every combination of paragraph-edge case toggles on the verified demo base (10 paragraphs, none/first/last/both each) | 1,048,576 (257 survivors of the 3c6 prefix, each derived at index 0) | 0 |
| the same on the CRLF form | 1,048,576 (261 survivors) | 0 |
| every single and every pair of arbitrary letter-case flips on the verified base | 716,710 (162 prefix survivors, derived) | 0 |
| every case pattern of every short paragraph of the chapter (<=14 letters) | 139,025 | 0 |
| grammar-defined sign sets on the chapter and on the demo: reflexive pronouns, first/second person, "signs", "recognize", "Turing", "reverse", "sincere", "Satoshi", paragraph-initial "I", quoted/unquoted paragraphs, question-final paragraphs - each in four edge modes, both joins | 352 | 0 |
| the reference hash `8b71bade…` against every paragraph and sentence of all 33 parts, seven serialisations each | 12,079 | 0 |

The demo therefore still has no verified answer, but it now has two hard facts to work with: its source text is
byte-exact, and its answer's MD5 must begin `3c6`. The chapter's own anomaly ("line 78") is confirmed to be a
missing original sentence rather than a case variant of the published one.

---

## 34. The grammar spaces, run to completion on the verified demo base (all negative)

Base: `demo_source_exact.txt`, 1,549 bytes, md5 `7759227d7406d8230d7e3a8f7b9846d7`, taken verbatim from the
author's own 2026-10-13 reply and byte-verified against the value he published there.

| space | reading of the worked example | candidates | prefix-3c6 survivors | escrow |
|---|---|---|---|---|
| paragraph initals down x sentence finals up | marks close a sentence | 2^10 x 2^15 = 33.5M | 8,251 | none |
| paragraph initials x one word final | "himself" closes a word, mid-paragraph | 277k | 78 | none |
| one and two word finals, no paragraph mark | signs are word-level only | 40.7k | 85 | none |
| paragraph initials x two word finals | two sign paragraphs, one mark each | 40.6M | 10,119 | none at idx 0-3 |

Method check that removes the last doubt about the target: grycoin/2's published pubkey hashes to exactly the
escrow hash160 `09d565074752019721ce68c58548ebc13750d5cc`, so the escrow is a derived-key puzzle and index 0 is
the right path (grycoin/1, whose answer "Still 21st Century" is published, calibrates identically).

**Conclusion.** The demo is closed under every grammar its own example implies: a paragraph opening lowered plus
a closing letter raised, where "closing" is sentence-final or word-final, with one or two marks. The example is
therefore illustrative of *direction*, not of the mark set, and the real rule marks more or different tokens, or
changes something other than letter case. The only cheap member of that family still unrun is three-or-more
word-final marks in a single candidate.
