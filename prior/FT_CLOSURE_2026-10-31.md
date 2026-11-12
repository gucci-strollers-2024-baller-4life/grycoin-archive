# The `F…t` closure, the 61 scattered sites, and the ¶238 `I`-adjacency derived

**Date:** 2026-10-31
**Script:** `sweeps/ft_closure.py` (results in `ft_closure_results.json`)
**Adds to:** `SELECTOR_CENSUS_2026-10-31.md` (`8308c71`) and `BOUNDARY_READOUT_2026-10-31.md`.
The edge-class table in the census is reproduced here exactly and is not in dispute.

## 1. What the `F…t` scarcity actually proves

The chapter contains exactly four `F…t` paragraphs: **¶6, ¶94, ¶169, ¶232**, one per window, each in
the second slot of its run, zero unconsumed.

Any site of the signature needs `s`, `t`, `n`, `m` in that order, so it needs an `F…t` in its second
slot. Therefore **every site must pass through ¶6, ¶94, ¶169 or ¶232.** That is containment.

It is not uniqueness. The census states "no fifth site exists in the chapter, contiguous or
scattered". Contiguous is right. Scattered is not: once span width is unconstrained, the other three
members can be drawn from anywhere, and **61 sites exist**, anchored 20 / 24 / 12 / 5 on
¶6 / ¶94 / ¶169 / ¶232. Twenty-six of them pull in paragraphs from outside the windows, from
`F…s` {5, 93, 100, 168, 231}, `W…n` {7, 52, 95, 139, 152, 157, 170, 233, 265} and
`W…m` {8, 30, 96, 171, 235}. Example: ¶5, ¶6, ¶52, ¶96 reads `FFWW` with finals `stnm` and shares
only ¶6 with any window.

So the conclusion holds but for a different reason than the one written: not "there is no fifth site"
but "no site can avoid the four `F…t` paragraphs". The 7,280-text matrix is exhaustive over 4-subsets
of the sixteen known paragraphs; it never covered the 26 hybrids.

## 2. Every site derived

| reading | sites | note |
|---|---|---|
| contiguous four | 3 | ¶5–8, ¶93–96, ¶168–171 |
| four of five (Hal form) | 4 | plus ¶231–235 |
| any four of up to eight consecutive | 4 | the same four |
| unbounded span | 61 | 57 hybrids, 26 reaching outside the windows |

All 61 derived, four serialisations each, indices 0, 1, 2, 5, 6, 7, 44, 76, 77:
**244 texts, 2,196 derivations, 0 hits, 0.27 s.** The selection space is now closed at every span
width, and the closure no longer depends on which reading of "same block" is chosen.

## 3. The ¶238 `I`-adjacency, which the census named as the next lead

The four `I` anchors, audited:

| anchor | first | final | final word | chars | words | relation to its site |
|---|---|---|---|---|---|---|
| ¶4 | I | n | `in` | 96 | 17 | immediately precedes W1 |
| ¶92 | I | w | `now` | 59 | 11 | immediately precedes W2 |
| ¶167 | I | s | `years` | 200 | 38 | immediately precedes W3 |
| ¶234 | I | g | `fascinating` | 370 | 63 | interleaved inside W4 |

Their finals spell `nwsg`; in document order `n w s g`, and in no order anything. Lengths 96 / 59 /
200 / 370 and word counts 17 / 11 / 38 / 63 show no progression, arithmetic or ordinal relation. The
invariant is positional only: **every one of the four sites has an `I`-opener paragraph adjacent to
its run**, interleaved in Hal's form and immediately preceding in the three novel ones. Base rate for
an `I` opener is 47/273 = 17%, so three-for-three is about 0.5% if the windows are independent draws,
which the reprint overlap already argues they are not.

Both readings of ¶238 were then derived rather than argued:

- **pentad** (four window paragraphs plus the anchor, 5 units): every subset of each pentad, 32 per
  site, plus the anchor substituted for each window member, 16;
- **union** readings: the four anchors alone, and the unions of two, three and four pentads.

**135 selections, 540 texts, 4,860 derivations, 0 hits, 0.6 s.** Neither "a fifth unit is added" nor
"the target shifts to the `I` paragraphs themselves" survives at site-local scale. The
`I`-adjacency is a real structural regularity and a spent one.

## 4. Two counting corrections

- **Chapter non-ITASM paragraphs: 118**, not 121. The initial-letter inventory over 273 paragraphs is
  T 50, I 47, A 36, W 27, S 19, O 15, F 14, H 11, B 11, Y 9, G 6, N 5, C 4, V 3, P 3, E 3, D 3,
  R 2, M 2, K 1, L 1, plus one paragraph with no letters at all. `ITASM` covers **154**, leaving 118
  with letters (119 counting the letterless one). The census reads 152 / 121.
- The per-section exception counts `20, 3, 4, 0, 5, 5, 6, 0, 4, 0, 2, 12, 6, 0` stand. A separate
  measurement, sliding a fixed 16-paragraph window across the chapter, gives a non-ITASM count
  ranging 1 to 13 with 14 windows at exactly four. Different statistic, same verdict: nothing yields
  four exceptions plus `FFWW`.

## 5. State

Closed: the windows as mark carriers (`2d0d100`); the selection space at every span width, tight and
scattered (this pass); the pentad and `I`-target readings of ¶238 (this pass); lexical openers,
terminal directives and the ¶229 exception rule as selectors (census `8308c71`).

Standing: the signature is co-extensive. Exactly three windows carry `FFWW` initials, exactly three
carry `stnm` finals, and they are the same three, zero misses in either direction. The fourth member
of every window, including the reprint, ends on the literal word "them", which is also the source's
own terminal word at that slot.

Open, and now the whole of what is left: the transformation. Three instances of `stnm` are one
four-letter string repeated three times, so the windows carry four letters of content, and the flip
axis over the sixteen window paragraphs is already spent.
