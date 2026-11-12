# The demo's asymmetric pair, measured on the chapter's syntax

Demo paragraph 5 carries two marks: `I expected` -> `i expected` (paragraph opening) and
`himself` -> `himselF` (final letter of the last word of the *first sentence*). One mark at the
macro edge, one at the micro edge. The question was whether the chapter contains that intersection
outside normal grammar.

## The macro edge: 10 paragraphs open on a lowercase letter, all of them enumerators

| paragraph | text |
|---|---|
| 176 | a) Satoshi's birthday |
| 182 | b) THOMAS and Satoshi |
| 209 | c) BITcoin is actually AHScoin |
| 215 | d) Outing himself as Satoshi on Bitcointalk |
| 250 | a) ALS Condition |
| 252 | b) Previous Experience |
| 254 | c) Mail Conversation With Himself |
| 256 | d) Not Citing RPOW in the Whitepaper |
| 258 | e) Coding Style |
| 260 | f) Overheating Computer |

Two enumerations, `a)..d)` at 176-215 and `a)..f)` at 250-260. Every lowercase initial is a list
marker. There is no paragraph in the chapter that opens lowercase for any other reason.

## The micro edge: 12 paragraphs whose first sentence closes on a capital

p2 (I), p88 (II), p163 (III), p183 (II), p184 (THOMAS), p194 (IBM), p195 (IBM), p211 (S),
p229 (W), p237 (STNM), p239 (STNM), p245 (I). All twelve are Roman numerals, acronyms, or the
letters she is quoting. All licensed.

## The intersection is empty

The set of paragraphs abnormal at both edges is empty. The two anomaly classes are disjoint, and
each is grammatically forced. Measured, not assumed.

## The class-3 slips do not sit on either edge

`ppM` (p73) is 11 words into the first sentence; the alphabet address (p126) is 28 words in;
`VIrgin` (p128) and `BItcoin` (p136) are mid-sentence. None of the planted-looking anomalies is at
a paragraph opening or at a first-sentence close, so the demo's pair has no exemplar among them.

## Why the pair cannot be the rule

The pair fires on every paragraph that opens on a capital and whose first sentence ends on a
lowercase letter, which is roughly 250 of 273 paragraphs. A rule with 92% firing rate is
indistinguishable from "flip the edges of the document", which is closed. The demo's asymmetry is
also forced locally: the demo's paragraphs all end in a full stop, so she had to reach inside the
paragraph to the first sentence to find a flippable letter. The chapter's paragraphs also end in a
full stop, but the last letter before it is available and legal, so the fallback is not needed.
**The asymmetric pair is an artifact of the demo's text, not the carrier of the rule.**

## Tests run, all negative

`sweeps/edge_intersection.py`: every structural class above (the two enumerations, the twelve
capital-close paragraphs, the all-caps-close subset, the union pool, and each of their complements),
eight mode directions, both certified bases, indices 0-2. **972 address-verified derivations, 0 hits.**

Supplement: the Finney block read as the sign set: {231-235} including the I paragraph, {230-235},
{229-235}, {231-237}, {229-241}, {220-246}, {222, 231}, {229 + 231-235}, five mode directions, both
bases, indices 0-2. **222 derivations, 0 hits.** The 231-235 reading gives 10 flips
(initial down plus first-sentence-close up on all five, `Finney` -> `FinneY` included) and is
negative like the rest.
