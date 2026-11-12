# The Hoax rule: the solution's capitalization is inherited from the source

Source: Wattpad part 720890652 ("Hoax"), paragraphs 19-25. The author found the pre-existing
address `137SFKp9MPjymMQVk85oarHoaxUd9QyeiA`, noticed the word `Hoax` inside it, and used it:

> "The solution is of course the word Hoax, starting with a capital letter because the address I
> found had it that way."
> "Solution is one word, capitalization will be evident."

Published format of that block: `[solution] BFUB [BFUB text] [link]`.

## Why this matters for the RBB

It fixes what "capitalization will be evident" means across the whole quizchain: the author does not
choose which letters are capital. She copies the case pattern out of a source string that already has
it. Block 29's `vOIce` is the same move (the O and I are the capitals present in the source phrase),
and stage one is the same move (the four paragraphs whose initials are F,F,W,W and whose final
letters are s,t,n,m supply the twelve letters).

So for the RBB the flip set is *read off a source*, not invented, and the answer's case pattern should
be reproducible from a visible artefact rather than guessed.

## Consequence for our search

Every "pick k letters and flip them" sweep we ran is looking in the wrong space. The productive
question is: **which visible string already carries the RBB's case pattern?**

Candidates, in order of plausibility:
1. the three planted FFWW windows in the chapter (5-8, 93-96, 168-171) - read, not chosen
2. the Finney reprint 231-235 as the source of the twelve letters
3. the prize address `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`, whose `MLRR44` block is the only
   digit-bearing run in it
4. the stage-one key/address pair

## Tests run this session

- anomalous-capital scan: the chapter contains exactly one word with an internal capital (`ppM`,
  para 73), so "flip the visible anomalies" has almost no signal to work with
- mid-sentence capitals: 322 hits, dominated by proper nouns (Satoshi, Finney, Aoi, Tom, Grycoin)
- flipping internal-capital words, then mid-sentence capitals, then both: 24 derivations, negative
- `BFUB`/`TOMI` field position confirmed as `[solution] F [F text] [link]`, so any RBB string with the
  field omitted is `[solution] [link]` only

## Numeric rewrite axis (2026-10-31)
Diffing chapter 11-29 against the source part "Second Life" gives five rewrites, all numeric or semantic:
`"2020."` <- `"Still 21st Century".`, `ten` <- `one hundred`, `A` <- `Third most`, `third` <- `second`,
plus the added sentence `I recognize the signs.` where the source has `right now.`
Reverting all five, alone and crossed with the Finney-4 and all-FFWW flip sets, both joins, indices 0-3: 64
derivations, no hit. The chapter's 23 distinct numerals tested as ordered, reversed, comma and unseparated
strings: also nothing. Numeric-rewrite axis closed.

## Operational
- `demo_oracle.py` wordlist path repaired to `harness/bip39_english.txt`; derivations working again.
- `ninjaops-puzzle-lanes` is a dangling symlink in this workspace and `quiz1_blocks.py` is not present
  anywhere under /app. Block calibration data must be re-supplied by the lane that holds it.
