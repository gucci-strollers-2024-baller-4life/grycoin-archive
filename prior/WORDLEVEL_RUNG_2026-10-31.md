# Word-level rung: 36 derivations at word edges, plus a 17-candidate byte-layer probe

**Date:** 2026-10-31
**Scripts:** `wordlevel_ladder.py`, `br_layer_probe.py`
**Ledgers:** `wordlevel_ladder_results.json`, `br_layer_probe_results.json`
**Predecessor:** `BLUEPRINT_LADDER_2026-10-31.md` (84 paragraph-level derivations, all negative)

Target throughout: `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`, the only live escrow.
Indices 0, 1, 2, 5, 6, 7, 44, 76, 77 on every candidate.

## Result

**36 word-edge derivations: 36 distinct md5, 0 hits, 0 no-ops.**
**17 byte-layer derivations: 17 distinct md5, 0 hits.**
Running total for the day: **137 named derivations, zero hits, no collisions.**

## What the word-level rung actually tested

The unit moves from the paragraph to the word edge inside the designated windows. Every candidate is
one hypothesis, not a position enumeration.

| rule | content |
|---|---|
| W1 | raise the final letter of the 12 terminal words of the three FFWW windows (`keyS`, `thaT`, `agaiN`, `theM` twice over). This makes the STNM letters visible in case, which is what the marker channel does. |
| W2 | W1 plus paragraph-initial lowering in the same 12 paragraphs: the demo's two-edge pair applied at the window. |
| W3 | W1 over the 12 "recognize the signs" paragraphs. |
| W4 | W1 over para 222 plus the Finney reprint 231-235. |
| W5 | the eight words ¶242 actually names: para 222's first four and last four, final letter of each raised. |
| W6 | the sign letters at word edges: inside each window paragraph, uppercase every word-edge occurrence of that paragraph's own STNM letter. |
| W7a-c | signs recognized by initial letter and **lowered**, the demo's direction (`I` -> `i`), at word level inside the windows, S3 and S5. |

Each in four serializations (`\n\n`, `\r\n\r\n`, trailing separator or not).

**Consistency check.** `W2` returns md5 `e4ec7577e9a80d66a06196f2c6e1182f`, byte-identical to
`S4/both_para` from the paragraph-level run. Two independently written implementations of the same
rule on the same paragraphs agree, which is what should happen and is worth recording.

**Full ledger:**

| derivation | md5 | addr @0 |
|---|---|---|
| `W1/windows-final-up/LF` | `b65f856e866a087d66629b2ce83cda8a` | `1PbuYLv4VVBBghfDHYsjY6vBigzm5QtUY5` |
| `W1/windows-final-up/LF+t` | `1ae9cd1d6f0e64f1a099104935d908c7` | `1KXb6GT4THT84ZJQk4XKFPbnoSkY5VHGrs` |
| `W1/windows-final-up/CRLF` | `b11376ce1e3ff50591054e4fcc8717dd` | `1MXPDwzSPd4EyMddWvxbnCuNzjq5qryjbr` |
| `W1/windows-final-up/CRLF+t` | `4a3997e2cbb1dc64a4992259ce6d0250` | `1JzrmTNBZhSSxbuMKMi6DT5auStZHeajPR` |
| `W2/windows-final-up+init-down/LF` | `e4ec7577e9a80d66a06196f2c6e1182f` | `17eAJEosbfgS2B4aqK9SvuACja2YvWqRkJ` |
| `W2/windows-final-up+init-down/LF+t` | `1eaab5fd452aaa60dfc1a20ae41af3ff` | `1PKfFJpT1oJgxfE9kGF6LauHHuppextnum` |
| `W2/windows-final-up+init-down/CRLF` | `e0ef4e5ad41596a16e82e1c9201b67a6` | `1AhkUFKAz5jr6LGDtvVqeh9epCU8sRtoQ` |
| `W2/windows-final-up+init-down/CRLF+t` | `f6e1502d0d959b1e8a35d5c79b263744` | `1DKfAdPd7vYBu6mwoErTqZYs1Do9v1aehc` |
| `W3/signs-paras-final-up/LF` | `b8765b3b741d9faefe94f5005a7ff7bf` | `12ufb7pKvE2HKoBXY2v9N5Fqg8CzzjqURw` |
| `W3/signs-paras-final-up/LF+t` | `baa742eb663f99f4c249d5259b363dce` | `1CVpw5BrisbxShZuZnmMEzqwSyjMufHJWW` |
| `W3/signs-paras-final-up/CRLF` | `dc39ca0e848020b145d587b6b9cdbbc5` | `19cpQmbmkSEzA1R6qd8gvj4PVW7HvCT8EP` |
| `W3/signs-paras-final-up/CRLF+t` | `7737e69a78f314321c2d5bd1a8fa79c5` | `19uxUksiNEKUPoQDwdcTwW7GTt8HE6bY3C` |
| `W4/reprint-final-up/LF` | `1b1ecc7647f65888609c6c45e4885ad2` | `19wz5gzD6YV5kcYVrc9tG23dQXiVLJCrGX` |
| `W4/reprint-final-up/LF+t` | `ba9ea3c51fd9b270ce336dbba1167ca1` | `1DMjfJxj8nY3v5Juo1n7eT4DTBUQC8tzhL` |
| `W4/reprint-final-up/CRLF` | `54e6f3425ef035e8f57fc6de36eff046` | `14CeVPXV12Y1CRbKFhrV5fa87ps3XYRsxD` |
| `W4/reprint-final-up/CRLF+t` | `7e0cb8c5efcda41f2d3f975c01c30bb4` | `1CY8Sf6Hg99jSv6qn9bfp5sKZvpg24tFPQ` |
| `W7a/windows/LF` | `c3fa932e9abaad32942ea2eeb62432f9` | `1PceAYhiBb4owAfYbQPw8ELrxLuGK7gfmW` |
| `W7a/windows/LF+t` | `f94c5cbe0f7b4cd468b126eb6e6ce4d3` | `1Dj9ruTJuqTeMU6QKxzTvtT7V7Hehf5sMu` |
| `W7a/windows/CRLF` | `fb591e31514a1000cd06c436e3bcee83` | `1J22YueSxsTY2iA64uputCS7qWVkwJLGd2` |
| `W7a/windows/CRLF+t` | `2f6b7d6889f88e284f77f8c627a722fb` | `1KpNKNRuADKn21QFuuBmxkPZExzP74JSp5` |
| `W7b/S3/LF` | `e0d864e8f1cfa99f74854ac8c9cf5d36` | `1ikqJwFyEa6AJGGwCnVkVMnLnBgeyihEj` |
| `W7b/S3/LF+t` | `3c3415f66ea103dd306fdf73759e7dc1` | `1MPFTAkiFrzuvDf1MtVNkGbcjPU1tyNHm4` |
| `W7b/S3/CRLF` | `b9ce53a0cc6c6e91da97d7c379f1ad0a` | `1HMDeLWSL19MnXixQnKZt8YPDRouxaKT7a` |
| `W7b/S3/CRLF+t` | `214b7202d842e95b3f0783bdcdb1dd7d` | `1Bv7N5pmCERshU1RCtzZBjWeD9JncLg4ag` |
| `W7c/S5/LF` | `fa0cd73e324efd9f6e20293446cfc09d` | `1GJNmFCGVTgGx9XPBcvCm6epm5wVEYiwcr` |
| `W7c/S5/LF+t` | `4d533dd528b3de9cc8c86eecac9173fb` | `1G59njC4ZdaAyWwXSNn3P1oAEF8UhxG1qX` |
| `W7c/S5/CRLF` | `f1ad03cbc09e801e253705db69515d92` | `1AyTTPfmYgcZTiHxzXw3ktYP2gBGPhmaWo` |
| `W7c/S5/CRLF+t` | `f40e6774360d0601f4a6ce60eec28e1b` | `1248WahKM8fcCvwErjvxscNpbhuYNE9eCS` |
| `W5/para222-operand-words-final-up/LF` | `e5a10b75f8f11cd01d52df4befe266a7` | `1CDQAEnKQ9566dDPba15BZ4qZxbhB8ABvo` |
| `W5/para222-operand-words-final-up/LF+t` | `dcca865ad4e50ce97b1ff1a0b14306dc` | `1FtqC1jD66DjnUp7jVdfXjWSc3VBYB8awJ` |
| `W5/para222-operand-words-final-up/CRLF` | `e7c589ae71b4fb496f79011bbba7c5fa` | `1JMqTSBfcr3DcmsyG8wDBQQTv7k6NYzGpN` |
| `W5/para222-operand-words-final-up/CRLF+t` | `078c2c4c029f9b4262af6d8f93d7e5ee` | `18L8qZUpUKw3cfnCuw5YkE25DfjjYpueqi` |
| `W6/windows-STNM-letter-at-word-edges/LF` | `bbde3908ca451d1f27e32bd091a73927` | `133PxF84sNGMZnMoFEgc3eixHe4jTotk5Y` |
| `W6/windows-STNM-letter-at-word-edges/LF+t` | `3667d475926755a46de97d490ee59261` | `1KQ6ZKiaFRSJjga2JYXohRt2SdNd2vARQ7` |
| `W6/windows-STNM-letter-at-word-edges/CRLF` | `bc39c7399bd3adc0e9670b4fb8d226c4` | `1J13PoWMKBg6BcoBq4QrKy6VaxkDNFay3h` |
| `W6/windows-STNM-letter-at-word-edges/CRLF+t` | `72a1af2059d56558bff55b0b10b34a90` | `1H5TNc1BKeZkQKUtTYHMFiLcetCVQzkHjR` |

## The audit finding that produced the second probe

`wp_paras.json` was built by stripping `<br>` with **no replacement**, so ten paragraphs contain
glued words that no human typed:

```
para 73   ...already?""Of course not. It takes time...        (quote closes and opens, no space)
para 184  ...anagram of "THOMAS".Satoshi and Thomas contain...  (sentence end, no space)
```

Paragraphs carrying an intra-paragraph break: 63, 73, 121, 124, 146, 160, 184, 189, 193, 213.

Wattpad's `p-id` matches the glued form, so the certification does not cover this: a p-id is a
tag-stripping dedup hash, and it certifies what the platform computes, not what the author typed
before pasting. Four renderings of those ten breaks are therefore live, and every candidate this hunt
has ever hashed used the least human of them.

| rendering | block sep | md5 | addr @0 |
|---|---|---|---|
| `BR=none/LFsep` | `48d318202691ffb873e00b63196eaf36` | `14isnRimk9qAzpm85qwiFgLjzxL1387TXL` |
| `BR=none/CRLFsep` | `f74e8e0122e114fe13c89a3bba25294a` | `1D1Scxy6rZYV34Xr1SFRLTsMBHeUiTJbHK` |
| `BR=space/LFsep` | `6bc77881b2eeb1298701d771f8330844` | `1PKJAtwv3yFdgnLBwq45sjawgMVUwpcgrF` |
| `BR=space/CRLFsep` | `2979ce16480d92d5f229d7b3dc16aabb` | `12ZZ1AQSi5zeTPdTPVYW1mYgn6EGXUiKVX` |
| `BR=LF/LFsep` | `46a308c279540a33e977ea1f660e8458` | `1DGrEwbRwANU28BgCnp6HeNhPzB2HbiyUL` |
| `BR=LF/CRLFsep` | `bd07e6ee209c5ab65d874bbbcfccda18` | `1BGh8btgbCSPDfjyESjnkjYyYvoB7xnDDb` |
| `BR=CRLF/LFsep` | `52be2f2c6a51020960d50adb470230ea` | `1C2bbCeYFD5zV45bEfbtwX1kMbw6DDT7r9` |
| `BR=CRLF/CRLFsep` | `db11a7fdba7b4867a24445a7a30709b8` | `1Ph7YoXiFDJtX7nRRArjmYoNhFv2NjYmjC` |
| `BR=space/LFsep/S1/both` | `3ca41bbf072e748556ae5748b21317c7` | `17wjUsgR2p7TJ5CHkzBqCMft7c89amTGAG` |
| `BR=space/LFsep/S3/both` | `54ae1eb17a3a3462df678c03912d1cc4` | `1MvnibZq6zjJiA8UbTVvqGfoa2j8tEapcV` |
| `BR=space/LFsep/S4/both` | `ba95f5c4d23fff909b3cd7a7d8b3d753` | `1A5pr3RXmq6YnTdb71QzNN6TaJe8pnpUG` |
| `BR=LF/LFsep/S1/both` | `bdc4edc8b3f3b74b671df4e7b6f1d05a` | `1Bq3MUpHseTiC1prqHi1ZZBnP2gL7ddQM4` |
| `BR=LF/LFsep/S3/both` | `524992ef37374acd71ccdeb6477757eb` | `1JdvRWLWJdtNGT5Jm9zLEsiZSSmZyRz7ow` |
| `BR=LF/LFsep/S4/both` | `b2c599fb90ae56c5946e96802d90fd9d` | `1LdbdGVfzCQ29uo1WeAk81J5UrNmN9tQcq` |
| `BR=CRLF/LFsep/S1/both` | `56c1b9c03d7c65cf9be50aba9eb99e0b` | `14pDkQVSGekdiqnzrBY1bJ3zHboUS5AaqT` |
| `BR=CRLF/LFsep/S3/both` | `8511feb0ba3964e8c94cdee5a1a7fc9a` | `1Jcry67yBkfCz34EnuFtdWTH9CEKxguGY` |
| `BR=CRLF/LFsep/S4/both` | `e749891b984ae3422b4905369cee2bec` | `1Ldw6AGrXJxrF96cuYrmRWMJ38SZixH53k` |

**Validation by reproduction.** `BR=LF/LFsep` returns `46a308c279540a33e977ea1f660e8458` ->
`1DGrEwbRwANU28BgCnp6HeNhPzB2HbiyUL`, which is exactly `base_chapter_lf.txt` in `SERIALIZATION.md`.
My reconstruction reproduces the repo's own canonical file bit for bit. So the probe is measuring what
it claims to measure, and two of the four renderings are already documented negatives.

## The interior-capital route is already closed, and this scan confirms the closure

Independently scanning the 273 paragraphs for words with an internal uppercase letter returns exactly
12 tokens, the same 12 `FINDINGS_MARKS_2026-10-31.md` lists: `ppM` 73, the two
`WorldWideAbsoluteCarbonBudget` addresses, three burn-address artefacts at 107, the two alphabet
demonstrations at 126, `VIrgin` 128, `BItcoin` 136, `BITcoin`/`AHScoin` 209.

That file already settles them, with a stronger argument than a single-chapter scan can make: `BItcoin`
and `VIrgin` are her `i`->`I` typing slip, and the slip appears in six separate parts of the story,
five of which carry no puzzle text at all. `BITcoin`/`AHScoin` are the heading's own subject. Only
`ppM` at 73 remains unexplained, and it is a single instance of a different slip class.

So inner-word case is **not** the untested lever. It was tested and closed before this session, and
the independent inventory reproduces it.

## What 137 negatives now exclude

Three independent selection geometries (paragraph-initial class, phrase-selected, window-selected),
crossed with four flip modes, four serializations, the word-edge channel, and four renderings of the
intra-paragraph break layer, all with a marker implementation validated against the author's own
worked example, and a pipeline certified on three separate vectors.

The marking rule is no longer the cheap explanation. Two structural questions remain that have not
been asked, and both are philological rather than combinatorial:

1. **Is the hashed object the whole document, or a division of it?** The three FFWW/STNM windows sit at
   division boundaries (5-8 opens section 1, 93-96 sits inside II.2, 168-171 opens 1. My Identity).
   If those windows mark divisions, the subdivisions they delimit are candidate containers, and a
   container is a different byte object than the whole chapter. `STRUCTURE_MAP.md` already carries the
   full division table, so the candidate set is about twenty spans, not a search space.
2. **Do heading paragraphs count as paragraphs?** The base treats `1. Second Coming` and
   `3. Other evidence` as ordinary paragraphs. A human copying the page would not, and the p-id cannot
   distinguish them. This changes the separator count at every heading.
