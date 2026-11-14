# Two new lanes, 2026-11-14 15:20 UTC

## Why: the demo marks inside a paragraph

The author's own format demo (cleczc, "Grycoin Block 2") says the answer changes the
"I" at the beginning of a paragraph to "i" **and** "himself" to "himselF". In the text
he actually posted, "himself" sits at a sentence end *inside* that paragraph
("...outing himself. Even after I explained the method used and the result in detail.").
A paragraph-edge rule cannot produce that mark. Every sweep in this hunt marks paragraph
edges, so the unit of marking was never controlled.

Note: the demo answer itself remains uncomputable from the post text. Marking the
Question text at sentence granularity (2^15 subsets x 3 mutation modes x 3 joins) yields
54 candidates whose md5 starts 3c6; none derives to `1tzieUf...` at BIP44 indices 0-77.
The demo is used here only as evidence about the *unit*, not as an address oracle.

## LANE 1: GAPS (`ci/gaps.py`, run 43609600805)

Both certified lanes pin one selector/mutation pairing: CLASS selects by paragraph
initial and mutates both ends, TAIL selects by paragraph final and mutates the tail only.
Paragraph 236 ("we are directed to look at the last letter of each of these") licenses
separating the two, so three pairings had never been hashed:

| lane | selection | mutation | masks |
|---|---|---|---|
| L1 | paragraph initial, 21 axes | tail only | 2^21 |
| L2 | paragraph initial, 21 axes | head only | 2^21 |
| L3 | paragraph final, 18 axes | head only | 2^18 |

28,311,552 derivations, both joins, indices 0-2, both escrows. Gate reproduces all three
certified digests and proves each lane's construction byte-identical at four probes.

## LANE 2: SENT (`ci/sent.py`, run 43609896672)

The certified mechanic applied to **sentences**: 670 units, 22 distinct initials
(ABCDEFGHIJKLMNOPRSTVWY), 2^22 masks, mark when the sentence initial is outside the
class, lower its first alphabetic and raise its last. Both joins, indices 0-2, both
escrows, 25,165,824 derivations. The identity mask reproduces 46a308c2 and bd07e6ee
byte-exactly, and the sentence space strictly contains the paragraph-edge class space
(the first and last sentence of every paragraph carry its head and tail).

## Status of the earlier queue

Mega run 43578710933 (viol 2^25 on the as-is base, class family on six cleaned base
variants, tail-only) still has 15 of 20 shards in progress at 15:25 UTC. Shard 8's
violator lane is a certified negative: 1,677,721 masks, indices 0, zero hits, 1,429
derivations/s.
