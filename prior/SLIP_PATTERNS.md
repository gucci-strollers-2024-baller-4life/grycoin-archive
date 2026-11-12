# Slip patterns in her own record (2026-10-31)

Hint 2 closed the prose case-mark lane with her own words: `DIscussion` is "just a mistake, not a
hint for the solution". The obvious follow-up is the one asked here: what *other* slip classes does
her own record admit, and what does each one do to this hunt?

Sources used: the Complete Quizchain log (`cq_paras.json`, 766 paragraphs, round one complete and
round two up to block 15), the Grycoin posts and comment dumps (`grycoin_posts.json`,
`as_*.json`, `t_*.json`), and the 33 Wattpad parts. Every quote below is verbatim.

The useful split is by **layer**: which part of the object the slip lands on. A slip at the
serialisation layer is invisible in the text; a slip at the text layer is invisible in the format.
They call for opposite searches.

---

## 1. Layer: the line breaks / copy-paste (text-serialisation)

| quote | where |
|---|---|
| "First major mistake on my part, not noticing that I copypasted a line break when hashing." | R1 b9 |
| "Line break mistake of block 9 also in this block." | R1 b10 |
| "Hashing failure mistake of block 15 also in this one." | R1 b16 |
| "Another block with failed hash. Switched to MD5 hash without noticing." | R1 b15 |
| "the one that happened in the first round at block 9, where I included a line break in the hash, leading to the first failed block of the round" | R2 b9 comment |

This is her most frequent error, and it is the one class that is *live* for the RBB: hint 7 exists
precisely because she was afraid of exactly this. Note the shape of her errors: they are always an
extra or missing newline, never a wrong word. That is why the join has been the corpus's central
variable, and why the certified paragraph-level base matters.

## 2. Layer: an omitted or misnamed field (format)

| quote | where |
|---|---|
| "Failed block, forgot including link in hash." | R1 b44 |
| "Failed block. Changed name of BFUB field to TOMI and hashed with old name (same failure in next blocks 49 and 50)." | R1 b48 |
| "Solved after about one hour, even while I messed up the hash for this block by not including the string "TOMI"." | R1 b55 |
| "Failed block because of wrong link." | R1 b37 |
| "half asleep I actually managed somehow to mess up the link from the previous block, the first time that happened." | R2 b9 comment |

Every one of these is a *round-one* format feature. Stage two of block 77 has no TOMI field and no
link, so this whole layer is structurally unavailable to the RBB. It stays in the record only as a
warning: her published format line and her hashed string routinely diverged.

## 3. Layer: the answer's capitalisation (the RBB's own layer)

| quote | where |
|---|---|
| "As noted in comments, solution was grycoin, not Grycoin. First mistake of this round." | R2 b12 |
| "(I made a mistake in answering a question in comments about the capitalization)." | R2 b12 |
| "The most difficult part was getting the spelling of the name Laszlo Hanyecz right, which went into the TOMI field." | R2 b13 |

**This is the one uncatalogued class that sits exactly on the RBB's surface.** Her answer in block 77
is nothing but a capitalisation pattern, and she documents getting the capitalisation of an answer
wrong, correcting herself in the comments after the block was already live.

Consequence: the searched object should not be "the pattern she intended", it should be "the pattern
she typed". A single wrong-direction flip, one stray capital, or one place where she capitalised the
*first* occurrence instead of the intended one, is inside her documented error behaviour.

## 4. Layer: her prose typing engine (not a slip at all)

`DIscussion` (hint 2), `FIrst`, `SInce`, `BItcoin` x6 parts, `VIrgin`. She names the device and calls
it a mistake. Measured corpus-wide in `FINDINGS_MARKS_2026-10-31.md`. Closed.

## 5. Layer: funding and administration (no text effect)

"I did a funding transaction already when I wrote this block yesterday. And just did another one
today, having forgotten about the previous one." (R2 b9). Explains the doubled prizes; nothing to do
with any preimage.

---

## 6. Correction this pass forces: the RBB has no recorded hash mistake

`PATTERNS.md` §2 lists "b77: Failed block, made subtle hashing mistake, but corrected that way
before anyone came close to the solution" among hashed-by-mistake blocks, and `FRESH_ANGLES.md` §D1
builds its "two byte states" prior for the RBB on that line.

The line is **round one's block 77**, not the RBB. In `cq_paras.json` the string sits directly under
the heading `Block 77` at paragraph 380, inside round one; the heading `Round 2 of the Quizchain` is
paragraph 416, and round two's log stops at block 15 (paragraph 766). So paragraph 381 describes
**q1 b77**, the genesis-address puzzle, solved and claimed 2019-07-15.

Consequences:
- No publication record says the RBB's hashed text differs from its published text.
- The "two byte states" hypothesis loses its documentary support. It is not refuted, just unsupported;
  the only declared property of the RBB preimage remains hint 7: multiple paragraphs, two line breaks.
- `PATTERNS.md` §2 and `FRESH_ANGLES.md` §D1 carry the old attribution; corrected here.

## 7. The statement that removes "judgment call" from the record

From her 2019-08-03 reply on the demo post (`as_cleczc.json`), verbatim:

> "One, I actually don't know. The question of what letters to change in capitalization is obvious
> if you know the solution to Satoshi's bitcointalk puzzle, which I revealed already. The question
> of how to go from that to claiming the prize is not, not even to me."

And, same thread, on copying the text:

> "I am saying copy paste and do not change anything with the line breaks, change only the
> capitalization of letters in solution."

Three things follow, and the first one contradicts the corpus's closing position.

1. **The flip set is not a judgment call.** She says it is *obvious* given Hal's solution, i.e.
   determined by the FFWW / stnm signature. `CLUES_CANONICAL.md` §7 and §15 conclude the opposite
   ("the remaining variable is exactly which letters the author edited"). Her own words say the
   letters are derivable; only the derivation step is unknown to her.
2. **The unknown is the claim step**, not the text. That is a different search: it points back at
   the pipeline (index, path, what exactly is hashed) rather than at more sign sets.
3. **No other edits.** "Change only the capitalization of letters" — deletions, insertions and
   reordering are excluded by the author, which makes the para-126 `st` deletion a typo rather than
   a signal.

## 8. What this makes worth testing next (cheap first)

1. **Signature-as-instruction, not selection.** If the letters are obvious from Hal's solution, the
   chapter's role may be to *supply* the signature rather than to be scanned for it. The four
   FFWW windows give the same twelve letters four times; the untested reading is that the flip set
   is the same four *positions within each window* (the F,F,W,W paragraphs plus the I between the
   W's), applied as one set of twelve and as four sets of four.
2. **Class 3 slips on the accepted sets.** Each window with exactly one paragraph's direction
   inverted, and each window with one stray capital — her documented error, never enumerated.
3. **The claim step.** Index 76 (block N, Nth key) has been swept; the *second* wallet hop and the
   "password manager" chain have been swept; what has not is the possibility that the hashed object
   is the chapter text *as the claimer would paste it*, i.e. with the trailing spaces of the 13
   paragraphs stripped by a browser copy.
