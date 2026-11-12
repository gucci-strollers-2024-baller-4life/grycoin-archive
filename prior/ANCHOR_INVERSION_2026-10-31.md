# ¶187's edges, and the solo/paired/whole-chapter inversions

**Date:** 2026-10-31 **Base:** `base_chapter_lf.txt` (45,450 chars, md5 `46a308c2…`)
**Harness:** `sweeps/sixteen_matrix.py`, `validate()` clean. **Derivations: 39. Hits: 0.**

## 1. ¶187

> It also has the added value of misdirection. Hal could make people picture a young man of Japanese
> ancestry in their minds by using this anagram.

Head **`I`**, last word `anagram`, tail **`m`**. So ¶187 is `I…m`, not a case self-pair, and it is not an
`Aa` site under any reading.

## 2. The clause census, corrected

| phrase | paragraphs |
|---|---|
| "For those who don't know me" | **¶6, ¶168, ¶231** |
| "young man of Japanese ancestry" | **¶187, ¶222** |
| "recognize the signs" | 12: ¶20, 42, 220, 222, 223, 225, 226, 230, 236, 244, 246, 273 |

Three sites, not two: the third is ¶231, the Hal reprint, which opens `"For those who don't know me, I'm Hal
Finney…` with a quotation mark. And "young man of Japanese ancestry" has two homes, not one, so the third
echo is not unique either. "Recognize the signs" occurs twelve times and discriminates nothing.

Two small quotation fixes: Hal ¶2 reads *"I got my **start** in crypto"*, and Hal ¶7 reads *"Satoshi's true
identity **has become** a mystery"*.

## 3. Inversion tests on `base_chapter_lf.txt`

Single-paragraph, paired and quadruple inversions, each end swapped in case (head `F`→`f`, tail `t`→`T`).

| candidate | paragraphs flipped | mode | md5 | idx0 address |
|---|---|---|---|---|
| ¶6 solo | 6 | both ends | `7ad0776f6c6e6efbf9897c186d6c1866` | `1D3uEriy26SbADg1VaLFzJCA3A3XsRVw4n` |
| ¶6 head only | 6 | head | `6010a7d63e6ee7bf6528942ab17f01dc` | `13UYhoLHGuQcjXVEqCCNbBRbrmFuyEU1QD` |
| ¶6 tail only | 6 | tail | `38b88bd078dd3ee7f9ad0cac8aac769d` | `1HuPiqppcCthMZ6vDhh7cYsTU5GcnhKsbQ` |
| ¶168 solo | 168 | both | `a4288da642544187d8e8bebffbe7e057` | `1FeQVHFR6cRdE4HD8P2QaWLPAope9MwUN7` |
| ¶187 solo | 187 | both | `eb45d60eb7219e64cf1dcb0944c46b6a` | `1DQspPE8dTqRBAuDuSrjBf23n73viEEcp8` |
| {¶6, ¶168} | 6, 168 | both | `f7e0fd3459b57d1a151e92c21db9d994` | `13HEjcPjFkPqCkH5gmroQZK9nKTGp4f4Y9` |
| {¶6, ¶168, ¶231} | all three clause sites | both | `db5b1bf24c8ccf7a588468490e9ae9c7` | `17qmCAs9HxKgfVp1Vji3htsDFWcYXmGuei` |
| {¶6, ¶168, ¶187} | the triple | both | `3b939312af9b78e24c7ec875aba59421` | `1BX32Ce7zuXbFxEfp8hiX9G8HYPXNBSCY4` |
| `F…t` quad | 6, 94, 169, 232 | both | `666887b55ff5149d21f59a0beb9645e1` | `1Kj6zyVVy4jmESr2dweLWFPh66aTUF9K9k` |
| `F…s` quad | 5, 93, 168, 231 | both | `488cb789f1b017601dcad9fbc3a6e651` | `1DtNHNnGtgnchhM5We9pB2r5ZDfCh3FnLv` |

And the whole-chapter variant, every paragraph's ends inverted:

| scope | mode | md5 | idx0 address |
|---|---|---|---|
| all 273 | both ends | `ecc8cbbdea63e448d27e31f3cc5ab331` | `15G1jUXyrKceVbC3jLXABfdkS1TUsDdwoj` |
| all 273 | head only | `cb79698c475df04cbbc1929c0ae36553` | `1C8Uhc6dKGr12uny4zh2BFMEBWjQiZV1x6` |
| all 273 | tail only | `d86b773060eeace177cf0aee484ceb04` | `1PpTo3E7UTht7rE74JYmKm3coPmovxBQka` |

None hits `14zMkTga…` at index 0, 76 or 77. §3 also closes the open question in the working state about
whether the inversion is anchor-only or chapter-wide: both scopes are negative, so the choice does not
separate the two readings on evidence. The distinguish point is therefore not the *scope* of the inversion
but its *selector*, which remains open.
