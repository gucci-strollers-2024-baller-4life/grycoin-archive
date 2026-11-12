# Full palimpsest index: 150 published block preimages vs the 273-paragraph chapter

Built 2026-10-31 from BTCxanter's dumps (repo issues #43/#49). Matching is on lowercased,
whitespace-collapsed text; fuzzy rows give longest-common-substring length.

| cov | block | len | para | match | fragment |
|---|---|---|---|---|---|
| 1.00 | R2b75 | 19 | 71 | EXACT | `reverse turing test` |
| 1.00 | R2b66 | 65 | 29 | EXACT | `a young woman of japanese ancestry who is very smart and sincere.` |
| 1.00 | R2b20 | 12 | 105 | EXACT | `burn address` |
| 0.91 | R1b23 | 45 | 47 | 41/45 | `climate emergency episode on this planet.` |
| 0.91 | R1b9 | 32 | 27 | 29/32 | `you will torture me to death.` |
| 0.75 | R2b27 | 36 | 125 | 27/36 | ` unspent transaction output` |
| 0.70 | R1b17 | 37 | 107 | 26/37 | `andrewyangforpresident2o2o` |
| 0.69 | R2b67 | 35 | 183 | 24/35 | ` harold thomas finney ii` |
| 0.64 | R1b32 | 55 | 17 | 35/55 | ` artificial intelligence explosion ` |
| 0.54 | R1b13 | 46 | 3 | 25/46 | ` second coming i thought ` |
| 0.33 | R1b29 | 1360 | 20 | 444/1360 | ` "fine with me. pleased to meet you, aoi. care to explain the meaning?" "artificial omnipotent intelligence, o` |
| 0.31 | R1b11 | 64 | 43 | 20/64 | ` the solution with a` |
| 0.22 | R2b77 | 5347 | 231 | 1200/5347 | `for those who don't know me, i'm hal finney. i got my start in crypto working on an early version of pgp, work` |
| 0.22 | R1b48 | 117 | 107 | 26/117 | `andrewyangforpresident2o2o` |

## Reading

- Exact: R2 b66 at 29 ("a young woman of japanese ancestry who is very smart and sincere"),
  R2 b75 at 71 ("reverse turing test"), R2 b20 at 105 ("burn address").
- b29's draft scene covers chapter 11-29; b77's Hal post is quoted at 231-235.
- No other published preimage is embedded at usable length, so the chapter is not a
  general palimpsest of her answers: it embeds the block-29 scene, the block-66 sentence,
  the block-67 name line and her own topical words.

## Tested alongside

The stage-one suffix (`\n[edited slightly]`, four spacing variants) applied to the chapter under
no-flip, not-ITASM and all-paragraph flip sets: 72 derivations, no match.