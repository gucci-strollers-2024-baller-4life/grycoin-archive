# Grycoin Block 77 stage two — consolidated state (2026-11-12)

Escrow: `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` — re-verified 2026-11-12:
77,700,000 sats, 1 funding tx, 0 spends, 0 mempool. UNCLAIMED.
Superseded escrow `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC` is dead. Use it only for calibration.

## Substrate, verified byte-level

- Chapter *Second* (part 720888559): 273 paragraphs, 44,906 characters, LF `\n\n` join,
  md5 of the joined text `46a308c279540a33e977ea1f660e8458`.
- 272/273 paragraph ids reconcile with `md5(paragraph text)`; the one outlier is the duplicate
  `"What?"`, whose Wattpad id is `md5(hex(md5(text))+"1")`. Confirms the corpus is the stored
  data, not a re-typed copy.
- Ten paragraphs carry internal `<br>` (62, 72, 120, 123, 145, 159, 183, 188, 192, 212). The
  flattened text is 44,896 characters; the true text is 44,906. Both were swept.
- Live escrow serialization is CRLF CRLF between paragraphs, author-confirmed in his own words
  on the old escrow thread; the earlier escrow used a single CRLF. He rehashed with a
  "slightly different solution" when he moved it.

## Pipeline, certified

`md5(text)` -> 16 bytes -> BIP39 entropy -> 12 words -> `m/44'/0'/0'/0/i`, compressed P2PKH.
Certified on 150 of 153 recorded answers in `prior/ANSWERS.md`:
R2 blocks (MD5, 12 words) all present rows hit; R1 blocks 15-75 (MD5) hit; R1 blocks 1-14 hit
only with the FULL 32-byte SHA-256 digest as entropy (24 words), 14/14. The three misses are
a truncated dump row and the two R2 blocks that have no solution (76 was solved later, 77 is
this one). Field convention: space-separated, index 0, compressed.

## Calibrations that keep the oracle honest

- Block 76 exact input: `EMERGENCY TOMI climate EMERGENCY` -> md5 `f8e5edbc…` ->
  `13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd` (7,700,000 funded and spent), WIF
  `L5h7ptMonsAHscBD6HFtWDBNnq6cfe79MaNi7Qx1PK4sz4LshRTL`.
- Pasted string `HoaxBFUB137SFKp9MPjymMQVk85oarHoaxUd9QyeiA[link]` = R1 block 34 with spaces
  lost; true preimage `Hoax BFUB 137SFKp9MPjymMQVk85oarHoaxUd9QyeiA HDD` -> md5 `fbe46589…` ->
  `1G6wfwVAuKP3PEm1d1uxCnp5qp5icXhb8V`, funded and swept same day 2019-04-13.
- Stage one of block 77 reproduced: `19TbyN5…`, and flipping the four F/F/W/W paragraphs
  regenerates `9dd2efb9…`, stage one's escrow.

## The question, verbatim (part 720895205)

  "The solution is the puzzle. Format: [solution] TOMI omit TOMI [link]
   Solution format is eight items in two sets of four. Two items ciphertext and
   two items plaintext each, 44 read from left and 44 read from right."

The link field is the previous block's full private key (Block 76 WIF above).
R2 answers in the dump are short (`reverse Turing test`), so the eight-item idiom belongs to
round one; this is our reading of the question and it is not certain.

## The eight case pairs

Folding each paragraph's first letter against its mirrored terminal yields exactly eight
pairs, matching stage one's flip count:
¶1/273 S-s, ¶8/266 W-w, ¶9/265 N-n, ¶46/228 T-t, ¶51/223 Y-y, ¶71/203 R-r, ¶92/182 I-i,
¶97/177 T-t. Zero same-case pairs. Under Atbash pair numbering (1 = AZ … 13 = MN) the eight
letters S W N T Y R I T read 8 4 13 7 2 9 9 7.

## Closed, with counts

| Lane | Size | Result |
|---|---|---|
| Whole-text rule grid: unit x 5 sign sets x 2 directions x 5 change types x joins x tails | ~2,160 texts | 0 |
| 1-flip and 2-flip among the 544 paragraph edges | 296,480 derivations | 0 |
| Power set of the 16 case-pair paragraphs | 131,072 derivations | 0 |
| Nine mechanics on the case pairs, both joins | 300 derivations | 0 |
| Stage-one-rule re-sweep on `<br>`-correct bodies, 2^16 sign subsets | 262,000 derivations | 0 |
| Anomaly-sign families, 25-rule sign grammar, 3 bodies, 4 modes | 24,600 + 3,600 | 0 |
| Caps-only families (verbatim, VI/BI fixes, unflip variants, 6 case modes, joins, trails) | 5,760 texts / 11,520 derivations | 0 |
| R2:77 skeleton on the observed R1 item shape | 29,160 + 17,280 + 506,880 | 0 |
| Boundary words at the eight case pairs with reversal | 4,608 | 0 |
| Chapter headings and short strings | 1,008 | 0 |
| Paragraph spans across all 33 publications, joined, wrapped with B76 WIF | 377,815 spans | 0 |
| Sliding window over the concatenated corpus at lengths 45,050 / 45,450 | 210,676 + 210,276 windows | 0 |
| Earlier campaign, 34 families across two independent efforts | 400M+ candidates | 0 |

## Live lane

**Two-edge case flips.** 544 paragraph edges (first and last letter of every paragraph).
Every unordered pair of distinct edges is flipped in case, for both joins, tested with the two
most likely wrap strings. Size: 147,443 pairs per join x 2 joins x 2 wraps = 589,772
derivations at about 250/s. Join 1 (`\r\n\r\n`) closed negative at 147,443 pairs; join 2
(`\n\n`) in progress. `edge.ckpt` resumes it, `HIT_EDGE.txt` is written on a match.

**Sliding window remainder.** Lengths 45,050 and 45,450 are complete and negative; length
45,994 has 101,732 of 209,732 windows left. This lane asks whether the answer is the
concatenated corpus clipped at both ends by a small amount rather than a whole paragraph span.

## What is actually blocking

The selector: which characters the author capitalised. Everything else is arithmetic. He says
so himself: "It is for 77, but you will not see it if you let a script solve the block."
No format hint for stage two was ever posted, and he lost his own solution record (part
762380140, "Starting Up"). Fairness doctrine from part 740685487 ¶24: all the resistance comes
from not knowing the method, none from not knowing a fact. So the answer is derivable from
public material; it is a reading problem, not a compute problem.

## Operating rules

- Never use sub-agents. Never spend credits without explicit confirmation.
- Every tool call finishes inside 290 seconds; detach anything longer with `setsid` and
  checkpoint it. Background jobs die about ten minutes after their parent shell closes.
- A negative needs a witness: a known-good input pushed through the same code and re-found.
- Never broadcast a transaction and never print private key material into the repo.
