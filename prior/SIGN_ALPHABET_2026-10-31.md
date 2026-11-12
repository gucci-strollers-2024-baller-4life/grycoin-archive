# The sign alphabet is `{A,I,M,O,S,T}`, all six necessary, and `H` is a live parameter

**Date:** 2026-10-31
**Script:** `sweeps/sign_letter_sweep.py`, results in `sign_letter_results.json`.
**Fast lane validated** against `harness/btc.py` before the run (standing rule).
**Derivation lane:** empty passphrase, no salt, reproduced in-sandbox (§4).
**Derivations:** 720 (64 texts at the three alphabets' carrier and anomaly sets, plus 16 strict-
conservation texts, nine indices each). **Hits: 0.**

The transport lanes themselves are `SAT_SET_TRANSPORT_2026-10-31.md` (`b8b6f32`), which ran nine lanes
per alphabet and is more thorough on set reduction than this entry. What is unique here is the alphabet
calibration, the reproduction of the derivation lane, and the receipts for the 178-set.

## 1. SATOSHI's letters do not reproduce the Finney post

| alphabet | hal_original (16 ¶) | demo / grycoin block 2 (10 ¶) |
|---|---|---|
| `{I,T,A,S,M}` | **4** — ¶2, ¶3, ¶4, ¶6 = `FFWW` | **5** — ¶3, ¶4, ¶6, ¶7, ¶8 = `FFOWW` |
| `{S,A,T,O,H,I}` | **5** — ¶2, ¶3, ¶4, ¶6, **¶11** = `FFWWM` | **4** — ¶3, ¶4, ¶7, ¶8 = `FFWW` |
| `{A,I,M,O,S,T}` | 4 — `FFWW` | 4 — `FFWW` |

SATOSHI's letters give exactly four in the demo, with ¶5 `I` and ¶6 `O` in class. Applied to the Finney
post they give five, because ¶11 *"My body began to fail"* opens on `M`. Each of the two named alphabets
works on exactly one demonstrated document and fails the other, which is the reason to look for the set
that satisfies both rather than pick a favourite.

## 2. The set that satisfies both, and its minimality

The letters that must be in class across the two demonstrated documents are the union of their in-class
letters, `{I,T,A,S,M} ∪ {I,A,O}` = **`{A,I,M,O,S,T}`**. Dropping one at a time:

| without | hal | demo | |
|---|---|---|---|
| `A` | 7 `FFWWAAA` | 6 `AFFWWA` | breaks |
| `I` | 7 `IFFWIWI` | 7 `IFFIWWI` | breaks |
| `M` | 5 `FFWWM` | 4 | breaks |
| `O` | 4 | 5 `FFOWW` | breaks |
| `S` | 5 `FFWWS` | 4 | breaks |
| `T` | 8 `FFWWTTTT` | 4 | breaks |

All six are required. **`H` is undetermined**: neither demonstrated document has an `H` initial, so both
`{A,I,M,O,S,T}` and `{A,H,I,M,O,S,T}` pass and nothing in the calibration prefers one. It is not a
cosmetic choice — it moves eleven paragraphs across the line:

| set | carrier | anomalies (with letters) | minus subheadings (out-class) |
|---|---|---|---|
| `{S,A,T,O,H,I}` SATOSHI | 178 | 95 (94) | 86 |
| `{A,I,M,O,S,T}` | **169** | **104 (103)** | 95 |
| `{A,H,I,M,O,S,T}` | 180 | 93 (92) | — |
| `{I,T,A,S,M}` | 154 | 119 (118) | 108 |

The subheading column is `b8b6f32`'s: ten paragraphs are list labels `a)`–`f)` at ¶176, ¶182, ¶209,
¶215, ¶250, ¶252, ¶254, ¶256, ¶258, ¶260, and eight of the SATOSHI out-class are those labels rather
than prose.

The one place the `H` ambiguity bites: **¶230 *"Having seen the signs before"*, the paragraph
immediately before the reprint, is a sign under the six-letter set and a carrier under the seven-letter
one.** Given ¶230's job is to introduce the reprint, `H`-out is the reading that makes structural sense,
which favours `{A,I,M,O,S,T}`.

Sorted, `{A,I,M,O,S,T}` is `AIMOST`, an anagram of **SATOMI**; `TOMI` is a post title here (`721505724`)
and `" TOMI Omit TOMI "` is a component of the certified preimage. Observation, not derivation, but it
explains why `ITASM` and `SATOSHI` are each *nearly* right: both are proper subsets of the same six.

## 3. Correction to my own previous entry

I wrote that the corrected carrier is 180 with 92 anomalies. **That was the seven-letter set with `H`
folded in, not the six-letter minimal set**, which gives 169 and 103. Both rows are in the table above
and they are different measurements, not a re-estimate. The transport runs in `b8b6f32` already use
169/103, so the two entries now agree; the 180/92 pair belongs only to the `H`-inclusive reading.

The other correction stands: **¶15 is `"2020."` and has no letters**, so the SATOSHI carrier is 178 and
179 only counts a member that cannot carry a sign letter.

## 4. The 178-set run, which is what was asked

Spec as given: in-class SATOSHI set, mass-conserved transport, both double-line-break formats, empty
passphrase, `m/44'/0'/0'/0/0` against `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`.

**Zero hits.** Under exactly that spec (two joins, no trailing separator): 4 texts, 36 derivations. With
trailing variants and both tail definitions: 8 texts, 72 derivations. Receipts:

| tail | join | md5 | idx 0 |
|---|---|---|---|
| first-sentence | LF | `e7255eacd4681a4befbb80631ceaa044` | `12oPtsx15WfSggRMUWEbivCyGKJJu8tyCG` |
| first-sentence | CRLF | `a9367bffd40f050a2af03fad9afd61a8` | `1Kdvt1YZEoDK7qVzXoVzMFh61i9LAaP1ek` |
| paragraph | LF | `21dfcbf8f6abc1ba1374300e40329f7b` | `1DXYK2Z19en6eq364uwvG7e2ufPpFtZehk` |
| paragraph | CRLF | `a1f82a62d6cea4661c60c81d7e95ff66` | `1DWcRACD2KB9bfK1Hw65cGaQqYEt4Bdt8m` |

Trailing variants `3e8b32dd…`, `5d5369c1…`, `5a2a4892…`, `ac42ba86…`. Every text also derived at indices
1, 2, 5, 6, 7, 44, 76, 77. The same pass covered the 169-set, the 180-set and all three alphabets'
anomaly sets under both tails and four joins.

## 5. Both remaining free parameters are pinned by evidence

*Hashing convention.* `demo_base.txt`, 1,549 bytes, `\n\n`, no trailing separator, hashes to
`7759227d7406d8230d7e3a8f7b9846d7` — the author-confirmed demo question hash. Two LF breaks.

**Correction:** this is the *demo's* join, not the chapter's. `STATE_OF_HUNT.md` records the live
`14zMkTga…` escrow's join as `\r\n\r\n`, on the author's 2019-08-01 note ("Hit enter twice … 13 10 13
10"). An earlier version of this entry generalised the LF result to the whole material and called the
CRLF branch decorative; that was wrong for the chapter, where CRLF is primary. No result moves — every
sweep here ran both joins.

*Derivation lane.* Reproduced in this sandbox rather than cited:

```
md5(safudev_stage1.txt) = 9dd2efb9bc976c2095bd534d7b8d431c
m/44'/0'/0'/0/0          = 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN
```

The certified `19TbyN5…` exemplar, produced with an **empty passphrase and no salt**. So the
`foryou` / `fouryou` / `FFWW` / `STNM` salt branches are not merely unrun, they are unmotivated: the one
lane with a verified end-to-end output has nothing in the passphrase field, and adding one would discard
the only empirical anchor in the corpus. Left unrun.

Corollary worth stating: `WW` = "four U, for you" is a *reading of the letters*, and ¶241 supplies that
reading in prose. It does not follow that "foryou" is a salt. If the dedication ever becomes a parameter,
the evidence for it would have to come from a lane that already works without it.

## 6. What this changes

1. **The alphabet is a detector, not a chapter selector.** Under `{A,I,M,O,S,T}` the chapter yields 103
   anomalous paragraphs, not four. The rule detects a sign block in the two documents the author
   demonstrates on; in the chapter the signs are hand-planted and ¶229–230 say so.
2. **"Exactly four" does not mean contiguous.** The demo's four are ¶3, ¶4, ¶7, ¶8 (two adjacent pairs);
   the Finney post's are ¶2, ¶3, ¶4, ¶6; the chapter's are three quads plus the reprint's four-of-five.
   A fifth chapter site need not be a quad, which is why the scattered closure in `dd0740d` was the right
   instrument.
3. **`H` should be carried as a parameter, not decided by taste**, and ¶230 is where it is testable.

Negative list, now including: window payloads, the 61 scattered sites, pentads and `I`-target readings,
lexical and directive selectors, the 44-char string, the `FFWW` locator reading, and transport of every
carrier and anomaly set under both tails, four joins, strict and forced conservation, nine lanes.
