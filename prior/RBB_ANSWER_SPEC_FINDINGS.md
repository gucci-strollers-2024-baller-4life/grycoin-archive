# RBB answer spec — findings 2026-10-29

> **Superseded 2026-10-29 (late).** The "rebuild b1→b76 and re-test with b76's key" next job below is
> cancelled: 76 of the 77 round-two WIFs are published and decode to their escrows, b76's key is
> unobtainable, and block 77 stage one is bare text, so the RBB cannot carry a link. See
> `CLUES_CANONICAL.md` §11 and §13. The stage-two sign set is also probably SATOSHI's letters rather
> than I,T,A,S,M — see §13.2.


## Source: Wattpad part 761570746 "The Satoshi Code" (published 2019-07-22, same day as the RBB)
This part IS the answer spec for block 77:
- Hint 4: "Two halves of the address. The first set of two ciphertext items is in the first half and the second in the second."
- Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa (genesis coinbase)
- Ciphertext pair 1 (first half) = "1A1" (read as HAL; doc says "certainly not HAL", TOM joke) + "efi2DM" (Finney via Atbash: 2=Y, M=N, reorder)
- Ciphertext pair 2 (second half) = "Nm ST" (right-to-left read with 7 and 5 as pointers; "Nm ST" = Nakamoto Satoshi)
- Plaintext pairs anchored by author-published md5 prefixes:
  * "Hal Finney" -> cc9485a (verified locally)
  * "ihsotaS otomakaN" -> d78c92f (verified locally)
- 8 items joined by single spaces = exactly 44 characters => "44 read from left and 44 read from right" = the string length.

## Tested negative (all vs 14zMk live and 1EFoj old escrow, m/44'/0'/0'/0/0)
- all 40,320 orderings x 2 item-sets x 4 link variants = 322,560 derivations
- 12,288 CRLFCRLF paragraph groupings of the 8 items
- every case variant of the Nm/ST pair (Nm ST, TS mN, ST Nm, mN TS, NM, nm...)
- TOMI placements (none / " TOMI omit TOMI" / " TOMI Omit TOMI")
- links: b76 (WIF last7 and hex last7), b75, b74, b73, b72, b71, b62, b46, grycoin-1, stage-one WIF/hex, genesis fragments
- 20 BIP39 passphrases; 25+ paths/indices (m/44'/0'/0'/0/0-9, m/0'/0'/0-9, m/0/0-9, account variants)
- SHA-256 -> 32-byte entropy (24 words) as well as MD5 -> 16-byte

## Solid side-facts
- Round-1 block 76 answer confirmed in log line 699: "Easter TOMI Second Life" (key last7 dBEhAz3, hex last7 4c19f4f)
- A block's exact_input hashes WITHOUT its link field => link is not part of the hash
- Chapter has a FOURTH sign replica at paras 231-235 (F,F,W,W endings s,t,n,m, I-paragraph at 234), besides 5-8, 93-96, 168-171
- Author lost the RBB solution: part 762380140 "Starting Up": "I have lost any information on the solution of that one. Tragic boating accident variation."
- Chapter single-CRLF join x 16 sign paras x all 65,536 subsets x 3 modes = 196,608 derivations: negative

## Untested axes remaining
1. The "two sets of four" = two of the chapter's sign replicas (s,t,n,m twice), with 2 flipped + 2 unflipped per set
2. A remaining derivation twist (author said he removed only ONE of the twists for the live escrow)
3. Exact plaintext/ciphertext item spellings other than the anchored pairs

## Session 2026-10-29 (late): arrangement hunt
Full 33-part Wattpad story fetched locally (wparts/). Key parts read:
- 757574334 "THOMAS and SATOSHI": Satoshi≈THOMAS anagram; extra S "may just mean Second. Like in Harold Thomas Finney II" (the chapter title!).
- 762380140 "Starting Up": confirms author LOST the RBB solution ("tragic boating accident variation") — reconstruction only.
- 720895609 "4444 and 4442": author's shorthand habit "4 can be read as 4 for".

NEW ARRANGEMENT (structurally exact fit to spec): "44 read from left and 44 read from right" =
the two FFWW sign replicas lying within 44 paragraphs of each end:
  LEFT set  = paras 5-8   (lasts s,t,n,m, firsts F,F,W,W)
  RIGHT set = paras 231,232,233,235 (Hal quote block; 234 = I-paragraph; lasts s,t,n,m, firsts F,F,W,W)
=> eight items in two sets of four; 2 ciphertext (F,F / W,W) + 2 plaintext (s,t / n,m) per set.
(Other replicas at 93-96 and 168-171 are NOT within 44 of either end.)

TESTED NEGATIVE this session (all vs 14zMk live + 1EFoj old):
- token strings from those replicas: lasts, uppercase lasts, last words, first words, pairs,
  joins (space/none/CRLFCRLF), links (''/dBEhAz3/4c19f4f/62tGor2/7DivfNa), md5+sha256 (171)
- firsts+lasts arrangement FFWW+stnm in all case/pair/order/join/quote variants, 3 paths (5,049)
- inverted flip modes (first UP + last DOWN, and singles) on the 8 sign paras, 4 joins, 2^8 subsets (3,072)
- word-level rule from the demo (all standalone I->i and himself->himselF) on chapter, 4 joins (24)
- "capitals travel" name-word flips (Satoshi/Nakamoto/Thomas/Finney/Hal/Bitcoin/Aoi/Second) 2^8 combos x 4 joins (1,024)
- full 8-item permutation sweep from earlier: 322,560 candidates; chapter single-CRLF 16-set sweep: 196,608

NEXT IDEAS (not yet tested):
1. Answer items drawn from part TITLES (33-part story, read 4 from each end of the list).
2. Two replicas' PARAGRAPH TEXTS hashed as 8 paragraphs (i.e., the chapter truncated to those 8 paras) in various joins.
3. The "I STNM"/"Nm ST" chapter-internal strings combined with the 8 replica tokens.
4. Ciphertext items = the story part titles "Second Life" / "Second Coming" (decode via that part's content).
