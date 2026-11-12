# Container test: the post bodies and the Wattpad framing, hashed and derived

**Date:** 2026-10-31
**Derivations:** 48 (16 candidate preimages × indices 0, 76, 77). **Hits: 0.**
**Harness:** `sweeps/sixteen_matrix.py`, `validate()` clean against `harness/btc.py` before the run.

## 1. This was already closed in this repository, one commit after the doc that opened it

`afe6ea4` (`CLAIM_FORMAT_717956015_2026-10-31.md`) speculated that *"the stage-two preimage is therefore
most likely the posted stage-two question text, byte for byte"*. The next commit, `44b32e7`
(`STAGE2_POST_AND_PART_2026-10-31.md`), tested that against the stage-two announcement and closed it:
the post names the chapter as the question and says it is *"hashed with two line breaks between
paragraphs"*, and the part itself carries no framing. So the premise of today's request is the older of
the two documents, and the repository already holds the refutation.

What was missing was the measurement, so it is below.

## 2. The factual correction that matters: document-as-preimage, not submission-as-preimage

The claim under test was that stage one's preimage is *"the complete 5,362-character Reddit question post
body verbatim, including its title, markdown line breaks, and trailing `[edited slightly]`"*. Every part of
that sentence is checkable, and each part fails:

| claim | file evidence |
|---|---|
| the body is 5,362 characters | `ca6jxv` `selftext` is **4,149** characters |
| it carries the post's title | the selftext does not contain the string `Quizchain2 Block 77` |
| it ends `[edited slightly]` | the selftext does not contain `[edited slightly]` |
| it contains the Finney text | it contains **seven quoted sentences** used as hints, not the document |
| it is a fixed preimage | `safudev_stage1.txt` starts *"I thought I'd write about the last four years…"*, the bitcointalk post |

The stage-one post's actual Question line is a URL:

> Question: https://bitcointalk.org/index.php?topic=155054.0

So the author hashed the **linked document**, not her own submission. That is the convention that
generalises, and it is exactly why stage two lands on the Wattpad part: its Question line is
*"Final version of the second chapter of Wattpad story"* with a link to `720888559-second`. Both questions
point at a document; neither hashes a post.

Two sentences elsewhere in the record stated this loosely and are now corrected in place:
`CLAIM_FORMAT_717956015_2026-10-31.md` ("the posted question text") and `STAGE2_POST_AND_PART_2026-10-31.md`
("the question *was* posted text").

## 3. The measurement

Sixteen candidate preimages, each derived at indices 0, 76 and 77 against both escrows.

| candidate | md5 | address at index 0 |
|---|---|---|
| `ca6jxv` selftext | `d8b7d47ce87343aebab598d78ea2afb4` | `1JCww89Ru6eYsiGd8qTiFeAPo44DGdcQVf` |
| `ca6jxv` title + body | `f01d5274fe39932c1f8eaeccb699d1ed` | `1CKxbhHsFJaLabTUMohosEPtvxiDWXiyEB` |
| `cgkpbb` selftext | `110dd73209b8e8018a7ead881ec2c1ff` | `15d3dobhZPt2wa1ti8187tEezFoW2HLHWn` |
| `cgkpbb` title + body | `acd2c217198ace322eb139542f641c2c` | `1HbUC5anroWv96mDQozhWsvGuLnpHVJqGG` |
| chapter body, LF | `6bc77881b2eeb1298701d771f8330844` | `1PKJAtwv3yFdgnLBwq45sjawgMVUwpcgrF` |
| + `Second` prefix, LF | `522d8a59665839b5c589fe22eabcc6f8` | `1277HyUSCbpQjrQBG5mdtGpZuom7iyaUXu` |
| + `1. Second Coming` prefix, LF | `c366d88c0041642ca4e5917b980b3f6c` | `1HiuUSXrkcE9G8xMSXSCqtymT6genTRCBR` |
| + `Hint for block 77.` prefix, LF | `57bc65e29a4fc97775930c91fc0541a7` | `1BdFN9ctRVuMP3isENjurYSZpmejnG1rsU` |
| + `Hint for block 77.` suffix, LF | `0f0d88fc1d70e6605fd60d4389750125` | `1Be4G9jKbDhUY6eQd1rVgbkrP1btdCrt3N` |
| + full title stack prefix, LF | `6f85d4be502283a90c6d8e4aefd93ca3` | `1ERQuR695Qj7Q3MgcRbYvRFFULfuxj85JU` |
| chapter body, CRLF | `2979ce16480d92d5f229d7b3dc16aabb` | `12ZZ1AQSi5zeTPdTPVYW1mYgn6EGXUiKVX` |
| + `Second` prefix, CRLF | `61ef03361557c772a10f2409c4fb93b5` | `1JYFDMRwTTb7uLbHah41t2k7DhKm3ge7eh` |
| + `1. Second Coming` prefix, CRLF | `8a2680226885666306bac92e96e37356` | `12YdVqHufaQwVB2GG8rNuwNC7hEibALvej` |
| + `Hint for block 77.` prefix, CRLF | `c3eb9952d79d47ea8a92250fce464554` | `14rdtyixGs766P9Toat8WiqN4Axm4dRHe2` |
| + `Hint for block 77.` suffix, CRLF | `70ae0315a1e0547f9c4a4507814cc1ef` | `1DfRB1o3i7cg2zURxDwA4hj9QzDcRCV9hb` |
| + full title stack prefix, CRLF | `0647897fe3bc563b1148e6737414f9b3` | `18i88FknzDdAbcKnCH8njRV7194CgXLw6p` |

**0 hits against `14zMkTga…` and 0 against `19TbyN5…`.** One candidate produces an address beginning
`14r` (`D_hint_pre_crlf`, md5 `c3eb9952…`). It is a five-character coincidence and not a hit; the escrow is
`14zMkTga…`, so the third character already differs.

So even granting the envelope hypothesis in full, and testing it six ways in both serialisations, the
envelope does not produce the escrow. The post bodies do not either, with or without their titles.

## 4. The three action items, answered

**1. Locate the stage-two post body.** Already in the repo: `grycoin_posts.json` id `cgkpbb`,
*"[777 mbtc] Quizchain last block"*, 2019-07-22, quoted in full in `STAGE_TWO_POST_2026-10-31.md` §1 and in
`STAGE2_POST_AND_PART_2026-10-31.md`. It contains no payload: one link to the chapter, one sentence naming
the serialisation, the funding and refund, two expiry conditions, and the close.

**2. The published 3-hex oracle for stage two.** There is none. 44 of the 91 posts publish a three-digit
MD5 prefix (block 76 `f8e`, demo `3c6`, Chain Block 1 `4c4`, block 22 "Prize claimed before posting"
included). The two block-77 posts are the only pair that withholds it, in terms that are hard to read
otherwise: *"I will give no information on solution format, no first digits of MD5 hash, nothing"* and
*"You are on your own completely with this one."* There is no MD5-only filter to build for this block, and
the repo has never used one: `14zMk…` is the oracle and it is exact.

**3. The outer envelope of part 720888559.** At story level the publication carries a description
(*"Hint for block 77."*) and the tag `#hintforblock77`; the chapter body is exactly 273 `<p data-p-id>`
paragraphs with no note, header, dedication or footer inside it, and the page's table of contents
(`Second`, `Second Life`, `Hoax`, `FU AOI`, …) is story navigation, not chapter text. Beyond the
description and tag, there is nothing to attach. And attaching them has now been tested: table rows 8–10
and 14–16 above.

## 5. State

| item | verdict |
|---|---|
| Stage one hashes a Reddit submission body | **no** — it hashes the linked bitcointalk post |
| Stage two hashes a Reddit submission body | **no** — the author names the chapter and its serialisation |
| Envelope variants of the chapter produce the escrow | **no** — 48 derivations, 0 hits |
| A stage-two 3-hex oracle exists | **no** — deliberately withheld, unlike 44 other posts |
| Wattpad framing inside the hashed text | **none exists**; story-level description and tag only |
| Derivation index | **0**, certified on stage one at every index 0–80 |

Unchanged: `CLUES_CANONICAL` §9 lead 1, which units get flipped, is the only open variable. The payload is
the chapter, its serialisation is two line breaks between paragraphs, and the index is 0.
