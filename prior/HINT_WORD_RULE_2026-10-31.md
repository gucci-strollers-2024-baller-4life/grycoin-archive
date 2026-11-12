# The chapter performs the ¶7 rule itself, and the rule tested negative on 293 candidates

**Date:** 2026-10-31
**Script:** `sweeps/firstlast4.py`

## 1. Three figures confirmed independently

- **Index 0 only.** Re-deriving `md5(safudev_stage1.txt) = 9dd2efb9…` at every index 0–80, the
  address `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` appears at index 0 and at no other index.
- **ca6jxv carries no Finney text.** Its transcript body is 4,146 characters by my parse of
  `agntn/ca6jxv.md` (the 4,149 figure differs by three characters of quote-block spacing), contains
  `Question:` and does not contain `I thought I'd write`. The 5,362-character preimage is the
  bitcointalk document.
- **91 posts** in `grycoin_posts.json`, both block-77 posts among the twelve titled `[77 mbtc]…`.
  A looser pattern than "first three digits … are X" matches 65 posts, so 44 is the strict count of
  posts that publish a prefix in the canonical form; the two block-77 posts publish none either way.

## 2. The chapter states the rule, then demonstrates it on Hal ¶7

¶242, verbatim: **"The first four and last four words of the paragraph hinting at the solution."**
Then ¶243 and ¶244 give them, as two consecutive four-word paragraphs:

    ¶243: "Today, Satoshi's real identity"
    ¶244: "I recognize the signs."

against Hal ¶7's actual edges:

    first four: Today, Satoshi's true identity
    last four : I recognize the signs.

The only change is `true` → `real`. ¶245 and ¶246 then split them: "Today, I" and "Satoshi's real
identity, recognize the signs".

So the mechanism is not inferred from the hint; it is written out inside the payload, at ¶242–246.

## 3. ¶20 is the same four words, planted bare, 223 paragraphs earlier

    ¶20: I recognize the signs.

It sits in Act I, subsection `1. Second Coming`, surrounded by dialogue, out of narrative place, and
it is a verbatim copy of Hal ¶7's last four words. It is also exactly four words, so it is its own
first-four and last-four — the one paragraph in the chapter where the two halves of the rule collapse
onto each other. Every other "recognize the signs" site is longer: ¶220 and ¶273.

## 4. Applying the rule to the chapter: negative

69 candidate paragraphs — every paragraph of five words or fewer, the sixteen window paragraphs, and
the cross-paragraph pairs (¶4's first four with ¶273's last four, ¶20 with ¶273) — each rendered as
first-four + last-four in both orders, as a doubled half, unquoted and lowercased: **293 distinct
strings, derived at index 0, zero hits** against `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`.

## 5. What that leaves

The rule is settled; the *target paragraph* is not. The chapter's own identification rule is ¶236–240:
read the last letters of the four anomalous paragraphs, get `STNM`, prepend the `I` of the paragraph
between them, get `I STNM` — the sign. So the live target has to be found by that marking logic, not
by picking plausible paragraphs, and the marking logic at letter level is what the sweeps have
already exhausted.

## 6. Echo map: where the chapter quotes Hal at all

Shared 4-word shingles, chapter paragraph against Hal paragraph, three or more shared:

| chapter ¶ | Hal ¶ | shared | what it is |
|---|---|---|---|
| 6 | 2 | 3 | "For those who don't know me, I am Thomas…" — Hal ¶2's opening rewritten |
| 168 | 2 | 3 | "For those who don't know me, I hope that fortunate state of affairs does not change" |
| 187 | 7 | 3 | "a young man of Japanese ancestry" |
| 217, 219, 238 | 5 | 46, 6, 6 | the RPOW sentence and its rewrites (¶219 states the rewrite rule) |
| 222 | 7 | 48 | Hal ¶7 quoted verbatim with `true identity` |
| 231–235 | 2–6 | 67, 37, 31, 59, 68 | the four-paragraph Hal block, quoted in full |
| 271 | 15 | 10 | "bitcoins through luck, with little credit to me" |

The two three-shingle hits that matter are **¶6 and ¶168**, which are the openers of W1 and W3. ¶6
rewrites Hal ¶2's first clause as the narrator's own introduction: "I am Thomas, though more people
know me under the name I created from that." So the first paragraph of the first anomaly window is
itself a Hal ¶2 plant, and the chapter contains no third "For those who don't know me".
