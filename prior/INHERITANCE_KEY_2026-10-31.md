# The inheritance key: `d78c92f` is not missing, and it kills the letter-class reading

**Date:** 2026-10-31
**Status:** the blocker recorded as open is closed. Recovered, verified, and its consequences run.

## 1. The oracle, verified

    md5("Hal Finney")          = cc9485a…   (left plaintext pair, forward)
    md5("ihsotaS otomakaN")    = d78c92f…   (right plaintext pair, reversed)

Both verified locally this session from the strings themselves. `d78c92f` is `Nakamoto Satoshi`
**reversed character by character**, not a different pair of names.

`RBB_ANSWER_SPEC_FINDINGS.md` (2026-10-29) already had this line. `WORDPLAY_RULES_CATALOG.md` §22 ends
by calling the second prefix unexplained after ~590,000 candidates, while §23 of the same file says the
reversal convention resolves it. The catalog is self-contradictory on this one point, and §22's closing
paragraph is the stale half.

Why the searches missed it: every one of them searched forward. `Nakamoto Satoshi` forward is `930bf3b5`,
which was tested and listed as a reference negative. `ihsotaS otomakaN` is a string no phrase search over
a corpus can produce, because it does not occur in any text; it is a transformation of one.

## 2. The reconstruction is confirmed structurally, not just by a hash match

    "1A1 efi2DM Hal Finney Nm ST ihsotaS otomakaN"

Eight items, joined by single spaces, item lengths 3 / 6 / 3 / 6 / 2 / 2 / 7 / 8, letters and spaces
    3+6+3+6+2+2+7+8 = 37, plus 7 separators = **44 characters exactly**

That is what "eight items in two sets of four. Two items ciphertext and two items plaintext each. 44 read
from left and 44 read from right" states: the item string is 44 characters long, read from the left for
the left half and from the right for the right half, which is why the right plaintext pair is stored
reversed. A four-orders-of-magnitude coincidence in item lengths is not available here, so the spec is
right in every part:

- ciphertext left: `1A1`, `efi2DM`  (HAL; Finney via Atbash, 2=Y, M=N)
- plaintext left:  `Hal`, `Finney`
- ciphertext right: `Nm`, `ST`  (Nakamoto, Satoshi, with 7 and 5 as pointers)
- plaintext right: `ihsotaS`, `otomakaN`

## 3. What it kills: inheritance cannot be a letter class

Distinct letters in the 44-character solution:

    A D E F H I K L M N O S T Y   ->  15 of 26, i.e. 58% of the alphabet

A rule of the form "change the letters that belong to the previous solution" would select more than half
of every word in the text. It is not a selection rule; it is the identity function with extra steps. So
the reading that was tested last session, and again this session, fails **structurally**, and its
negatives were never going to be luck.

Verified by running it anyway, three classes, paragraph and sentence granularity, four serializations,
screened by the author's own `3c6` prefix:

| sign class | derivation | candidates | `3c6` matches |
|---|---|---|---|
| uppercase of the solution `{A,D,F,H,M,N,S,T}` | the author's published uppercase letters | 8 | 0 |
| letters of the plaintext pairs `{H,A,L,F,I,N,E,Y,A,K,M,O,T,S}` | union, 13 letters | 8 | 0 |
| `{I,T,A,S,M}` | control, the geometry this repo has used all along | 8 | 0 |

24 candidates, none even passes the 3c6 filter, so no derivation was owed.

## 4. What survives: pattern inheritance, and the count it implies

`R2` in the catalog is the rule the author states in *Hoax*: the solution's case pattern is copied from a
visible artefact, **never chosen**, and "capitalization will be evident". That is the only inheritance
that the arithmetic above leaves standing.

The previous solution's case pattern:

    uppercase sequence:  A D M H F N S T S N      (10 uppercase over 44 characters)

So the demo's answer should carry **ten** changed letters. That is consistent with what this session
proved mechanically (the answer is not any text with two or fewer case changes), and it contradicts a
literal reading of "a couple of letters" in the same way: the phrase describes the operation, not a
count.

## 5. The two facts that reframe the project

Both are in `RBB_ANSWER_SPEC_FINDINGS.md` and neither has been treated as decisive:

1. **The author lost the RBB solution.** Part 762380140 *Starting Up*: *"I have lost any information on
   the solution of that one. Tragic boating accident variation."* Reconstruction only, no confirmation
   available from him.
2. **The demo was solved by someone else, and the author does not know how.** `agntn/aoinakamoto-2019-08-03-cleczc.md`:
   *"The question of what letters to change in capitalization is obvious if you know the solution to
   Satoshi's bitcointalk puzzle… The question of how to go from that to claiming the prize is not, not
   even to me."* The winner, `puzzleponky`, was congratulated and never posted a method.

So for both objects the author is not an oracle. The only oracles in existence are the ones he published
mechanically: `7759227` (demo base), `3c6` (demo answer prefix), `cc9485a` and `d78c92f` (the two
plaintext pairs), and the four escrow addresses.

## 6. Runs this session

| family | candidates | screening | matches |
|---|---|---|---|
| the 44-char item string and 7 renderings of it, all four escrows, indices 0-77 | 8 strings x 78 indices | address | 0 |
| solution-derived sign classes at paragraph and sentence granularity, 4 serializations | 24 | `3c6` prefix | 0 |

## 7. Where the next unit of work belongs

Not another RBB family. Two routes, in order of what they would settle:

1. **Find the winner's method.** `puzzleponky` solved the demo, which is the only object with a published
   prefix oracle. If he described his method anywhere, in that thread's later comments, in
   `r/Grycoin`, or on Bitcointalk, it settles the geometry and the sign set at once. This is reading, not
   computing, and it is the highest-value unread document in the project.
2. **Exhaustive three-change closure on the demo.** Given two changes or fewer are disproved, three is the
   next integer. C(1197,3) = 285,129,390 texts, 4 serializations, screened only by `3c6` at the measured
   297k/s: about 16 minutes of screening and no address derivations until a survivor appears (~69,000
   expected survivors, so derivation cost is real: roughly 18 further minutes at three indices).

Route 1 is the one consistent with the author's own remark that this *"should be someone mining with the
mind"*, and it is the one that can return a rule rather than a negative.
