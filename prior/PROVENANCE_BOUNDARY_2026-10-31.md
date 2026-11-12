# The demo's preimage boundary, settled from the primary source

**Date:** 2026-10-31
**Sources:** `grycoin_posts.json` `data[2]` (`cleczc`, "Grycoin Block 2", posted 2019-08-03, `edited: false`),
`as_cleczc.json` (the post's 13-comment tree).
**Files compared:** `demo_base.txt` (1,549 ch, `7759227d7406…`), `demo_post_lf.txt` (1,456 ch, `2bc61c2e…`).

## 1. What the post actually says

The post labels its own payload with `Question:` and closes with:

> "I added the extra line breaks between paragraphs necessary for correct display in Reddit before hashing.
> And for the record, each of these resolves to the combination of the ASCII codes 13 and 10, for 13 10 13 10
> meaning two line breaks, or `\r\n \r\n` as another way of saying the same thing. Anyway, there should be no
> problem if you just copypaste everything in the **Question** from this Reddit post. **Start with the first
> "I" and stop with the period after "method"**, with no spaces or line breaks before or after that included
> in the hash. First three digits of MD5 hash are 3c6."

It is parsed as two instructions plus one check, and each of them is ambiguous exactly once:

| instruction | ambiguity |
|---|---|
| "start with the first `I`" | the **post's** first `I` is the preamble ("**I** still have not completely given up"); the **Question's** first `I` is "**I** thought I would write a bit about the format for block 77" |
| "stop with the period after `method`" | `method` occurs **twice inside the Question** — ¶5 "the **method** used and the result in detail." and ¶10 "the thinking only **method**." — plus once in the instruction sentence itself |
| "first three digits of MD5 are `3c6`" | question hash or answer hash |

## 2. The four slices, enumerated

Every combination, taken from the post itself:

| start | stop | chars | md5 | matches anything published |
|---|---|---|---|---|
| post preamble | ¶5 `method` | 1,456 | `2bc61c2e` | no — **this is `demo_post_lf.txt`** |
| post preamble | ¶10 `method` | 2,286 | `8ef14154` | no |
| Question block | ¶5 `method` | 719 | `63f78215` | no |
| **Question block** | **¶10 `method`** | **1,549** | **`7759227d`** | **= `demo_base.txt`, = the published question hash** |

One combination in four is certified, and it is the ten-paragraph Question block from "I thought" to
"the thinking only method." `demo_post_lf.txt` is not a rival reading of the same rule; it is the *wrong*
reading on **both** boundaries at once (preamble start, first `method` stop), which is why it is 93
characters short and hashes to a value nothing in the corpus ever published.

## 3. `3c6` is the answer's prefix, not the question's

The prefix is attached to the sentence about how to build the text to hash, so it can be read either way.
The thread settles it. `martypyouknowme` asked exactly this:

> "So you're saying if we simply copy and paste, change the line breaks, we should get the hash that starts
> with 3c6?"

and the author answered:

> "I am saying copy paste and do not change anything with the line breaks, change only the capitalization of
> letters in solution."

So the construction rule produces the **question** text, and `3c6` is the prefix of the **answer** once the
capitalisation changes are made. That is how every sweep in this repo has used it, and it stands.

## 4. The certification chain, corrected: the hash is the solver's, confirmed by the author

The repo's docs say "author-confirmed `7759227`" without saying where it comes from. It comes from a comment,
and the chain is stronger than a single statement:

1. `BTCxanter`, a solver who was working the block, posted in the thread: *"Who solved this part? I only
   found the source text. MD5: `7759227d7406d8230d7e3a8f7b9846d7` first seven digits: 7759227 text = "I
   thought I would write a bit about the format for block 77…"* — an **independent 2019 reconstruction**
   that reaches the same boundary we do, and publishes the digest of it.
2. The author replied: *"I really like the answer, turns out that the first seven digits of that MD5 hash
   are 7759227, with three numbers 7 turning up there."*

So the base is attested twice, from opposite sides of the puzzle, in 2019, and `edited: false` on the post
means the payload has not moved since. `demo_base.txt` should be cited as *"BTCxanter's text, hash confirmed
by the author"* rather than as an author statement.

Note the one thing that does **not** hold: `BTCxanter`'s pasted literal, recovered from the comment body
under any of the three plausible unescapings, does not itself reproduce `7759227…` (1,589 / 1,571 / 1,629
chars). That is a Reddit-escaping artifact in the comment, not a contradiction: the digest he states is the
digest the author then quotes, and it is the digest of `demo_base.txt`.

## 5. There is no `3ce` near-miss anywhere in this corpus

Searched every `.md`, `.json`, `.txt` and `.log` in the repo: `3ce` occurs only as a substring inside hex
private keys, transaction ids and one base58 address (`1Gj4s6mi4euu3ce1…`). The only two prefixes the
author ever published are `7759227` (question) and `3c6` (answer). Any `3ce` result would be a
three-hex-character near-miss with no evidentiary status, and none is recorded.

## 6. Verdict

- The boundary question is **closed**, and it was closed before this pass (`SESSION_2026-10-30_second.md`
  §3.1 reached the same conclusion from the hash alone). This pass adds the primary-source mechanism: which
  two boundaries were confused, why the confused slice is exactly 1,456 characters, and the interactive
  exchange that fixes `3c6` to the answer.
- **No sweep needs re-running because of it.** `demo_base.txt` is the preimage, and the families that were
  run on `demo_post_*.txt` tested a text the author never hashed, which the repo already recorded.
- The live open item for the demo is unchanged and is a *rule* question: the answer is not within four case
  edits of this base, the POS-filtered five-change space is exhausted, and L1/L0 (135.4M / 283.7M) remain
  unrun by decision.
