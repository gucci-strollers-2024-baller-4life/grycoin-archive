# The two Block 77 posts are in the repo, and they answer all three questions

**Date:** 2026-10-31
**Sources:** `grycoin_posts.json` (91 r/Grycoin posts, full `selftext`), `agntn/` (15 per-post markdown
files), `wp_page.html`, `wp_raw_720888559.html`.

## 0. Correction first: the repo has the author's Reddit posts, and I said it did not

`PAYLOAD_AUDIT_2026-10-31.md` §2 concluded that the repository held "two external primary documents" and
no authorial Reddit corpus. That is wrong. `grycoin_posts.json` holds **91 posts with full `selftext`**,
retrieved 2019-07-25 to 2019-08-29, and `agntn/` holds 15 of them as markdown. `VERIFY_POSTS.md`,
`RBB_DOSSIER.md` and `B76_INDEX_AND_ARCHIVE_2026-10-31.md` already cite them, including the Wattpad tag.

So does `PATHWAY_B_AUDIT_2026-10-31.md` §1's line that "the post body itself was not captured". It was
not captured *in the archived HTML*; it is captured in the JSON dump. Both statements are now fixed in
place. What remains true from the earlier audit is narrower: there is still no byte stream of the 2008
announcement, the v0.1 release post, the genesis coinbase parameter or the whitepaper anywhere here.

## 1. Stage two's post, verbatim

`cgkpbb`, *"[777 mbtc] Quizchain last block"*, 2019-07-22, 15 comments:

> Thank you for playing the quizchain. Second stage of last block, with a 777 mbtc prize. Funding
> transaction below. […]
>
> If you look at the funding address, you will find it is: **1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC**
> […]
>
> **You are on your own completely with this one.** Good luck. I will shut down now, while publishing the
> Wattpad update.
>
> There are two expiry conditions. If no one solves this and claims the prize before either condition
> becomes true, I will send the prize to a climate emergency related charity and disclose the solution.
> The first condition: The 200 day moving average the Mayer Multiple is based on hits $100 per mbtc […]
> The second condition: Tanabata 2022 comes. […]
>
> **Question: Final version of the second chapter of Wattpad story, which I will publish in a moment.**
>
> Your turn, humanity.
>
> Update: Started up again […] direct link to the chapter in question is:
> **https://www.wattpad.com/720888559-second**
>
> Update: Took back the funds from the address above and sent them to a new address, funding transaction
> below, **because I wanted to remove one of the twists I had. The block is now slightly easier. It is
> also hashed with two line breaks between paragraphs now.**

That is the whole stage-two announcement. It contains **no payload text, no format line, no TOMI field,
and no MD5 prefix**. It names one document, by link, and states the serialisation in eight words: two line
breaks between paragraphs.

## 2. The container theory, on the evidence

The argument was that stage one hashed "the entire post body as submitted to Reddit, ending with
`[edited slightly]`", so stage two might hash a post envelope too. Stage two's own announcement refutes
it, and stage one's does as well:

**Stage two.** The author says the question is *"Final version of the second chapter of Wattpad story"*
and that it *"is also hashed with two line breaks between paragraphs now"*. A post envelope has no
paragraphs to put line breaks between. The hashed object is paragraph-joined chapter text.

**Stage one.** The stage-one post (`ca6jxv`, 4,149 characters of selftext) does not contain the Finney
post at all. It says:

> Question: https://bitcointalk.org/index.php?topic=155054.0

The hashed text is therefore the **bitcointalk post**, 5,362 characters, whose certified preimage ends
`…my legacy.\n[edited slightly]` with no trailing newline. The `[edited slightly]` tag travels with the
bitcointalk text as captured, not with a Reddit envelope. So the "verbatim posted challenge text"
observation is right about the *document*, and wrong about the *container*: it is a linked document, not
the submission body.

## 3. The three questions

**Q1. The stage-two post's raw text, and whether it reveals a format, prefix or endpoint.** It is in the
repo, quoted in full above. It reveals none of those things, and it says so in as many words: *"You are on
your own completely with this one."* There is no submission form anywhere in this series; prizes are
escrowed and the solver takes the funds.

**Q2. Did the Wattpad publication carry framing outside the 273 paragraphs?** Yes at story level, no at
chapter level. The publication page's own metadata reads:

- `description`: *"Read story Second by AoiNakamoto with 6,722 reads. **hintforblock77**. Second I. Second
  Life"*
- story description paragraph: **"Hint for block 77."**
- tag: **`#hintforblock77`**

The chapter body itself is exactly 273 paragraphs: `wp_raw_720888559.html` contains **273 `<p
data-p-id>` elements and nothing else**, and all 273 match `wp_paras_br.json` paragraph for paragraph,
with no author's note, header, dedication or footer inside the text. So the framing exists, and the
author uses it to label the chapter as the hint, but it is page furniture rather than part of the hashed
body. The story is also titled `Second` in a series whose parts are a numbered list, which is where the
33-part modulo idea came from.

**Q3. What was the published 3-character hex oracle for stage two?** There isn't one. Of the 91 posts,
**44 publish a three-digit MD5 prefix**, and the two block-77 posts are the only pair that deliberately
does not:

| block | prefix |
|---|---|
| 13, 14, 18, 20, 22, 24–26, 28, 29, 31, 32, 35–37, 41–51, 54, 56–58, 60–62, 64–66, 69, 72–76 | published, e.g. block 76 = `f8e (copypasted)` |
| Grycoin Chain Block 1 (2019-07-28) | `4c4` |
| Grycoin Block 2 (2019-08-03), the demo | `3c6` |
| **Quizchain2 Block 77 Stage One** | **none** — *"no first digits of MD5 hash, nothing"* |
| **Quizchain last block (Stage Two)** | **none** — *"You are on your own completely"* |

So a 3-hex screen for stage two does not exist to be found, and it is not needed: the escrow address
`14zMkTga…` is an exact oracle, which is what every sweep in this repo has been checking against.

## 4. The index, measured rather than argued

Stage one's certified address `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` was re-derived from
`md5(safudev_stage1.txt) = 9dd2efb9bc976c2095bd534d7b8d431c` at **every index 0–80**:

- index 0 → `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` **match**
- every other index → no match

So the one certified lane in this puzzle is **index 0**, which is what the manual Ian Coleman workflow
produces as the first row, and what the user's argument predicted. My earlier narrowing to index 76,
based on the round-2 block-2 sentence *"pick the second private key … because this was block 2"*, is
withdrawn: the measurement contradicts it for the only lane we can verify. The round-2 sentence still
stands as an author statement about round-2 blocks, so the two do conflict, and the certified datum wins
on evidence.

## 5. What the author says the hint actually is

This closes the question carried over from the last pass, and it is documentary rather than analytical. In
the stage-one post, under **Hint two**, she quotes four sentences of the Finney post and then says:

> This is Satoshi's hint right in the post on how to decode it. After removing the misdirecting part, I
> will rearrange the first four and last four words a bit:
>
> Today / I / Satoshi's true identity / recognize the signs.
>
> That in itself is a pretty clear message. To translate it for those who may not get it even in this
> format: **Today I come out. If you want to know Satoshi's true identity, recognize the signs.**

The sentences are ¶7 of the post (*"Today, Satoshi's true identity has become a mystery… so I recognize the
signs."*). The sub-paragraph unit is therefore the **sentence group**, and the author says the mechanism
is the first four words and the last four words of it. ¶7's own edges are `T…s`, and its tail `s` is the
one that resolves to ¶10's head `S` in the boundary matrix. That is not a coincidence to be built on, but
it is where the author points.

Also from the same post, on what the hint is *for*: *"When solving the genesis block puzzle, I had the
advantage of having solved this one already, so I knew what to look for. Was much easier to recognize the
signs in the genesis block that way."* The `Aa` comment in 2020 is that same statement again, one year
later: recognise the case device, then look.

## 6. State

| claim | verdict |
|---|---|
| Repo holds the two block-77 posts verbatim | **yes**, `grycoin_posts.json` |
| Stage two hashes a Reddit envelope | **no** — author says chapter text, two line breaks between paragraphs |
| Stage one hashes the Reddit submission body | **no** — it hashes the linked bitcointalk post |
| Stage two published a 3-hex oracle | **no** — deliberately withheld, unlike 44 other posts |
| Wattpad page had framing outside the 273 paragraphs | **story-level only**: "Hint for block 77.", `#hintforblock77` |
| Certified derivation index | **0**, measured across 0–80 |
| The "hint in the post by Hal" | **¶7's first four and last four words**, per the author |

Unchanged: the open variable is still *which* units get flipped (`CLUES_CANONICAL` §9 lead 1). What
changed this pass is that the payload is confirmed to be the chapter and nothing else, the index is
confirmed to be 0, and both of those were already answerable from files in this repository.
