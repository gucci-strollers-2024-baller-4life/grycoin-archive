# The decoy discriminator: what it selects, and the 4.3M-candidate closure it licenses

**Date:** 2026-10-31
**Base:** `demo_base.txt`, md5 `7759227d7406` (the author confirmed `7759227` for the unedited question).
**Oracle:** md5 begins `3c6`, escrow `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi`.

## 1. The author's two examples are a controlled pair, and they discriminate on grammar, not letter class

| | where the mark sits | author's verdict |
|---|---|---|
| `capitalizatioN` | final letter of ¶2's only sentence, which is also the **paragraph's final** sentence | **not part of the solution** |
| `himselF` | final letter of ¶5's **first** sentence, which is followed by another sentence in the same paragraph | **the solution** |

¶2 is `As is already clear from the reference to block 29, … their capitalization.` — one sentence, so its
end is both the sentence end and the paragraph end.
¶5 is `I expected … outing himself.` + `Even after I explained the method used and the result in detail.` —
two sentences, so `himself` ends a sentence that is **not** the paragraph's end.

That is the criterion, and it is grammatical: **a mark may sit on the final letter of a sentence that is
followed by another sentence inside the same paragraph. A mark may not sit on the paragraph's last letter.**

The author confirms the second mark independently (¶7): *"you would end up changing 'I' to 'i' and 'himself'
to 'himselF'"*, where the `I` is ¶5's first letter. So ¶5 is selected and the edits are at its start and at
its first sentence's end.

Encoding that criterion turns the four candidate edit geometries into two:

| geometry | flags `capitalization`? | status |
|---|---|---|
| raise the final letter of every sentence | yes | **falsified by the decoy** |
| raise the final letter of every paragraph | yes | **falsified by the decoy** |
| raise the final letter of every non-paragraph-final sentence | no | consistent |
| raise the final letter of the first sentence of multi-sentence paragraphs | no | consistent |

Two of the four geometries die on the author's own negative control. That is the filter working, and it is
worth recording because the repository has been carrying all four as live.

## 2. First closure: the geometry crossed with every initial-letter sign class

Every one of the 31 non-empty paragraph-initial classes, applied as the down-mark selector, crossed with
each surviving geometry and all four serializations: **256 candidates, 128 pass the decoy discriminator,
0 pass `3c6`.**

## 3. Second closure: the geometry enumerated without any letter-class assumption

The criterion above bounds the up-marks to five positions: the final letters of the non-paragraph-final
sentences, which in this text are `himself`→**f**, `signs`→**s**, `block`→**k**, `now`→**w**, `mind`→**d**.
The down-marks are unconstrained by the decoy, so both plausible families were enumerated in full:

- every subset of the 5 licensed up-mark positions: 2^5 = 32
- every subset of the 10 paragraph initials: 2^10 = 1,024
- every subset of the 15 sentence initials: 2^15 = 32,768
- four serializations

    total 4,325,376 candidates, 1,026 pass the `3c6` prefix, all derived at indices 0–4

    **0 escrow hits**

This is exhaustive over the entire two-edge family that the author's own examples license. Nothing about
letter classes, sign sets, or "recognising the signs" can rescue it, because no letter class is used.

## 4. Third closure: the author's named pair as an anchor

¶7 fixes two of the answer's edits. So the answer's size can be enumerated exactly around that anchor:

| edits in the answer | candidates (4 serializations) | `3c6` survivors | derived | escrow |
|---|---|---|---|---|
| 2 (the named pair alone) | 4 | `b668273e` (CRLF) | — | no |
| 3 (named pair + 1 free edit, all 1,194 free positions) | 4,776 | **0** | — | — |
| 4 (named pair + 2 free edits, all 712,221 pairs) | 2,848,884 | 724 | indices 0–3 | **0** |

So the demo's answer is **not** three or four case changes from this base, in any serialization, for any
choice of positions, interior ones included.

## 5. What is now proved, and the one thing left

Closed by enumeration, not by argument:

1. no edit set confined to the two edge families the author describes (4,325,376 texts);
2. no answer of 2, 3 or 4 case edits anchored on the pair the author names (2,853,664 texts);
3. no answer selected by any first-letter class at paragraph or sentence granularity (the earlier 1,076);
4. no answer within two case edits of the base at all (2,868,016 texts, earlier session).

The demo answer therefore has **at least five** case changes from this base, or it is not a case edit of
this base. Five from the anchor is C(1,194,3) = 283,129,390 candidates: about 16 minutes of `3c6` screening
with no derivations owed until a survivor appears. That is the terminal integer for this base, and it is the
only remaining fast route.

If that too returns nothing, the conclusion is not "keep searching": it is that the demo's escrow is not
derived from this text through the md5 → BIP39 → address chain that the rest of this hunt assumes, since
every case-edit family up to four changes is now excluded, and five is the next integer rather than a new
idea.
