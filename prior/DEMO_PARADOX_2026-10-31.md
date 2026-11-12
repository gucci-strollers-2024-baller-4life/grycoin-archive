# The demo's paradox, located exactly

**Date:** 2026-10-31
**Script:** inline; ledger printed below. Base `demo_base.txt`, md5 `7759227d7406…` (the verified hashed
object per `CLUES_CANONICAL.md` §6). Oracle `3c6`, escrow `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi`.

## 1. What the instruction actually says

Three separate statements, and they do not agree with each other.

| ¶ | statement | what it licenses |
|---|---|---|
| 3 | "if the letter 'n' at the end of the last paragraph was part of the solution, you would be expected to change it to 'N'" | a **paragraph-tail** mark — hypothetical |
| 4 | "that 'n' is not part of the solution, which is obvious to anyone able to recognize the signs" | tail marks exist, and sign-recognition is the discriminator |
| 6 | "if you were able to recognize the signs and thought that the 'I' at the beginning of the previous paragraph was one of them, you would be expected to change that 'I' as well to a 'i'" | **one** change: ¶5's head, lowered |
| 7 | "When you do that, you would end up changing 'I' to 'i' and 'himself' to 'himselF'." | **two** changes |
| 8 | "once you do that for all the paragraphs where you recognize the signs. And keep the rest completely unchanged." | the generalisation |

## 2. Where the two diverge

¶6 describes one edit. ¶7 reports the outcome as two. The second edit, `himself` -> `himselF`, is not
derivable from anything in ¶1-¶8: no sentence states "raise the last letter of the first sentence", and
no rule mentions which word class carries a sign. It is licensed only by ¶5's *content* —

> "not many people do recognize the signs in Satoshi's Bitcointalk post outing **himself**"

— the word that performs the outing is the word that gets marked. So the demo's own worked example
selects its second mark **semantically**, then hands the reader a **positional** rule for everything
else, and never reconciles the two.

Compounding it: ¶5 says the signs are *in Satoshi's Bitcointalk post*, not in the demo. The demo's
selector sentence therefore cannot be applied to the demo text at all. The demo is a format document
(¶9: "should be enough to completely clear up the remaining problems with finding the correct format
for both stages of block 77"), and the sign-set it describes lives in another text.

## 3. What the marked set produces

| text | md5 |
|---|---|
| ¶7 verbatim: ¶5 head `I`->`i`, `himself`->`himselF` (2 changes) | `98966fafe2e086f826881faaf01f5662` |
| plus the quoted `himself` in ¶7 (3 changes) | `c76c4c38e99345b79af97cc816b9ef3b` |
| {4,5,6,8} head-down + sign-sentence-tail-up, LF (8 changes) | `13082a4503a5fae6c65f113e9d8eb722` |
| same, CRLF | `0f69c8ea8e7f27a9ece1593de788c47e` |

The marks in that last text, spelled out:

```
P4  F -> f   ...ize the signS      (sign word "signs", sentence-final)
P5  I -> i   ...uting himselF      (first sentence of two: sentence-final, not paragraph-final)
P6  O -> o   ... well to a "I"     (paragraph-final; ¶6 contains no sign, it describes one)
P8  W -> w   ...ize the signS      (sign word "signs", sentence-final)
```

None begins `3c6`.

## 4. No positional selector at paragraph scale works

Exhaustive: 6 mark modes (`head`, `head+paragraph-tail`, `head+first-sentence-tail`,
`head+sign-sentence-tail`, `head+every-sentence-tail`, `paragraph-tail`) x all 1,024 subsets of the ten
paragraphs x 2 joins = **12,288 texts**.

| texts | beginning `3c6` | landing on the demo escrow |
|---|---|---|
| 12,288 | 2 | **0** |

Both `3c6` hits are at the chance rate (12,288 / 4096 ≈ 3) and both are positional nonsense:
`head+ftail {2,4,8,9,10}` -> `14iJQCWD…`, `head+alltail {1,2,3,8,9}` -> `1MuStkzQ…`.

**Conclusion.** No choice of paragraphs and no choice of tail, under the demo's own words, reaches its
own oracle. The failure is not in the enumeration; it is in the sentence that names the selector. And
the same sentence is the one the chapter repeats twelve times: *"the paragraphs where you recognize the
signs."* Every family selected by that phrase has now failed in both texts — 12 paragraphs in the
chapter, 4 in the demo. The phrase is the decoy string.
