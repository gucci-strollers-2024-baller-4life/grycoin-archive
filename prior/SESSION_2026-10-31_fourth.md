# Session 2026-10-31 (fourth): the literal "all except four" reading and the sentence-edge reading, both negative

Harness: this session ran in a fresh sandbox from the tarball of `main` (commit `abae83f`), no carry-over.
Certification before any claim:
- `base_chapter_lf.txt` md5 `46a308c279540a33e977ea1f660e8458` (45,456 bytes on disk),
  `base_chapter_crlf.txt` md5 `db11a7fdba7b4867a24445a7a30709b8`, `base_chapter_mixed.txt` `bd07e6ee209c5ab65d874bbbcfccda18`.
- Legacy corpus `chapter_paras_exact.json`: LF `48d318202691ffb873e00b63196eaf36`, CRLF `f74e8e0122e114fe13c89a3bba25294a`.
- Stage-one self-test: md5 `9dd2efb9bc976c2095bd534d7b8d431c` -> `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` ✔.
- Throughput here: ~73 address-verified derivations/second, pure Python (`harness/btc.py`).

Both tests below compare against the LIVE (`14zMkT…`) and OLD (`1EFojc…`) escrows on the address string,
at indices 0-7, 44, 76, 77.

## 1. "All paragraphs except four" as a literal rule — negative
Script `test_four_exception.py`. Flip the first and last *letters* of every paragraph except
222, 231, 243, 244 (the four non-voice paragraphs).

| set | modes | bases | derivations | hits |
|---|---|---|---|---|
| all-but-four (269 paras) | fd+lu, fu+ld | 4 | 88 | 0 |
| four-only (4 paras) | fd+lu, fu+ld | 4 | 88 | 0 |
| all-273 | fd+lu, fu+ld | 4 | 88 | 0 |

Bases: corrected corpus (`wp_paras_br.json`, internal `<br>` kept) and legacy (`chapter_paras_exact.json`),
each joined CRLFCRLF and LFLF. **264 derivations, 0 hits.**

Structural facts found while running it:
- **262 of 273** paragraphs begin with an uppercase letter; **263 of 273** end with a lowercase letter.
  So the literal 269-set produces a document in which nearly every paragraph starts lowercase and ends
  uppercase. That is a total case inversion, not a "change the capitalization of letters in solution"
  edit on a few words, which is the reading the stage-one reproduction supports.
- All four exception paragraphs are quotation-marked lines (`"Today, Satoshi's true identity…`,
  `"For those who don't know me, I'm Hal Finney…`, `"Today, Satoshi's real identity"`,
  `"I recognize the signs."`), and the chapter carries **63** quotation-marked paragraphs, so that
  four is not a unique structural class.
- Under the inverse mode those four are case-invariant (first letter already lowercase, last already
  uppercase), so the four-only and all-273 variants collapse onto the same preimage, which is why their
  md5s repeat.

## 2. Sentence-edge unit, dialogue as the invariant exception — negative
Script `test_sentence_edges.py`. Unit = sentence (`.!?` plus optional closing quote), flip first and last
letter of each selected sentence. Sentence census: 664 sentences on the corrected CRLF base, 658 on the
legacy CRLF base; 140 and 139 of them sit in quotation-marked paragraphs.

| variant | sentences selected | derivations | hits |
|---|---|---|---|
| all except sentences in quoted paragraphs | 524 / 519 | 88 | 0 |
| all sentences | 664 / 658 | 88 | 0 |
| quoted-paragraph sentences only | 140 / 139 | 88 | 0 |
| all except sentences opening on a quote mark | 599 / 594 | 88 | 0 |

Same 4 bases, 2 modes, 11 indices. **352 derivations, 0 hits.**

## 3. Cost correction on the exclusion space
Gemini proposed sweeping every four-element exclusion subset. `C(273,4) = 245,310,250`. At this sandbox's
measured **73 derivations/s** that is **~39 days** on one core, not 41 minutes: the chapter has no MD5
prefix oracle (only the demo question hash has `7759227`), so every candidate must be fully derived to
an address before it can be rejected. A fast EC build (~570/s) still leaves ~5 days.

## 4. Where this leaves the selection problem
Both cheap readings of "all paragraphs except four" are now closed on four bases in both directions.
What remains untested is the same exclusion idea restricted to a **pool** of structurally odd paragraphs
(quoted, non-voice, duplicate pair, the 13 trailing-space paragraphs, section heads), which is ~10^4
states and ~1-2 hours here, rather than the full 2.45x10^8.

## 5. Dual constraint (Vector A x Vector B), Gemini's combined pipeline — negative
Script `test_dual_constraint.py`. Gemini supplied a script for this; it could not be run as written
(stub loader returning `Paragraph 1`…, `swapcase()` on the whole paragraph instead of the edge letters,
and a `7759227` MD5 pre-filter that only exists for the demo question hash, not the chapter). Implemented
faithfully instead, on the certified corpora.

Vector A sets: all-but-four (269); all-but-four restricted to paragraphs whose first letter is outside
I, T, A, S, M (119 openers outside that set, 154 inside); all-but-four restricted to openers inside it.
Vector B: paragraphs 34 and 78 are both exactly `"What?"`, index delta 44, so each is given its own
treatment enumerated over four options (untouched / first-down-last-up / first-up-last-down / whole-
paragraph case swap), 16 combinations per set and direction.

Stage 1: 4 bases x 3 sets x 2 directions x 16 anchor combinations = 384 preimages -> **4,224 derivations, 0 hits.**
Stage 2, direction splits at the anchor boundaries (34, 44, 78, 136): 4 bases x 3 sets x 4 splits x 2
orders = 96 preimages -> **1,056 derivations, 0 hits.**

**Combined: 5,280 address-verified derivations, zero hits.** Neither the semantic four nor the delta-44
anchor produces the escrow in any direction, on any corpus, under any anchor treatment tested.
