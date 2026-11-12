# The 273-paragraph `data-p-id` audit: the base is byte-exact except at ¶78

**Date:** 2026-10-31 **Source:** `wp_raw_720888559.html` (59,607 bytes, 273 `<p data-p-id>`).
**Method:** for each of the 273 paragraphs, hash the inner markup under a cross product of `<br>` handling
(removed, `\n`, ` `, literal `<br>`, `\r\n`), trailing character (none, one space), and NBSP handling (kept,
converted to ASCII space), and compare to the stored id.

## Result: 272 of 273 match, with no trailing characters anywhere

| variant | matches |
|---|---|
| tags stripped, `<br>` **removed**, no trailing char, NBSP **kept** | **272 / 273** |
| same, NBSP converted to ASCII space | 267 / 273 (fails ¶90, 125, 126, 196, 257) |
| `<br>` as `\n` / space / literal / `\r\n` | 262 / 273 (fails all ten break paragraphs) |
| any variant with a trailing space | never better |

So the `data-p-id` is a **content hash of the paragraph text**, and it certifies the base text at the byte
level. The three specific questions:

**1. Which paragraph needs a trailing space?** None. 272 of 273 match with nothing appended, so the premise
that one paragraph requires a retained trailing space is not borne out by the ids. `base_chapter_lf.txt`
appends nothing anywhere and is correct.

**2. The six U+00A0 sites (¶90, 125, 126, 196, 257 and one more).** They match **with the NBSP kept**, and
break when it is converted to ASCII space. So Wattpad hashed U+00A0, and `base_chapter_lf.txt` keeps all six
(`t.count('\u00a0') == 6`). Observed at ¶90: `…built on Bitcoin as a\xa0 mechanism…`, an NBSP sitting where a
double space belongs.

**3. The ten `<br>` sites.** All ten fail under `\n`, space, literal `<br>` and `\r\n`, and match only when
the break is **deleted**: Wattpad's content hash concatenates the segments. That is Wattpad's storage
convention, not the author's. Two things settle which one she hashed:

- Wattpad's stored `length` (45,451) counts a character per break: 44,896 chars + 10 breaks + 2×272
  separators + 1 trailing newline. So the rendered, copyable text carries one newline at each break.
- The certified stage-one preimage does exactly that: `safudev_stage1.txt` ¶16 contains
  `legacy.\n[edited slightly]`, one internal newline where the bitcointalk HTML had a single `<br>`.

So `base_chapter_lf.txt` (`\n` at the ten breaks, `\n\n` between paragraphs, 45,450 chars, md5
`46a308c279540a33e977ea1f660e8458`) is the correct serialisation, and it is now verified paragraph by
paragraph rather than assumed.

**4. The scar at ¶78.** Confirmed as the single anomaly, and more sharply than before:

| ¶ | text | stored id | md5 of text |
|---|---|---|---|
| 34 | `"What?"` | `184826be0ea6837abb5851807f7a9e2b` | `184826be0ea6837abb5851807f7a9e2b` ✓ |
| 78 | `"What?"` | `8b71bade9685d3388452bc4755b06a0d` | `184826be0ea6837abb5851807f7a9e2b` ✗ |

¶34 and ¶78 are byte-identical, and ¶34 matches its id exactly while ¶78 matches nothing. A 168-variant probe
of ¶78 (five quote styles × four word forms × six trailing characters) found no match. Since the field is
demonstrably content-derived, ¶78's id is a leftover from **different content**: she edited that paragraph at
some point and the id did not follow.

That matters for the sweeps in one direction only. The chapter's `modifyDate` is `2019-07-23T23:12:04Z`, a day
after the re-funding post, so the current text of ¶78 is the *final* text, which is what she hashed. The stale
id is evidence of an edit **before** the hash, not after it. The pre-edit wording is unrecoverable (MD5 is
one-way), but it is not needed.

## What this changes

Nothing about the preimage: the 273-paragraph chapter, `\n\n` between paragraphs, `\n` inside the ten
break paragraphs, NBSP preserved, index 0. What it changes is confidence: the baseline every sweep has run on
is now certified at 272/273 by independent per-paragraph hashes, with the one gap identified and bounded to a
single paragraph whose present text is the final one. The concern that "every document-level sweep was
operating on a slightly corrupted baseline" is answered in the negative, and it is answered with a hash, not
an argument.
