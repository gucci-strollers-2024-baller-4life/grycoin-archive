# Session 2026-10-29 (evening) — exhaustions, one corrected bug, and a base-text risk

Harness: `/tmp/fast.py` (coincurve; 0.9 ms/derive vs 17.5 ms in `work/btc.py`). All address checks
against `14zMkTga…`; demo checks against `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` and MD5 prefix `3c6`.

## 1. Demo (Grycoin block 2) — paragraph-edge family EXHAUSTED, and a bug caught

First run used `buf[pos] = up` for every mutation, so all paragraph-FIRST flips were no-ops
(that is why it reported 0 `3c6` hits on the LF join, an impossible result). Corrected: each
mutation stores its own flipped character.

Pool: 10 paragraph-first→lowercase, 10 paragraph-last→uppercase, `himself`→`himselF`. All 2^21 subsets.

| join | tested | `3c6` hits (expect ~512) | escrow matches |
|---|---|---|---|
| `\n\n` (base md5 `7759227…` = author-confirmed) | 2,097,152 | 452 | 0 |
| `\r\n\r\n` | 2,097,152 | 496 | 0 |

Extended pool (+ last letter of every `signs` occurrence, 25 mutations, 2^25 = 33.5M, LF): 8,296
`3c6` hits, 0 escrow matches.

**Consequence.** The demo's own solution is not reachable by paragraph-edge flips at all, even though
the author states those as the demo's flips. He also says he does not know the demo's solution
("I actually don't know… not even to me"). So the demo cannot calibrate the chapter: its answer
contains a further wrinkle the winner scripted, now unrecoverable.

## 2. Chapter — the 16 "signature paragraph" family is closed (exhaustive, not sampled)

Fourth FFWW/stnm window found at **231–235**: the verbatim Hal quote. It is the only window with the
intervening I-paragraph (234), i.e. the only one that reproduces Satoshi's post exactly. Raw-first-char
scans miss it because 231 opens with a quote mark.

All 2^16 subsets of {5,6,7,8, 93,94,95,96, 168,169,170,171, 231,232,233,235}, modes
first-only / last-only / both, joins `\r\n\r\n`, `\n\n`, `\r\n`: **zero hits** (18 runs).

## 3. Mechanism precedent: flips spell a NAME, inside words

- Block 2: `message→messaGe`, `you→You`, `on→oN` plus the planted `A` = A,G,Y,N (Yang).
- Block 29: `voice→vOIce` — two interior letters, "same method as in Block 2".

Greedy name-spelling tests on the chapter (21 names x forward/backward x 2 joins): zero hits.

## 4. The real weak link: the base text is not verified against 2019

`data-p-id = md5(paragraph text)` certifies only that today's text is self-consistent; Wattpad
recomputes it. No 2019 capture of `wattpad.com/720888559` is in the corpus. The author edited the
chapter ("final version… which I will publish in a moment", 2019-07-22) and re-funded on 2019-07-30
with "a slightly different solution". If even one character of the current text differs from what she
hashed, every sweep in this repo is void.

## 5. THE BASE TEXT WAS WRONG — 10 missing line breaks (found after §1-4 were written)

Authoritative source: `https://www.wattpad.com/apiv2/storytext?id=720888559` (59,613 bytes of
`<p data-p-id=...>` HTML). Parsing it shows **10 paragraphs contain a `<br>`**, i.e. a single
internal line break: 63, 73, 121, 124, 146, 160, 184, 189, 193, 213. The corpus's `wp_paras.json`
has those two halves glued together with nothing between them (e.g. `already?""Of course not.`,
`"THOMAS".Satoshi`, `naturally.And again`).

Arithmetic check against Wattpad's own metadata (`/v4/parts/720888559`: length 45451):

    sum of paragraph characters        44,896
    + 10 internal line breaks              10
    + 2 per separator x 272 paragraphs    544
    + 1 trailing newline                    1
    = 45,451   == length reported by Wattpad.

Exact. So the chapter as hashed contains ten single line breaks the repo has never had. Every sweep
in this repo used a base 10 bytes short. `wp_paras_br.json` now holds the corrected paragraphs as
segment lists (internal breaks preserved).

Corrected plain-base md5s (no flips):
`\n\n` join, `\n` breaks: `46a308c279540a33e977ea1f660e8458` -> `1DGrEwbRwANU28BgCnp6HeNhPzB2HbiyUL`
`\r\n\r\n` join, `\n` breaks: `bd07e6ee209c5ab65d874bbbcfccda18` -> `1BGh8btgbCSPDfjyESjnkjYyYvoB7xnDDb`

## 6. Base-text drift risk: RESOLVED (no archive needed)

`/v4/parts/720888559` reports createDate 2019-04-17T23:06:03Z, **modifyDate 2019-07-23T23:12:04Z**.
The part has not been edited since 2019-07-23, i.e. before the 14zMk solution was made (funding block
2019-07-30). Today's text is the 2019 text. Archives are moot: Wayback has no capture of
`wattpad.com/720888559` or the story URL, archive.today has no Memento, Common Crawl's index is
returning 504s.

## 7. Hypotheses re-run on the corrected base

plain / three windows / four windows (incl. the 231-235 quote run) / quote run alone / the 14 "signs"
paragraphs / the 119 non-ITASM paragraphs, across joins {CRLFCRLF, LF} x internal breaks {LF, CRLF} x
trailing {"", LF, CRLF} = 72 candidates: zero hits. Full 2^16 closure of the 16 window paragraphs on
the LF serialisation, mode first-down+last-up: zero hits.

## 8. Corrected base built, and a wordplay census of all 33 chapters

`build_base.py` emits `base_chapter_lf.txt`, `base_chapter_crlf.txt`, `base_chapter_mixed.txt` from
`wp_paras_br.json`. LF variant: 45,450 chars, md5 `46a308c2…` -> `1DGrEwbR…`; Wattpad's stored
length is 45,451, i.e. this text plus one trailing newline. The segment model reproduces Wattpad's
`length` exactly for 31 of the 33 story parts, which is what validates the repair.

Census (all 33 parts fetched from `apiv2/storytext`):

- FFWW-first / stnm-last four-paragraph windows occur in **one part only: the RBB chapter**
  (starts 5, 93, 168, plus the 231-235 quote run with its intervening I-paragraph). No other chapter
  of the story carries the device, so "recognize the signs" cannot be resolved from sibling chapters.
- Internal-capital tokens ("vOIce" style): RBB chapter 11, The Satoshi Code 19 (mostly genesis-address
  fragments plus `FInally`, `FIbonacci`, `ELiZABETH`, `NmST`), everything else 0-6 and mostly
  camel-case addresses. The device is real but is used for demonstration, not as a key.
- Text in the chapter is stable: `modifyDate` 2019-07-23 on part 720888559.
- `Fran` does not appear anywhere in the story; the only hit is "frantic" in part 762380140. The
  "who FF is" riddle (para 241) stays open and has no corpus support.

Re-ran on the corrected base with the census-derived rule sets — FW-first (42 paras), FW+stnm (31),
the quote run with and without the I-paragraph, and both combined with the three windows — under
joins x internal-break styles x {first-down+last-up, first-down, last-up}: zero hits.

## 9. Documented wordplay rules, extracted and applied (all on the corrected base)

Read off the corpus, not invented:

1. **Inheritance rule** (`RULE_INHERITANCE.md`, part 720890652 "Hoax"): "The solution is of course the
   word Hoax, starting with a capital letter because the address I found had it that way" and
   "capitalization will be evident". The case pattern is copied out of a visible source artefact.
2. **Index convention** (part 730790756 "Quizchain as a Password Manager", paras 19-20): "use the first
   private key for the first site... the second for the second one". Round-two b2's published
   explanation confirms it: "Second private key because this was block 2". For the RBB, block 77, the
   derivation index 77 is therefore a live candidate that the corpus's sweeps largely skipped.
3. **Stride acrostic** (same part, para 12): "We highlight every 7th word and use the first letter of
   each of these words to get the string BaSCifCatfAaa1i", then quote-wrapping and an added word as
   "twists". Documented author device, tied to 7 and to 44.
4. **Failure modes** (`PATTERNS.md` §2): b77's own log entry reads "Failed block, made subtle hashing
   mistake, but corrected that way before anyone came close", so a join/field-level mismatch is the
   expected failure shape, not a wrong flip rule.

Applied to the corrected base this session, all negative:

- capital sets following rule 1: paragraph-initial lowering, segment-initial lowering (this now covers
  the ten new post-break starts), mid-sentence lowering, paragraph-final raising, each under LF, CRLF
  and mixed serialisations, indices 0-77 where cheap and 0-9/44/76/77 elsewhere;
- rule 3: strides 1-88 with every starting offset, first-letter strings in both cases, indices 0 and 77;
- the window/signature sets (W12, W12+quote run, quote run, FW+stnm, each window alone) again at
  indices 0-9, 44, 76 and 77.

Still open: rule 3 with the documented twists (quotes around the string, one extra word appended), the
full 0-99 index sweep for the word-level families, and the demo crack that would settle the flip rule.

## 10. Demo cracked at word level? No. And two new primary sources read

Demo word-level, exhaustively (MD5 `3c6` oracle, then escrow `1tzieU…` at indices 0-9):
- every within-word interior-capital subset: 5,550
- all interior positions, k<=2: 217,776
- all interior positions, k=3: 45,770,725 (11,209 oracle hits, 0 escrow)
- all word-final positions, k<=3: 3,535,087
Zero. Combined with the earlier edge closure (2^21 per join) the demo is not reachable by paragraph
edges, word-final capitals up to 3, or interior capitals up to 3. Its answer must mix families or
carry an appended field, and the author says he cannot reconstruct it either.

Two primary sources read this session:

- Part **742662804 "Complete Second Round of the Quizchain"** (367 paragraphs, the author's own round-two
  log; it stops at block 32, so there is no b77 entry). Its **Block 2** entry reads: "Another big prize
  (77 mbtc) block because of mistake in block 77 of first round. **Format: [solution]**. Needs context
  from Wattpad story. Solved in two hours without hint." That is the author stating a bare `[solution]`
  format for a round-two block, which settles the field question for the RBB in the same direction as
  stage one and the demo.
- The same log gives the password-manager recipe with real numbers: master string
  `"BaSCifCatfAaa1i"Metamon` -> MD5 `2941774a…` -> BIP39 -> take the Nth private key ("the 2nd private
  key because the 1st one is used for something else"). This is the documented index convention in use,
  and it matches what part 730790756 describes.

New tests on the corrected base, all negative: sentence-level and paragraph-level unit flips under the
ITASM rule (629 sentence units, 282 paragraph units, 3 modes, 3 serialisations, 4 indices), and the
field+link family (4 field spacings x {stage-one WIF, its last 7, block-44 WIF} x 4 flip sets x 3
serialisations = 288 candidates).
