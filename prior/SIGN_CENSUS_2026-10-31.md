# The sign census: the two channels do not co-occur in any act

**Date:** 2026-10-31
**Script:** `sweeps/sign_census.py` (results in `sign_census_results.json`)
**Derivations:** 1,044 in total: 180 on the four live occurrences (§4) and 864 on the hybrid
channel (§5). Nothing here interacts with any earlier negative.

## 1. Basis and counts

273 paragraphs, minus 18 structural headings, 10 list labels `a)`–`f)` and ¶15 (`"2020."`, no
letters), leaves **244 prose paragraphs** and **627 sentences**. Acts split at the four window
starts.

| act | ¶ range | prose ¶ | sentences | `sign`/`signs` | `sign*` stem | "recognize the signs" |
|---|---|---|---|---|---|---|
| I | 1–92 | 83 | 205 | 2 | 2 | 2 |
| II | 93–167 | 68 | 193 | **0** | **0** | **0** |
| III | 168–230 | 58 | 137 | 10 | 11 | 6 |
| IV | 231–273 | 35 | 92 | 6 | 7 | 5 |
| | | **244** | **627** | **18** | **20** | **13** |

Act II is empty of the vocabulary. Its single "sign" substring is inside "software designers" at
¶124, which no word-boundary search counts. The `1+1+1+1` model dies here: there is no sentence in
Act II to select, and the acts are not comparable in size, 205 sentences against 92.

## 2. The eighteen sentences, classified

Three are not the vocabulary at all: ¶206 twice is "dollar sign", ¶240 is the verb "to sign".

| class | n | paragraphs |
|---|---|---|
| live use of the instruction | 4 | ¶20, ¶42, ¶220, ¶273 |
| quotation | 2 | ¶222 (Hal ¶7), ¶244 (the quoted line alone) |
| author's analysis | 9 | ¶223, 225, 226, 227, 228, 230, 236, 246 (twice) |

The four live uses distribute 2 / 0 / 1 / 1: ¶20 Aoi saying "I recognize the signs" in dialogue,
¶42 "Did anyone recognize the signs?", ¶220 "it will become very easy to recognize the signs", and
¶273, the last sentence of the chapter, "At least for those of us who are able to recognize the
signs." Act II contributes none.

The phrase also occurs well outside ¶236–¶246, at eight of its thirteen occurrences: ¶20, 42, 220,
222, 223, 225, 226, 230 and 273. What is confined to ¶223–¶246 is the *analysis* of the phrase,
not the phrase.

## 3. The case-odd channel, and a correction

Prose-wide there are **10 occurrences in 9 distinct tokens**, distributed **1 in Act I, 9 in Act
II, 0 in Acts III and IV**. A previous message of mine said twelve and eleven; both were wrong, an
arithmetic slip in a per-act sum that double-counted a token appearing in two paragraphs.

| ¶ | token | act | reading |
|---|---|---|---|
| 73 | `ppM` | I | planted: 350 ppm, the CO2 target |
| 106, 112 | `WorldWideAbsoluteCarbonBudget` | II | quoted burn address |
| 107 | `FUCKFuck…FUCKX`, `AndrewYangForPresident`, `oXXX` | II | quoted addresses |
| 126 | `abcdefghijkLmnopqruvwxyz`, `…qrstuvwxyz` | II | alphabet addresses, capital L |
| 128 | `VIrgin` | II | prose-internal, capital injected at index 1 |
| 136 | `BItcoin` | II | prose-internal, capital injected at index 1 |

`CLUES_CANONICAL` §12.3 holds the canonical inventory at fourteen instances over all 273
paragraphs, including hyphenated forms and headings; the table above is the prose subset with the
act distribution added.

**The two channels are disjoint by act.** Sign vocabulary is 18 of 20 in Acts III and IV with zero
in Act II; planted orthography is 9 of 10 in Act II and zero in Acts III and IV. Whichever channel
carries the marks, the other cannot supply a per-act partner.

The injected capitals in document order are M (¶73), L, L (¶126), I (¶128), I (¶136). The tail is
two `I`s. Under the block-29 device, where interior capitals spell a name, that reads `II`, which
is the "Second" of the chapter title and of Harold Thomas Finney II. Interpretive, not derived.

## 4. The four live uses derived

| set | reason | derivations | hits |
|---|---|---|---|
| {20, 42, 220, 273} | the four live uses | 36 | 0 |
| {20, 42, 222, 273} | Hal's own sentence substituted | 36 | 0 |
| {20, 42, 244, 273} | the quoted line substituted | 36 | 0 |
| {20, 220, 244, 273} | four act-closers | 36 | 0 |
| {20, 206, 220, 273} | the signs-ending variant | 36 | 0 |

Strict transport, capitals 1344 → 1344 in every case, four serialisations, indices
0/1/2/44/76/77.

## 5. The hybrid channel derived

If Act II's member must come from the planted orthography, the prose-internal candidates are ¶128
and ¶136, both injecting `I`. Selection {20 or 42} × {128 or 136} × {220 or 222} × {273} = 8 sets,
three modes each: certified edge transport on all four, repair the Act II anomaly and transport the
other three, and repair alone.

**8 sets × 3 modes = 96 texts, 864 derivations, 0 hits.**

The letters make the outcome structural rather than accidental. ¶128 is `V…l`, ending on "fuel",
and ¶136 is `B…s`, ending on "emissions". Every other candidate in the pool is `I…s`, `A…s` or
`T…s`, because four of them end on the literal word "signs". So the finals of any hybrid set are
`s l s s` or `s s s s`, never `stnm`, and the initials are one of `IVAA`, `IVTA`, `IBAA`, `IBTA`,
never `FFWW`. No member choice within this pool can produce the signature, so the hybrid reading is
closed by its own letter inventory, before any derivation.

## 6. What survives

- The per-act distribution is real and disjoint, and it is the cleanest structural fact found in
  this pass.
- The four live uses are a natural cardinality-four set, and they are not the marks.
- Act II's participation cannot be mediated by a paragraph edge, because its two planted tokens sit
  in a `V…l` and a `B…s` paragraph.
- Untouched: which sentences carry signs, and how many. The census narrows the vocabulary to 18
  sentences and shows that the vocabulary is concentrated where the rule is being *explained*,
  which is the material the format says to leave unchanged.
