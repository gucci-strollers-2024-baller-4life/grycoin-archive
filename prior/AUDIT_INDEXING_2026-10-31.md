# Indexing audit, 2026-10-31

## 0. Verdict

The pipeline itself is sound: all three published chains reproduce (stage one `9dd2efb9…` ->
`19TbyN5…`, R1:77 `684b250e…` -> `1FAAKp…`, R2:76 `f8e5edbc…` -> `13Cv6S…`), both chapter digests
reproduce, and the new 11-check suite passes. The flaw was in *sweep scripts*, not in the crypto:
positions were taken from the decoded string and applied to encoded bytes.

Three scripts were affected. One was already superseded, two are live lanes and are now fixed and
re-run, and a third is a case of silent rot: it had marked itself complete after sweeping **a text
that is not the published chapter at all**. That family has therefore never actually been tested.

Damage is bounded: offsets are correct for every paragraph before **90**, so early-paragraph sets
(W1 at 5-8, the W4 pair at 230-235 is *not* early, see below) were never at risk.

## 1. The failure mode, stated once

There is exactly one dangerous pattern:

```
positions computed on  text (str)   ->   applied to  text.encode() (bytes)
```

Char-space editing with a single `encode()` at the end is safe, however the offsets were derived.
Byte-space everything is safe. Mixing the two silently toggles the wrong letter, and the candidate
is rejected for the wrong reason: it looks like a clean negative.

Audit criterion used: find every site that mutates bytes, then check the space its indices live in.
17 files build a `bytearray`; 14 of them mutate it in place. No `[:len(str)]` slice-into-bytes
pattern exists anywhere in the repo.

## 2. Corpus census and the drift table

The chapter holds **six U+00A0 characters**. They are the only non-ASCII content.

| char index | paragraph | byte index | drift after |
|---|---|---|---|
| 9,084 | 90 | 9,084 | +1 |
| 16,922 | 125 | 16,923 | +2 |
| 17,272 | 126 | 17,274 | +3 |
| 17,780 | 126 | 17,783 | +4 |
| 33,411 | 196 | 33,415 | +5 |
| 43,301 | 257 | 43,306 | +6 |

Chars 45,994 vs bytes 46,000 (CRLF form); 45,450 vs 45,456 (LF form).

**Canonical corpus:** only `wp_paras_br.json` reproduces the published chapter, which is certified
byte-exactly against the Wattpad page (`bd07e6ee…` / `46a308c2…`, CLUES_CANONICAL §15).

**Not canonical:** `chapter_paras_exact.json` is byte-identical to `[rec[1] for rec in
wp_paras.json]` and hashes to `48d318202691ffb873e00b63196eaf36` (LF) / `f74e8e0122e1…` (CRLF).
It is **ten characters short**: the ten internal line breaks are collapsed. It is a legitimate
calibration object (`14isnRim…`) but it is not the text the RBB is asking for.

## 3. Script verdicts

| script | byte mutation | index space | verdict |
|---|---|---|---|
| `sweeps/class3_slips.py` | yes | char spans vs bytes | **VOID -> FIXED, re-run** |
| `sweeps/typo_marker.py` | yes | char spans vs bytes | **VOID -> FIXED, re-run** |
| `sweeps/edge_intersection.py` | yes | char spans vs bytes | **VOID -> superseded** |
| `aoi_chapter.py` | yes | char spans vs bytes **and wrong corpus** | **VOID, guarded, reopened** |
| `sweeps/edge_intersection_byte.py` | yes | bytes | correct |
| `sweeps/letter_class.py` | yes | bytes (scans the encoded base) | correct |
| `sweeps/slip_extension.py` | yes | bytes (`len(para.encode())`) | correct |
| `sweeps/name_marking_word_edges.py` | yes | explicit char->byte map `boff` | correct |
| `sweeps/r129_device_chapter.py` | yes | explicit `bo(i) = len(text[:i].encode())` | correct |
| `demos/*`, `nagy_sweep.py`, `wordsweep.py` | yes | demo base, pure ASCII | unaffected |
| `harness/btc.py`, `harness/fast2.py` | n/a | no text indexing | correct |
| `sweeps/short_mark_channels.py`, `sweeps/short_marks_sentence_and_wordedges.py` | no | char space, single encode | safe |
| all remaining scripts | no byte mutation | char space, single encode | safe by construction |

`aoi_chapter.py` merits its own line: it read `wp_paras.json` element `[1]`, which is the
`chapter_paras_exact` object, so it swept a ten-characters-short text, and it indexed those
character offsets into the encoded bytes. It then wrote `{"join": 2, "span": 0, "done": 53787}` and
stopped. **Its 53,787 candidates tested neither the published text nor the letters it claimed.**

## 4. What was void, and what replaced it

| family | void | replacement | result |
|---|---|---|---|
| class-3 slips, tiers A+B | the run reported in the last session | `sweeps/class3_slips.py` byte-exact | **16,660 candidates, 83,300 derivations, 0 hits** |
| typo-restored masks | the last session's 130 | byte-exact re-run | **130 derivations, 0 hits** |
| edge-intersection classes | 1,194 (reported last session) | `edge_intersection_byte.py` | **1,770 derivations, 0 hits** |
| AOI-in-one-sentence | 53,787, never on the right text | not yet re-run | **family is open** |

Inside the old class-3 run, sets W1 (5-8) were computed before paragraph 90 and were therefore
valid; W2, W3, W4, W4b, ALL3 and ALL4 were shifted and void. The byte-exact re-run covers all of
them and is negative, so nothing was lost, but the previous turn's numbers do not stand as evidence.

## 5. Guards added

- `harness/corpus.py` — the only approved way to build a chapter base: byte spans, certified digest
  asserted, `toggle()` refuses any non-letter byte, explicit non-ASCII census and drift table.
- `tests/test_index_integrity.py` — 11 checks: three published chains, both chapter digests, span
  alignment on both bases, census, drift table, letter-only toggles, refusal of non-letters,
  non-canonical corpora identified, and every cooperating sweep script's `build()` re-validated.
  Run it before trusting any number.
- `sweeps/class3_slips.py`, `sweeps/typo_marker.py` patched to byte spans.
- `aoi_chapter.py` now asserts the certified digest before sweeping, and falls back to `fast2` when
  `bip_utils` is missing (the import error is what stopped it from ever being re-run here).

## 6. The one live item this audit produced

The AOI-family sweep (`Aoi` marked inside one sentence, the block-29 `vOIce` mechanic) has never
been run against the published chapter. It is a small family (53,787 candidates, ~90 s) and needs
re-pointing at `wp_paras_br.json` with byte spans before it counts. Until then it is the only lane
in the repo whose status is "unknown" rather than "negative".

## 7. Digest assert guard, deployed 2026-10-31

`guard.py` at the repo root. Every chapter-touching script now carries, immediately after its
top-level imports:

```python
from guard import install as _guard_install
_guard_install(__file__)
```

**102 scripts guarded**, which is every `.py` in the repo that mentions a chapter corpus. It does
three things before the script is allowed to transform anything:

1. **Corpus parity.** Re-derives the canonical digests from the source file the script actually
   reads and raises if they moved. Tested by tampering the expected value: SystemExit with the
   actual digest in the message.
2. **Drift refusal.** A tiny dataflow check separates byte names from str names, then refuses any
   offset accumulator built from a character length. It flags exactly one file in the repo,
   `sweeps/edge_intersection.py`, the superseded void script, which can no longer be run by
   accident. Two synthetic controls confirm it: a char-span builder with a byte toggle is refused,
   the same file with `len(t.encode())` passes.
3. **Non-canonical notice.** Scripts that build from `chapter_paras_exact.json` or
   `wp_paras.json` get a loud stderr notice that they are ten characters short of the published
   text, so their results cannot be read as tests of the RBB base.

Six files were reviewed by hand and exempted from the drift check because they are consistently
char-space (`verify_blocks.py`, `verify_corpora.py`, `pal2.py`, `verify_full.py`,
`verify_posts.py`, `harness/sweep1.py`); the exemptions and the reason for each live in
`guard.REVIEWED_CHARSPACE`.

`tests/test_index_integrity.py` grew to **13 checks** and now includes guard coverage (no future
chapter script can be added without the guard) and a detector self-test both ways.

**One pre-existing casualty found while patching:** `derive_multi.py` line 3 is not valid Python
(`from demo_oracle import _pbkdf2, _mnemonic_from_entropy if False else None`) and the file has
never compiled. It is untouched by this audit, but anything it was supposed to sweep was never
swept. Either repair or delete it deliberately.

## 8. The AOI lane, closed byte-exact (2026-10-31)

`sweeps/aoi_chapter_byte.py` replaces `aoi_chapter.py`. Same family (block-29 `vOIce` mechanic: mark
A, O, I inside one sentence by uppercasing every occurrence, A < O < I, one candidate per triple),
same three indices, same two escrows, but built from `wp_paras_br.json` with byte spans from
`harness/corpus.py` and the guard in front.

| | old `aoi_chapter.py` | `aoi_chapter_byte.py` |
|---|---|---|
| base | `wp_paras.json[1]`, LF md5 `48d31820`, 10 chars short | published, `bd07e6ee` (CRLF) and `46a308c2` (LF) |
| offsets | character offsets into encoded bytes | byte offsets |
| sentence spans | 641 on both bases | 641 on both bases |
| candidates | 53,787 | **53,562** (26,781 per base) |
| derivations | 161,361 | **160,686** |
| hits | 0 (meaningless) | **0 (definitive)** |

**Hit-detector control [V].** Target the sweep at the address of candidate 500 at index 2
(`1ERhcynFsz7vUiqWMfzm8C1ybcmcdCtkHa`) and scan candidates 495-505: it reports exactly
`[(500, 2)]`. The derivation and comparison path works, so zero is a real negative and not a dead
comparator.

The 225-candidate difference from the old run is the base: ten characters of internal line breaks
change both the sentence spans and the A/O/I populations slightly.

Family status: **closed**. Every lane in the repo is now audited or closed, with the single exception
of `derive_multi.py`, which has never compiled and therefore never ran.
