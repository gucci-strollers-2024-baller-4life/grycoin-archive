# Grycoin — Legend, Lexicon, Compass, Mapping

Every entry carries its source. Nothing here is inferred without a citation.
Sources are cited as part (pid) ¶paragraph.

---

## 1. The two blocks

| | Round one, block 77 | Round two, block 77 |
|---|---|---|
| Subject | Genesis coinbase address `1A1zP…DivfNa` | Wattpad chapter **Second**, 273 ¶, 45,450 chars |
| Status | **Solved**, then re-hashed | Stage one solved; **stage two unsolved** |
| Format stated | `[solution] TOMI omit TOMI [link]` (720895205 ¶384) | none stated anywhere |
| Solution shape | "eight items in two sets of four. Two items ciphertext and two items plaintext each, 44 read from left and 44 read from right" (720895205 ¶385) | unknown |
| Verdict in his own index | "Failed block, made subtle hashing mistake, but corrected that way before anyone came close to the solution" (720895205 ¶381) | "Stay tuned…" (720895205 ¶707) |

The chapter is titled *Second* and its own description line reads **"Hint for block 77."**
He states that stage one's solution becomes stage two's question.

---

## 2. Lexicon

### Aa, the case pair
The same letter in opposite cases at the two ends of a string. It is a **pointer**, not decoration.
> "this address explains in its very first letter A that Atbash is used here. Not because Atbash starts with A, but because the very last digit is a as well. This tells the reader to look out for this inverse relation of letters" (761570746 ¶19)

His own hint 2 restates it: "the first digit and the last digit of the address are both the letter A. One capital A at the start and one lower case a at the end" (761570746 ¶108).

### Atbash
The 2000-year-old inverse alphabet. A↔Z, B↔Y, C↔X, D↔W, E↔V, F↔U, G↔T, H↔S, I↔R, J↔Q, K↔P, L↔O, M↔N (761570746 ¶44).

### Atbash foldover
Two things share the name:
1. The paired alphabet itself: `AZ BY CX DW EV FU GT HS IR JQ KP LO MN` (761570746 ¶44). Also the TOMI field of round-two block 30 (742662804 ¶357-362).
2. A foldover of a string: position *k* paired with position *n+1−k*, giving pairs in order (761570746 ¶39). Described as "the first step when looking at something related to Atbash" (¶38).

### BIT → GRY
Earlier letters: "GRY is what you get if you do an Atbash substitution on BIT and rearrange the letters. B resolves to Y, I to R and T to G" (720888559 ¶102).

### BFUB
The old name for the TOMI field: "brute force user block" (721505724 ¶1-5, 717956015 ¶21).

### Ciphertext / plaintext items
Round-one 77's four-part vocabulary: each set of four holds "two items ciphertext and two items plaintext" (720895205 ¶385).

### FFWW
The dedication. "WW obviously is UUUU or four U, for you" (720888559 ¶240). FF is left deliberately unexplained.

### GOOF
"Google Only One Fay" — a one-way-function joke coined for the Hoax (720890652 ¶42).

### Grycoin
`gry` + `coin`, from GRY, from BIT through Atbash and rearrangement.

### Hoax
A word found inside an address, used as a clue while the published hint points elsewhere. Policy: "I definitely reserve the right to mislead people when writing a quiz. Avoiding falling for the Hoax is part of the challenge" (720890652 ¶34).

### Keystone
The **central P** of the genesis address. "P resolves to K in Atbash. K as in keystone, the central stone holding in place the ceiling of a cathedral" (761570746 ¶115). Also floated: "P" as "puzzle", as "password", or as "pointer" (¶63-64, ¶51).

### Minmin
A solver who does not script. "From the short slogan 'mine with your mind', which in turn uses the fact that 'mine' and 'mind' share the first three letters" (717956015 ¶48).

### Nakamoto
"in Atbash the pair MN is actually right in the middle of the list. Naka means middle in Japanese. And moto is origin" (761570746 ¶59). MN is pair 13 of 13, the exact centre.

### Nm ST
"Nakamoto Satoshi" with the family name first, the Japanese convention (761570746 ¶35). Same four letters as the chapter's `STNM` (720888559 ¶239).

### Nonce
Two uses. Cryptographically, random filler for proof of work (757574334 ¶11). In the anagram, the spare letters: "An extra I and a missing M in Satoshi" (757574334 ¶3), and the pair "might be read as 'I'm' or 'I am'" (¶18).

### Pointer
A digit or letter that tells you where to look. "the 7 is in Atbash pair 7, P7. I think the P means 'pointer'" (761570746 ¶51). His first hint: "7 … at the 7th digit counted from the end. And I think this digit '7' is one of the keys to break this code" (731219798 ¶4).

### Satommi
The Grycoin subunit, 10^8 per coin, honouring Thomas (720888559 ¶104, ¶208).

### Second
Three meanings, all live: the chapter title; Harold Thomas Finney **II**; and the extra **S** in SATOSHI. The last is offered only hedged and third: "'may just mean Second'" (757574334 ¶26).

### Signs
The letters whose first-letters you recognise. Stage one: the sign set is `I T A S M`, and the four paragraphs that fail it are the ones to flip (720888559 ¶227-229). "Signs" occurs in 14 paragraphs, ¶20 through ¶273.

### STNM
The signature. Terminals of the four flipped paragraphs, in document order. Printed in the chapter as its own paragraph, ¶237, followed by "I STNM." at ¶239.

### TOMI
"Thinking Only Method", plus an I that is "just a nonce … making the thing four letters". Means "wealth" in Japanese (721505724 ¶6-9).

### 44
In round one, "44 read from left and 44 read from right" (720895205 ¶385). Also hints about the number four meaning "divide by four" or "solution string length 4" (720895609 ¶8-9).

---

## 3. Compass — how he reads a puzzle

Distilled from the genesis walkthrough, which is the only complete worked example of his own reading (761570746 ¶13-61):

1. **Find the pointer.** Look at the two ends for a case pair, and at digits for positions. `Aa` says: this is inverted.
2. **Fold.** Pair first with last, second with second-from-last. Print the pairs with ordinals.
3. **Read from the end, not the start.** "Reading from right to left, I see a lucky number 7 there. It tells us to look at the seventh digit from the N" (¶32).
4. **Count from each pointer to the next.** "I note the S two digits left from the m … And the fifth digit from the S is T" (¶33).
5. **Skip the delimiter.** "The L between m and S is Atbash for O, or zero, to show the reader that he should skip this digit" (¶34).
6. **Split in two and ask two questions.** "Two parts. Two partial questions" (¶116).
7. **Name comes family-first.** "in Japanese names, the family name is given first as a default" (¶35).

---

## 4. Mapping — address to chapter

| Device | Genesis address | Chapter | Verified? |
|---|---|---|---|
| Case-pair pointer at the ends | `1A1…DivfNa`, A…a | ¶1 "Second" → ¶273 "…signs." = S…s | **yes** |
| Foldover | 33-char payload, 17 pairs (761570746 ¶39) | 273 ¶, 136 pairs, middle ¶137 | **yes** |
| Case pairs in the foldover | pair 1 = `Aa` | **exactly 8**: ¶1/273, 8/266, 9/265, 46/228, 51/223, 71/203, 92/182, 97/177 | **yes** |
| Two halves | 16 digits, central P, 16 digits (¶114) | left set ¶1-97, right set ¶177-273, cleanly split | **yes** |
| Keystone at the centre | central `P` = `K` | middle ¶137 "Since the Grycoin blockchain…", no P | **no correspondence found** |
| Pointer digit | `7` at 7th from the end | no analogue identified | **unknown** |
| Signature | `Nm ST` | `STNM` at ¶237, ¶239 | **yes** |
| Two sets of four | 8 items = 2×4 (720895205 ¶385) | 8 pairs = 4+4 | **arithmetic matches** |
| The answer | a name, family-first | unknown | — |

---

## 5. What the legend does not buy

The lexicon explains round one **completely**. The chapter reproduces three of its features — the pointer, the eight-pair foldover, and the STNM signature — and all three are verified.

What the chapter does **not** reproduce is the digit-pointer. In the address, the reading was driven by `7` and `5` as ordinals: count seven from here, five from there. Those two numbers are what turn a foldover into a message. In the chapter there is no located `7`, so the foldover gives a marked set without giving a direction of reading.

That is the precise gap, stated in his own vocabulary: we have the `Aa`, we have the foldover, we have the eight items in two sets of four. We do not have the pointer.

---

## 6. Where to read it

- `wattpad/761570746_the-satoshi-code.txt` — the only complete worked example of his method. Read first.
- `wattpad/720895205_complete-quizchain.txt` ¶380-385 — round-one block 77's official entry and format.
- `wattpad/717956015_welcome-to-the-quizchain.txt` — claim procedure, TOMI, Minmin.
- `wattpad/740685487_exceedingly-unfair-riddle.txt` ¶24 — the fairness doctrine.
- `wattpad/720888559_second.txt` — the chapter itself.
