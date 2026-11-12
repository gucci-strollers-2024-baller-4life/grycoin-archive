# RBB (Real Big Block) — Research Dossier
Updated: 2026-10-28. Target: 0.777 BTC at 14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W (unspent since 2019-07-30).

## Certified facts (do not re-derive)

### Pipeline (verified end-to-end)
solution text -> MD5 (16 bytes) -> BIP39 entropy (4-bit checksum) -> 12 words -> PBKDF2-SHA512(words, passphrase="", 2048) -> BIP32 m/44'/0'/0'/0/i (P2PKH). Author funds at index 0 ("the first one", note 4 chn8un; stage one idx 0 certified). Author also browses an m/0'/0'/i list (its 7th WIF contains "777" - verified).

### Stage One (ca6jxv, 77 mbtc, SOLVED by puzzleponky 2019-08-03)
- Base: Hal Finney's "Bitcoin and me" (bitcointalk topic 155054, raw HTML, ISO-8859-1), 16 paras; para 16 = "...legacy.\n[edited slightly]" (single br gotcha; <br><br> = para break, single <br> = NOT).
- Flips: paras 2,3,4,6 (firsts F,F,W,W down; para-lasts s,t,n,m up -> STNM).
- MD5 9dd2efb9bc976c2095bd534d7b8d431c -> 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN at m/44'/0'/0'/0/0. WIF KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2.
- Sign grammar: paragraphs NOT starting with a letter of ITASM {I,T,A,S,M} are flipped (all non-flipped paras in Hal start ITASM; M-para 11 stays).

### Demo / Grycoin Block 2 (cleczc, 7 mbtc, SOLVED by puzzleponky 2019-08-03, ~15.5h)
- Base (question): demo_base.txt, 10 paras LF(\n\n)-joined, MD5 7759227 (author-confirmed; his "13 10 13 10" CRLF claim is his clipboard artifact - CRLF gives 5e35365, wrong).
- Oracle: solution MD5 starts 3c6. Escrow 1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi (funded f11eca99, 700k sats; swept 35137158 to puzzleponky wallet 129jw1GUGwiJbf4rL7qEANPbxvSRC5zfHN).
- ELIMINATED spaces: all 2^33 subsets of 33 boundary positions (2.09M raw hits, 130,784 unique, idx 0-2 + lowpop idx 0-20); all 1024 para-subsets x {para,s1} x {both,last,first} x 4 joins; word-boundary k<=3 (548 positions, idx 0-20); up-to-4-anywhere + 5-boundary (GPU hunter Sea_Ferret, >100B candidates); stated pair {I@535->i, himself-f@652->F} + up to 3 arbitrary positions (69,393 3c6 hits, idx 0-6); word-spelling flips (HAL/AOI/STNM/TOMI/SATOSHI/NAKAMOTO subsequences); de-flips; signs-word flips {531,607,778,1106}; non-Satoshi (95) / non-ITASM (118) / intersection (70) sets on chapter; TOMI/link concatenation formats (no TOMI field - author-confirmed).
- Stated flips in the text are CONDITIONAL EXAMPLES on para 5; para 2's ending "n" explicitly NOT part. Remaining hypothesis: >=5 flips at word-internal positions.

### RBB Stage Two (cgkpbb, 777 mbtc, UNSOLVED)
- Question: "Final version of the second chapter of Wattpad story" = Wattpad part 720888559 ("Second", story 184148284). Tag: hintforblock77.
- Base: wp_paras.json (273 paras). CERTIFIED byte-exact via Wattpad data-p-id = md5(paragraph text): 272/273 match (13 paras carry trailing spaces - keep them; "exact" base). Para 78 pid 8b71bade... = Wattpad dedup hash md5(md5("What?")hex+"1") -> no edit; all 273 paras certify (see CORRECTION_para78.md).
- Join: author's 2019-07-30 update = "two line breaks between paragraphs now"; by the demo LF precedent this = \n\n (his CRLF display belief was wrong before; test both \n\n and \r\n\r\n).
- Old escrow 1EFojcAo (funded 2019-07-22 from author wallet 1FtU2GwV, swept 2019-07-30 by author to hot wallet 36nwcMJwoy99xyENeRcCCQmA3FZibji3Un, then 14zMkTga funded from 3E7gTGXp4EcKhcLo69Utw3vae4Axj5ZPh7).
- Author's funding txs and hot wallets do NOT derive from known entropies (checked vs stage-one wallet lists).
- The author LOST his own solutions ("not even to me"); puzzleponky (only solver) never revealed; no reply to requests.
- Timeline: expiry July 7, 2022 (Tanabata) passed silently; author inactive since Aug 2019.

## Eliminated chapter rules (all x {exact,stripped} x {para,s1} x modes x 4 joins x idx 0-99 x both escrows)
ITASM-excluded (118), non-Satoshi (95), STNM-ending (146), intersection non-ITASM & stnm-ending (70), all cluster sets (C1/C1I/C2/C2I/C3/C3I/quote/quoteI/all3/all3I/+/quote combos), four-around-222 (218-221, 223-226), pure text, de-flips, TOMI-link formats.

## Open leads
1. Demo: anchored stated-pair + k=4 anywhere (C(1197,4) ~ 1.2e11, ~34h C) - launch when idle.
2. Demo: wide idx 3-99 on all boundary hits (running).
3. If demo flips found: same rule -> chapter (sign paras), then port + hash + derive vs 14zMkTga at idx 0.
4. Author's first-run Block 2 lineage: flipped letters spell a NAME scattered in one sentence (A,G,Y,N); Block 29: word-internal flips ("voice"->"vOIce") + previous-key-tail link. The 77 "slightly developed" format = both directions at boundaries, per stage one.
5. puzzleponky's Medium/other channels for a demo-solution disclosure (Reddit history exhausted; no post-2019 reveal).

## Author record set (agntn/)
45.real-big-block.md, 77.md/ts, quizchain2_77.ts, r1b2.ts, r1b29.ts, grycoin2.ts/story, cgkpbb, chf8k2, chn8un, civj2n, cleczc, ca6jxv (2026 comments incl. Sea_Ferret_9615 = prior hunt sessions' own messages).

## UPDATE 2026-10-29 (logic-only session, no GPU/no network)
- NEW ELIMINATIONS on demo (oracle 3c6 + escrow 1tzieU, idx 0-2):
  (a) sentence-edge flips: all 2^15 sentence subsets x 4 direction modes x 4 joins (LF/CRLF/CR/LFCR) = 524,288 cands, 31 oracle hits, 0 escrow.
  (b) stage-one lower set {P3f,P4f,P7f,P8f = F,F,W,W} x every in-text embedding of STNM (694,082) x 3 lower variants = 2.08M cands, 484 oracle hits, 0 escrow.
  (c) name-in-span spellings (STNM/AOI/NAKAMOTO/SATOSHI/AOINAKAMOTO/GYN/AGYN) x {raise only, raise+stage-one lowers} = 11,804 cands, 4 oracle hits, 0 escrow.
  => demo answer has >=5 flips at arbitrary incl. word-internal positions, mixed directions.
- STRUCTURAL FINDING (from agntn/r1b2.ts + r1b29.ts): the first-run format is NAME-SPELLING BY CASE, positions arbitrary:
  block 2 "message->messaGe, you->You, on->oN" (G,Y,N at internal/initial/final), block 29 "voice->vOIce" (O,I interior only, "same method as in Block 2").
  Therefore "which N positions flip" is an ill-posed framing; the unknown is the TARGET NAME. Measured subsequence sizes in demo_base: STNM 694,082; AOI 158,366; AOIN 2.9M; NAKA 89,228; SATOSHI 5.6e9.
- STNM-in-demo is impossible at edges: no paragraph or sentence in the demo ends in M (lasts t,n,N,s,l,i,F,d,e,d / sentence lasts t,n,N,s,f,l,i,F,d,e,k,w,e,d,d), so the stage-one signature rule cannot port to the demo. Confirms stage one's rule is a signature detector, not a flip grammar.
- Next: span-constrained name search (word/sentence) for long names; chapter: locate name letters near hint para 222 instead of sweeping.

## UPDATE 2026-10-29 (third session): block-29 mechanic decoded, chapter families closed

### Certified sign mechanic, now readable in context
Block 29 (q1 b29, MD5 982301b8...) hashed the draft of the scene that appears in the final chapter at
para 11: chapter 'A pleasant female voice.' -> b29 'A pleasant female vOIce.'
The chapter itself supplies the key to those letters: para 18 '"Good question. How about Aoi? ..."',
para 20 '"Pleased to meet you, Aoi ..."', para 21 '"Artificial Omnipotent Intelligence, obviously."'
So the author's sign is the name AOI marked by case, and block 29's flip touches only the two letters
that were not already capital (O and I inside 'voice'; the A was the sentence-initial article).
Rule shape: find A, O, I in order with minimal span inside one sentence, uppercase the ones that are lower-case.

### Chapter (stage two) families closed this session
Base verified: wp_paras.json == chapter_paras_exact.json (273 paras, 13 keep trailing spaces), joins LF2 and CRLF2.
Every candidate hashed, then derived at m/44'/0'/0'/0/{0,1,2} and compared with BOTH escrows
(14zMkTga live, 1EFojcAo original). All negative:
- every in-sentence AOI marking (the certified block-29 shape): 53,787 candidates (resumable script aoi_chapter.py)
- tightest-AOI-per-sentence only: 868
- the four quoted Hal paragraphs inside the chapter ({230,231,232,234} and +{233}), both directions and toggle,
  with/without title and section headers: 48
- deterministic minimal-span marking of AOI / NAKAMOTO / STNM / SATOSHI / AOINAKAMOTO / AOMI at sentence and
  paragraph granularity with span caps 5/7/10/14: 152
- word-occurrence case rules on Aoi, voice, signs, sign, recognize, Satoshi, identity, Artificial, Omnipotent,
  Intelligence (first/last/all/toggle), singles, pairs and triples: 30,450
- consecutive-paragraph signature windows (paragraph lasts or firsts containing STNM or AOI as a subsequence,
  windows of 3-10 paragraphs, both directions): 864

### Other parts parsed
- part_724030807 (block 60 notes): the author's own joke about 'letters A and I are in both names' - confirms the
  name-marking habit is a running theme, gives no new flip rule.
- part_762380140 (shutdown note): 'I have lost any information on the solution of that one' - the RBB solution is
  gone with the author, so no disclosure route remains.
- part_761570746 (genesis-address essay, 146 paras) and part_757574334 (Thomas anagram essay) explain the genesis
  signature and the anagram theory; they are the source of the FF/WW dedication reading, not of a flip grammar.

Conclusion after ~86k additional chapter derivations: the answer is not a name marking, not an edge signature at
paragraph or sentence granularity, and not any single-word or single-occurrence case rule. The remaining live
hypothesis is a unit the story supplies that has not been tested as a unit yet, or a multi-site rule.
