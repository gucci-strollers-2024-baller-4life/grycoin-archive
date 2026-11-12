# Patterns across the block log (new source fetched 2026-10-29)

Source: Wattpad part **720895205 "Complete Quizchain"**, 766 paragraphs, fetched from
`wattpad.com/apiv2/storytext?id=720895205`. This is Aoi's own running log: round 1 blocks 1-77 with
question, format and outcome per block, then round 2 blocks with the winners' explanations.
Saved as `cq_paras.json` / `cq_blocks.json`.

## 1. The 3-character codes are the previous block's private key, not checksums

23 entries state it. Examples, verbatim:

- b10: "The last three digits from the broken link in block 9 are set as fnw"
- b12: "Two words in harmony. Format: word1 word2 gFm (last block private key link)"
- b15: "append the last three digits of the private key of the previous block, with a space between"
- b46: "use last 7 digits of previous private key for link"
- b4 / b3 / b40 / b59 / b67 / R2 b3-b6: same construction.

That is exactly the `Pzd`, `Uzp`, `HwX`, `zff`, `KPb` ... suffixes. They are chained private-key
fragments, which is why no hash relation to the text exists (12 derivations tested, all zero).

**Consequence:** a solution string is `[solution] TOMI [method name] [3-char code] [link digits]`.
Bare-text sweeps of the chapter cannot match unless the appended fields are reproduced.

## 2. Hashed-by-mistake blocks are a declared pattern (11 blocks)

- b9: "not noticing that I copypasted a line break when hashing"
- b15: "Another block with failed hash. Switched to MD5 hash without noticing."
- b16: "Hashing failure mistake of block 15 also in this one."
- b44: "Failed block, forgot including link in hash."
- b48: "Changed name of BFUB field to TOMI and hashed with old name (same failure in blocks 49 and 50)."
- b55: "even while I messed up the hash for this block by not including the string 'TOMI'"
- **R1 b77: "Failed block, made subtle hashing mistake, but corrected that way before anyone came close."**
  (Correction 2026-10-31: this line is paragraph 381 of the Complete Quizchain log, directly under the
  round-one heading `Block 77`. It describes q1 b77, the genesis-address puzzle, NOT the RBB. See
  `SLIP_PATTERNS.md` §6.)

So the author's published text and her hashed text repeatedly diverged on: line breaks/joins, hash
algorithm, and included/missing fields. For block 77 (the finale's parent) a join-level or
field-level mismatch is the expected failure mode, not a wrong flip rule.

## 3. The answer format of block 77, in her own words

    Format: [solution] TOMI omit TOMI [link]
    Solution format is eight items in two sets of four. Two items ciphertext and two items
    plaintext each, 44 read from left and 44 read from right.

Also: "Question: The solution is the puzzle." So the solution string is built out of the puzzle text,
in eight items, four per side, read 44 in from each end.

## 4. The TOMI field grammar

- b58: "[TOMI] is the name of the method used to get it, one word in upper case (only first letter capital)."
- b48: the field was called **BFUB** before block 48, then renamed TOMI (and 18 published inputs still
  carry `BFU`/`BFUB`/`BotFU`).
- Micro-rules used repeatedly: exactly one space between fields, no period anywhere (b20), solution
  first letter capitalised (b20, b61, R2 b7).

## 5. Word-count puzzle families

b52 "Six three letter words", b54 "4 four letter words", b55 / b61 / b75 "four letter word",
R2 b8 "Eight words", R2 b7 "Four words and a period at the end". The author reuses small integers as
answer shape, which is why "eight items in two sets of four" is a shape declaration, not decoration.

## 6. The Wattpad chapter is used as a key store

b22 "Needed Wattpad story as reference", b23 "until final version of chapter 2", b29 "look at Chapter 3",
b32 "Needs chapter 3 text as reference", R2 b2 "using the puzzle string in the latest Wattpad chapter on
quizchain as a password manager in exactly the way it was described there and then ... Second private
key because this was block 2". So **index = block number** is a documented convention in round 2.

## 7. Chapter-side patterns that survive all of this

- The FFWW / s,t,n,m signature occurs exactly three times: paras 5-8, 93-96, 168-171 (gaps 88 = 2x44,
  then 75). Para 93 is the chapter's only 44-character paragraph.
- Para 229 states the rule in words: "All paragraphs except for four, which start with F F and W W."
  Para 230 follows: "the only ones where we don't recognize the signs."
- The `"What?"` duplicate at 34 / 78 is 44 apart and is original text (Wattpad dedup hash, certified).
- 13 paragraphs carry significant trailing spaces: 86, 108, 122, 128, 139, 147, 165, 166, 192, 201,
  209, 220, 267.

## 8. Tests run off the new material (all negative)

- 2,652 derivations: 5 selection sets (plain, FFWW/stnm pairs, the three windows, ITASM, not-ITASM) x
  4 edge modes x 2 joins x key indices 0-77 against `14zMk...`.
- 360 derivations: end-quadruples (1-4 + 270-273), 44-in pairs (44/45 and 229/230), stride-44 from
  left, from right, both, and "all except the four FFWW", x 5 edge modes x 3 joins x indices 0/1/2/77.

No hit. Combined with section 1, the most likely reason is that the hashed string is not the bare
chapter at all: it is the chapter plus the TOMI/method/code/link fields.
