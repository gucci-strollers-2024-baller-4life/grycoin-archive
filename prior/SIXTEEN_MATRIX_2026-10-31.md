# The 16-paragraph matrix: C(16,4) across the four FFWW/stnm windows, fully derived

**Date:** 2026-10-31
**Script:** `sweeps/sixteen_matrix.py` (coincurve fast lane, validated against `harness/btc.py`)

## 1. Universe

Four windows, each certified in-script before the sweep (initials `FFWW`, paragraph-finals `stnm`):

| window | paragraphs |
|---|---|
| W1 | ¶5, 6, 7, 8 |
| W2 | ¶93, 94, 95, 96 |
| W3 | ¶168, 169, 170, 171 |
| W4 | ¶231, 232, 233, 235 |

16 paragraphs, 1,820 quads, x 4 serialisations (LF/CRLF, +/- trailing) = **7,280 texts**,
**65,520 derivations** at m/44'/0'/0'/0/{0,1,2,5,6,7,44,76,77}.

## 2. Result

**0 hits.** 15.7 s at 465 texts/s (2.16 ms per text for nine indices), all seven thousand texts
derived, none screened. `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` is not reachable from any four-paragraph
selection inside the four windows under the edge-marking rule.

Fast-lane validation: `addrs()` reproduces `harness/btc.py`'s `addr_from_md5hex` on two digests, so the
negative is about the hypothesis and not about the implementation.

## 3. Two corrections carried forward

**(a) W4 is inherited, not engineered.** ¶231-235 has 0.99 word overlap with `hal_original.txt`
(the stage-one plaintext, reprinted in the chapter). Its `FFWW`/`stnm` is therefore forced by copying
the source document, and cannot count as an independent witness for a deliberate authorial template.
The independent windows are W1 (0.55 overlap), W2 (0.36), W3 (0.35); W1-W3 remain candidates for
"same signature, different text", W4 does not.

**(b) ¶234 is the source document's own skip, not a planted negative control.** `hal_original.txt` runs
¶2 `F…s`, ¶3 `F…t`, ¶4 `W…n`, ¶5 `I…g`, ¶6 `W…m`, and the certified stage-one answer marks ¶2, ¶3, ¶4,
**¶6** — skipping ¶5. The chapter's reprint reproduces the skip because it reproduces the document.
The exclusion is inherited with the text.

**(c) What still stands.** ¶236 is verbatim: *"We are directed to look at the last letter of each of
these. Because we are directed by the fact that the 'recognize the signs' instruction comes last in the
paragraph."* That is authorial text supporting the paragraph-final anchor in the chapter, and it survives
the W4 correction because it is evidence about geometry, not about selection.

## 4. What this closes

The four windows are exhausted as a selection mechanism, at every subset size up to four and both
directions of the conservation law. The remaining description of the chapter is not "which four
paragraphs of these sixteen", it is "what names four paragraphs anywhere in 273".
