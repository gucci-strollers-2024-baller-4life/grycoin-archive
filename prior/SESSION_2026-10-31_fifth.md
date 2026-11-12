# Session 2026-10-31 (fifth): claim step closed, reprint verified verbatim, letter-class family swept

## 1. The claim step is closed, so every negative is about the text

`BLOCK77_KEYS.md` and `ESCROW_KEY_AUDIT_2026-10-31.md` settle the address side: pipeline
`md5(text) -> BIP39(16 bytes) -> seed -> m/44'/0'/0'/0/0 -> P2PKH`, verified independently on three
blocks (R1:77 `1FAAKp…`, R2:77 stage one `19TbyN5…`, R2:76 `13Cv6S…`), and the live escrow
`14zMk…`'s key has never signed, so it cannot leak and is not at index/path risk. Consequence worth
stating plainly: our negatives are not "right text, wrong address". They are "wrong text".

## 2. The Finney reprint is verbatim, with exactly one correction

Token-level diff, chapter 231-235 against `hal_original.txt` H2-H6:

| chapter | hal | tokens | differences |
|---|---|---|---|
| 231 | H2 | 81 | none |
| 232 | H3 | 48 | none |
| 233 | H4 | 38 | none |
| 234 | H5 | 70 | `facinating` -> `fascinating` |
| 235 | H6 | 79 | none |

One change in 316 tokens, and it is a spelling correction. So the quotation layer is a faithful
copy, not a remix: the FFWW/I structure and the STNM tails are Hal's own, and the author's only
intervention in the whole block is fixing his typo. `DISCREPANCIES.md` §9 said "three verbatim
paragraphs"; that came from a faulty substring test and is corrected in place.

## 3. The chapter never describes stage two

Grepping all 273 paragraphs for `stage`, `second stage`, `two line breaks`, `slightly different`
returns exactly one hit, paragraph 137, about "the early stage of Bitcoin". The chapter documents
stage one exhaustively (229-241) and says nothing about the stage-two format. The demo is the only
place the stage-two format is described. That is why the demo is the spec and the chapter is only
the question: no amount of rereading the chapter will yield the stage-two rule, because the author
never states it there.

## 4. New family: letter-class masks

Her phrase for the format is "change only a couple of letters in their capitalization" (demo,
paragraph 2). The corpus read that as a couple of *positions* and closed every space up to four
arbitrary positions. The other reading is a couple of *letter symbols* applied to every occurrence,
which changes hundreds of characters and is still "a couple of letters". `CLUES_CANONICAL` §12.4
tested letter sets only for candidate names (THOMAS, FINNEY, NAKAMOTO, SATOSHI, STNM, GRYCOIN,
SECOND); arbitrary alphabet subsets were never enumerated.

Script `sweeps/letter_class.py`, both certified bases, indices 0, 1, 2, 76, 77:

| mode | subsets | candidates | derivations | hits |
|---|---|---|---|---|
| swap every occurrence, k <= 4 | 17,901 | 35,802 | 179,010 | 0 |
| lower every uppercase occurrence, k <= 3 | 2,951 | 5,902 | 29,510 | 0 |
| capitalise every lowercase occurrence, k <= 3 | 2,951 | 5,902 | 29,510 | 0 |

**238,030 address-verified derivations, zero hits.**

Next increment on the same family: `swap` at k = 5 is 65,780 subsets, 657,800 derivations, about
20 minutes here in four chunks. Run it before declaring the family dead.
