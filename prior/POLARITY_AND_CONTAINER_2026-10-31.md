# The container claim does not survive the two certified preimages; the polarity blueprint tested negative

**Date:** 2026-10-31
**Script:** `sweeps/polarity_flip.py`

## 1. The stage-one preimage has no envelope

The claim was: hashing the 16 paragraphs of Hal's post alone does not reproduce the escrow; it
reproduces only when hashing "the complete 5,362-character Reddit question post body verbatim,
including its title, markdown line breaks, and trailing `[edited slightly]`".

What `safudev_stage1.txt` actually is:

    first line  "I thought I'd write about the last four years, an eventful time for Bi…"
    last line   "[edited slightly]"
    length      5,362 chars, 16 paragraphs
    md5         9dd2efb9bc976c2095bd534d7b8d431c   (certified prefix 9dd)
    index 0     19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN   (the escrow)

There is no title line, no "Thank you for playing the quizchain", no funding-transaction link. It is
the 16 prose paragraphs and nothing else. **The 16 paragraphs alone are exactly what reproduce the
escrow.** The envelope was never part of it.

The real announcement body is a different, smaller object: 4,146 characters, opening "Thank you for
playing the quizchain. / I publish this block out of schedule for two reasons." It does not contain
the Hal text at all — "I thought I'd write" does not occur in it, and the 5,362-character preimage is
not a substring of it. Hashing the post would hash prose the author never hashed.

The same holds on the stage-two side by the author's own words in cgkpbb:

> **Question: Final version of the second chapter of Wattpad story, which I will publish in a moment.**

and

> It is also hashed with two line breaks between paragraphs now.

So the hashed object is the chapter body. Its container is measurably empty: `apiv2/storytext` for
720888559 returns exactly 273 `<p data-p-id>` paragraphs and no residue, and the part has not been
modified since 2019-07-23T23:12:04Z. There is no envelope to recover, on either stage.

Conclusion: the chapter sweeps were not hashing a stripped excerpt. They were hashing the object the
author named. The open variable is the case edit, not the container.

## 2. The three follow-up items

| item | answer |
|---|---|
| stage-two post body in the repo | yes, `agntn/aoinakamoto-2019-07-22-cgkpbb.md`, full transcript; see above for why it is not the preimage |
| 3-hex oracle for stage two | **none published.** Stage one's post says "I will give no information on solution format, no first digits of MD5 hash, nothing"; asked later for more digits for block 76 the author refused: "would make it too easy to script the block". `9dd` is stage one's alone |
| Wattpad framing in Jul–Aug 2019 | none. 273 paragraphs, nothing else; part modified 2019-07-23, story 2019-07-23, never since |

## 3. The polarity blueprint, applied literally, is negative

The operation certified in `HAL_BOUNDARY` (`ff7ee65`) is endpoint case inversion on the anomalous set:
`F…s → f…S`, `F…t → f…T`, `W…n → w…N`, `W…m → w…M`, internal prose untouched. Applied to the
chapter's anomalous set — the sixteen window paragraphs — on the certified base (LF, `\n\n` joins, no
trailing newline), derived at index 0:

| variant | md5 | index 0 |
|---|---|---|
| unmodified base | `46a308c2…` | `1DGrEwbRwANU28BgCnp6HeNhPzB2HbiyUL` |
| 16 both endpoints | `7c85cd14…` | `1dwb5ApzNNHQzgr9kvXLCVYHnk56cCYjh` |
| 16 initials only | `b991023c…` | `1MPc6z7MwYVXFv8KdBuF6MgAKbtLoNyJhD` |
| 16 finals only | `a55b8c4e…` | `13Bi3f5qwpgoRVkLz4DmRHXWVAGrweoLFN` |
| 8 F-initial, both | `433a5308…` | `1CRD1GqsgyV5fV8tMWeYD4Yd7emfbyxnHr` |
| 8 W-initial, both | `bf752f23…` | `1LVhUufPqdaUapkM6vDVYXk8YbukQmeSUk` |
| 4 `F…t`, both | `666887b5…` | `1Kj6zyVVy4jmESr2dweLWFPh66aTUF9K9k` |
| 4 window openers, both | `488cb789…` | `1DtNHNnGtgnchhM5We9pB2r5ZDfCh3FnLv` |
| 4 window openers, initials | `b848c48e…` | `12vH2RJjyZRBA9qdJCgrsQaTzhSgdaCM2h` |
| 4 `F…t`, finals only | `f6bcdc44…` | `141iLQhghg1Qgcgw9NXsXsdnZmhNs46uhJ` |

Zero hits against `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`.

Note on the implementation: the first run showed "finals only" leaving the md5 unchanged, because a
paragraph's final character is usually punctuation. The flip has to target the last *alphabetic*
character, which is what the table above does.
