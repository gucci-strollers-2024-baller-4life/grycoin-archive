# Isolated extraction of paragraph subsets: 20 texts, 60 derivations, 0 hits

**Date:** 2026-10-31 **Base:** `base_chapter_lf.txt` **Harness:** `sweeps/sixteen_matrix.py`,
`validate()` clean. **Indices:** 0, 76, 77. **Target:** `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`.

The 2^16 closure in `SERIALIZATION.md` covered every *flip subset within* the 16 window paragraphs while
keeping the other 257 in place. What had never been run is the opposite operation: **dropping** the other
paragraphs and hashing only the marked ones. That is what this pass tests, since Hypothesis A in the request
predicts it.

| subset | raw, index 0 | inverted, index 0 |
|---|---|---|
| W1 ¶5–8 | `1FLxEyanExyf2wz671yQnGVHRbHjNcvZrn` | `18T7eGZ4N8AjsuVFtWSCYxL3aHht3bRZJb` |
| W2 ¶93–96 | `16mtfobXRThUaEV5hKFrgupKVRYJhM8VKq` | `1LFiBwzw9GjrqkZkb2YwoPCCprvfwJxZ7H` |
| W3 ¶168–171 | `13FAAeUEXa9oMjbgrzcjnbpGARNew3YLa9` | `1NW8WJLjc1tKJ5JwuuXiZEdChiVtyMvemm` |
| `F…t` anchors ¶6, 94, 169, 232 | `16BYgcywdwWfhaN7YDazaVDGGW1b4KG3X2` | `1CGzKFFzhno11bgX5RdMyD1PW3HJSyoDsL` |
| W4 ¶231, 232, 233, 235 | `1FZXKz93je81ZDGZsrBD3i5iNHaXstMnYU` | `15aHJ9kqFuJf6amPVA6pVVQQAXMHBV39tz` |
| reprint ¶231–235 (with ¶234) | `1CCRV7Zn7g4P8nnErSA7Z1y5hNc2rtFSoi` | `12nT5b9sZVMm6jKW5g48kikk4BtH5oTDEx` |
| signs ¶20, 42, 220, 273 | `1P3jC7bPiZaDo5Uq2QEAodiC16L76j7tvq` | `13hsdgbb3xu1Xkj24qwJAQqHrvsroerfsj` |
| W1+W2+W3 (12 paragraphs) | `179EjRFpKCjvPEvJox7nhBLPdTtoSzhV3` | `1PPvLEVJhA3ufqzAHo3B4FudH34sgduRkK` |
| W1+W2+W3+W4 (16 paragraphs) | `1Prge5vTxMNrpHENqbLrD8TRQ9fGPrwfet` | `1CZZj1rrgy6ZhPSujLGq5aEiuCGn6RyMvY` |
| whole chapter, Atbash | `1GoJMozHrBEBspRFLegz92MtnjRk1v6AX9` | — |
| W3, Atbash | `1QBimwHh67DFsZpELRCK1beUprzCAV7yjC` | — |

**No hits.** Isolated extraction is dead as a model, raw and inverted, at all three indices, for every
subset proposed.

## The Atbash / bisection reading is contradicted by the author

Round 1's part 761570746 is **not in this repo** (it is referenced in `RBB_DOSSIER.md`,
`FINDINGS_MARKS_2026-10-31.md` and `RBB_ANSWER_SPEC_FINDINGS.md`, but the text is not held), so the claim
that `Aa` meant Atbash there cannot be checked locally. It does not matter for block 77, because the author
states the format for this block herself, in the demo post:

> The main point of this block is to give a simple example for **the format used in both phases of block 77**
> […] people are supposed to **keep the whole long text and change only a couple of letters in their
> capitalization.**

That sentence rules out substitution ciphers, bisection and reordering for both stages. Atbash is not "a
couple of letters in their capitalization", and a bisected half is not the whole long text.

What the demo does *not* certify is a flip count: both of its illustrative flips are flagged as not being
the answer (*"that 'n' is not part of the solution"*; the `I`/`himself` pair is introduced as what you would
do *"if you … thought"* they were signs). The only certified answer shape in this puzzle is stage one's:
**four paragraphs, both ends each**, joined `\n\n`, index 0. So the stage-two answer is plausibly *k*
paragraphs with both ends flipped, and *k* and the **selector** are what remain unknown. Selection, not
scope, is now the whole problem.
