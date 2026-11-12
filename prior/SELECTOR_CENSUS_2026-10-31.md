# Which four paragraphs: both candidate selectors closed, plus the one ¶229 states

**Date:** 2026-10-31
**Base:** `wp_paras_br.json`, mixed, md5 `bd07e6ee…`, 46,000 bytes, 273 spans, self-check clean.
**Script:** `sweeps/selector_census.py` (results in `sweeps/selector_census_results.json`).
**Derivations run:** none. This is a text-structure census only, so nothing here interacts with the
`2d0d100` negative.

## The one-line result

Neither scan produces four. Scan A produces 210, Scan B produces 10 (7 after removing quoted
paragraphs), and the reason neither can be pruned to four is the same and it is decisive: **the
`FFWW`/`stnm` site exists exactly four times in the whole chapter, and all four are the known
windows.** There is no fifth site to name, under any selector, anywhere in 273.

## Scan C first, because it decides the other two

Every one of the 273 paragraphs classified by (first letter, last letter). Nothing sampled.

| class | total | in the four windows | outside |
|---|---|---|---|
| `F…s` | 5 | 4 | **¶100** |
| `F…t` | 4 | 4 | **none** |
| `W…n` | 9 | 4 | ¶52, ¶139, ¶152, ¶157, ¶265 |
| `W…m` | 5 | 4 | **¶30** |

A fifth sign block needs one paragraph from each row. `F…t` has nothing outside the windows, so a
fifth site must include one of the four `F…t` paragraphs: **containment**, not uniqueness. Contiguous
sites are exactly the four windows. Scattered sites are not — the `s`, `n` and `m` members can be
drawn from anywhere, and there are 61 of them, each anchored on ¶6, ¶94, ¶169 or ¶232. All 61 have
since been derived negative; see `FT_CLOSURE_2026-10-31.md` (`dd0740d`), which corrects this section.
This is not a sampling result: it is the whole space, one pass, no derivation.

Consequence for `2d0d100`: the negative was stated over a 16-paragraph union. It now holds
chapter-wide. Any *different* four paragraphs the author may have meant must have paragraph-final
letters other than `s t n m`, because those four letters cannot be assembled a fifth time.

## Scan A: lexical openers (the "narrative echo" hypothesis)

Paragraph openers in the chapter:

| opener | paragraphs |
|---|---|
| `Fast` | **¶232 only** |
| `For` | ¶6, ¶93, ¶100, ¶102, ¶106, ¶120, ¶168, ¶231 |
| `When` | ¶7, ¶8, ¶48, ¶95, ¶96, ¶233, ¶235, ¶259 |
| `While` | ¶170, ¶171 |
| `First` / `Fairly` / `Face` | ¶5 / ¶94 / ¶169 |

Two things follow.

1. **"Fast forward" is not an authorial opener.** It occurs as a paragraph opener exactly once in
   273 paragraphs, at ¶232, which is the `hal_original.txt` reprint. The comparative table's
   "temporal anaphora: both F paragraphs open with a purpose preposition followed by an explicit
   chronological advance" does not hold for W1, W2 or W3. The F paragraphs there are `First` (¶5),
   `For` (¶6), `For` (¶93), `Fairly` (¶94), `For` (¶168), `Face` (¶169). The W paragraphs are
   `When` (¶7, ¶8, ¶95, ¶96) and `While` (¶170, ¶171).
2. **At letter level the rule is far too permissive to be a selector.** 25 non-window paragraphs
   start with `F` or `W`, and they contain **210** `F,F,W,W` quartets in document order. That is not
   a low-cardinality candidate set; it is a filter that has stopped filtering.

The one real textual echo across the independent windows is not the template's *structure*, it is
its *opener formula*: "For those who don't know me" appears at ¶6, ¶168 and ¶231 (`¶231` being Hal
Finney's own sentence). Two copies plus the source, and W2's ¶93 is `For starters`. That is
consistent with the author seeding the windows by hand from the Finney paragraph she was reading,
which is the same conclusion the W4 overlap already forced: the windows are copies of a source, so
they carry no independent information about a selector.

## Scan B: terminal directive clauses (the ¶236 anchor as a locator)

| filter | n | paragraphs |
|---|---|---|
| directive vocabulary anywhere | 29 | — |
| **final sentence** carries it | 18 | 20, 42, 107, 193, 195, 196, 206, 214, 220, 222, 226, 227, 228, 236, 240, 244, 246, 273 |
| final sentence ends on `sign`/`signs` | 10 | 20, 42, 206, 220, 222, 226, 227, 244, 246, 273 |
| …minus paragraphs that are themselves quotations | **7** | 20, 206, 220, 226, 227, 246, 273 |

¶42, ¶222 and ¶244 are quoted paragraphs (¶222 is Hal Finney's ¶7 verbatim, ¶244 is the four-word
quote on its own line). Applying the W4 standard to them removes three of the ten. Seven is closer
to a candidate set than 210, but seven is not four, and no rule tested here divides seven by
anything.

That 7-vs-4 gap is the honest state of the ¶236 anchor: **¶236 tells you where in a paragraph to
look once you have decided a paragraph is a sign, and it says nothing about which paragraphs those
are.** The user's own `GEOMETRY_RESOLVED_2026-10-31.md` reached the same place from the derivation
side. This census confirms it from the text side.

## Scan D: the selector ¶229 actually states

¶229: *"All paragraphs except for four, which start with F F and W W."*
¶230: *"we are directed to look at those four paragraphs, the only ones where we don't recognize the
signs. Those paragraphs are (with one paragraph starting with I in between):"*

This is a **rule**, not just a description, and it can be checked on its source. `hal_original.txt`,
16 paragraphs:

```
initials  I F F W I W T A T S M A T I A T
tails     e s t n g m s s s g t n s n o y
```

Twelve paragraphs start with a letter from `{I, T, A, S, M}`. Exactly four do not: ¶2 `F`, ¶3 `F`,
¶4 `W`, ¶6 `W`. Their paragraph-final letters are `s t n m`. And ¶5, which starts with `I`, sits
between the two `W`s, which is precisely ¶230's parenthetical.

So ¶229–¶230 are verified verbatim against the primary source, and the rule they state is:

> the four sign paragraphs are the paragraphs that **break** a dominant initial-letter alphabet.

Applied to the rest of the corpus (all 31 posts in `wparts/`, split again at every bold heading, so
63 documents of eight paragraphs or more, plus `hal_original.txt`), the only documents where exactly
four paragraphs break the initial alphabet and spell `F F W W` with tails `s t n m` are:

| document | n | quartet | tails | complement alphabet |
|---|---|---|---|---|
| `hal_original.txt` | 16 | ¶2, ¶3, ¶4, ¶6 | `stnm` | `A I M S T` |
| "Second" / 2. The Satoshi Code | 10 | ¶4–¶7 (= ¶168–¶171) | `stnm` | `A I O S` |

The second one is W3 in its own section: its quartet is ¶168–¶171. It is not a new site. Of the 63
documents scanned, only **two** contain a four-paragraph `F F W W` exception structure at all, and
both spell `stnm`; the other is the block that contains the Finney reprint (W4). Block labels in this
scan are approximate because headings are excluded from the paragraph sequence, so the corpora were
matched by paragraph text, not by heading name.

The rule also cannot be pointed at the 273-paragraph chapter as a whole. `{I, T, A, S, M}` covers
154 paragraphs once the ten lettered subheadings (`a)` … `f)`) are case-folded, and 118 fall outside
it (119 counting the one paragraph with no letters). An earlier draft of this section said 152/121
because it did not fold those ten; `dd0740d` §4 has the correct inventory. Per section, the numbers of exceptions to the best
five-letter alphabet are 20, 3, 4, 0, 5, 5, 6, 0, 4, 0, 2, 12, 6, 0. No section has four. ¶229's
scope is the Finney post, and it stays there.

## ¶234: the correction is right and the mechanism is sharper

`hal_original.txt` ¶2–¶6 map one-to-one onto ¶231–¶235 of the chapter, in order, with no omission:
¶234 **is** Hal ¶5, *"I was more positive…"*, and its initial is `I`.

So the reprint does not skip the `I` paragraph, it includes it. It is the *window* that skips it,
and the reason is ¶230's parenthetical: the four are the `F F W W` ones, `with one paragraph
starting with I in between`. The exclusion is **prescribed by the stated rule**, not inherited by
copying an omission. That is a stronger version of the user's point: ¶234 was never a control,
planted or otherwise, and its exclusion is a documented instruction.

## What this closes and what it leaves

Closed, from the text side, matching the derivation side:

- the windows as mark carriers (already closed by `2d0d100`)
- the edge-letter geometry as a **locator** for any other four paragraphs (new: census above)
- lexical openers as the selector (210 quartets: not a selector)
- terminal directive vocabulary as the selector (10, or 7 after removing quotes: not four)
- ¶229's exception rule as a selector for the chapter (no section has four exceptions)

Left open, unchanged: **which sentences carry signs, and how many.** The census adds one specific
thing to look at there. ¶238 is the only paragraph that pairs a sign with an adjacency claim:

> *"Combined with the I as the first letter in the paragraphs close to that. The paragraph containing
> the words 'I made an attempt to make my own proof-of-work based currency, called Bitcoin.'"*

That is Hal ¶5 again (with RPOW misquoted as Bitcoin), and the `I`-adjacency is the "in between"
paragraph from ¶230. If ¶238 is meant to generalise past the Finney post, the locator it describes is
not a letter class but **an `I`-initial paragraph adjacent to the block**, which is a different kind
of rule and one that has not been swept. Worth a look before anything else in the sign pool.
