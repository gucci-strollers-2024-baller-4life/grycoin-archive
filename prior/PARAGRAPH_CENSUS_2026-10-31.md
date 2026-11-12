# Paragraph-level census, second pass (2026-10-31)

Asked for: filter the chapter's paragraph data again for structure other than the I/T/A/S/M
initial test. Scripts: `sign_unit_scan.py`, `sweep_signature.py`. Base: `wp_paras_br.json`
(273 paragraphs), certified against `bd07e6ee…` (CRLF) before any claim below.

## 1. Eleven-feature census, all 21 sections

For each feature I counted violations per section and looked for the chapter's own phrase,
"all paragraphs except four". Sections with exactly four violators:

| feature | sections with exactly 4 |
|---|---|
| first letter in I,T,A,S,M | 4 Why (152-156), 2b (182-208), Finney reprint (231-235) |
| starts uppercase | 2 b (182-208) |
| ends with a quote mark | 5 What (157-160), Finney reprint |
| ends with "?" | 5 What, 2 c (209-214) |
| has a trailing space | 5 What |
| is a single word | 5 What |
| shorter than 40 characters | 4 Why, 2 a (176-181) |
| contains a digit | 4 Why, 2 a |
| first letter == last letter | 5 What |
| contains "I " | 4 Why, 5 What |

Every one of these is an artefact of a four- or five-paragraph section: "four violators in a
section of five" and "two in a section of four" are what small samples look like. No feature
produces four exceptions in a long, meaningful span except the initial-letter test in 2 b, whose
four exceptions start b, O, O, H, not F, F, W, W. **No second sign system.**

## 2. The dialogue class (new, and it explains the messy counts)

63 paragraphs open with a quotation mark. Their distribution is the sharpest structural
asymmetry in the chapter and is not recorded elsewhere:

| section | quoted paragraphs |
|---|---|
| I (1-87) | 59 |
| II (88-162) | 0 |
| III (163-273) | 4 (222, 231, 243, 244) |

Section I is narrated as a conversation between Tom and visitors; II and III are essays. So the
opening-letter test is not applied to a homogeneous text: 59 of the 121 non-I,T,A,S,M openers sit
in dialogue, where a paragraph begins with whatever the speaker said.

Excluding quoted paragraphs: **82 violators in 210 paragraphs** (39%). Still not "all except
four", so the dialogue explanation *reduces* the noise but does not rescue the transfer.

## 3. No invariant offset for the three signatures

Roman headings at 2, 88, 163; the FFWW/stnm windows start at 5, 93, 168. Offsets are +3, +5, +5.
There is no constant distance from a section heading, and the one section with a subheading
(3) breaks the only candidate rule. Hypothesis dropped.

## 4. Duplicates

No two paragraphs longer than ten characters are identical. The short duplicates are dialogue
(`"What?"` at 34 and 78, which are 44 apart, already documented). So the chapter carries no
repeated block that could act as a second key.

## 5. The one test this pass added (negative)

`sweep_signature.py` widens each window by its neighbours, which the 2^16 window closure never
covered (its closure held only the 17 window paragraphs, so paras 4, 9, 92, 97, 167, 172 were
outside every swept set). Sets: each window alone, all three, each widened by its previous or
next paragraph, all three plus both flanks, and every paragraph in the chapter whose
(first,last) completes the signature F->s/t, W->n/m (23 paragraphs, 20 without dialogue). Both
flip directions, two certified bases, two joins, indices 0/1/2/76/77.

**520 derivations, 0 hits.**

## 6. Where this leaves the paragraph data

The only structure in the paragraph data that survives a second filter is the one already known:
three exact replicas of Hal's twelve-letter signature (firsts FFWW, lasts stnm at 5-8, 93-96,
168-171) plus the verbatim Finney reprint at 231-235, which carries the signature naturally
(FFWIW / stngm, the I-paragraph between the W's).

Paragraph-level feature mining is now exhausted: eleven features, 21 sections, both halves of the
dialogue split, and 520 derivations of every neighbour-widened reading. Further paragraph
filters re-cover this ground.
