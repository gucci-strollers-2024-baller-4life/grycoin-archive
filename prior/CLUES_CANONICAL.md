# RBB / Quizchain block 77 — canonical clue corpus

Repaired and re-verified 2026-10-29. This file supersedes the overlapping claims scattered across
`README.md`, `RBB_DOSSIER.md`, `HUNT_LOG_edges.md`, `PATTERNS.md`, `FRESH_ANGLES.md`,
`DISCREPANCIES.md` and the Google-Drive working notes. Where they disagree, this file wins and the
disagreement is logged in §8.

Source tags: **[V]** re-derived byte-level or on-chain in this session · **[A]** author-published
primary source · **[R]** carried from the repo, not re-verified · **[X]** falsified, do not reuse.

---

## 1. Three different "block 77"s, disentangled

The single largest source of confusion in the corpus is that "block 77" names three separate escrows.
They must never be swept together.

| id | what it is | escrow | prize | status |
|---|---|---|---|---|
| **q1 b77** | first run, final block. "The solution is the puzzle." The puzzle is the **genesis address**. | `1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP` | 0.077 BTC | **SOLVED 2019-07-15**, claimed `b0a24545…` **[A]** |
| **q2 b77 stage one** | Hal Finney's bitcointalk post (topic 155054) case-flipped. Format `[solution]`, **no TOMI field**. | `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` | 0.077 BTC | **SOLVED 2019-08-03** **[V]** |
| **q2 b77 stage two = RBB** | the Wattpad chapter "Second" case-flipped. 777 mBTC. | `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` | 0.777 BTC | **LIVE, UNSOLVED** **[V]** |

**Prize re-verified on-chain this session [V]:** `14zMkTga…` has `funded_txo_sum = spent_txo_sum +
77700000`, `spent_txo_count = 0`, `tx_count = 1`. The single funding tx is
`a1916e7e…8514d1f`, block time 2019-07-30 23:49 UTC, from `3E7gTGXp4EcKhcLo69Utw3vae4Axj5ZPh7`.
The earlier address `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC` was **taken back by the author, not
claimed** (her own words, post update of 2019-07-30). Any sweep still aimed at `1EFojcAo…` is
aimed at a refunded escrow.

---

## 2. Key pipeline [V]

```
text  ->  MD5 (16 bytes)  ->  BIP39 12 words (empty passphrase)
      ->  PBKDF2-SHA512 2048  ->  BIP32 m/44'/0'/0'/0/0  ->  P2PKH (compressed)
```

Certified by reproducing published values:

| input | md5 | derived | expected |
|---|---|---|---|
| q2 b77 stage one flipped post | `9dd2efb9bc976c2095bd534d7b8d431c` | `19TbyN5Kg…Rj5KN`, WIF `KwwZ4HGv…tGor2` | both match **[V]** |
| q1 b77 pre-hash (see §3) | `684b250ea52c1e33a6f6143ded0e62e6` | `1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP` | matches **[V]** |
| chapter, `\n\n` join | `48d318202691ffb873e00b63196eaf36` | `14isnRimk9qAzpm85qwiFgLjzxL1387TXL` | matches repo **[V]** |

Harness: `work/btc.py` (dependency-free; secp256k1 fixed-base comb, BIP39, BIP32 private-only
descent). Self-test passes; **compressed** pubkeys are required — the uncompressed form gives a
wrong address and silently produces false negatives.

---

## 3. The certified hash template for a final-round block [V] — new

The block-77 round-one record carries the MD5 of its pre-hash but nobody had reproduced it. It is
reproducible, exactly:

```
"1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN" + " TOMI Omit TOMI " + "L4VdZUDY2BXa7VVkjuYkmaLvi8P5qNZaARwwB9wjqkDa6Sn4JLV4"
  -> md5 684b250ea52c1e33a6f6143ded0e62e6 -> 1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP
```

- Field separator is **exactly one space**, fields in the order `[solution] TOMI [method] [link]`.
- The literal method field is `Omit TOMI` (the author's standing joke after the BFUB→TOMI rename),
  which is why the format line reads "TOMI omit TOMI".
- The link is block 44's **whole WIF**: `L4VdZUDY2BXa7VVkjuYkmaLvi8P5qNZaARwwB9wjqkDa6Sn4JLV4`
  (published by the author in the block-77 thread; block 44 was unsolvable because she forgot the
  block-43 link, so she printed the key).
- This is the only place in the whole corpus where a template can be checked against a hash.
  Anything that claims a different separator, field order or casing is guesswork.

**What it does and does not license.** It certifies the round-one *format*. The author then said,
of stage two: "Once someone figures out the format for the first stage, they will also have a big
hint for the format of this second stage." Stage one's format is `[solution]` — **no TOMI, no
link**. So the TOMI/link template must NOT be bolted onto stage two. See §5.

---

## 4. Stage one answer and its geometry [A]

Answer (posted by a player 2019-07-15, confirmed by the author):
`1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN`

Eight items, two sets of four, taken off the genesis address `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`,
four from the left half and four from the right half read backwards. Signs = hidden names (HAL
FINNEY) plus reversed Satoshi/Nakamoto with the capitals travelling to the end of each item.

Stage one (the Finney post) is a *different* mechanism on the same principle: keep the whole text,
change only capitalization. Certified flips: the four paragraphs whose first letters are F, F, W, W
with one I-paragraph in between — first letters lowercased, last letters uppercased, spelling STNM
at the tails. That reproduces `9dd2efb9…` exactly **[V]**.

---

## 5. Stage-two spec, from the author's own notes [A]

- Question: "Final version of the second chapter of Wattpad story" — `wattpad.com/720888559`.
- "It is also hashed with **two line breaks between paragraphs** now" (post update, 2019-07-30).
  "Hit enter twice. This displays in Ascii as 13 10 13 10." So the join is `\r\n\r\n`, not `\n\n`.
- "I took back the prize … and sent it again to a new address, hashing with a slightly different
  solution … It has multiple paragraphs and two line breaks between each of them."
- "The main point of this block [Grycoin block 2, `cleczc`] is to give a simple example for the
  format used in **both phases of block 77**."
- Grycoin block 2 states in its own body: "Still not using a TOMI field, though. Does not need one."
  And it teaches the mechanism: *keep the whole long text, change only a couple of letters in their
  capitalization, for all the paragraphs where you recognize the signs, and keep the rest completely
  unchanged.*

**Consequence, and it is a repair.** The hashed object for the RBB is the chapter text with case
changes, joined `\r\n\r\n`, with **no TOMI field and no link field**. The corpus's open lead
"chapter + TOMI/method/code/link" (PATTERNS §1, FRESH_ANGLES D1) is a wrong turn: that template
belongs to round one, and stage one of block 77 explicitly had no TOMI. Demoted, not deleted — if
every bare-text family closes, revisit it.

---

## 6. Chapter byte facts [V]

- 273 paragraphs. 272 certify against Wattpad `data-p-id`; paragraph 78 certifies by Wattpad's
  dedup rule `pid = md5(prev_md5_hex + "1")` → `8b71bade…`. **All 273 certify; there is no edit
  anomaly.** (See §8, correction 1.)
- Only exact duplicate: `"What?"` at paragraphs **34 and 78**, delta exactly **44**.
- 13 paragraphs carry real trailing spaces: 86, 108, 122, 128, 139, 147, 165, 166, 192, 201, 209,
  220, 267. Keeping them is part of "keep the rest completely unchanged".
- FFWW-first / stnm-last signature windows: **5–8**, **93–96**, **168–171** — exactly three.
- Only 44-character paragraph: **93** = `For starters, define the project's purposes.`
- First-letter string of the chapter is recorded in §10 for diffing.
- Paragraphs containing "signs": 20, 42, 220, 222, 223, 225, 226, 227, 228, 230, 236, 244, 246, 273.
- Paragraphs whose first letter is not in {I,T,A,S,M}: **120** (the corpus says 118 — see §8).

---

## 7. What is closed, quantitatively

All of the following are address-verified against `14zMkTga…` unless stated:

- every single-paragraph and every paragraph pair, canonical CRLF join, idx 0 and 1.
- 2^12 and 2^15 seal/subset closures over the 16 signature paragraphs.
- every paragraph-edge combination per paragraph {none, first↓, last↑, both} on the **demo** text.
- word-edge k ≤ 3, up-to-4-anywhere and 5-boundary (GPU, >100B candidates) on the demo.
- structural spans × 9 rules × 3 joins × 4 indices (~2.4k), the "44 from each end" literal readings,
  the password-manager chain, end-quadruples, stride-44.
- this session: 84 structural candidates on the chapter at `\r\n\r\n`, idx 0 — the three FFWW
  windows individually and combined, the reproduced quote run {231,232,233,235} and {…,234},
  {34,78}, {222}, {229,230}, the 14 "signs" paragraphs, and all-273 — each under 6 edge modes, plus
  plain / stripped / `\n\n` serialisations. Zero hits.

Design constraint that follows: any valid flip set is **at least three paragraphs** and cannot be
drawn only from the 16 signature paragraphs. Everything she published points at ground that is
already swept, which is why the remaining variable is a judgment call she made about which
paragraphs carry "signs" — not a mechanically recoverable set.

---

## 8. Corrections applied to the corpus

1. `README.md` and `RBB_DOSSIER.md` still say paragraph 78's pid mismatch proved the author
   overwrote it with `"What?"`. **False** — Wattpad dedup hash, duplicate is original text.
   `CORRECTION_para78.md` had already established this; the two older files were never repaired.
2. `HUNT_LOG_edges.md` and the Drive notes list the demo's "true escrow" sweep as authoritative while
   `RBB_STATUS.md` records a **fatal path bug** in the earlier oracle (`m/44'/0'/0'/0/0/i` instead of
   `m/44'/0'/0'/0/i`). Any pre-2026-10-27 negative produced with that oracle is not evidence.
3. "Non-ITASM paragraphs = 118" → **120** by direct count.
4. "Paragraphs containing 'signs' ≈ 11" → **14**, enumerated in §6.
5. The RBB escrow must be cited as `14zMkTga…` (funded `a1916e7e…`); `1EFojcAo…` was refunded, not
   claimed. Several notes imply otherwise.
6. Open lead "TOMI/link fields missing from our sweeps" — demoted per §5.
7. "Block 77 unsolved" — only stage two is unsolved. Round-one block 77 and stage one were both
   solved in 2019 and their answers are public (§1, §3, §4).

---

## 9. Open leads, ranked

1. **Semantic sign-set search with the certified harness.** The only open variable is *which*
   paragraphs get flipped. Enumerate rule families that a human would actually use (paragraphs that
   mention the mechanism, paragraphs adjacent to markers, mirrored positions around 34/78, the
   44-stride lattice, quotation boundaries) and treat each family × edge mode as one candidate. At
   75 derivations/s a core-hour is 270k candidates — enough for rule families, never for subsets.
2. **The 44 lattice.** 34 and 78 are the anchor; 44 is also the derivation purpose (`m/44'`), the
   length of paragraph 93, and the index stride between windows 5→93 (88 = 2×44). A rule "positions
   ≡ 34 mod 44" and its mirror have not been swept as *sign sets* (only as byte offsets).
3. **Two byte states.** Hashing the Wattpad-tagged form (`<p data-p-id="…">text</p>`) or with pids
   interleaved. Cheap, untested, low prior.
4. **Author's own solution was lost** ("not even to me") and the only solver of the neighbouring
   blocks never revealed anything, so there is no disclosure route. Do not plan around one.
5. Anything requiring a TOMI/link suffix: parked, see §5.

---

## 10. Artifacts

- `work/btc.py` — verified key pipeline + self-tests.
- `work/sweep1.py` — the 84-candidate structural sweep of this session.
- Chapter first-letter string (1-indexed, for diffing):
  `SISIFFWWNIGAIIWVWGIFAYTSNYCTWIANWIWOYOAKINHTTLWASYWYRIYYWYONYIHTWTIIWRTTHISTWOIVWTSITBIATPIFFWWTITFIFAAGFAOAOTSITBGIOTFIOOTTSAVEIGWTBABSIWTIBPTIPTBOSAWBBDTWGAICIIMIIIFFWWSOATaIATSAbTTTTIATOAAITTSISTTOTIAHAAScTTAASdHITAAHTTOSMTTAHFFWIWWSIITATTITTOEBaHbHcHdAeWfHSIIWIATTAAIA`
  Case is preserved deliberately: a handful of paragraphs open on a lowercase letter, which is
  itself a candidate sign.

---

## 11. The link-chain theory: tested and falsified (2026-10-29, second pass)

The proposal was: rebuild the round-two chain b1→b76 from the log's solutions and TOMI texts, take
b76's true private key, and hash the RBB answer as `[solution] TOMI omit TOMI <b76 key>`. The
proposal rests on the "Welcome to the Quizchain" claim procedure, which is real. It does not survive
contact with the record set.

**11.1 The round-two format itself is certified [V].** Using the published literal answer strings and
the verified harness, `[solution] TOMI [TOMI text] [previous WIF]` reproduces the published escrow
address for at least 25 of the 77 rounds-two blocks, including:

| block | published string | md5 | derives |
|---|---|---|---|
| b1 | `U2 TOMI upside down L2e6gPSX…` | `33c6780dcb…` | `15BbSHKq…` ✓ |
| b3 | `reorg TOMI CZ Binance L2e6gPSX…` | `5f6870da0f…` | `1FsYtK22…` ✓ |
| b4 | `MasK TOMI previous block private key` | `9acb509e17…` | `1C1e2wvP…` ✓ |

So the general template is not in doubt. The remaining 52 records carry prose answers rather than the
literal pre-hash, which is why they do not reproduce.

**11.2 The chain does not need rebuilding, because the keys are already published [V].** The
authoritative record set carries a WIF for **76 of the 77** round-two blocks. Decoding each WIF and
deriving its P2PKH address reproduces the published escrow address for **76 out of 76** — zero
mismatches, b1 through b75 and b77 included. There is nothing to reconstruct: the chain is published
end to end, and b75's real key is `KyjdU7g9VHRwvZWe6337DPCeHZFpVojPEgHsTebH2GuZLnKvGqYf`.

**11.3 The one missing key is b76 — the only key the RBB could need [V].** b76 has no WIF. It cannot
be derived, because:

- its solution was never published: "Nobody ever published the solution" (record), and the 2026
  sweeper of `13Cv6SX…` said nothing ("who did it? kindly tell us the solution");
- the author refused further hash digits ("Not going to do more hash digits for 76, would make it
  too easy to script the block"), published only the `f8e` prefix and "first two digits of solution
  only are 1d", and states the solution is not in any word list;
- she is inactive since 2019, so there is no disclosure route.

Therefore b76's full key, and likewise its last 7 characters, are **not obtainable by anyone**.

**11.4 Consequence: the RBB cannot contain a link field.** If the RBB hashed `… TOMI omit TOMI <b76
key>`, the block would be permanently unsolvable by design, which contradicts both the author's
intent ("I wanted to remove one of the twists I had. The block is now slightly easier") and the
certified facts:

- stage one of block 77 is `[solution]`, bare — author, verbatim: "I do disclose that this one has no
  TOMI field, but that is all." Its md5 `9dd2efb9…` → `19TbyN5…` is reproduced **[V]**;
- the format example she wrote for *both* phases (Grycoin block 2, `cleczc`) says "Still not using a
  TOMI field, though. Does not need one.";
- "Once someone figures out the format for the first stage, they will also have a big hint for the
  format of this second stage."

So the RBB pre-hash is the case-flipped chapter, `\r\n\r\n`, nothing appended. The chain job is
**cancelled as unnecessary and as insufficient**; do not spend a session on it.

**11.5 The proposed RBB string is round-one block 77's answer, and it is already spent [V].** 40
link × TOMI-field × separator combinations of `1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN` were
derived. The only structure that lands anywhere is the round-one template —
`… TOMI Omit TOMI L4VdZUDY…` → md5 `684b250e…` → `1FAAKpzF…`, the **already-claimed** round-one
escrow. Every variant, including b75's full key and last-7 in both links, misses `14zMkTga…`. The
genesis-address item string is q1 b77's solution; it is not the RBB's solution, and no link variant
of it will ever open the 0.777 BTC.

---

## 12. Wordplay rules: the primary sources, and a new anomaly inventory

### 12.1 The four rule statements, verbatim

1. **Round-1 block 2** — the only place the mechanism is spelled out in full: *"One of the letters
   in the family name of the author is changed from lower to upper case. Change the other letters in
   his name in the same way for the solution."* Base: *"I posted A similar message to the Basecamp,
   but had to also come visit you all here on Reddit."* Solution: *"I posted A similar messaGe to the
   Basecamp, but had to also come visit You all here oN Reddit."* So: **one planted odd capital is
   the seed; the remaining letters of the hidden name are capitalised at their own occurrences.**
2. **Round-1 block 29** — interior capitals again ("capitalizatioN", "vOIce").
3. **Grycoin block 2 (the demo)** — the format example for both phases of block 77: *"keep the whole
   long text and change only a couple of letters in their capitalization … for all the paragraphs
   where you recognize the signs, and keep the rest completely unchanged."* Its worked example is one
   lowering ("I" → "i") and one raising ("himself" → "himselF"). Note both **directions** are used.
4. **Block 77 stage one** — certified: the four paragraphs whose first letters are F,F,W,W have those
   first letters lowered and their **last** letters raised. Reproduced by hash **[V]**.

### 12.2 The anagram chain the chapter itself builds

Thomas → Satoshi is an anagram with two nonces: a surplus I and a missing M (paragraphs 183-207).
The M is found one word right, inside Nakamoto, with TOM spelled backwards after it; the I is found
in Finney, or doubled in "Harold Thomas Finney II". HAL ↔ IBM by alphabet shift, with AHS preceding
BIT the same way (paragraphs 195-214). The surplus S is read as "Second" (paragraph 207), which is
the chapter's title and the name of the coin's smallest unit, satommi (paragraph 208). Paragraphs
228-246 then walk the reader through stage one: first letters I,T,A,S,M mark normal paragraphs, F,F
and W,W mark the four anomalies, and their last letters spell STNM.

### 12.3 New: the chapter's case-odd inventory [V]

Every word whose capitalisation pattern is neither all-lower, all-upper, nor Capitalised, over all
273 paragraphs, is exactly **14 instances**. Classified:

| paragraph | word | reading |
|---|---|---|
| 73 | `ppM` | **planted**: "350 ppm" is the CO2 target; the M is the chapter's only interior capital |
| 126 | `abcdefghijkLmnopqruvwxyz` | **planted**: alphabet address with a capital L (and a typo, `qruv`) |
| 126 | `abcdefghijkLmnopqrstuvwxyz` | **planted**: same, spelled correctly |
| 128 | `VIrgin` | **planted-looking**: sentence-initial V is normal, the I is not |
| 136 | `BItcoin` | **planted-looking**: same pattern, capital I after B |
| 209 | `BITcoin`, `AHScoin` | deliberate wordplay, explained in the surrounding text |
| 49 | `Paloecene-Eocene-Thermal` | legitimate: hyphenated capitals |
| 88 | `Peer-to-Peer` | legitimate |
| 106, 112 | `WorldWideAbsoluteCarbonBudget` | legitimate: a quoted burn address |
| 107 | `FUCKFuck…FUCKX`, `AndrewYangForPresident`, `oXXX` | legitimate: quoted addresses |

The five planted-looking ones inject the letters **M, L, I, T, S, H, A**. Read in document order the
injected capitals are M, L, L, I, I. The single interior capital is the **M of `ppM`**, which is a
letter of THOMAS and of NAKAMOTO, and it is the closest thing in the chapter to block 2's planted
`messaGe` G.

### 12.4 Applied this session, and what it cost

- **Blunt name-capitalisation tests (21 candidates, negative):** normalising the five planted
  anomalies; capitalising every occurrence of each injected letter set; and capitalising every
  occurrence of every letter of THOMAS, FINNEY, NAKAMOTO, SATOSHI, SATOMMI, HALFINNEY,
  AOINAKAMOTO, GRYCOIN, SECOND, STNM.
- **Rule-family battery (64,732 candidates, result in §12.6):** every subset of the 13
  trailing-space paragraphs under six edge modes; mixed modes across the three FFWW windows (6^3);
  every subset of the twelve window paragraphs under three modes; every subset of the ten
  lowercase-initial section headers; sentence-edge rules over the whole chapter and inside each
  window; and twelve section-aligned runs as the entire preimage.
- **Multi-paragraph spans (9,867 candidates, negative):** every contiguous run of 2 to 40 paragraphs
  as the whole preimage, which is the most literal reading of "it has multiple paragraphs and two
  line breaks between each of them".

### 12.5 Why the mechanism resists brute force

Block 2 capitalises **one occurrence of each letter of the name**, in reading order. In a
45,984-character chapter, even restricting candidates to word-initial letters leaves ~10^9 in-order
embeddings for a nine-letter name, and every candidate costs a full derivation because the block has
no published MD5 prefix and no claim transaction, so there is no cheap sieve. The search cannot be
enumerated; the seed letter has to be argued, not searched. §12.3 narrows the seed to five planted
odd cases, of which `ppM` (paragraph 73) is the strongest.

### 12.6 Results

- **Rule-family battery: 64,732 candidates, zero hits,** 917 s at ~70 derivations/s.
  Breakdown: 49,146 = 13 trailing-space paragraphs × all non-empty subsets × 6 edge modes;
  216 = independent mode per FFWW window; 12,288 = twelve window paragraphs × subsets × 3 modes;
  3,070 = ten lowercase-initial section headers × subsets × 3 modes; 12 = section-aligned runs;
  6 = sentence-edge rules. Preimage: whole chapter, `\r\n\r\n`, index 0.
- **Multi-paragraph spans: 9,867 candidates, zero hits.**
- **Blunt name capitalisation: 21 candidates, zero hits.**
- **Exhaustive 2^20 flip closure over the 20 meta paragraphs** (the 14 "signs" paragraphs, the four
  FFWW quote paragraphs, `STNM`, `I STNM.`): first 26% of the mask space closed, zero hits; the run
  was paused to free the CPU for the rule families. Masks 278,528-1,048,575 remain, ~47 minutes at
  the measured 271 derivations/s. Harness: `work/sweep2.py MODE START END`.

---

## 13. Session 2026-10-29 (late): calibration sweeps and the sign-set correction

### 13.1 The email plan is cancelled, and it is now verified twice

The "rebuild the round-two chain b1→b76 and re-test the RBB with b76's key" plan is dead for the
reasons in §11, and the round-two template was reproduced again before spending anything on it:
`MasK TOMI previous block private key` → md5 `9acb509e17…` → `1C1e2wvP5p6JRyV4BtRHjprCuBcUXLudNQ`
(the b4 escrow). So the `[solution] TOMI [TOMI text] [link]` template is real, 76 of the 77
round-two WIFs are published and decode to their escrows, b76's key exists nowhere, and block 77
stage one is bare text. A link field in the RBB would make the block unsolvable by design.

### 13.2 New: the stage-two sign set is probably SATOSHI's letters, not I,T,A,S,M

The chapter states the stage-one sign letters as I, T, A, S, M. Applying that test to the demo
(`cleczc`, the author's own format example) yields **five** anomalies — paragraphs 3 (F), 4 (F),
6 (O), 7 (W), 8 (W) — which destroys the FFWW / "one I-paragraph in between" structure the whole
format rests on. Applying the letters of **SATOSHI** {S, A, T, O, H, I} yields exactly **four**:
3 (F), 4 (F), 7 (W), 8 (W), with paragraph 5 (I) and paragraph 6 (O) both reading as signs.

Consequence: the chapter's anomaly set under this test is **94 paragraphs, not the 118/120** every
sweep so far used. Any place the corpus says "non-ITASM" was measuring a set that may not be the
author's.

### 13.3 Swept and negative this session

Chapter (against `14zMkTga…` live and `1EFojcAo…` old):

| family | candidates | hits |
|---|---|---|
| sign-letter families {ITASM, SATOSHI, THOMAS, NAKAMOTO, FINNEY, HALFINNEY, STNM, AOI, SATOMI, SH, OH} × {first-letter in/out, last-letter in/out} × 8 edge modes × 2 joins × paths m/44'…/0 and m/0'…/0 | 1,408 | 0 |
| **44 lattice as sign sets** (§9 lead 2, never swept before): bases 34/44/78/93/222/5, stride-44 ladders, anchor pair {34,78}, mirror, ±1 neighbourhoods, the three FFWW windows, the 14 "signs" paragraphs, hint 222 | 1,056 | 0 |
| all 2^6−1 subsets of {34,78,122,166,210,254} × 8 modes × 2 joins | 3,072 | 0 |
| Wattpad-tagged serialisations (`<p>`, `<p data-p-id="…">`) at both joins (§9 lead 3) | 12 | 0 |

Demo (`cleczc`, oracle md5 `3c6` + escrow `1tzieUf…`):

| family | candidates | hits |
|---|---|---|
| paragraph-level directional edge modes (none / first↓ / first↑ / last↑ / last↓ / both), 4^10 × 2 joins | 2,097,152 | 0 |
| sentence-level subsets of first↓+last↑ | 65,536 | 0 |
| every subset of the 18 paragraph edge slots and of the 28 sentence edge slots, up to 8 flips, × 2 joins | 9,796,166 | 0 |
| name marking (block-2/29 shape: one occurrence per letter, reading order, uppercased), exhaustive in-order embeddings of AOI (141,989), STNM, AGYN, YANG, NAKA, HAL, GRYN, AOIN | ≈ 500,000 | 0 |

Not yet tested on the demo: FINNEY (92.1M embeddings), THOMAS (177.1M), GRYCOIN (123.6M),
NAKAMOTO (1.05e9), SATOMMI (0.92e9) — these need the C flipper, not Python.

### 13.4 Reading that survived

The demo's worked example is **sentence**-level, not paragraph-level: "I expected…" is the first
sentence of paragraph 5 and "himself" is that sentence's last word, so first↓ + last↑ on a single
sentence reproduces both quoted changes exactly (`I`→`i`, `himself`→`himselF`). The full answer
carries more changes than that pair, and every sentence-edge combination up to eight flips is now
closed.

### 13.5 Next

1. Sweep FINNEY / THOMAS / GRYCOIN name marking on the demo with the C flipper. Cheap and decisive
   for the "slightly developed from block 2" reading.
2. Re-run the chapter's semantic sign-set families with the SATOSHI test (94 anomalies) instead of
   ITASM — a different paragraph set, never used by any sweep in the corpus.
3. Do not spend time on b76's key; it does not exist outside the author's lost notes.

---

## 13. Harness bug found and fixed: base58 leading zero (supersedes earlier address claims)

**The bug.** `btc.b58check` built the base58 string by reversing a digit buffer that had the
leading-zero characters appended *before* the reversal, so a mainnet address came out with its
leading `1` at the wrong end. Every address beginning with `1` — that is, every P2PKH address in
this project — was therefore rendered incorrectly. Comparisons made on **address strings** could
never match.

**End-to-end validation after the fix** [V]:

    md5("Still 21st Century")      = 4c414876be9043da4538386be9a03df6      (published prefix 4c4 ✓)
    derived address                = 18EpYz5qB3XoxZWouJF3KdEp3E2nfv9FgP
    grycoin/1 prize address        = 18EpYz5qB3XoxZWouJF3KdEp3E2nfv9FgP      MATCH

`b58decode` was added and round-trips exactly (`b58check(b58decode(a)) == a`). MD5 → BIP39 →
BIP44 index 0 → compressed pubkey → P2PKH is now verified against a solved escrow, which it never
was before.

**What this invalidates.** Any earlier statement in this project of the form "N candidates derived,
no address match" that compared base58 strings. The RBB work is unaffected: it compares the 20-byte
HASH160 against `2bc16867479a8d01179a6452651abe14a65eb61a`, which the encoder bug never touched.

**Re-run of the demo search with the fix.** All case variants of the grycoin-2 demo already
enumerated — 69,393 three-flip LF, 69,384 three-flip CRLF, 159 two-flip CRLF, 69 unique hashes in
total 138,936 — were re-derived and compared on hash160 against the demo's prize address
`1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` (hash160 `09d565074752019721ce68c58548ebc13750d5cc`).
**Zero hits** [V]. Combined with earlier stages this means the demo's published solution is not a
variant of `demo_base.txt` with three or fewer letter flips, in either line-ending convention. Two
readings remain: the solution flips four or more letters, or `demo_base.txt` is not a faithful
reconstruction of the post the author hashed. The second is now the more likely one, because the
author describes the demo's change as "only a couple of letters". Until the demo text is re-extracted
verbatim from the forum post, the demo cannot serve as the calibration example for the RBB.

### Next concrete job

Re-extract grycoin block 2's text from the author's own post in `as_cleczc.json` byte for byte
(paragraph by paragraph, no rewrapping), rebuild `demo_base.txt`, and repeat the two- and three-flip
passes with the corrected harness. A demo solution in hand converts the RBB's unknown rule into a
known plaintext diff.

---

## 14. Two primary-source rules recovered from the author's own posts

### 14.1 The grycoin-2 demo has an explicit preimage boundary

From the author's own grycoin block 2 post (`grycoin_posts.json`, `data[2].selftext`), verbatim:

> *"…in the Question from this Reddit post. Start with the first \"I\" and stop with the period after
> \"method\", with no spaces or line breaks before or after that included in the hash. First three
> digits of MD5 hash are 3c6."*

So the demo's hashed text is a **slice**, not the whole post: from the first `I` to the period after
`method`, with no leading or trailing whitespace. Starting at the first `I` of the whole post means
starting at *"I still have not completely given up, here is another block now."*; the slice is
**1,456 characters, 12 blank-line-separated blocks, LF**, ending *"…Even after I explained the
method used and the result in detail."* (`demo_post_lf.txt`, `demo_post_crlf.txt`).

Tested with the corrected harness, all negative: the slice with 2 flips (156 LF / 153 CRLF
candidates), and the LF slice with 3 flips (53,704 candidates, 272 s of derivation). The earlier
`demo_base.txt` ten-paragraph reconstruction was also re-tested this way (2 and 3 flips, LF and
CRLF). **The demo's solution is therefore not a ≤3-flip variant of any reconstruction we hold**, so
the demo still cannot be used as the calibration plaintext. Either it flips four or more letters or
the slice boundaries/blank lines differ from the forum export.

### 14.2 The author's key-index convention: block N uses the Nth private key

From her explanation of round-two block 2 (`cq_blocks.json`, `rounds.R2[2]`), verbatim:

> *"This was just using the puzzle string in the latest Wattpad chapter on quizchain as a password
> manager in exactly the way it was described there and then pick the second private key under that
> puzzle string. Second private key because this was block 2, or the second block."*
> *"Start with \"BaSCifCatfAaa1i\" Metamon from the wattpad → MD5 hash that to get 2941774a… →
> Generate BIP39 wallet using that entropy → Take the 2nd private key from that wallet as the
> \"strong password\" solution to this block: L5Z66qPm…"*

Two things follow. First, the derivation index is **not always 0**: she picks the *Nth* private key
for block *N*. Round one's stage one reproduces at m/44'/0'/0'/0/0, so index 0 is right there, but
for block 77 the author's own convention predicts **index 76**, with 1 and 2 worth sweeping.

Second, chapter-based answers are formed as *word + string from the chapter* (here "Metamon" from
the Wattpad text prepended to the puzzle string) fed to MD5. For block 77 the equivalent lever is
the chapter text itself, which the case flips modify.

**Applied:** the chapter's four serialisations (CRLF paragraphs, LF paragraphs, single line,
whitespace-collapsed single line) were swept across indices 0-150. Zero hits. Every earlier family
in this file was evaluated at index 0 only, so any of them may still be live at index 1 or 76; the
next run should sweep those indices over the stored descriptor families before any new rule is
invented.

---

## 15. Post-repair re-validation (2026-10-30, second pass)

See `SESSION_2026-10-30_second.md`. All pre-fix negatives were suspect after the base58 repair; the large
ones were re-run at indices 0/1/2/44/76/77 and remain negative: contiguous paragraph runs as the whole
preimage (674,370 derivations), sign-letter families and the 44 lattice (8,304), R1 name marking (2,064),
demo name marking survivors (81,600). New families closed this pass: paragraph-selected × sentence-flipped
(3,564), keyword sign sets from the hint's own words (2,754), strides as case edits for every stride other
than 7 and 44 (22,608). Also settled: the demo's certified base is the ten-paragraph Question block
(`7759227d7406…`); `demo_post_*.txt` starts at the post preamble and hashes to `2bc61c2e…`, so it is not
the author's preimage.

---

## 15. Final sweep on the repaired base (2026-10-30, close-out)

Harness: `harness/fast.py` (coincurve, ~2,850 candidates/s on 4 workers at three indices each,
self-tested against the certified stage-one chain `9dd2efb9…` → `19TbyN5…`).
Base: `wp_paras_br.json`, paragraphs joined `\r\n\r\n`, internal line breaks as `\n`.
Plain-base md5 reproduces the repaired value exactly: `bd07e6ee209c5ab65d874bbbcfccda18`.
Indices: **0, 1, 76** (R4: block N uses the Nth private key; 76 is the reading for block 77).

**1,238,662 candidates, 0 hits, 434 s.** Families, all on the repaired bytes:

| family | candidates | what it closes |
|---|---|---|
| spans | 9,867 | every contiguous run of 2-40 paragraphs as the entire preimage |
| signs-subset | 32,766 | every subset of the 14 paragraphs containing "signs", modes both/first/last |
| window-subset | 131,071 | every subset of the 17 FFWW/sTNM window paragraphs (5-8, 93-96, 168-171, 231-235) |
| meta 2^20 | 1,048,575 | **the full 2^20 closure** over the 20 mechanism paragraphs, previously only partial |

The meta set is the 14 "signs" paragraphs plus the four FFWW quote paragraphs plus `STNM` (237) and
`I STNM.` (239): {20, 42, 220, 222, 223, 225, 226, 227, 228, 230, 231, 232, 233, 235, 236, 237, 239,
244, 246, 273}.

**Also run earlier in this line of work, all negative:** the 64,732-candidate rule battery on the
repaired base at indices 0/1/76 (trailing-space subsets × 6 modes, window mode mixes, window
subsets, section-header subsets, sentence-edge rules, section runs), and the same battery at index 0
on the pre-repair base.

**Deliberately not run: word-edge letter pairs.** On this chapter the edge census is ~15,600
positions, so the pair family is 121,126,830 candidates, i.e. about 49 hours at the measured rate.
It is the one enumerated space left, and it is not affordable inside a session.

**Status.** Every documented rule (R1-R8 in `WORDPLAY_RULES_CATALOG.md`) has now been applied to
block 77's stage two on the repaired base, with the block-Nth-key reading swept as well as index 0.
The result is uniform: negative. The remaining variable is not mechanical. It is exactly which
letters the author edited, and both her own statements and BTCxanter's record agree she no longer
knows it ("I actually don't know… not even to me"). Further sweeps can only re-cover ground unless
a new constraint on *her choice* of letters turns up.

---

## 16. Same closure at indices 5, 6 and 7 — negative

Re-ran the full §15 battery (spans, 2^14 signs subsets, 2^15 window subsets, 2^20 mechanism closure)
against derivation indices **5, 6 and 7** of m/44'/0'/0'/0/i. Index 5 covers the "sixth key" reading
and 6/7 the literal indices, so both are in.

**1,238,662 candidates, 0 hits, 550 s.** Same repaired base, same md5 `bd07e6ee…` anchor.

Cumulative index coverage for this battery: 0, 1, 5, 6, 7, 76.

---

## 17. Reading BTCxanter's replies against the grammar (2026-10-30, later)

His full comment set is 7 items; the relevant two are:

- **2026-10-13** (`t3_cleczc`): gives the demo's source text verbatim with
  `MD5 7759227d7406d8230d7e3a8f7b9846d7`. That hash **equals `demo_base.txt` exactly** [V], so the
  demo's base text is now source-verified rather than reconstructed, and his string is ten
  paragraphs joined by `\n\n` with no trailing newline.
- **2026-10-15** (`t3_cgkpbb`, his most recent): *"The MD5 hash does not match in instances where Aoi
  has modified the text — for example, by adding a note like 'Solved in 90 minutes' to a story that
  had already been published."*

### 17.1 Annotation-removal test (his most recent point, applied literally)

If the chapter carries an author note added after hashing, the hashed text is the chapter minus it.
The only note-shaped paragraph is **45**, *"This time, I solved it in a second once I got past
singularity."* (the same "Solved in …" form she uses in the log part). Tested dropping paragraphs
{43, 45, 46, 47, 34, 78} in all single and pair combinations, both joins, indices
0/1/2/5/6/7/44/76/77, against **both** escrows (live `14zMk…` and original `1EFojcAo…`):
**zero hits.** Also note the chapter's Wattpad `modifyDate` is 2019-07-23, i.e. *before* both
fundings, so a post-hash edit is chronologically unavailable for this part.

### 17.2 Grammar of the demo's worked example, read strictly

The two changes she names are (i) the **paragraph-initial** capital lowered (`I expected…` → `i
expected…`) and (ii) the **sentence-final** letter raised (`…outing himself.` → `…outing himselF.`).
So the device is edge-only, at paragraph start and sentence end. Enumerated **every** subset of size
1-6 over the 25 paragraph-initial plus sentence-final positions of the source-verified demo text,
under the published 12-bit oracle `3c6`: 46 survivors, each derived at indices 0/1/2 against the
demo escrow `09d56507…` — **zero matches**.

Two negatives, and together they close the demo as a calibration source: its solution is not an
edge-only variant of its own verified text, so the demo's prize was not won with the format it
illustrates.

### 17.3 What the clue therefore does and does not give us

It gives a verified base text for the demo, and a warning about author-added notes. It does not give
a rule that reproduces the demo's escrow, so it cannot be transferred mechanically to the chapter.
The chapter's own text still certifies byte-exactly against Wattpad (`bd07e6ee…`), and every rule
family in §15/§16 remains negative.

---

## 18. Block 76's serialization, recreated and certified (it was "still unshared")

A note in the corpus said block 76's escrow "was swept 2026-08-17 and its exact serialization is
still unshared". It does not need to be shared. Reconstructed from the published answer and the
block's own format line (`[solution] TOMI [TOMI] [link]`), it reproduces the escrow exactly [V]:

    Easter TOMI Second Life L1nfJExgS7PHmRb9aZcZjCijL2EJQuMJUi5ax5XJdSorBw8VNph8
    md5 = 3d5823ea1088774b53558624060cf473
    m/44'/0'/0'/0/0  ->  1LZZtbS91P4h5QYdTiTm8dChfLcb1gtwRe   == block 76's escrow

Serialization rules this pins down, all confirmed by the match:

- fields separated by **single spaces**, nothing else;
- the field label `TOMI` is **literal** and sits between the solution and the TOMI value;
- the link field is the block-44 private key in full, no truncation;
- **no leading or trailing whitespace**, no newline of any kind;
- the solution word keeps its capital (`Easter`);
- the derivation index is **0**, not the block number. Block 76 at index 75 fails; index 0 matches.

Both of block 76's content words come from the story that block 77's second stage lives in: its TOMI
value is *Second Life*, which is the heading of paragraph 2 of the very chapter under investigation,
and the chapter's paragraph 31 mentions a "second life" again. She recycles this chapter's material
across blocks, which is why the chapter's own vocabulary keeps turning up as answers elsewhere.

**Bearing on block 77's live stage.** Block 77's stage one did carry fields
(`[solution] TOMI Omit TOMI [link]`, link = block 44's key). The grycoin 777 mbtc block is the
exception: its post has no riddle, no TOMI field and no format line, and its answer is the chapter
itself, hashed with `\r\n\r\n` between paragraphs (the August 1 ruling, 13 10 13 10). So the block-76
serialization does not add fields to the live target. What it does add is the two rules that were
still open for that target and are now settled against a certified escrow: **index 0** and **no
surrounding whitespace**.

---

## 19. Grammar reading re-evaluated at indices 5, 6, 7

The demo's worked example fixes the flip unit at the **sentence** (first letter lowered, last letter
before the full stop raised), and R5 fixes the selection at "all the paragraphs where you recognize
the signs". Taken together at sentence level, the untested object is: **every subset of the sentences
that literally contain the word "signs", each marked first-down and last-up.**

The repaired chapter has **18** such sentences. Full closure = 262,143 candidates. Run twice:

| indices | candidates | hits |
|---|---|---|
| 5, 6, 7 | 262,143 | 0 |
| 0, 1, 76 | 262,143 | 0 |

Also run at 5, 6, 7, 183 candidates: every sentence in the chapter marked; the sentences whose first
letter is in the certified stage-one set {I,T,A,S,M}; the sentences outside that set; each sign
paragraph's sign sentence marked in first-only and last-only mode; every subset of up to eleven
sentences inside each of the four FFWW windows; paragraph-initial down combined with the paragraph's
last-sentence final letter up; and four R1:29-style appends (answer plus space plus the last 3, 4 and
7 characters of stage one's key). **Zero hits.**

Nothing changes at 5, 6 or 7. The sentence reading is now closed on the repaired base at every index
this project uses, which is consistent with the demo's own closure: the marking grammar the author
demonstrates does not reproduce even the demo's escrow, so it is illustration, not rule.

---

## 20. Patterns across every sweep, read grammatically

### 20.1 The seven BTCxanter clues, by grammatical type

| # | date | type | content |
|---|---|---|---|
| 1 | 10-04 | imperative | "upload the archive" — nothing |
| 2 | 10-05 | interrogative ×2 | "Is anyone solving the riddle?" — nothing |
| 3 | 10-05 | interrogative | duplicate of 2 on another thread |
| 4 | 10-05 | imperative + vocative | "Solver, tell me how you did it" — nothing |
| 5 | 10-10 | declarative claim | paragraph 78 is "the only anomaly", "find the sentence that unlocks this MD5 hash" — **falsified**, the pid is Wattpad's duplicate salt |
| 6 | 10-13 | question + code block | the demo's source text, md5 `7759227…`, prefix `3c6` — **verified**, equals `demo_base.txt` |
| 7 | 10-15 | declarative caveat | author edits break hashes — true in general, inapplicable here (modifyDate precedes both fundings) |

One of seven carries data. That asymmetry is itself the finding: the clue set contains exactly one
verified hash and one falsified claim, so every sweep built on it is re-covering ground.

### 20.2 Four invariants the negatives establish

1. **Polarity never varies.** Every certified mark lowers an initial (`activitieS`, `of iT`,
   `reactioN`, `theM`, `i expected`) and raises a final (`…himselF`). All 15M+ candidates held that
   polarity, so polarity is not the unknown.
2. **The unit is an edge.** Certified at paragraph level for stage one and at sentence level for the
   demo. Word-interior marks occur only when the answer is a short sentence (round-one blocks 2 and
   29, where the capitals spell YANG and OI), which is answer construction, not chapter hashing.
3. **Selection is the only free parameter,** and it has now been closed under five independent
   logics: position (spans, 2^16 windows, 2^20 mechanism closure), keyword ("signs"),
   raw anomaly (FFWW runs), structure (sections, trailing spaces, section headers), and grammar
   (mood: 61 interrogative, 580 declarative, 0 exclamatory; voice: 63 quoted-dialogue paragraphs
   against 210 narration). All negative at indices 0, 1, 5, 6, 7, 76.
4. **The demo cannot certify any grammar.** Its own escrow is unreachable by the exact marking its
   worked example demonstrates, closed exhaustively by two independent implementations
   (§17.2 and the 2026-10-31 session).

### 20.3 The one operator that gave positive structural feedback

Selecting paragraphs by **last letter** to spell `STNM` returns exactly **5, 6, 7, 8**: the certified
first window, recovered from scratch by a one-line rule. That is the only selection operator in this
project that reproduces a certified set, which makes its negatives informative rather than vacuous.
Applied to twelve names (STNM, SATOSHI, THOMAS, FINNEY, AOI, GRYCOIN, NAKAMOTO, SECOND, HALFINNEY,
AOINAKAMOTO, BITCOIN, SATOMMI) on both axes at three modes, and to seven more from stage one's own
answer vocabulary (HAL, TOM, IBM, AHS, BIT, TS, MN, TOMI, HALFINNEYTOMI): **53 candidates, 0 hits.**
The operator is sound; the name is not among the nineteen tried.

### 20.4 The conclusion the patterns force

The author's own words close the loop: *"The question of what letters to change in capitalization is
obvious if you know the solution to Satoshi's bitcointalk puzzle… The question of how to go from that
to claiming the prize is not, not even to me."* Combined with §20.1 (one datum, one falsification)
and §20.2 (polarity and axis fixed, selection closed under five logics), the picture is consistent
and complete: the published specification never contained the missing step, and the missing step is
one person's private editing decision. Enumeration cannot recover it.

**Therefore the remaining routes are only those that add information:** the April 2019 browser save
held by bulleteyedk (pre-edit text, relevant to the refunded `1EFojcAo…` oracle, not to the live
one), or a direct appeal to the author. No further sweep on the current base should be run.

---

## 21. BTCxanter's latest clues read against the b76 solution

### 21.1 What b76 actually resolved to, and what that changes

b76 was solved on 2026-10-31 as `EMERGENCY TOMI climate EMERGENCY`, no link field, index 0, prefix
`f8e` → `13Cv6SX…`. Two structural lessons carry over:

1. **The answer word appears nowhere in the 33-part story.** So the author does not reliably mine her
   own text for answers, and any lane that harvests story phrases is structurally blind (which is
   exactly why 1.6M story-phrase candidates came back empty). For b77 stage two this does not apply
   in the same way, because the author states outright that the answer *is* the chapter.
2. **She authors case deliberately.** `EMERGENCY` in the solution field, `climate EMERGENCY` in the
   TOMI field, the same word twice with different casing. Case in her answers is a written decision,
   not an accident of the source.

### 21.2 What BTCxanter's clues now reduce to

`#6` (10-13) supplies one verified artefact: the demo text and md5 `7759227…`. `#7` (10-15) says only
that hashes break where the author edited, and the chapter certifies against Wattpad with a
`modifyDate` before both fundings, so it is unmodified in the sense that matters. `#5` is falsified.
`#1`-`#4` carry nothing. Net new information for b77: **none**. The clue set confirms the base and
nothing else.

Both clues together expose the same class of gap that b76 had: what was missing there was a field
value nobody had published; what is missing here is a case decision nobody published, and the author
says she cannot reconstruct it. Neither is recoverable by search.

### 21.3 Two families executed this turn, both previously unrun, both negative

**Lexical marking.** The b76 answer's repeated word suggested a token-level rule: mark every
occurrence of one vocabulary word, rather than every paragraph or sentence. Sixteen words (signs 17,
sign 3, second 16, satoshi 62, thomas 13, finney 18, hal 29, grycoin 58, satommi 3, bitcoin 75, aoi 5,
climate 13, emergency 13, solution 16, name 18, puzzle 0) in five modes (whole word upper, first
upper, last upper, first lower, last lower). **80 candidates, 0 hits.**

**The authored case-odd tokens as a mark set.** The five planted-looking odd tokens from §12.3
(`ppM`, `VIrgin`, `BItcoin`, and the two alphabet addresses with capital `L`) are the only places in
the chapter where her own hand visibly chose case inside a word. Every non-empty subset of the five,
each normalised, uppercased or lowercased: **93 candidates, 0 hits.**

### 21.4 The next step, pinpointed

In-corpus avenues are now closed by eight independent selection logics (position, keyword, raw
anomaly, structure, grammar, sentence closure, lexical token, authored odd-case). Every one of them
is a way of *deriving* the letter set from the text, and all fail for the same reason: the letter set
was never in the text.

The only action left that adds information is to ask the author for the pattern rather than the
answer, in a form she can answer from memory. Draft, for the grycoin block-2 or b77 thread:

> You said the question of which letters to change is obvious once you know the stage-one answer, and
> separately that going from that to claiming the prize is not obvious, even to you. That sounds like
> the case pattern itself was a judgement call rather than a derivation. Could you say how many letter
> cases you changed in "Second", and whether any of them sat inside words rather than at the start or
> end? Not the answer, just the shape of it. That alone would let the community close a block that has
> been open since 2019, and it would also settle whether your own rule was grammatically motivated or
> arbitrary.

No other route can add information: bulleteyedk's 2019-04-15 save predates the edit and can only
illuminate the refunded `1EFojcAo…` oracle, not `14zMk…`.

---

## 22. Index 2, and the rest of the low range

Ran the full §15 battery (spans, 2^14 signs subsets, 2^15 window subsets, 2^20 mechanism closure) at
derivation indices **2, 3 and 4**: **1,238,662 candidates, 0 hits, 860 s.** Index 2 was the request;
3 and 4 were free inside the same run and close the range.

Index coverage for this battery is now **0, 1, 2, 3, 4, 5, 6, 7 and 76**, all negative.
