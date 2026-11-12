# ¶78 does not duplicate ¶34's id, and the k=1 solo sweep is negative

**Date:** 2026-10-31

## 1. ¶34 and ¶78 have the same text but different ids

    ¶34  pid 184826be0ea6837abb5851807f7a9e2b   text '"What?"'   md5(text) 184826be…
    ¶78  pid 8b71bade9685d3388452bc4755b06a0d   text '"What?"'   md5(text) 184826be…

The two paragraphs are byte-identical — both are `"What?"` — but their ids are different. ¶34's id is the
md5 of its own text, so it reconciles; ¶78's id is not, so it does not. The "duplicate pid" premise is
therefore wrong: `8b71bade` is not ¶34's id, it is the md5 of text that no longer sits at ¶78.

Substituting ¶34's text into ¶78 is consequently a no-op. The strings already match.

## 2. What that establishes

Wattpad does not recompute `data-p-id` when a paragraph is edited. Since 272 of 273 paragraphs reconcile
against their ids, **exactly one paragraph in the chapter has ever been edited since creation: ¶78.** The
twist the author removed on 2019-07-23 is therefore confined to one paragraph's worth of text, and the
pre-edit content is whatever hashes to `8b71bade`. It is not `"What?"`, and it is not a 1-to-14-word
phrase drawn from the chapter's own vocabulary (407,432 candidates tested, no match).

## 3. `himself` as a terminal word

Exactly one paragraph ends on "himself": **¶254**, the heading `c) Mail Conversation With Himself`. No
prose paragraph terminates on it. ¶248 mentions "outed himself" but mid-sentence, and Hal's ¶16 ends on
"legacy", not "himself".

## 4. The k=1 solo sweep, run

Each paragraph in turn, head character lowercased and last alphabetic uppercased, the other 272 left
untouched, joined by `\n\n`, derived at index 0. ¶15 (`"2020."`) has no letters and is skipped:
**272 candidates, zero hits.**

Script: `sweeps/solo_k1.py`.
