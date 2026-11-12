# Hunting the solver's method: archive exhausted, and what the archive actually proves

**Date:** 2026-10-31
**Source:** `pp_comments.json`, the recovered comment archive of `u/puzzleponky`, the only person who ever
solved the demo (cleczc) and stage one of block 77 (ca6jxv).

## 1. The archive is complete and contains no disclosure

70 comments, 2019-04-13 to 2020-06-21. Distribution: 38 in `r/Grycoin`, 30 in `r/bitcoinpuzzles`, 2 in
`r/Bitcoin`. 36 of the 70 disclose a block solution or a method.

On the two blocks that matter, he said this and nothing more:

> **2019-08-03, t3_ca6jxv** (block 77 stage one): *"Solved! it was easy after solving block 2. There were
> some tricky bits though. I will wait for now before revealing the full solution. Thanks"*

He never came back. The archive ends 2020-06-21 with an unrelated album-puzzle comment. External search
returns only his Reddit profile (no Medium, no Bitcointalk identity), and `old.reddit.com/user/puzzleponky`
is 403 behind the login wall. The dossier's line "Reddit history exhausted; no post-2019 reveal" is
confirmed rather than assumed: this is the complete recovered record.

So the method disclosure does not exist in the recoverable corpus. The hunt is closed, and the honest
reading is that this route cannot yield the rule.

## 2. What the archive does prove, which is worth more than the method would have been

**(a) The inheritance direction, from the solver's own mouth.** "It was easy after solving block 2" is a
solver telling us that block 77 stage one inherits from the demo. Together with the author's own line that
the demo's letters are obvious "if you know the solution to Satoshi's bitcointalk puzzle", the chain is
block 29 / earlier device → demo (round-2 block 2) → stage one (block 77). Nobody has to infer it now.

**(b) The `i`→`I` capitals are the author's typing habit, confirmed in 2019 by the solver.**
> **2019-06-10:** *"Just to verify: Is the I in HI supposed to be a capital? I assume it is because of the
> whole Atbash thing but in your posts the second I is often weirdly capitalized like with FIrst two times
> in this post, or SInce in the previous, BItcoin in others, so not sure."*

That is the only person who solved two of these blocks noticing `FIrst`, `SInce`, `BItcoin` as recurring
noise and asking whether they are marks. It is independent, solver-side confirmation of `FINDINGS_MARKS`
§2: `VIrgin` and `BItcoin` in the chapter carry no information. My closure last session was right, and now
it is corroborated from the other side of the puzzle.

**(c) His extraction convention, stated plainly.** Block 16:
> *"Solution was A1zP1eP7DivfNa. last seven from the address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa and first
> seven AFTER the 1, I was lucky to solve puzzle 16 an hour earlier which gave me the idea"*

Same convention as the block-14 shape the spec cites, and the same convention that produces `Hal Finney`
and `ihsotaS otomakaN`. His working style is: find the reference string, take N from each end, skip the
prefix, check the hash digits.

## 3. The identification the archive forces: the "Satoshi's bitcointalk puzzle" is block 29

The demo's first sentence is *"As is already clear from the reference to block 29, people are supposed to
keep the whole long text and change only a couple of letters in their capitalization."* The reference to
block 29 is **inside the demo**. So the puzzle whose solution makes the letters obvious is round-1 block
29, and the author had indeed revealed it: `ANSWERS.md` carries it, MD5-verified, as

> `"Good morning, Tom." / A pleasant female vOIce. / I answer. "Good morning. When is this?" / I expect
> that a couple of centuries have passed since my first life end…` + `zff`

Block 29's answer is its own input with exactly two characters changed, `vOIce`. Read as a name:

    "A pleasant female vOIce."    capitals: A · O · I    =  AOI

The sentence-initial `A` is already capital and counts. Two interior capitals are added. The marked
capitals spell a three-letter name. **That is the device**: "a couple of letters", interior capitals, and
the resulting capitals spell a name using the sentence's own initial as one of its letters.

This is a sharper target than `Hal Finney`, and it explains the demo's worked example differently from the
edge geometry this repo has been using. In `I expected … outing himself.` → `i expected … outing himselF.`
one capital is **removed** (`I`→`i`) and one is **added** (`f`→`F`). Under the block-29 device that is not
"first letter down, last letter up": it is *unmark a false sign, mark the true one*, which is exactly what
the demo's prose says — "'n' is not part of the solution", "if you thought the 'I' was one of them".

## 4. Tested this session

| family | candidates | screen | matches |
|---|---|---|---|
| greedy R1 name-marking on the demo: HALFINNEY, HAL, FINNEY, NAKAMOTO, SATOSHI, NAKAMOTOSATOSHI, SATOSHINAKAMOTO, HALFINNEYSATOSHINAKAMOTO, THOMAS; first-occurrence and last-occurrence order; both joins; trailing separator or not | 72 | `3c6` prefix | 0 |

None of the 72 even passes the prefix filter, so no derivation was owed.

## 5. Where this leaves the hunt, stated plainly

The method is not recoverable from the solver, and the author lost it himself. What remains is the one
object in the corpus where **question and answer are both published and both verified**: block 29. It is
the only fully-solved instance of the device, it is 1,360 characters, and its marking is exactly two
interior capitals that spell a name using a sentence-initial capital as the first letter.

That is a template, not a guess. The next unit of work is to take block 29 as the calibration object,
state its device exactly, and ask what name the demo's text would have to spell for the two changes in the
worked example to be consistent with it. If the answer is a three-letter name, the demo has 10 paragraphs
and a handful of candidate sentences, which is a reading task of a few candidates, not a sweep.
