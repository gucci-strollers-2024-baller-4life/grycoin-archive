# Investigation log

Chronological. Each entry is a session; findings are stated as they were established,
including the ones later retracted.

## 2026-11-12 — Phase 2, reading and closure

**Corpus.** All 33 Wattpad publications synced to `corpus/`. 31 read in full
paragraph by paragraph. *Complete Quizchain* read to ¶330 plus both block-77
entries; the remainder is block Q&A enumeration.

**Major structural find.** Part 761570746 ¶19-21 explains his own "Aa" pointer:
the same letter in opposite cases at the two ends. The chapter has it — ¶1 "Second"
to ¶273 "…signs." = S/s. Folding first letters against mirror terminals yields
**exactly eight** case pairs: ¶1/273, 8/266, 9/265, 46/228, 51/223, 71/203, 92/182,
97/177. Eight is stage one's flip count.

**And it is negative.** Nine mechanics across those 16 paragraphs, both joins:
300 derivations, zero. Then the full 2^16 power set of those 16 paragraphs:
131,072 derivations at index 0, zero.

**Round-one block 77's format recovered** from Complete Quizchain ¶385:
*"eight items in two sets of four. Two items ciphertext and two items plaintext each,
44 read from left and 44 read from right."* That matches the foldover arithmetic
exactly, and ¶381 documents that round-one 77 was itself a failed block with a
"subtle hashing mistake".

**Reprint diff.** Chapter ¶231-235 vs Hal ¶2-6: three insertions only, +3 chars —
an opening quote at offset 38358, an `s` at 39562 repairing "facinating", a closing
quote at 39968. A paste preserves spelling, so he retyped it, breaking his own
"copy paste and change only the capitalization" rule in the one place he
demonstrates the method.

**Closed this session:** GRY (absent from the preimage; authorial pun only),
44-from-each-end (union of end blocks, and the complement reading of ¶229),
the index axis 0-999 on six selections, character-level foldover, and the
foldover power set.

~144,000 derivations today. All empty.

## Earlier — Phase 1

- 400M+ candidates across 34 families, two independent efforts.
- 296,480 derivations closing every 1-flip and 2-flip among the 544 paragraph edges.
- The demo oracle (3c6) proven permanently dead: the demo was edited after
  publication, so the text that hashed to it no longer exists.
- The author's 418 Reddit comments recovered; the demo was likely won by a
  collision hunt on a 12-bit target, not by the intended rule.
- Fairness doctrine found (part 740685487 ¶24): *"all of the resistance to solving
  will come from not knowing the method and none will come from not knowing some
  fact or other."* So the answer is derivable in principle, from public material.
