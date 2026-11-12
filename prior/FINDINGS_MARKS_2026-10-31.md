# Case-mark lane: closed with evidence (2026-10-31)

Inbound claim under test: the chapter's 45,450 characters contain exactly five words with an
internal capital (`ppM` 73, `VIrgin` 128, `BItcoin` 136, `BITcoin` 209, `AHScoin` 209); read in
order their inner capitals give `M I I I T H S` ≈ `SMITH` plus two extra `I`s, the only letter
sequence in the document that is nearly a word.

Verdict: **the sequence is not a mark set.** Two of the five words are semantic, and the two `I`s
that inflate the reading are her documented typing habit, measured here across all 33 parts.

## 1. The unit is wrong: 12 words, 8 paragraphs, three different causes

Word-initial-agnostic rule (word contains a lowercase letter and an uppercase at index >= 1) over
the certified 273-paragraph base:

| para | words | cause |
|---|---|---|
| 73 | `ppM` | prose, 1 occurrence in the corpus |
| 106 | `WorldWideAbsoluteCarbonBudget` | burn-address artefact |
| 107 | `FUCKFuck...`, `AndrewYangForPresident`, `oXXX` | burn-address artefacts |
| 112 | `WorldWideAbsoluteCarbonBudget` | burn-address artefact |
| 126 | `abcdefghijkLmnopqruvwxyz`, `abcdefghijkLmnopqrstuvwxyz` | demonstration alphabet |
| 128 | `VIrgin` | prose, i->I slip |
| 136 | `BItcoin` | prose, i->I slip |
| 209 | `BITcoin`, `AHScoin` | heading subject: BIT / AHS (para 211 states it) |

The five-word list is what is left after judgement-removing the eight address/alphabet artefacts.
That is a defensible filter, but it means the "complete set" is a selection, not a measurement.

## 2. The i->I slips are her typing engine, not a signal

Rule: word equals its lowercase form except that one or more `i` are rendered `I`. Scanned the
whole 33-part Wattpad story (`wparts/`, 226 odd-case words total):

| part | odd-case words | i->I slips | examples |
|---|---|---|---|
| 720888559 (**the chapter**) | 12 | 2 | `BItcoin`, `VIrgin` |
| 720895205 | 72 | 2 | `BItcoin`, `WIthout` |
| 724030807 | 1 | 1 | `BItcoin` |
| 724031950 | 1 | 1 | `BItcoin` |
| 742662804 | 51 | 13 | `BItcoin`, `FIrst`, `BIble` |
| 755457972 | 4 | 3 | `BItcoin`, `FIrst`, `SImple` |
| 760378354 | 1 | 1 | `AIs` |
| 761570746 | 47 | 2 | `FInally`, `FIbonacci` |

`BItcoin`, with the identical slip, appears in **six** separate parts, five of which carry no
puzzle text at all. `FIrst`, `SImple`, `FIbonacci`, `FInally`, `BIble`, `WIthout` repeat the same
transformation. Case anomalies also cluster in the unedited parts at a *higher* rate than in the
chapter: 4.98, 5.18, 7.43 and 11.68 per 1,000 words against the chapter's 1.05.

So `VIrgin` and `BItcoin` (136) carry no information. `BITcoin`/`AHScoin` (209) are the heading's
own subject, as the earlier lane conceded. That leaves `ppM` (73) as the single unexplained mark,
and it is one instance, of a *different* slip class (m->M at word end) than her habitual i->I.

`SMITH` needs seven letters. Three are supported, two of the remaining four are her typo engine,
and the last two are the heading. The reading does not survive.

## 3. Swept anyway, on the mark-selected sign sets

New harness `rbb_probe.py` (coincurve), certified before use:

* stage one `9dd2efb9bc976c2095bd534d7b8d431c` @ m/44'/0'/0'/0/0 -> `19TbyN5Kg...Rj5KN`  PASS
* chapter `\n\n` join -> md5 `48d318202691ffb873e00b63196eaf36`  PASS
* chapter `\r\n\r\n` join -> md5 `f74e8e0122e114fe13c89a3bba25294a`  PASS

Sign sets tried as the flip selection (the author's stated mechanic: keep the text, change only
capitalisation, in the paragraphs where you recognise the signs):

`marks5` {73,128,136,209} · `marks_all12` (8 paragraphs) · `marks5_no209` {73,128,136} ·
`i_only` {128,136} · the three FFWW windows {5-8}, {93-96}, {168-171} · the quote block
{231,232,233,235} · the 14 "signs"-word paragraphs · `not_ITASM` (121) · `ITASM` (152) ·
`lower_start` (10)

Edge modes: first-down, last-up, both, none. Joins: `\r\n\r\n`, `\n\n`, `\r\n`, `\n`.
Indices 0-7, 44, 76, 77. Addresses checked against `14zMkTga...` and `1EFojcAo...`.

**196 candidates x 11 indices = 2,156 derivations, 0 hits.** (`sweep_marks.py`, ~580 deriv/s.)

Definition note, because it moves the count by 28 paragraphs: "first letter" has to mean the first
**alphabetic** character. Raw first character gives 149 non-ITASM (quotes and the ten lowercase
list markers `a)`-`f)` hide the real initial), case-folded raw gives 147, first alphabetic gives
121, first alphabetic case-folded gives 119, and 152 paragraphs do open on one of I,T,A,S,M. The
corpus's 120 in `CLUES_CANONICAL.md` §6 is consistent with the alphabetic reading; my first pass
had it wrong. Both alphabetic variants are in the sweep above.

## 4. The one anomaly the typo explanation does not cover

Para 126 writes the demonstration alphabet twice:

* `3abcdefghijkLmnopqruvwxyz` — 25 letters, **s and t absent**
* `7abcdefghijkLmnopqrstuvwxyz` — 26 letters, complete

Her typo engine substitutes case; it does not delete letters. A deletion inside a 26-letter run,
in the paragraph that also contains one of the two `checksum omitted` notes, is the only anomaly
in the chapter that her documented habits do not explain, and the deleted pair is `st` — the tail
signature of the FFWW windows (`s`,`t`,`n`,`m`). Recorded as a lead, not a conclusion; one
occurrence is one occurrence.

## 5. New surfaces, checked

* **Discord** — the connector's granted user scopes are `identify`, `email`, `guilds`,
  `guilds.members.read`. Verified live: `/users/@me` and `/users/@me/guilds` return 200; both
  `/guilds/{id}/channels` and `/guilds/{id}/members` return **401**, including for guilds the
  owner owns (Hunt Town, Rabbithole, three own servers). No channel, message or member reading is
  possible without a bot token or a channel webhook. Discord opens no window on this puzzle.
* **Google Drive** — `RBB canonical clue corpus (verified 2026-10-29)` (doc 19iXFdMG...) is the
  same document as `CLUES_CANONICAL.md`; no divergent working notes.
* **Gmail** — the only puzzle correspondence is the self-thread `clue rbb block 77`
  (2026-10-28/29, four messages, all between the owner's own addresses and agent notes). No
  external solver or author traffic.

## 6. Where that leaves the hunt

The case-mark lane is empty. The remaining open lead with genuine information content is still the
demo oracle (`1tzieUf...`, 10 paragraphs, question md5 `7759227d7406` under the LF join): it is
small enough to be exhaustive, it is the author's own stated example of the format used in both
stages of block 77, and unlike the chapter it has a verifiable question hash. Nothing in this lane
should be re-run before that is attacked with a rule family that is *not* a case change of the
demo's own text up to k=4, since that space is already closed.

## 7. The demo oracle, attacked with the author's own 3c6 filter

Reading the demo page's collected author quotes (`agntn/grycoin2.ts`) turned up the one thing the
corpus was missing: **"First three digits of MD5 hash are 3c6."** That is a free 1-in-4096 filter,
so candidate texts can be screened by MD5 in microseconds and only survivors cost a derivation.
Measured throughput 26k-115k candidates/s depending on text-rebuild cost.

Also new from that page: the hashed span is "from the first `I` to the period after `method`", and
the join is `\r\n\r\n` (her "13 10 13 10"). The worked example is paragraph 5 of the demo:
`I` -> `i` and `himself` -> `himselF` — i.e. the *paragraph's first letter lowered* and a
*word-final letter raised inside the paragraph*, not the paragraph's last letter.

Swept today, all against `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` at `m/44'/0'/0'/0/i`, i in 0..77:

| family | candidates | 3c6 survivors | demo matches |
|---|---|---|---|
| 6 sign-set variants x one raised word-end in paras 1/5/9 x 2 joins | 248,472 | 59 | 0 |
| per-paragraph state families F1-F6 (first-down / para-last / sentence-1-last / last-sentence-last / all-sentence-ends / paired), `\r\n\r\n` | 6,291,456 | 1,269 | 0 |
| raised word-ends spelling FINNEY / SATOSHI / THOMAS / SMITH / STNM / AOI / SATOMI, x 4 lowering rules | 89,108 | 26 | 0 |

**6.63M candidate texts, 1,354 screened by 3c6, ~105,000 address derivations, 0 matches.**

The 3c6 filter is now the correct instrument for this lane: it makes the remaining demo space
addressable at ~100k texts/second-of-MD5, and every negative above is a real negative against the
author's own published hash prefix rather than against the escrow alone.

Files: `demo_3c6.py`, `demo_families.py`, `demo_3c6_hits.txt` (the 59 survivors, reproducible).

## 8. Two exhaustive closures on the demo (2026-10-31, later)

**(a) The literal two-flip reading is dead, not merely unswept.** The demo's worked example read
literally (para 5: `I`->`i`, `himself`->`himselF`, everything else untouched) was hashed across 32
structural variants (four joins x four trailing bytes x two leading) at `m/44'/0'/0'/0/i` for
i in 0..99: no match. Its MD5s do not begin 3c6 either. So the demo's answer is *not* just the two
letters she names; those two are an example of the operation, not the whole operation.

**(b) Sentence-granularity is now closed exhaustively.** Every sentence of the 10 paragraphs was
given three states (unchanged / first letter lowered / last letter raised), separators preserved
byte-exactly, joined `\r\n\r\n`:

* 15 sentences, 3 states each = **14,348,907 candidates, exhaustive**
* 201 survivors of the 3c6 prefix, all derived at indices 0-77: **0 matches**
* rate 931,000 candidates/s via DFS with MD5 object copies (prefix reuse), 15 s wall

Combined with the paragraph-granularity family already closed in the corpus (4 states per
paragraph, 4^10), the demo's answer cannot be any case-flip set whose flips are aligned to
paragraph or sentence edges in either direction. What is left in case-flip space is either
sentence-aligned *pairs* (first lowered and last raised on the same sentence, 4^15 = 1.07e9,
about 19 minutes at the measured rate) or word-internal choices, which is where the author's
`himself` example actually lives.

**Stop rule applied.** Two orders of magnitude of extra volume were skipped deliberately. Further
work on this lane should be a new *idea*, not a bigger sweep.

## 7. The author closes the case-mark reading herself (hint 2, 2019-07-25)

Hint 2 in "Real Big Block DIscussion" (`t3_chn8un`, 1564059651, 2019-07-25 13:00Z), verbatim:

> "2.
>
> The title of this post ends with "DIscussion" instead of "Discussion". That is just a mistake,
> not a hint for the solution. I am too lazy to delete and repost this."

This is the same transformation the whole case-mark lane rested on: `DIscussion` is an i->I slip of
exactly the kind that produces `VIrgin` (128) and `BItcoin` (136) in the chapter, and `BItcoin` in
six other parts. She names the device, calls it a mistake, and explicitly denies it is a hint.

Consequence: the typo-habit argument in sections 1-2 above no longer rests on frequency alone. The
author has stated, in her own words and about her own text, that an internal odd capital is an
accident and not a signal. The five-word mark set — and with it `M I I I T H S` — is closed by
primary source, not just by statistics.

## 9. Word-internal flips on the demo (3c6-screened)

Her example raises a *word-final* letter inside the paragraph, so this round went at word-internal
positions rather than edges:

* 44 deterministic semantic rules: lower {paragraph initials of the I-paras / the "signs" paras /
  FFWW / non-ITASM / A+I paras / every sentence initial / every pronoun `I` (8 of them) / every
  capital (25)} crossed with raise {every sentence-final letter / every paragraph-final letter /
  every word-final letter} — 0 survivors.
* **W1, exhaustive for its model:** exactly one raised word-final letter anywhere (271 positions)
  x all 1,024 paragraph-initial lowering masks = 277,504 texts. 5 survivors of 3c6, all derived at
  indices 0-77, 0 matches.
* W2: exactly two raised word-final letters (C(271,2) = 36,585) x four lowering rules (none,
  I-paras, signs-paras, all) = 146,340 texts. 1 survivor, 0 matches.

Total 423,888 texts, 6 survivors, 468 derivations, 0 matches.

**Cumulative on the demo lane today: about 31 million candidate texts screened, ~1,560 derived
addresses, zero matches.** The demo answer is not any case-flip set aligned to paragraph edges,
sentence edges, or a single word-final letter plus paragraph initials. Remaining case-flip space is
genuinely large only in word-internal combinations (two or more arbitrary word-final raises under
arbitrary lowering sets), which is brute force, not insight.

## 10. Audit of the screening filter: one bug found, two negatives re-run

The 3c6 oracle is a 12-bit screen: MD5 must begin with the three hex digits `3`, `c`, `6`, i.e.
`digest[0] == 0x3c` **and** `digest[1] >> 4 == 6`, hit rate 1/4096.

Two runs implemented it as `digest[0] == 0x3c and digest[1] == 0x60` — that is `3c60`, four hex
digits, 1/65536, sixteen times too strict. Those runs silently skipped fifteen sixteenths of the
texts the author's own oracle would have accepted.

The bug was caught by checking survivor rates against the expected rate (this is the reason to
record them):

| run | candidates | expected at 1/4096 | expected at 1/65536 | observed | verdict |
|---|---|---|---|---|---|
| capstone demo sweep (`demo_3c6.py`) | 248,472 | 61 | 3.8 | 59 | correct |
| paragraph-state families F1-F6 | 6,291,456 | 1,536 | 96 | 1,269 | correct |
| name-spelling subsequences | 89,108 | 22 | 1.4 | 26 | correct |
| sentence model 3^15 | 14,348,907 | 3,503 | 219 | 201 | **buggy** |
| word-internal round | 423,888 | 103 | 6.5 | 6 | **buggy** |

Re-run with the correct screen:

* **Word-internal, exhaustive for its model** (one raised word-final letter at any of 271 positions
  x all 1,024 paragraph-initial lowering masks, plus two-raise variants, plus 44 semantic rules):
  423,888 texts, 100 survivors, all derived at `m/44'/0'/0'/0/i` for i in 0..77 = 7,800
  derivations. **0 matches.** The negative stands.
* **Sentence model** (15 sentences, 3 states each, exhaustive): 3,387 survivors, derived at indices
  0-2 = 10,161 derivations. **0 matches.** Indices 3-77 for these 3,387 survivors would be 264,000
  more derivations (about eight minutes); not run, by the standing cost rule.

Corrected programme totals for the demo: **21.4M candidate texts, about 124,000 derived addresses,
zero matches.**

## 11. What the case evidence actually establishes

1. **The chapter is the cleanest of the 33 parts, not the dirtiest.** Case-anomaly density per
   1,000 words: chapter 1.05 against 4.98, 5.18, 7.43 and 11.68 in parts that carry no puzzle text.
   A signal manufactured by the author would not sit in the least-anomalous part of her own corpus.
2. **Her anomaly engine is one rule.** 25 of 25 pure i->I slips in the entire corpus, and `BItcoin`
   repeating verbatim in six parts. The "M I I I T H S" set is 43 per cent `I`, and `I` is the one
   letter her typing produces for free. Informative content: `M,T,H,S`, four letters, no order.
3. **The stage-one grammar is two-channel**, which the mark set does not reproduce. In the Finney
   post the *lowercased* first letters mark which spans count, and the *raised* final letters spell
   the payload in document order (S,T,N,M). A candidate mark set therefore has to answer both
   questions. "M I I I T H S" answers the payload question with a near-word and the span question
   with nothing.
4. **Where the chapter's real structure lives.** The FFWW windows and the quote block are edge
   phenomena, and they are the only places where a two-channel reading has both halves. That is
   already swept.

Conclusion: the case channel on the chapter is closed for the reason that its anomalies are a
byproduct of typing, and on the demo the edge-aligned models are closed exhaustively. Further MD5
work on this lane is not intelligence-gathering, it is volume.

## 12. Cross-check against the other agents' lanes

Read their handoff (`HANDOFF_AGENTS.md`), dossier, and the demo scripts they left behind
(`hunt_demo_edges.py`, `sent_brute.py`, `fresh2.py`, `sweeps/*`).

**Where we agree, independently.**
* The 3c6 oracle is the right screen and their implementations are correct:
  `h.hex().startswith('3c6')` everywhere. The sixteen-times-too-strict `3c60` test was mine alone
  and is fixed, so none of their negatives inherit it.
* `RBB_DOSSIER.md:19` already states that the demo's flips are "CONDITIONAL EXAMPLES on para 5" and
  that para 2's final `n` is explicitly excluded. My 32-structural-variant hash of the literal
  para-5 reading is an exhaustive confirmation of their reading, reached the other way round.
* Their remaining hypothesis, `>=5` word-internal flips in mixed directions
  (`RBB_DOSSIER.md:48`), is exactly the gap my sweeps leave: I closed k=1 exhaustively
  (271 word-final positions x all 1,024 paragraph-initial masks) and k=2 under four lowering rules.
* `HANDOFF_AGENTS.md` §6 already lists "sentence-edge flips" as closed, so my 3^15 sentence model
  was partly a redo of `sent_brute.py`. Their version enumerates 2^15 subsets in which each chosen
  sentence gets both edges flipped, at the `\n\n` join. Mine enumerates 3^15 at `\r\n\r\n` with each
  sentence taking one of none / first-down / last-up. The union still misses *mixtures* (some
  sentences both, others single-sided).

**Where comparison found real gaps, now closed.**
* `hunt_demo_edges.py` closes the paragraph-edge space (4^10, `\n\n`) but derives `D.derive(h)` at
  the default path only, i.e. index 0. My paragraph families used `\r\n\r\n` and had no "both"
  state. Neither of us had covered **both joins x all 4^10 edge states x indices 0-77**. Done now:
  2,097,152 candidates, 540 survivors, 42,120 derivations, **0 matches**.
* Their `I`/`himself` subset family (2^9 masks) was derived at index 0. Re-run over all 1,023
  non-empty subsets of the 10 real sites (8 pronoun `I` plus both `himself` occurrences) at indices
  0-9: 10,230 derivations, **0 matches**.

**The one genuine disagreement about method.** Their plan for the remaining space is k=4 flips
anywhere, about 1.2e11 candidates and 34 GPU-hours. Mine is that this is no longer a search problem:
the space they would sweep is the space where a case mask is *chosen*, and the evidence says the
author's masks were not chosen at all on the chapter side. On the demo side a 34-hour GPU run has a
prior of roughly (number of true solutions)/1.2e11, which is not a plan, it is a lottery ticket.
Better use of the same effort: get puzzleponky's 2019 disclosure.
