# Handoff for the other agents

## 1. Restored calibration set (was lost this week)
`calib_restored.json` — 149 of the 153 published block inputs, as `{id, algo, input}` with `id` = `R1:n` or `R2:n`.
Rebuilt from `answers_raw.json` after `quizchain/calib/*.py` disappeared from this workspace.
Still missing: **R1:53, R1:63, R1:70, R2:49, R2:50** — re-supply from whichever lane holds the repo.
Self-test that must pass before any run: `R2:77` -> md5 `9dd2efb9...` -> `m/44'/0'/0'/0/0` -> `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`.

## 2. Oracle
`demo_oracle.py` had a dead wordlist path; it now reads `harness/bip39_english.txt` (2048 words). Verify with
`python3 -c "import demo_oracle as D; print(len(D.WL))"` -> 2048. Never trust a negative from a run that
did not print that number first.

## 3. Certified base
- `wp_paras.json`, 273 paragraphs, part 720888559 "Second", 45,450 chars in the LF build.
- 273/273 pids verify: 272 direct md5, and para 78 by Wattpad's dedup rule `md5(md5_hex+"1")` = `8b71bade...`.
- Whole-chapter digests: `\r\n\r\n` join -> `f74e8e01...`; `\n\n` -> `48d31820...`.
- Join for the live escrow is `\r\n\r\n` (author: "Hit enter twice ... 13 10 13 10", Aug 1 2019).
  Single `\r\n` belongs to the refunded `1EFojcAo...` era only.
- The chapter is a compilation: 24 paragraphs have verbatim 70+ char sources (17 from "THOMAS and SATOSHI",
  3 from "Second Life", 3 from the block-77 Stage One post, 1 from the block 57 post). The THOMAS reprint is
  byte-identical; the Second Life reprint carries five rewrites, all numeric/semantic. See `PALIMPSEST_FULL.md`.

## 4. Oracles to test against
`14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` live 0.777 | `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC` refunded
`1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` demo | `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` stage one
Demo question md5 must start `7759227` — use it to validate any new base text before sweeping.

## 5. Prize protocol
No published WIF, no test transfer, no third-party relay. On a hit: build the sweep transaction offline,
fee >= 100 sat/vB, broadcast once, and only then announce.

## 6. Closed (do not redo)
Eight-token address decode 559,872 | triangles 6.6M | single-letter flips 107,475 | quad subsets and anomaly
masks ~500K | deletion k=1 and contiguous runs 510,000 | numeric rewrite 64 | sign-location demo rule 1,062 |
alternate derivation paths 36 | demo under SHA-256 80 | serialisation 19 byte forms | appended fields 1,176 |
pid chain 32 | sentence-edge flips | paragraph-as-preimage 1,638 | surface strings 1,726.
Class-3 slips (one paragraph's direction inverted; one stray capital inside the set) 24,062 |
same inversion over twelve sets x four bases incl. claimer's-paste 5,628 — both negative 2026-10-31.

## 2. Calibration completed and verified
calib_restored.json now has 153 entries. ANSWERS.md supplied R1:53, R1:63, R1:70, R2:49.
Chain proof, compressed WIF at m/44'/0'/0'/0/0, suffix must appear in the next block's link field:
R1:53 -> NRqEsd7 (found in R1:54); R1:63 -> full WIF inside R1:64; R1:70 -> Uj8MCe6c (found in R1:71).
Only R2:50 is absent from every local source. Conflicts to resolve: R1:9, R1:10, R1:29, R2:77 differ between
the two tables; answers_raw wins there because it reproduces 9dd2efb9 -> 19TbyN5 for R2:77.
Correction: my earlier note calling R1:53 unrecoverable was wrong; its input exists and validates.

## 3. Calibration set complete: 154 of 154
R2:50 recovered from the solver's own explanation (BrainForceOne, r/Grycoin c5kst3) and verified against all
three published constraints: md5("4oLvT2 TOMI address checksum") = c3260755, md5("4oLvT2") = 8c258415,
md5("address checksum") = 64ef0768. Input is `4oLvT2 TOMI address checksum`, MD5, no link field.
Set now holds R1:1-77 and R2:1-77.

## 4. The four table conflicts, resolved by chain proof
answers_raw wins on R1:10 and R1:29 directly (its WIF suffix appears in the next block's link field; the
ANSWERS.md variant does not). R1:9 also resolves to answers_raw once you notice R1:10's input ends with a
literal backslash-n, the surviving trace of the block 9/10 extra-line-break mistake. R2:77 has no successor
to check, but answers_raw is the variant certified by 9dd2efb9 -> 19TbyN5.
Do not strip or normalise the literal `\n` in R1:10; it is part of the published string.

## 5. Key metadata for the top of both chains
second_key_metadata.json holds, for R1:1-3 and R2:1-3: entropy hex, 24/12-word mnemonic, priv hex, compressed
WIF, address at m/44'/0'/0'/0/0, and the chain link that consumes it.
Verified links at the top: R1:1 -> R1:2 (`Uzp`), R1:2 -> R1:3 (`hBF`), R1:3 -> R1:4 (`83S`). All MATCH.
Round 2 does not chain by 3-char suffix: its link field is a full or truncated WIF, and **R2:1 and R2:3 carry
the same link prefix `L2e6gPSXnq7KJBfkoD7cHG`**, so one upstream key gates two separate blocks.
Round 2's "second key" (index 1 of a wallet) is used as a solution string, per the author's own recipe; the
reproduction needs the verbatim phrase from Complete Second Round para 268, since the paraphrase `BaSCifCatfAaa1i"Metamon`
hashes to b3e2b605, not the published 2941774a.

## 6. The second-key chain, reproduced end to end (verified)
Verbatim phrase from Complete Second Round para 268, quotes included, is `"BaSCifCatfAaa1i"Metamon`.
md5 -> 2941774a2abec9f30c7d6777d1d53d91
mnemonic -> citizen arm spoon fever uncle wet cradle provide jelly modify exhaust casual
index 1 WIF -> L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex  (the published solution string)
md5(WIF) -> 7b44cc11c866ab85b7078c43ad6795e1
second wallet index 0 WIF -> KzFB7hBGmLBqm8nqVCVLBmgyd1NxnoJXZUhE377QL4T2iy5rw4Wz  (published block key)
address at index 0 -> 13qUHVzMYAneyyBGYvEey4SHy2iMSz3Jzh
All four published values match. The straight double quotes are part of the hashed string; omitting them gives
b3e2b605 and breaks the chain. "2nd private key" = derivation index 1, and the solution field may be a WIF
that is hashed again rather than text. Apply that shape to the RBB: chapter -> md5 -> wallet -> index 1 WIF ->
md5(WIF) -> wallet index 0.

## 7. Two-hop shape applied (2026-10-31)
Verified shape from the author's own recipe: text -> md5 -> wallet -> index-1 WIF -> md5(WIF) -> wallet -> index 0.
Ran it on the chapter: 5 flip states x 2 joins x 4 tails x hops {0,1} x second-wallet indices {0,1} = 128 checks,
no hit. Ran it on the demo at four flip states, four joins, hops {0,1,2,6,7}, both WIF cases = 640 checks, no hit.
So the two-hop shape alone does not explain the demo's resistance to 100-billion single-hop sweeps.

## 8. Lane queue, ranked by expected value
1. Two-hop against the sign-selected flip sets only (small ordered spaces), not arbitrary states. Use fastderive.
2. R2:2 proves the solution field can be a WIF; test the chapter as a WIF-producing preimage (index 1) with the
   link tails certified from round 1.
3. Rewrite any lane script still importing demo_oracle to fastderive.addresses for a 5.6x multi-index win.
4. Only after 1-3: the 31.8M non-adjacent deletion space, which no lane has started.
