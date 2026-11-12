# Block 76/77 indexing against `corpus.json`, and what the block 77 snapshot actually contains

**Date:** 2026-10-31
**Script:** `sweeps/part_index.py` (results in `part_index_results.json`)
**Derivations:** none new. Everything below is counting and reading.

## 1. How the 33 parts are indexed, and why the index is ill-defined

`corpus.json` is a dict of 33 entries keyed by Wattpad post ID, ordered ascending by that ID.
There is no block number, no ordinal field, and no author-supplied sequence: the order is just the
post ID order, which is publication order for a Wattpad series.

The list is **not a partition of 33 units**. Paragraph-level overlap:

| measure | value |
|---|---|
| paragraph instances ≥ 40 chars | 1,337 |
| distinct paragraphs | 1,236 |
| instances that repeat another part | 101 (7.6%) |
| distinct paragraphs appearing in more than one part | 89 (7.2%) |

Two entries are compilations that contain other entries: ord 6 "Complete Quizchain" (766 ¶, of
which 66 repeat elsewhere) and ord 23 "Complete Second Round" (367 ¶, 63 repeats). The chapter
itself, ord 1, shares 23 paragraphs with other parts. "Part N of 33" therefore has no stable
referent; any modular scheme lands on an ordinal whose contents are partly duplicated in two
superset entries.

## 2. Where 76 and 77 land

| reading | 76 | 77 |
|---|---|---|
| `N mod 33` as 0-based ordinal | ord 10 → 722270069 **Satoshi's Stash** | ord 11 → 724030807 **Satoshi's Real Identity** |
| `N mod 33` as 1-based position | ord 9 → 721795188 Tragic Boating Accident | ord 10 → 722270069 Satoshi's Stash |
| `(N-1) mod 33` as 0-based ordinal | ord 9 → Tragic Boating Accident | ord 10 → Satoshi's Stash |
| `(N-1) mod 33` as 1-based position | ord 8 → 721505724 TOMI | ord 9 → Tragic Boating Accident |

The distinct landing pool is four posts: Satoshi's Stash, Satoshi's Real Identity, Tragic Boating
Accident, TOMI.

The 0-based reading is the only one that produces a non-trivial convergence: 77 → **Satoshi's Real
Identity**, which is the document title the chapter's own acrostic extraction ends in (`"Today,
I"` / `"Satoshi's real identity, recognize the signs"`, ¶243–¶246). Two cautions. First, that post
is block 60's post, and its answer is "Tom Marvolo Riddle"; nothing in it touches block 77's
ciphertext. Second, the corpus holds roughly eight identity-themed posts, so landing on one of them
is not a rare event. Satoshi's Stash is a joke post about the million-bitcoin rumour that ends "If
Satoshi's stash exists in the first place and can still be found somewhere, you need to look
somewhere else."

## 3. Does any part carry a four-anomaly set under `{A,I,M,O,S,T}`?

Four of the 33 do, and none carries the signature:

| ord | post | part | anomalies | initials | finals |
|---|---|---|---|---|---|
| 5 | 720893344 Utter Disaster Three Block Series | ¶4, 6, 8, 11 | `FFNW` | `knnn` |
| 7 | 720895609 4444 and 4442 | ¶2, 8, 11, 13 | `BBBW` | `ssel` |
| 26 | 752631800 Quizchain and AI | ¶1, 9, 10, 11 | `BWWW` | `rtes` |
| 30 | 760378354 Waking Up | ¶5, 6, 10, 14 | `BWBN` | `eoot` |

Four hits in 33 parts at 12% is the chance rate. `FFNW` shares its first two letters with `FFWW`
and dies on the finals, `knnn`; the letter-inventory argument that closed the hybrid channel
applies unchanged.

None of the four candidate landings from §2 is one of these: Satoshi's Stash has 2 anomalies
(`DG` / `es`), Satoshi's Real Identity has 3 (`HWB` / `dsy`), Tragic Boating Accident 2 (`UB` /
`le`), TOMI 3 (`WPN` / `ttd`). So the "the indexed part contains the four units" prediction fails
on every reading of the modulus.

## 4. What the 440 KB snapshot is

`ca6jxv_arch.html` (440,495 bytes) is not the block 77 post. It is the archived **comment page**
for `r/Grycoin/comments/ca6jxv/`, "[77 mbtc] Quizchain2 Block 77 (Stage One)", captured
2020-07-28. Checked for submission machinery and found none: no `<form>`, no `<input>`, no hidden
fields, no query parameters carrying a block index, no data attributes describing a submission
format. The only form on the page is archive.org's own URL box.

What it does hold is one substantive exchange: a player's complaint that the block cannot be solved
without a hint, and **the author's reply**:

> "I am quite sure that it is impossible to write a script solving this block. Actually there is a
> hint on how to solve this right in the post by Hal. Much like the Aa in the genesis block address
> hinted at the solution."

Two things follow, and both are new primary-source evidence rather than inference:

**The route is a reading, not a search.** "Impossible to write a script solving this block" is the
author saying the space is not to be enumerated. That is an independent constraint against every
sweep in this repo, including the ones run today, and it is the strongest statement in the record
that the answer is a rule a human applies.

**"The Aa in the genesis block address" is a description of her own teaching device.** The genesis
address `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` opens on a capital `A` and closes on a lowercase `a`.
She names that head-capital/tail-lowercase pair as the thing that "hinted at the solution". That is
the same eligibility condition the transport rule requires, first letter upper and last letter
lower, and it says the hint is carried by the edges of an example rather than by a phrase about it.
If the chapter hints the same way, the hint is an edge pair in the text, not a sentence containing
the word "sign".

The same reply offers "another rapid fire hint session on the last Sunday of this experiment".

## 5. The Wattpad page's own metadata

`rebuild_page.html` carries the author's page tags:

```
<meta name="description" content="Read story Second by AoiNakamoto with 6,825 reads. hintforblock77. …">
<meta name="keywords" content="hintforblock77,Science Fiction,eBooks,reading,stories,fiction">
```

The chapter is tagged `hintforblock77` by its own author. It is the hint for block 77, in her own
metadata, not a decoy and not a manual for a payload held elsewhere.

## 6. Leads this opens

1. **The rapid fire hint session.** The author says she ran one on the last Sunday of the
   experiment, and `corpus.json` contains nothing matching "rapid fire" or "hint session". Those
   r/Grycoin threads are a direct-quote channel about block 77 stage two and are not in the corpus.
2. **Edge pairs as hints.** If "Aa" is the device, the chapter's hint should be a paragraph whose
   first letter is a capital and whose last is a lowercase of the same letter. Counted: **ten**
   paragraphs qualify, and every one of them is head-upper/tail-lower, none the reverse.

   | ¶ | pair | opening |
   |---|---|---|
   | 9 | `Nn` | "Next I check my body movements…" |
   | 46 | `Tt` | "This time? I was not aware…" |
   | 73 | `Tt` | "Tell me more about your solution…" |
   | 77 | `Tt` | "There are two ways to make sure of adoption…" |
   | 86 | `Tt` | "The scene changes again…" |
   | 140 | `Tt` | "They will be restricted in their decisions…" |
   | 172 | `Ss` | "So I feel it is best to stay anonymous…" |
   | 195 | `Tt` | "The movie 2001: An Odyssey in Space…" |
   | 218 | `Tt` | "That would be exactly what one would expect Satoshi…" |
   | 228 | `Tt` | "Turns out, there are some signs we recognize…" |

   Ten sites is not a selection, and seven of them are `Tt`, which is what `T`-initial paragraphs
   ending on "it" or "that" produce anyway. The only mildly remarkable members are ¶172 `Ss` and
   ¶9 `Nn`, and the set of distinct pairs is `N, S, T`, with no `M`. Worse for the idea, the
   reverse shape, tail-upper/head-lower, which is what the transport *produces*, occurs nowhere,
   as L5 established. So the "Aa" hint is best read as the author explaining the operator on an
   example whose edges demonstrate it, not as a locator she planted ten times in the chapter.
