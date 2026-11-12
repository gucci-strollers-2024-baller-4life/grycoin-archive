# Fresh angles, 2026-10-29 (zoom-out pass)

## A. The chapter is a structured document, and part of it is a rulebook

Section map (1-indexed, from the short-line scan):

| part | paras | sections |
|---|---|---|
| title + I. Second Life | 1-87 | 1. Second Coming (3), 2. Running (54), 3. Reverse Turing Test (71) |
| II. Second Layer: Grycoin | 88-162 | Abstract (89), 1. Purpose (91), 2. Bitcoin With Two Changes (115), 3. Incentives (130), 4. Why Blockchain? (152), 5. What Grycoin can do for Bitcoin (157), 6. Conclusion (161) |
| III. Second Identity | 163-273 | 1. My Identity (164), 2. The Satoshi Code (175, subsections a-d), 3. Other evidence (247, a-f), 4. What Does it Mean? (265) |

Paras 228-246 are the puzzle rulebook in the author's own prose, including literal markers:

- 229 `All paragraphs except for four, which start with F F and W W.`
- 237 `STNM`
- 239 `I STNM.`
- 244 `"I recognize the signs."`

So a third of the document is a paper ("Second Layer: Grycoin", with an Abstract) and another part is
the code explanation. The hashed object may well be a subset, not all 273 paragraphs.

## B. Round-2 mechanics from the log (new, and they change what to try)

- R2 b1: solution `U2`, "reading M upside down and then W as UU"; TOMI field "upside down".
- R2 b2 (the big one): the documented **password-manager chain**:
  chapter phrase -> MD5 -> BIP39 wallet -> take the **Nth private key (N = block number)** as the
  "strong password" -> MD5 that -> second wallet -> the block's private key.
- R2 b3: Atbash (`XA` = `CZ` in Atbash).
- R2 b4: the answer word is **hidden inside a private key**: `...QnMasKLpz...` contains `MasK`.
- R2 b6: use the first six words of the Coleman wordlist of the previous solution.

## C. What I ran this pass (every candidate address-verified against `14zMk...`)

| family | candidates |
|---|---|
| structural segments: 21 spans (whole, I, II, III, 13 sections, tail, Satoshi Code) x 9 rules (plain, all-flip, first-only, last-only, not-FFWW, not-Finney-4, not-Finney-5, ITASM, strip-trailing-spaces) x 3 joins x 4 indices | 2,376 derivations |
| demo text + chained 3-char code (novel): 2 bases x 4 separators x all base58 3-char codes | 1,560,896 hashes, 380 with the `3c6` prefix, all derived |
| stage-one text re-transformed (de-flip, all-flip, ITASM, not-ITASM, parity, two-sets-of-four) plus 44th-character flips | 176 derivations |
| literal "44 read from left and 44 read from right": first 44 paragraphs, last 44, both, the middle 185, para 93, and the 93-96 window, with 5 flip rules x 3 joins x 6 indices | 540 derivations |
| the documented two-stage password-manager chain: 4 chapter variants x 2 joins x indices 0-77 x 2 target indices | 1,248 derivations |
| "44th character from each end" inside each paragraph (all / FFWW / windows / long paragraphs) | 64 derivations |

**Total: ~4,400 address-verified derivations plus 1.56M hash candidates. No hit.**

## D. The three angles still genuinely untested

1. **Two byte states.** Block 77 is logged as "Failed block, made subtle hashing mistake, but corrected
   that way before anyone came close." The chapter certifies paragraph-for-paragraph, so the difference
   has to be *serialisation*: the Wattpad HTML form (`<p data-p-id="...">text</p>`), the pids included
   in the hash, or the paragraph ids as a key. Nobody has hashed the tagged form.
2. **Words hidden inside private keys** (R2 b4 mechanic). The stage-one WIF
   `KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2` has no dictionary word in it (checked), but
   the same trick applied to *other* keys in the chain (the demo key, the finale's own key once found)
   is how this author signals the TOMI field.
3. **Subset by document logic, not by geometry.** Since Part II is a paper and Part III is the code,
   the plausible hashed object is "the story" (paras 1-87) or "story + identity" (1-87 + 163-273) rather
   than the flat 273. Not tested as a combined selection with flip rules.
