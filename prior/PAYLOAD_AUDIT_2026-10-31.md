# External payload audit: the repo holds no Satoshi announcement and no genesis byte stream

**Date:** 2026-10-31
**Question asked:** does the repo hold explicit raw text files for the Satoshi announcement candidates?
**Answer:** No. Two external primary documents exist here, and neither is one of them.

## 1. The search, and what it returned

Every file in the repository, all extensions, searched for the markers that any raw capture of these
documents would have to contain:

| marker | the document it pins | hits |
|---|---|---|
| `working on a new electronic cash system` | the 2008-10-31 cryptography-list announcement | **0** |
| `first release of Bitcoin` | the 2009-01-09 v0.1 release post | **0** |
| `The Times 03/Jan/2009` | the genesis coinbase headline | **0** |
| `Chancellor on brink` | the same headline, alternate framing | **0** |
| `04ffff001d010445` | the genesis coinbase scriptSig, hex form | **0** |
| `conventional currency` | the 2009-02-11 "root problem" post | **0** |
| `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` | the genesis address | 6, all *citations* in prose docs |

So the genesis artefact appears only as an **address string quoted in analysis**, never as a byte stream.
There is no copy of the whitepaper, no v0.1 source tree, no mailing-list post, and no coinbase parameter
block anywhere in the material.

## 2. What raw documents the repo does hold

| path | bytes | what it is | external? |
|---|---|---|---|
| `hal_original.txt` | 5,331 | the Finney "Bitcoin and me" post, edited heading | **yes** |
| `hal_post.html` | 5,429 | HTML capture of the same | yes |
| `demo_base.txt` | 1,549 | grycoin block 2, the format example | no (author's) |
| `safudev_stage1.txt` | 5,362 | the certified stage-one marked text | no |
| `preimages/r1b77.txt`, `r2b76.txt`, `r2b77_stage1.txt` | 112 / 32 / 5,362 | the three certified answer strings/texts | no |
| `corpus.json`, `wparts/*.txt` (31 files) | — | **all 33 author posts**, incl. "Complete Quizchain" (766 ¶) and "Complete Second Round" (367 ¶) | no |
| `cq_raw.txt` | 101,743 | the published question set, `data-p-id` form | no |
| `wp_page.html`, `wp_raw_720888559.html`, `base_chapter_*.txt`, `chapter_*.txt` | ~45,000 each | the 273-paragraph chapter in every join form | no |
| `ca6jxv_arch.html`, `ca6jxv_full.html` | 440,495 / — | archive.org capture of the Block 77 quizchain page | no |
| `tweet1.html`, `sotwe.html`, `nr2/nr3.html`, `nitter_*.html` | 5–48k | one tweet; the rest are Cloudflare "Just a moment" or empty nitter shells | no |
| `ak4_*.txt`, `wordk*_out.txt`, `*_hits.txt`, `tumble_ledger.txt` | MBs | sweep output logs | no |

**Correction (2026-10-31, later the same day):** the paragraph that stood here claimed the Finney post and
the genesis address string were "the whole external corpus". That was wrong. The repository also holds
`grycoin_posts.json`, **91 r/Grycoin posts with full `selftext`**, and `agntn/`, 15 of them as markdown,
which together contain the author's own block-77 stage-one and stage-two announcements verbatim. See
`STAGE_TWO_POST_2026-10-31.md`. The finding of §1 is unaffected: there is still no byte stream of the 2008
announcement, the v0.1 post, the genesis coinbase parameter or the whitepaper.

**What the external corpus actually contains**: the Finney post (`hal_original.txt`, `hal_post.html`); the
genesis *address* as a quoted string; and the author's 91 Reddit posts.

## 3. What that means for Pathway A

Pathway A, as posed, cannot be run from this repository: the payload would have to be captured first.
It also has to overcome a documentary statement rather than a silence. `CLUES_CANONICAL` §5 names the
hashed object outright — *"Final version of the second chapter of Wattpad story" at `720888559`,
"hashed with two line breaks between paragraphs"* — and `BLOCK77_KEYS.md` restates it. Under that
statement the payload is in the repo in thirty forms, and Pathway A is not merely untested but
contradicted.

That does not make Stage one's precedent irrelevant: stage one's rule was explained in the question text
and applied to an external document. But the author, writing about her own block, names the chapter. A
pathway that requires her to be wrong about which document she hashed is not cheap and not symmetric
with Pathway B.

## 4. Pathway B: the missing corpus may actually be here

`gh_leads.md` §4 is precise about the state of the numbered-corpus method:

> A method confirmed on 3 other blocks in the same series (56, 57, 58) uses the block's own number as a
> position index into a specific corpus (a numbered post by Satoshi Nakamoto or Hal Finney on
> bitcointalk, read in a specific order). The same method, tried against every corpus and ordering
> available … does not produce a post containing "change" or "from" at position 76. The corpus this
> method should index for block 76 has not been identified; candidates not yet tried include … the
> author's own r/Grycoin posts read as their own numbered sequence.

That last candidate is no longer missing. `corpus.json` holds **33 numbered author posts**, and
`wparts/` holds the same set as raw files. So the untried candidate is now testable offline, and it is
the only untried candidate that is also in-repo.

One caution, stated plainly: this method targets a block's **question** side, and block 76 was swept
closed on 2026-08-17 without it. It is a way to find what a block asks, not what stage two hashes. If
Pathway B is pursued it should be pursued for what the precedent actually establishes.

## 5. The section-partition claim, which is not reproducible from the record

The claim: dividing the text by narrative sections yields exactly three 4-anomaly sections, two of them
`GFVE` and `WVWB`, both derived negative, the third being W3.

- `GFVE` and `WVWB` appear **nowhere** in the repo. Neither does any section-boundary definition for the
  chapter. So the partition cannot be reconstructed from the record as it stands.
- Sliding windows of 6 to 24 paragraphs over the chapter, counting out-of-class paragraphs under
  `{A,I,M,O,S,T}`, give **81 distinct four-anomaly codes**. The frequent ones:

| code | windows |
|---|---|
| `FFWW` | 82 |
| `HCDH` | 55 |
| `FFGF` | 36 |
| `CDHH` | 36 |
| `WVWB` | 16 |
| `VEGW` | 15 |
| `HFFW` | 15 |
| `HWVW` | 15 |
| `GFVE` | 2 |

So "a span with exactly four anomalies" is not rare, and `FFWW` is the *most* common such code in the
chapter, 82 times. Any partition can be made to produce a four-letter code by choosing its edges. A
section-level claim therefore needs a section definition that is justified independently of the code it
produces, and the two derived windows (`GFVE` at ¶116–130, `WVWB` at ¶77–88) are simply two more
negatives among a family of 81 that would all have to be derived for the selection to be principled.

This does not make the two negatives wrong. It makes them non-discriminating, and the record should say
so rather than carry them as evidence.

## 6. Two corrections carried into the record

**The `14z` collision is 166× more likely than the entropy estimate.** P2PKH addresses always begin `1`
(30,000 of 30,000 in a measured sample), and `14` occurs at 4.20%, so `14z` occurs at **1 in 1,580**
(19 of 30,000), not 1 in 262,144. Expected count across 120 derivations is 0.076. The collision is noise
by a wider margin than the bits-per-character argument suggests, because Base58 address characters are
not uniformly distributed at the head of the string.

**The join differs between the two oracles, and I had it backwards for the chapter.** The demo's
question hash `7759227d7406` reproduces only under `\n\n`. But `STATE_OF_HUNT.md` records the live
`14zMkTga…` escrow's join as `\r\n\r\n`, on the author's 2019-08-01 note *"Hit enter twice … 13 10 13
10"*. So CRLF is the chapter's primary join and LF is the demo's. My earlier line that "the CRLF branch
is decorative for this author" was wrong for the chapter. No result moves: every sweep in `d6675c3` and
`dce5ae2` ran both joins, and so did `e3b32b3` / `b8b6f32`.

## 7. Phantom references pruned

`SAT_SET_TRANSPORT_2026-10-31.md` §5 attributed the open sentence variable to a `§13.9` of
`CLUES_CANONICAL`. That section does not exist; §13 runs 13.1 to 13.5. The citation has been replaced
with the sections that do exist, and the sentence-variable status is recorded in `SENTENCE_UNIT_2026-10-31.md`
§2 (664 sentences, 2^664 as a free subset, no rule anywhere in the corpus).
