# Catalog audit, and the demo's last two case-flip families closed

**Date:** 2026-10-31
**Scripts:** `demo_pair_closure.py`, `demo_two_edit_closure.py`
**Object:** the demo block (`demo_base.txt`, md5 `7759227d7406`, 1,549 bytes, 10 paragraphs)
**Oracles:** md5 prefix `3c6` (published), address `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi`

## 1. The catalog's checkable claims, verified against the bytes

| claim (`WORDPLAY_RULES_CATALOG.md`) | check | verdict |
|---|---|---|
| §22 `md5("Hal Finney") = cc9485a…` | independent md5 | **holds** (`cc9485a`) |
| §2 13 trailing-space paragraphs at 86, 108, 122, 128, 139, 147, 165, 166, 192, 201, 209, 220, 267 | exact match | **holds** |
| §7 para 93 is the only 44-character paragraph | `len == 44` | **holds** |
| §2 duplicate `"What?"` at 34 and 78 | both present, identical | **holds** |
| §17 para 126 alphabet `3abcdefghijkLmnopqruvwxyz` / `7abcdefghijkLmnopqrstuvwxyz` | present, capital `L`, `st` missing in the first | **holds** |
| census: 273 paragraphs, 20 occurrences of "sign(s)" | counted | **holds** |
| §3.3 ten internal-break paragraphs 63, 73, 121, 124, 146, 160, 184, 189, 193, 213 | reconstructed from the live part | **holds** |
| §12 base fidelity: `48d31820…` at `\n\n`, `46a308c2…` at `\n\n` with breaks, `db11a7fd…` at `\r\n\r\n` | all three reproduced | **holds** |

No factual error found. The two corrections below are arithmetic, not claims.

## 2. Correction: the "sentence pair" family is 32,768, not 1.07 billion

`FINDINGS_MARKS_2026-10-31.md` §8(b) closes sentence granularity with three states per sentence
(unchanged / first down / last up), 3^15 = 14,348,907, exhaustive. It then states the remaining family:

> *"What is left in case-flip space is either sentence-aligned pairs (first lowered and last raised on the
> same sentence, 4^15 = 1.07e9, about 19 minutes at the measured rate)"*

The label and the count do not describe the same family. If the unit is the **pair** — both edges changed
on the same sentence or neither — each sentence has two states and the family is **2^15 = 32,768**. The
count 4^15 = 1.07e9 describes something else: four independent states per sentence (unchanged / first
down / last up / both), i.e. the mixed family, which is genuinely open and genuinely that large. Recorded
here because the two must not be confused in either direction: the pair reading is 32,000x cheaper than
the catalog implies, and the mixed reading is not closed by anything below.

`demo_pair_closure.py` enumerates it exhaustively, both joins, trailing separator or not:

| serialization | candidates | `3c6` survivors |
|---|---|---|
| `\r\n\r\n` | 32,768 | 8 |
| `\r\n\r\n` + trailing | 32,768 | 9 |
| `\n\n` | 32,768 | 9 |
| `\n\n` + trailing | 32,768 | 13 |

All 39 survivors derived at `m/44'/0'/0'/0/i`, i in 0..77: **0 escrow matches.** Wall time 44 seconds,
not 19 minutes.

The implementation is calibrated: applied to the sentence beginning `I expected` it produces exactly

```
i expected otherwise, but actually not many people do recognize the signs in Satoshi's Bitcointalk post outing himselF.
```

## 3. New closure: every text that differs from the base by two case flips or fewer

Every demo sweep to date constrained *which units* were selected while assuming the edits sit on
structural edges. The author's sentence constrains the **edit count**: *"change only a couple of letters
in their capitalization"*. Taken as a bound rather than as a unit rule, that is not a hash space, it is a
complete enumeration:

- 1,197 alphabetic positions, direction fixed by `swapcase` (an uppercase letter can only go down, a
  lowercase only up, so each position has exactly one effective flip)
- C(1197,2) + 1197 + 1 = **717,004 texts** per serialization, × 4 serializations = **2,868,016**
- screened by the published `3c6` prefix, survivors derived at indices 0, 1, 2

| serialization | candidates | `3c6` survivors | derived | matches |
|---|---|---|---|---|
| `\r\n\r\n` | 717,004 | 159 | 159 | 0 |
| `\r\n\r\n` + trailing | 717,004 | 175 | 175 | 0 |
| `\n\n` | 717,004 | 162 | 162 | 0 |
| `\n\n` + trailing | 717,004 | 162 | 162 | 0 |

**2,868,016 texts, 658 prefix survivors, 0 matches.** 44 seconds, of which most was derivation.

## 4. What that settles about the demo, and why it stops the port

The demo is the only object in this hunt carrying two oracles at once, which makes it the only place a
rule can be *calibrated* rather than guessed. Its case-flip space is now closed at every granularity that
has been enumerated:

| family | volume | status |
|---|---|---|
| paragraph, 4 states, 4^10 | 1,048,576 | closed, negative |
| sentence, 3 states, 3^15 | 14,348,907 | closed, negative |
| sentence pairs, 2^15 | 32,768 | closed this pass, negative |
| any text ≤ 2 case flips | 2,868,016 | closed this pass, negative |
| word-edge substitutions by name | 89,108 + 248,472 | closed, negative |

So the demo's answer either carries **three or more case changes**, or it is not a case-edit of this
base at all. Her words "a couple of letters" are then not a literal count, which is consistent with
§8(a)'s earlier finding that the two letters she names are an example and not the operation.

The consequence for stage two is the one that matters, and it is not comfortable: **the rule cannot be
ported, because it has never been validated on the object that has a published oracle.** Every RBB family
run so far, including the 949 candidates from this session, tests a rule whose only support is a
sentence in the demo prose that the demo's own answer contradicts. That is why 5.47M negatives and 0
positives are consistent rather than unlucky.

## 5. The only defensible next move

Not another RBB family. The demo's answer must be recovered first, and the constraint on it is now sharp:
≥ 3 case changes, and the `3c6` prefix screens candidates at ~300k/s with zero derivation cost. A
3-change enumeration over the 1,197 positions is 2.8e8 texts, about 15 minutes of screening at the
measured rate and no escrow derivations at all until a survivor appears. That is cheap, exhaustive, and
it terminates an argument instead of extending it.

The alternative, if a 3-change sweep is judged too close to brute force: read `agntn/` for the demo's
collected author quotes, since the `3c6` prefix itself came from there and the same pages may state the
edit count or the sign set outright. That is a reading task, not a computation, and it is where every
factual gain in this hunt has actually come from.

## 6. The author's own statement about where the letters come from (found while auditing `agntn/`)

`agntn/aoinakamoto-2019-08-03-cleczc.md` is the demo's own Reddit thread, and it contains the answer to
the question this session has been circling. Aoi Nakamoto, on being asked to post the cleczc solution:

> *"One, I actually don't know. The question of what letters to change in capitalization is obvious if you
> know the solution to Satoshi's bitcointalk puzzle, which I revealed already. The question of how to go
> from that to claiming the prize is not, not even to me."*

> *"Two, as mentioned before knowing this is an advantage for solving the real big block. So I don't want
> to take that advantage from the winner."*

Three things follow, and they are worth more than any sweep in this file.

1. **The sign set is inherited, not read out of the text.** The letters to change are determined by the
   solution to Satoshi's Bitcointalk puzzle — the previous block. That is R2 (inheritance) promoted from a
   hypothesis to the author's own account, and it means no selection rule that reads only the chapter can
   be the right one. Everything the hunt has run on the chapter, including this session's 949 candidates,
   assumes exactly the thing the author says is false.
2. **The author's constraint was the format, not the solution.** He knew which letters change and did not
   know how to get from that text to the address. So the "clever" part he designed is the marking; the
   derivation off the end is the standard chain, which is why the demo's answer was found by someone
   else and never explained afterward.
3. **The sign set is at least partly the letters of `Hal Finney`.** That is the only piece of the previous
   solution that is independently verified (`cc9485a`), and it is what the chapter's own thesis states.

Read as a letter class, `{H,A,L,F,I,N,E,Y}` (and `{H,A,L}`, `{F,I,N,E,Y}`, the union with `{I,T,A,S,M}`,
and the genesis-address reading `A1zP1eP7DivfNa`) applied with the validated geometry at paragraph and
sentence granularity, both joins, trailing separator or not, screened by the `3c6` prefix: **56
candidates, 0 prefix matches**, so no derivation was even owed.

That is not a refutation of the inheritance reading; it is a refutation of the cheapest first guess at
what "the solution" is as a bare letter set. The inheritance reading needs the *actual* previous solution,
and §22 recovered only half of it: the left plaintext pair. Hint 3's warning is explicit that the
ciphertext part must be very short, and the second prefix `d78c92f` is still unexplained after ~590,000
candidate phrases across the corpus.

## 7. The order of operations the evidence now imposes

1. Recover the second plaintext pair (`d78c92f`). It is a 28-bit oracle over a *closed-form*
   reconstruction, and it is the missing half of the thing the author says the whole family inherits from.
2. With the complete previous solution in hand, apply it as the inheritance source for the demo, screen
   with `3c6` at 300k/s, and only then port anything to the RBB.

Doing (2) without (1) is what the last several sessions have done, and it is why they all came back empty
for the same reason.
