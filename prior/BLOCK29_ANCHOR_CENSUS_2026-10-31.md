# Block 29 as the template: the anchor is a one-letter sentence opener, and the chapter has only one

**Date:** 2026-10-31
**Script:** `sweeps/block29_spelling.py`
**Ledgers:** `block29_spelling_{int,any}_*_results.json`
**Total this pass:** 13,076 candidates, 117,684 address-verified derivations, 0 hits, 0 duplicate md5.

## 1. The template, stated exactly

Block 29's answer is the block text with one word changed:

```
A pleasant female voice.        ->  A pleasant female vOIce.
```

and the block then *names* what that spells, in dialogue: "How about Aoi?", "Third most popular name
for Japanese girls", "Artificial Omnipotent Intelligence, obviously."

Read as an instruction, that fixes three things and only three:

| part | in R1:29 |
|---|---|
| **anchor** | the sentence's first letter, which is also the name's first letter — here the one-letter word `A` |
| **marks** | the remaining name letters, set as capitals at occurrences already present *inside* words — `o` and `i` inside `voice` |
| **everything else** | untouched. Nothing is lowered, nothing is inserted, no edge moves |

That is a different geometry from the demo's (paragraph-first **down** + sentence-final **up**): additive,
word-interior, and anchored on the *sentence*. The distinction is worth stating once because it is what
decides everything below.

## 2. Mapping the rule onto the demo: nothing drops out, and it is not luck

The demo edits demo ¶5 to `i expected … outing himselF`. Read through the template:

| reading | string it yields |
|---|---|
| anchor + marks | `I` + `F` = **IF** |
| marks only (anchor unmarked, as the author instructs) | **F** |
| marks across all four marked paragraphs, in text order | **SFIS** |
| anchors across all four marked paragraphs | **FIOW** |

None is a name, and the four-paragraph version is the 8-change text already derived (§8 of
`GRAMMAR_AUTOPSY_2026-10-31.md`): md5 `13082a45…` / `0f69c8ea…`, neither of which begins `3c6`.

The reason is structural, not statistical. **The template needs a sentence that opens on a one-letter
word**, because that is the only way the anchor can be both the sentence's capital and the name's first
letter without changing anything. Counted on both texts:

| text | sentences opening on a one-letter word |
|---|---|
| chapter, 273 ¶ | `I` ×81, `A` ×3, and the list markers `a`–`f` (2 each, `B` 1, `e` 1, `f` 1) |
| demo, 10 ¶ | `I` ×3 (¶1, ¶5, ¶9). **No `A` opener at all.** |

So a block-29 name inside the demo would have to begin with **I**, and no candidate name in the hunt
does. The demo cannot host this template, by construction. That is the answer to "what name drops out
of the demo": none, and the demo's own sentence-inventory is the proof rather than a failed search.

## 3. The chapter: exactly one name is expressible, and it is already closed

The chapter's three `A`-opening sentences carry one, two and one interior `o…i` pair. Complete inventory:

| ¶ | embedding | shape |
|---|---|---|
| 12 | `A pleasant female v**OI**ce.` | anchor `A` + interior `o`, `i` — the certified one |
| 19 | `A p**O**pular name for Japanese g**I**rls.` | anchor `A` + interior `o`, `i` |
| 19 | `A p**O**pular name for Japanese g**I**rls.` | (second `i` site, same sentence) |

Three embeddings, two paragraphs, one name: **AOI**. Every other candidate name has **zero** instances
of the anchor shape — HAL, STNM, THOMAS, FINNEY, SATOSHI, GRYCOIN, SECOND, NAKAMOTO all begin with a
letter for which the chapter has no one-letter sentence opener (only `A` and `I` exist). And the AOI
family is already closed byte-exact: `sweeps/aoi_chapter_byte.py`, 53,787 candidates, published base,
zero.

**This is the clean result of the pass.** Taking block 29 literally, the chapter is capable of spelling
exactly one word, `AOI`, in exactly two paragraphs, and that lane was already swept. The template does
not open the chapter; it closes it.

## 4. The chapter writes the template out for you, and that was untested

¶237 is a paragraph consisting of the string `STNM`. ¶239 is a paragraph consisting of `I STNM.` — a
one-letter word followed by four capitals, which is precisely the block-29 shape: **anchor + marks**.
¶240 then says it "dovetails nicely with 'Nm ST'". So the chapter's own text asserts a five-character
answer string, and the hunt has only ever treated `STNM` as the four-letter signature.

Treated as a spelling target, `ISTNM` and its variants run:

| name | anchor | candidates | hits |
|---|---|---|---|
| `ISTNM` | `I` (81 openers) | 184 | 0 |
| `NMST` | `N` | 0 | 0 |
| `ISTNMS` | `I` | 0 | 0 |

`NMST` returning zero is itself informative: no sentence in the chapter begins with `N` *and* carries
`M`,`S`,`T` in order inside words, so the ¶240 gloss cannot be a marks-string on this base.

## 5. The relaxed reading, and its numbers

Dropping the one-letter-word requirement — the sentence's first *letter* is the anchor, marks stay
interior — gives a family that no earlier sweep covered, because `name_marking_word_edges.py` was built
to allow **word-edge** positions only (728,072 derivations) and `aoi_chapter_byte.py` covered AOI alone.

| name | interior-mark candidates | hits |
|---|---|---|
| AOI (control, already closed) | 1,642 | 0 |
| HAL | 196 | 0 |
| STNM | 282 | 0 |
| THOMAS | 482 | 0 |
| FINNEY | 8 | 0 |
| SATOSHI | 2,130 | 0 |
| GRYCOIN | 870 | 0 |
| SECOND | 1,382 | 0 |
| NAKAMOTO | 0 | — |

Serialisations LF/CRLF, indices 0/1/2/5/6/7/44/76/77: **6,992 candidates, 0 hits, all md5 distinct.**
A superset arm (marks at any position, not only interior) was run for the four short names and AOI:
**5,414 candidates, 0 hits.** The superset arm for THOMAS, SATOSHI, GRYCOIN and SECOND is open
(43,848 candidates, about twelve minutes at 590 derivations/s) and is the only unfinished piece here.

## 6. The one thing the template did reveal: the demo's marks form a chain, not a spelling

Laid out as anchor→mark per marked paragraph:

| ¶ | anchor (lowered) | mark (raised) |
|---|---|---|
| 4 | F | S |
| 5 | I | F |
| 6 | O | I |
| 8 | W | S |

Two of the raised letters are the *next* paragraph's lowered anchor: ¶5 raises `F`, which is ¶4's
lowered anchor; ¶6 raises `I`, which is ¶5's lowered anchor. Reading the chain the way it links gives

```
¶6 (O -> I) -> ¶5 (I -> F) -> ¶4 (F -> S)      and  ¶8 (W -> S)
```

i.e. an order **6, 5, 4** — not the text order 4, 5, 6 — ending on the same `S` that ¶8 also terminates
on. Under block 29's template a mark is a *name letter*, so a chain of marks that hands each letter to
the next paragraph is a different device from spelling: it is a **sequencing rule**, and the paragraph
order it implies has never been used by any sweep in the repo (every family so far marks a *set*, in
text order, and never re-orders the paragraphs before serialising).

That is the only testable lead this pass produced: the demo's four marked paragraphs, serialised in
chain order 6-5-4-8 (and 6-5-4 with ¶8 left alone), under the two mark geometries already in the
harness, on both joins, at the nine indices. Four texts on the demo, screened by `3c6`, is a two-minute
test.

## 7. Verdict

- Block 29's template transfers as **anchor + interior marks**; as a *spelling* device it expresses only
  `AOI` in this chapter, in two paragraphs, and that lane is closed.
- Applied to the **demo** it yields nothing, and the demo's sentence inventory (three `I` openers, no
  `A` opener) makes that structural rather than unlucky.
- The relaxed arms are now negative: 6,992 interior candidates, 5,414 superset candidates, 0 hits.
- The residue is not a name but an **order**: ¶6 → ¶5 → ¶4, because the demo's raised letter in each
  paragraph is the previous paragraph's lowered anchor. That is where the next probe should go.

## 8. Postscript: this does not contradict the paragraph-edge closure, it explains it

`safudev_stage1.txt` (md5 `9dd2efb9…`) certifies stage one as a **paragraph-edge** device: first letter
down, last letter up, on the four paragraphs whose initial is not in {I,T,A,S,M}. See
`BLOCK29_TEMPLATE_2026-10-31.md` §2.

So the two devices are distinct and both now closed on their own terms:

| device | anchor | marks | status |
|---|---|---|---|
| stage one | paragraph | first + last letter of the paragraph | certified by digest (preimage recovered) |
| block 29 | sentence (one-letter opener) | interior letters of the name | AOI only, closed byte-exact; 13,076 candidates here, 0 hits |
| demo | ? | one down, one up per marked paragraph | no 3c6 survivor in any family |

The anchor census is the reason block 29's device cannot be the chapter's: only `A` and `I` open a
sentence as one-letter words in 273 paragraphs, so the device can spell `AOI` and nothing else, and it
does so in two paragraphs, both already swept. That is a structural exclusion rather than another
negative, and it is the useful output of this pass.

## 9. The 44-character string read as an operator spec, and the cross-window test

The certified block-77 round-one solution is

```
1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN          (44 chars)
md5 684b250ea52c1e33a6f6143ded0e62e6 -> 1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP
```

Two halves. The first is forward (`1A1`, `efi2DM` are literal substrings of the genesis address
`1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`, at offsets 0-2 and 11-16); the second is **mirrored**.
Item by item, the mirror is the same operation every time:

| forward | mirrored | what moved |
|---|---|---|
| Satoshi | ihsotaS | letter order, capital to the end |
| Nakamoto | otomakaN | letter order, capital to the end |
| `Nm` | `mN` | capital to the end |
| `ST` | `TS` | letter order |

So the mark is not a toggle but a **transport**: take the capital off the front of a unit and deposit
it at the back of the same unit. Applied to the Finney post at paragraph scale that is *exactly* the
certified stage-one edit (`F…s` -> `f…S`, four times, `9dd2efb9…`). Unit size is the only free
parameter: item (block 77), paragraph (Finney post), sentence (demo ¶5).

**Verified conservation law.** Capital count is invariant under the transport: `hal_original.txt` 174
capitals, `safudev_stage1.txt` 174; `demo_base.txt` 25, its eight-flip answer 25. Block 29 (`vOIce`)
is the outlier: it *adds* two capitals, which is why it is the wrong template for stage two.

**This retires the ¶6 objection I raised in `GRAMMAR_AUTOPSY_2026-10-31.md` §7.** Under the transport
reading ¶6 is not self-contradictory: one capital leaves the paragraph's first letter (`O`->`o`) and
lands on the sentence's last (`i`->`I`), and the sentence's own quoted "I"->"i" is commentary on the
front half of that same move, not a second operation.

**The mirror inside the chapter.** ¶240 quotes the signature as `Nm ST` and calls it the genesis-block
signature. The certified answer contains `TS mN` — the transported form of the same four characters.
The chapter prints the before, the answer prints the after: that is the whole operator demonstrated on
a four-character unit, and it is the intertextual link that does not depend on borrowed prose.

**The untested reading of "two sets of four".** Stage one's answer has four forward items and four
mirrored ones, and the worm in the chapter is that three structurally identical quads (¶5-8, ¶93-96,
¶168-171) all carry the same signature, so the down-set and the up-set need not be the same four
paragraphs. Tested: every ordered pair of windows (and the Finney reprint quad ¶231/232/233/235) as
down-set x up-set, both joins, nine indices.

| | |
|---|---|
| texts | 24 |
| derivations | 216 |
| hits | 0 |

`down=W1 up=W2` … `down=rep up=W3`, all distinct md5, all zero. Cross-window transport is closed.

## 10. The 44-char string as receipt, not salt; and the four-unit family closed

**Composition is contraindicated before it is tested.** The certified round-one hash is
`md5("1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN" + " TOMI Omit TOMI " + <block-44 WIF>)`
= `684b250e…` -> `1FAAKpz…`. That shows the 44-char string's role: it is the **`[solution]` field of
the submission hash**, not a salt on the prize hash. The prize hash is the one certified mechanism,
marked text -> md5 -> BIP39 -> address, reproduced exactly on stage one (`9dd2efb9…` -> `19TbyN5K…`).
Adding the string to the chapter's bytes would be a third construction with no precedent in the corpus.

Tested anyway, on the five principal zero-balance texts, six compositions each (prefix+space, suffix,
bare prefix, bare suffix, and the full certified TOMI template both ways), both joins:

| texts | derivations | hits |
|---|---|---|
| 60 | 540 | 0 |

**The receipt reading is the productive one.** The solution is four items encoded forward and four
encoded mirrored: four head-marks and four tail-marks. The certified stage-one answer is exactly that,
4 paragraphs x (head down + tail up) = 8 edits, net zero. The demo's answer is also 4 paragraphs. So a
"move the capitals" answer in this family has **four units**, not twelve — which parameterises the
"non-binary selector" hypothesis instead of leaving it vague.

The chapter names twelve paragraphs as sign-bearing (¶20, 42, 220, 222, 223, 225, 226, 230, 236, 244,
246, 273). Four of twelve is 495 quads, each one deterministic transported text:

| texts | derivations | hits | time |
|---|---|---|---|
| 990 | 8,910 | 0 | 15 s |

`receipt_four_units.py`, ledger `receipt_four_units_results.json`.

**Where that leaves the selector.** Both selectors the prose actually states are now closed: the eleven
"recognise the signs" paragraphs and their complement the FFWW four. The only *inherited* selector,
stage one's `initial ∉ {I,T,A,S,M}`, is 126 paragraphs = 252 changes, and it is closed as well
(`paragraph/nonITASM`, +6 net). So inheritance and receipt disagree by a factor of thirty-one: the
receipt says four units, the inherited rule says a hundred and twenty-six. That disagreement, not a
missing axis, is the open problem.

**And the upstream anomaly remains.** The demo is unsolved. Its own instruction, applied to its own
certified marked set {4,5,6,8} under transport, yields one text (md5 `13082a45…` LF / `0f69c8ea…` CRLF),
and that text does not begin `3c6`. Every cheaper family on the demo is closed. Until the manual
solves, the exam cannot be read.
