# Phase 1 and Phase 2: the POS/punctuation pools, and the C engine that ran them

**Date:** 2026-10-31
**Files:** `pos_pools.py`, `pos_pools.json`, `sweeper.c`, `base_lf.txt`, `anchor_lf.txt`, `pool_L2s.txt`

## 1. Phase 1: what the six certified marks actually constrain

Six case marks are certified anywhere in this corpus. Their part of speech and their position inside the
word are the only evidence available, so they were tabulated before any filtering was designed:

| source | word | POS | position in word | neighbour |
|---|---|---|---|---|
| block 29 | `vOIce` | common noun | letters 2–3 of 5, **interior** | none |
| demo ¶5 | `himselF` | pronoun | letter 7 of 7, **final** | immediately before the full stop |
| stage one | `activitieS` | common noun | final | immediately before the full stop |
| stage one | `iT` | pronoun | final | immediately before the full stop |
| stage one | `reactioN` | common noun | final | immediately before the full stop |
| stage one | `theM` | pronoun | final | immediately before the full stop |

**What survives:**

- **Never the word's first letter.** 6 of 6 marks are non-initial. This is the strongest invariant.
- **Nouns and pronouns only.** 3 nouns, 3 pronouns, 0 verbs, 0 adjectives, 0 adverbs, 0 articles, 0
  prepositions, 0 conjunctions, 0 proper names. `Satoshi'**S**` and `Bitcointal**K**` are never touched
  in any certified answer, and both occur inside the demo.
- **Punctuation does not repel.** 5 of 6 marks sit immediately before a terminal full stop. So the
  punctuation-barrier hypothesis is falsified in the direction the marks actually run.

**What does not survive the evidence:**

- *"Word-internal only."* `himselF` is the word's last letter and the sentence's last letter. `vOIce` is
  interior. The two certified marks disagree on position within the word, so position within the word
  cannot be the rule. Only *non-initial* is common to all six.
- *"Content words only."* Both pronouns that were marked, `himself` and `them`/`it`, are closed-class in
  most grammatical traditions. So "barred from closed-class words" cannot be stated as a rule; what the
  evidence supports is narrower, "nouns and pronouns yes, the rest unobserved".

## 2. The pools, measured on the demo

The demo has 1,549 bytes, 282 words, 1,197 letters, 15 sentences, 140 distinct word forms (classified by
hand in `pos_pools.py`; the classification is mine, not a tagger's, because this image has no POS model).

| level | rule | pool size | 5-change space from the anchor |
|---|---|---|---|
| L0 | every letter | 1,197 | C(1,195,3) = **283,701,365** |
| L1 | up-marks non-initial only | 936 | C(934,3) = **135,360,884** |
| L2 | up-marks non-initial in nouns/pronouns, down-marks any word-initial capital | 360 | C(358,3) = **7,583,156** |
| L2s | as L2, but down-marks restricted to the 15 sentence initials | 350 | C(350,3) = **7,084,700** |
| L3 | up-marks word-final nouns only, plus initials | 65 | C(65,3) = **43,680** |

The POS constraint alone is a **40× reduction** of the 283M space. That is where the win is.

## 3. Phase 2: the engine, and two corrections to the plan

`sweeper.c` implements the four-stage cascade requested: mutate only the K target bytes, hash, test the
prefix, and reserve address derivation for prefix survivors only (derivation stays in Python).

Three things about this box changed the design:

1. **`nproc` is 1.** OpenMP cannot help here; a `#pragma omp parallel for` over the outer index would
   spawn one thread and add overhead. The program is written single-threaded with the loop nest factored
   so the guard can be dropped in on a wider machine without restructuring.
2. **There is no `libcrypto` on this image** (`-lcrypto` fails to link, `/usr/include/openssl/md5.h`
   absent). MD5 is implemented inline, RFC 1321, no dependency.
3. **The speedup is 1.6×, not 600×.** Measured: Python bytearray+hashlib gives 0.297 M candidates/s, the
   C engine gives **0.49 M/s** on this core. Because every candidate must hash the 1,549-byte text, the
   per-candidate cost is dominated by MD5 throughput, and the cascade of cached MD5 prefix states recovers
   only the blocks before the first edit. 600× would require ~30 cores and was never on the table here.

The engine is verified, not assumed: with a 65-position pool it was asked to find a specific known triple
(83, 96, 133) at a 4-hex prefix and returned exactly that triple and no other
(`35d330f8d4f89c07b1cf831090bc6a4c 83 96 133`), which cross-checks the inline MD5 and the edit cascade
against Python's hashlib.

## 4. Phase 3, the run: the POS-filtered five-change space, exhausted

Anchor: the two edits the author names in ¶7, applied first (`I`→`i` at 535, `himself`→`himselF` at 652).
Free: three further edits from the L2s pool.

| run | candidates | throughput | `3c6` survivors | derived 0–4 | escrow |
|---|---|---|---|---|---|
| L3 (word-final nouns + initials) | 45,760 | 0.51 M/s, 0.09 s | 16 | 16 | **0** |
| **L2s (nouns/pronouns + sentence initials)** | **7,084,700** | 0.49 M/s, 14.5 s | 1,762 | 1,762 | **0** |

So: **the demo's answer is not five case changes from this base, with the author's two named edits fixed,
for any choice of the remaining three among every position that six certified marks permit.** 7,084,700
texts, exhaustively, in fifteen seconds.

## 5. What the filter did not buy, and the honest next numbers

The POS constraint is the only thing standing between this closure and a full five-change closure. Drop it
and the space is L1, 135,360,884 candidates, 4.6 minutes at the measured rate. Drop everything and it is
L0, 283,701,365, 9.7 minutes. Both are now cheap enough to be routine rather than "an explosion", which is
the real result of this session: the 283M figure that looked like a wall is under ten minutes of a single
core.

If L1 also returns nothing, the conclusion is no longer about search: the demo answer would have to place
an up-mark on a verb, adjective, adverb or function word, which nothing certified ever does, or it would
have to be more than five changes, or the escrow is not derived from this text by this chain.
