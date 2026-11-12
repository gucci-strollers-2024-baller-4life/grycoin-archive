# The act census, run: the mutual exclusion survives in its important direction, and three cells do not

**Date:** 2026-10-31
**Script:** `sweeps/act_census.py`, results in `act_census_results.json`.
**Basis:** `wp_paras_br.json`, 273 paragraphs, four act ranges as given (1–92, 93–167, 168–230, 231–273).

The thesis is that the semantic directive channel (`sign*`) and the planted orthographic channel are
mutually exclusive across the chapter, which is why every single-channel macro-filter collapsed. **That
survives**, and the three cells supporting it reproduce exactly. Three other cells do not, and one of
them inverts a boundary inference.

## 1. What reproduces exactly

| check | result |
|---|---|
| `sign*` tokens in Act I | **2**, at ¶20 *"I recognize the signs."* and ¶42 |
| `sign*` tokens in Act II | **0** |
| case-odd tokens in Act III prose | **0** |
| case-odd tokens in Act IV prose | **0** |

The semantic channel is genuinely silent across 68 prose paragraphs, and the orthographic channel is
genuinely absent from 92 prose paragraphs. Mutual exclusion is real, and it is the explanation for the
macro-filter failures.

## 2. The census, as measured

Two sentence figures are given because the splitter matters: `sentQ` splits before a quote after a
terminal mark (the demo's own dialogue-heavy convention), `sentP` never does.

| act | range | prose ¶ | chars | sentQ | sentP | `sign*` | `sign*` ¶ | case-odd (prose) |
|---|---|---|---|---|---|---|---|---|
| I | 1–92 | **85** | 9,106 | 206 | 202 | 2 | 20, 42 | 1 |
| II | 93–167 | 68 | 17,985 | 189 | 189 | 0 | — | **9** |
| III | 168–230 | 58 | 10,436 | 136 | 134 | **13** | 177, 206, 220, 222, 223, 225, 226, 227, 228, 230 | 0 |
| IV | 231–273 | **34** | 6,821 | 90 | 89 | **6** | 236, 240, 244, 246, 273 | 0 |
| sum | | **245** | 44,348 | 621 | 614 | **21** | 17 paragraphs | 10 |

Non-prose, itemised so the count is auditable: 17 headings (¶1, 2, 3, 54, 71, 89, 91, 115, 130, 152,
157, 161, 163, 164, 175, 247, 265), 10 `a)`–`f)` labels (¶176, 182, 209, 215, 250, 252, 254, 256, 258,
260), and ¶237 `STNM`. That is 28, hence 245 prose.

## 3. What does not reproduce

**Prose counts.** 85/68/58/34 sums to 245, not the 244 with 83/68/58/35. Act I is two higher and Act IV
one lower than stated. And 244 cannot be reached under any single rule I can find: excluding ¶239
`I STNM.` as well gives 244 in total but puts Act IV at 33; counting ¶237 and ¶239 as prose puts Act IV
at 35 but takes the total to 246. So at least two cells of the prose column are wrong, in a way that no
consistent definition reconciles.

**Sentences.** 621 (prose only, quote-splitting), 614 (prose only, conservative), or 664 (all 273
paragraphs including headings). The stated 627 is not any of these; it appears to be a prose-plus-partial
mix. Since sentences are the unit of the last sweep (`dce5ae2`), the number used matters, and 621 is the
defensible prose figure.

**`sign*` counts.** 13 tokens over 10 paragraphs in Act III, 6 tokens over 5 paragraphs in Act IV, against
the stated 11 and 7. Neither token counting nor paragraph counting yields 11 and 7. The totals differ by
one (21 against 20).

**Case-odd tokens.** Act II is 9 by my tokeniser, not 11. The nine, classified:

| ¶ | tokens | what it is |
|---|---|---|
| 106, 112 | `WorldWideAbsoluteCarbonBudget` ×2 | the author's own camel-case project name |
| 107 | `FUCKFuckFUCK…X`, `AndrewYangForPresident`, `oXXX` | a burn-message example line |
| 126 | `abcdefghijkLmnopqruvwxyz`, `abcdefghijkLmnopqrstuvwxyz` | alphabet strings, the first missing `s` and `t` |
| 128 | `VIrgin` | **internal-capital plant** |
| 136 | `BItcoin` | **internal-capital plant** |

Only two of the nine are plants in the narrow sense. Acts III and IV prose are zero either way. Act I is
1 (`ppM` ¶73) plus two hyphenated compounds my tokeniser flags and a narrower rule would not
(`Paloecene-Eocene-Thermal` ¶49, `Peer-to-Peer` ¶88).

Note that **9 + 2 = 11**, and the two missing tokens are `BITcoin` and `AHScoin` at **¶209**, which is
in Act III and is a label: *"c) BITcoin is actually AHScoin"*. If the stated 11 is the raw count
including labels, then it is not an Act II number, and the paragraph that inflates it is the one that
breaks the exclusion (§5).

## 4. The two boundary carriers are anomalies, not carriers, and the inference inverts

This is the consequential one. The stated openings and terminals for both paragraphs do not match the
text:

| ¶ | stated | actual |
|---|---|---|
| 128 | opens *"And the sixth one is…"* → **A**; closes *"…would make it work."* → **k** | opens **V** — *"VIrgin bitcoins are the only source of grycoins."*; closes *"…and by extension to the burning of fossil fuel."* → **l** |
| 136 | opens *"In fact, the first…"* → **I**; closes *"…was still possible."* → **e** | opens **B** — *"Before BItcoin, there were remailers."*; closes *"…setting a global cap to carbon emissions."* → **s** |

`V` and `B` are both **outside** `{A,I,M,O,S,T}`. So under the unified alphabet ¶128 and ¶136 are
**out-of-class anomalies**, i.e. exactly the class that carries signs. The stated conclusion — *"both
paragraphs are in-class carriers … neither qualifies as an out-of-class anomaly"* — is inverted.

The inversion helps the thesis rather than hurting it. Act II is the pure orthographic channel, so if any
Act II paragraph is to route into a sign set, it has to be one of these two. Under the correct
classification, both are available as sign units, and the routing needs no new rule: the author's own
internal-capital plants sit in them, and they are already anomaly-class. What the inversion does kill is
the claim that Act II contributes nothing to a bridging 4-unit set on boundary grounds.

## 5. The exclusion leaks in exactly one place, and it is thematically pointed

`¶209 "c) BITcoin is actually AHScoin"` is in Act III and contains two internal-capital tokens. It is a
label, so the prose filter drops it, and that is why the prose census shows zero in Acts III–IV. But the
claim as stated — *"Acts III and IV contain zero internal casing corruptions"* — is only true of prose
paragraphs. The author puts a case plant in a subheading of the semantic half, and its content is the
`BITcoin`/`AHScoin` anagram thesis.

Including headings and labels, the chapter's case-odd paragraphs are: ¶73, 106, 107, 112, 126, 128, 136,
**209**. So the orthographic channel is not absent from Act III. It is absent from Act III *body text*.

## 6. The three plants' edge signatures, and one that matches

Every genuine plant sits in a paragraph whose (initial, final) pair is:

| ¶ | plant | initial | final | edge-matched? |
|---|---|---|---|---|
| 73 | `ppM` | T | t | **yes** — same letter, opposite case |
| 128 | `VIrgin` | V | l | no |
| 136 | `BItcoin` | B | s | no |

¶73 is a `T…t` pair, which is the same shape as `F…f` and `W…w` in the windows and `s…s`, `t…t` in the
`stnm` terminal reading: the head and tail are the same letter in opposite case, so lowering the head and
raising the tail is a strict-conservation unit with both moves real. The other two plants are not
edge-matched. Recorded as an observation, not a derivation.

## 7. What the census does not establish

No 1+1+1+1 partition is derivable from the lexical instruction. That part of the claim holds: with Act II
carrying zero `sign*` tokens, any rule that reads "recognize the signs" cannot span the text. But it
should be recorded that the section boundaries themselves are still not derived from anything. The
author's own part headings are `I. Second Life` at ¶2 and `III. Second Identity` at ¶163, and there is
**no `II.` heading anywhere** in the chapter, so the text labels two of its parts and leaves the middle
unmarked. The four acts used here are a partition imposed for testing, not one the text declares: Act
III as defined (168–230) begins five paragraphs *after* the author's own `III` heading at ¶163, and the
1–92 / 93–167 line falls inside the Grycoin spec between ¶92 and ¶93 rather than at any structural
boundary. That does not sink the mutual-exclusion result, which holds for the partition as imposed, but
and `PAYLOAD_AUDIT_2026-10-31.md` §5 remains the record on section-level codes: 81 distinct four-anomaly
codes, no section definition anywhere, `GFVE` and `WVWB` non-discriminating.

## 8. The external vectors

Answered in `PAYLOAD_AUDIT_2026-10-31.md`, and unchanged: the repository holds **no** raw capture of the
2008 announcement, the v0.1 release post, the 2009 "conventional currency" post, the genesis coinbase
heading or its scriptSig hex, or the whitepaper. Two external primary documents exist, `hal_original.txt`
and `hal_post.html`. For §4 indexing, `gh_leads.md` states the method is confirmed on blocks 56–58 but
that the corpus for block 76 was never identified; its one untried candidate that is also in-repo is the
author's own numbered posts, all 33 of which are present in `corpus.json` and `wparts/`. That method
finds what a block asks, not what stage two hashes.

## 9. State

Confirmed: mutual exclusion of the semantic and orthographic channels, in prose.
Corrected: prose counts (245 not 244, 85/68/58/34), sentence count (621 not 627), `sign*` tallies
(13/6 not 11/7), case-odd tallies (9 raw / 2 plants not 11), and the classification of ¶128 and ¶136
(both anomalies, V and B, not carriers).
Leaked: the orthographic exclusion, at ¶209, in a label.
