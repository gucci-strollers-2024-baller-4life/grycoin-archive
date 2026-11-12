# Blueprint ladder: 84 derivations, zero hits

**Date:** 2026-10-31
**Script:** `blueprint_ladder.py` (results in `blueprint_ladder_results.json`)
**Rule under test:** `STRUCTURAL_BLUEPRINT_2026-10-31.md` sections 3 and 4.

No sweeps. Five selection hypotheses named in the blueprint, four flip modes, four serializations,
nine derivation indices each, against every escrow the hunt records.

## Harness certification before use

`harness/btc.py` self-test, run first:

```
stage1 addr: 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN OK
stage1 wif : KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2
stage1 mnem: oven number unveil junior item aware finger price symbol express degree
```

Chapter base control, `\n\n` join, no trailing newline:

```
md5  48d318202691ffb873e00b63196eaf36
addr@0  14isnRimk9qAzpm85qwiFgLjzxL1387TXL
```

Both match the certified vectors already in the repo. The pipeline is trusted on the chapter, not
only on the stage-one demo.

## The marker implementation is validated against the author's own worked example

Applied to demo paragraph 5 with the blueprint geometry (paragraph-initial down, first-sentence-final
up), the script returns exactly what the author says it returns:

```
in : I expected otherwise, but actually not many people do recognize the signs in Satoshi's
     Bitcointalk post outing himself. Even after I explained the method used and the result in detail.
out: i expected otherwise, but actually not many people do recognize the signs in Satoshi's
     Bitcointalk post outing himselF. Even after I explained the method used and the result in detail.
```

`I`->`i` and `himself`->`himselF`, character for character, with the paragraph's real final word
(`detail`) left alone. **The geometry is therefore not the source of the negative below.**

## Selection sets actually used

| set | hypothesis | paragraphs selected |
|---|---|---|
| S1 | in-class initials `{I,T,A,S,M}`, first character | 126 |
| S2 | in-class initials, first alphabetic character (dialogue-tolerant) | 154 |
| S3 | paragraphs that say "recognize the signs" | 12 (20, 42, 220, 222, 223, 225, 226, 230, 236, 244, 246, 273) |
| S4 | the three FFWW windows | 12 (5-8, 93-96, 168-171) |
| S5 | rulebook-adjacent container | 6 (222, 231-235) |

Modes: `both` (author's geometry), `down`, `up`, `both_para` (paragraph-final up, the falsified control).
Serializations: `\n\n` and `\r\n\r\n`, each with and without trailing separator.
Indices: 0, 1, 2, 5, 6, 7, 44, 76, 77.

## Witness states, read live on-chain during this run

| address | role | funded | spent | txs | state |
|---|---|---|---|---|---|
| `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` | RBB live | 77,700,000 sat | 0 | 1 | **unspent, claimable** |
| `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC` | RBB original | 77,700,000 sat | 77,700,000 sat | 2 | drained, refunded 2019-07-30 |
| `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` | demo escrow | 700,000 sat | 700,000 sat | 2 | drained |

Only one target is live. The ladder was therefore 84 derivations against a single meaningful oracle,
`14zMkTga...`. Any future hit against the other two would be meaningless.

## Result

**84 derivations, 84 distinct addresses, 0 hits.** Full ledger:

| # | derivation | n | md5 | addr @0 |
|---|---|---|---|---|
| 1 | `BASE-LF` | 273 | `48d318202691ffb873e00b63196eaf36` | `14isnRimk9qAzpm85qwiFgLjzxL1387TXL` |
| 2 | `BASE-LF+t` | 273 | `0f9090ec09549e7d1f9d185bb3c31bba` | `1KRigTPfvxXMiuTefFEhZJxmhWGSXGv96Y` |
| 3 | `BASE-CRLF` | 273 | `f74e8e0122e114fe13c89a3bba25294a` | `1D1Scxy6rZYV34Xr1SFRLTsMBHeUiTJbHK` |
| 4 | `BASE-CRLF+t` | 273 | `5eefdba549ba8c1f40a02e4f0df0197b` | `1Gj4s6mi4euu3ce1ZXyqLUHCzTqCZkwDEP` |
| 5 | `S1/both/LF` | 126 | `d2218d4253139560517a1991450e1763` | `1G4k1zBtARZbqDnCug5V5nJNM3F5UQz6dY` |
| 6 | `S1/both/LF+t` | 126 | `025b6bccf794bbd330a67fbed8bccb10` | `1HomHA6xFWsa3eYKYqPDrfR7z9LgNPFWXq` |
| 7 | `S1/both/CRLF` | 126 | `2838953a7684b7738331e85c15196883` | `1FchvGfq5vorL2bEHdAaZxHNXdZXyHuDu5` |
| 8 | `S1/both/CRLF+t` | 126 | `82a87d6f4d599a62bfcd524fd9f830f1` | `19sVtEr1SaJc641KyLTmZDyVu5HzJufhzc` |
| 9 | `S1/down/LF` | 126 | `833015501857a8719c08b4e3b53ebcf7` | `1A4X88SLm39fgAQK9tiUgMN3dG8Jv7cGH` |
| 10 | `S1/down/LF+t` | 126 | `55fd7be78081046756a75ed81f2802e1` | `1HqwgkrqGWEENWmMNJn9UXndL5nX18LAuD` |
| 11 | `S1/down/CRLF` | 126 | `fea0bdb38098390e533cdd6633430a6b` | `1LB7TdJSXNDv2WdouRhLGwt4E5NkNeTLws` |
| 12 | `S1/down/CRLF+t` | 126 | `76c4798b96dfdade082bf7247e473323` | `1PpK5G2PxhueaxqvtdeZRY5fK1RdjytnAi` |
| 13 | `S1/up/LF` | 126 | `6ca7e2017c863e7e24215e23665776d5` | `1HEL89xpRwJoyCLA8u78dDbX1vNup3QLR5` |
| 14 | `S1/up/LF+t` | 126 | `a787fc9a3785a1cc483d62c6b3322689` | `1AfDZ9BGYjsvJzSn8D3hXmQhQZ8W3zKiTQ` |
| 15 | `S1/up/CRLF` | 126 | `abc100949bae00561ba3fd36c1961aff` | `19MAZqXRCE4Qf3eCa3tVDbpwNDhhgMA3hV` |
| 16 | `S1/up/CRLF+t` | 126 | `fe192b14661f149b9a31bb776412719a` | `1Hk4p83yLiwG7zM1m98BoEALoh6k7tm6w3` |
| 17 | `S1/both_para/LF` | 126 | `49476082336ae8b6d2b836a94e16cbbd` | `1KvsJ21jA1mBvHgYrY8vWZqpvab2RrL2vP` |
| 18 | `S1/both_para/LF+t` | 126 | `9dbba0ea6b2cef71136deb9dd57549d2` | `1EX5CKEJ1mXCba2SGUs777SxiB5yMU4ftG` |
| 19 | `S1/both_para/CRLF` | 126 | `3b08611b9b9f4c157c527ff793d3f315` | `1GjQ4m77N2rWKvdKoBHEhmixBFDBX4QeEG` |
| 20 | `S1/both_para/CRLF+t` | 126 | `28b0809d289300a8612bb4f94139454d` | `1DEruMhHnp7mSMg59V2d1bmkD2xPJSoiM9` |
| 21 | `S2/both/LF` | 154 | `b893b812e3434ddd75523ce7d638b382` | `1UxCTZekwprmXhBtpUxibGdUr6MwqSHJ7` |
| 22 | `S2/both/LF+t` | 154 | `09045cbf24a069c26ac39ff98cd3d127` | `1HiGhFMBQBUPCiS7FHWZ9H9fQtudfXHYk5` |
| 23 | `S2/both/CRLF` | 154 | `743d5fd1bfce9a4f57225ea8e90262eb` | `198rsJrWgP4qvywkkfBdxWgijCZ9Kxxcmi` |
| 24 | `S2/both/CRLF+t` | 154 | `7d550242d6d3aa53f1011ceda62f5231` | `1GPjYmcipGkPdegd8S5LLDW2rs716PipYr` |
| 25 | `S2/down/LF` | 154 | `9d0614a30a430fe2bb38bc01541c8e1c` | `1P3ccZW53BgrFs3xEwR9fkDgEacdnXvnRi` |
| 26 | `S2/down/LF+t` | 154 | `22ba18aba908bfeccf61e362f302a454` | `17Scmh2P9E9DWS5cQz7eWAw18M7289WsJp` |
| 27 | `S2/down/CRLF` | 154 | `47c555185b96c050b5d399296f5bdf42` | `1MXLjqnLDGrKqVz7U5vMDdzyp6HcfiGcR8` |
| 28 | `S2/down/CRLF+t` | 154 | `4b66210c8021855802b6b17eb3ca66d0` | `1PybzkNKx8jDyk1GahPqt7CEWwbsS4eWv7` |
| 29 | `S2/up/LF` | 154 | `f1ec6c8874685657fc99eb23182ab44b` | `1F7ZKvro4xCoJ4m735aQi4k4HfvHcJVaw` |
| 30 | `S2/up/LF+t` | 154 | `d7bc6be07906cae398a5c01eff2c40ae` | `1BJF2UJC7RxDyPLfBaWs2q37cKKaXpT7nX` |
| 31 | `S2/up/CRLF` | 154 | `35e0441b13f8e5e5bf2adb0051c07e38` | `1H9dhTw6f4opY27JnxkK1dBS5jEdJJhdLk` |
| 32 | `S2/up/CRLF+t` | 154 | `58a09eefe0f1b2e12c0808ef9696cb36` | `17qqy2aoKWpL3vqC32VvajLAVExSy6oKbD` |
| 33 | `S2/both_para/LF` | 154 | `30afbf659c0f9ca1c2e8b98166820b6d` | `1NTgF8rFNEkNPhU7VGqFJLGt9Y6BtfiFvx` |
| 34 | `S2/both_para/LF+t` | 154 | `1d974dc8cbfe3bab37c567f6df6c1038` | `1Q5Z1DRXBK6ddyP2P2UMynohYBRpUdFNex` |
| 35 | `S2/both_para/CRLF` | 154 | `97ec25dbe611fc1d7161cb28afa7895b` | `14JUddAMahmFD8nGWWzEgFGzvkEEAFjnSV` |
| 36 | `S2/both_para/CRLF+t` | 154 | `f06ca76e970f4757faaa99114c990f9f` | `19FFUbW8JQWVgrvkvxkH54EumfwKzBXKeQ` |
| 37 | `S3/both/LF` | 12 | `5d78315b79ea6eecc50e656cf1ab194f` | `13igTZTEwZxohk75nBWFWSjV4edosTeGFh` |
| 38 | `S3/both/LF+t` | 12 | `0f71c511d849cbbb7a90ca4e4f6cc133` | `1Q5gyPL6GnzuKU6oN55d9EiKrduF1Ws7fd` |
| 39 | `S3/both/CRLF` | 12 | `5b27634eecf41192c291b62f84e4fc53` | `19RHm75DAkLZPXqhEv5ugSQGkQRFpKfiMw` |
| 40 | `S3/both/CRLF+t` | 12 | `af40d35904b4f67fd0b7a561d33b4073` | `1FFzWi31J86yBuWTvqkjanLQasmYt7PaiW` |
| 41 | `S3/down/LF` | 12 | `92fe906553448eecf398b15a0499abc0` | `1DXSQNnw1XqvrzzwGB757MaSvvbMHuoS14` |
| 42 | `S3/down/LF+t` | 12 | `2ff27e254c86f41cdc7c268ea8e4ab99` | `16aSeMEsMgrnAjCYah47Z5RrLcp8GuXtLM` |
| 43 | `S3/down/CRLF` | 12 | `66c9a147c646a9ae901207825df1b9d8` | `16UpVXMqfgcxdywiRxPE3taHjeApgBtbEX` |
| 44 | `S3/down/CRLF+t` | 12 | `703b8bd14fd69ba6c3a13deeddb987e8` | `1Dg9z5SgfPN17S79b9CWko63dsA221zoT2` |
| 45 | `S3/up/LF` | 12 | `c27a92b1e39b1805ae6ea41b4b2ba176` | `1GqWLBC1c1AWbsCX3M9ierKeXMsUqkrzhY` |
| 46 | `S3/up/LF+t` | 12 | `b440d3aef22bf6983f2dff8d23a0ea18` | `1ANCDNLEa8WL8Asjnw5gKQSWtPaPeDyt3F` |
| 47 | `S3/up/CRLF` | 12 | `9da9d30a2a2bef29249f0b8cec2b6c2a` | `1EMaCHVvi9cgSo3bsYg93vzWcfF3mYiVbf` |
| 48 | `S3/up/CRLF+t` | 12 | `6d4b684ba966c454db104d174777bebb` | `1F1Nvm9pkxhmdQ5ddCcPV2eWAdAm7GMVQK` |
| 49 | `S3/both_para/LF` | 12 | `c9bc79d06c5524e18dc9f6e1091072c2` | `18YR29tjUe3MKENQeBL4UrU9hXXcP2YR59` |
| 50 | `S3/both_para/LF+t` | 12 | `4f0a094695fa97913656ced8fc79979f` | `13tbzkpruVLVpxuQM4ARQpAj7SKWcGqEEb` |
| 51 | `S3/both_para/CRLF` | 12 | `0735717c1d9c3f3c9c334860353e1604` | `1K7UEiBSH1yCogu6qDYy3tp6t7YAEhkysg` |
| 52 | `S3/both_para/CRLF+t` | 12 | `68021ab3d8977eb2080f4487474cef8c` | `1AmhkBXgEkfBorSvWpkas3dLiKL3kHEuBV` |
| 53 | `S4/both/LF` | 12 | `502f0923cb8ea1982080f0ed3c3146fa` | `17Wu5RPmfYQTDUmVn6seoYS2T9zXUZhcXU` |
| 54 | `S4/both/LF+t` | 12 | `002887dc5492f9e927c677bca4635262` | `1Nwk6ftQiwWLgumtpv42jmZxGfDF5k1Jiw` |
| 55 | `S4/both/CRLF` | 12 | `0bf7cd6a9015203e3f70bdaf7740f032` | `1BAhtw8y5Gd9FCGXmfc9NCPGSwEwEHfh4x` |
| 56 | `S4/both/CRLF+t` | 12 | `8bb531d45ff56bfe372982066fc55635` | `15WpeBTHjKbuEe1exsT53JBj6q3wUzkfXb` |
| 57 | `S4/down/LF` | 12 | `e55f2112c501e306b542d32f441f0d43` | `142oh2GoxPTAKvRcNRE7F7UoZVGhUMWsBu` |
| 58 | `S4/down/LF+t` | 12 | `80003b03c7ccadf594d0d945cda7623e` | `18JxJ7e35VnQygQ491zViZAeM85zsJ15Xt` |
| 59 | `S4/down/CRLF` | 12 | `5e2671fb3d94c706191f1b0531170e95` | `1FWYKmaZNWzk4ijbL9bxeSwjCeudju6Npf` |
| 60 | `S4/down/CRLF+t` | 12 | `e355fa6d0832369b840eaec4ec44f19c` | `1Nrqh5vJ4LkKWBkveZk2R4fTsYmVw2Lv6W` |
| 61 | `S4/up/LF` | 12 | `6faa5f3ff02f26b0aec01deac4f65e48` | `15nF5Edo7njxSKmR2U8251P3QYTANbJCmp` |
| 62 | `S4/up/LF+t` | 12 | `499f550b436116f4876c05733d719e43` | `1P9DAxrfkpSVVfx7Y1dHFcw55iN1muWuFP` |
| 63 | `S4/up/CRLF` | 12 | `8ab971427b6d37ecc184bb518ad6b09c` | `18Q7Rz3PqD8kzU4pfsaJovgXK9wRoNQz21` |
| 64 | `S4/up/CRLF+t` | 12 | `55d29db3b56135783e1dc244f9d7ce7f` | `12Aekuo6a6LvTpApZmaFJ756ps9mdx8EeF` |
| 65 | `S4/both_para/LF` | 12 | `e4ec7577e9a80d66a06196f2c6e1182f` | `17eAJEosbfgS2B4aqK9SvuACja2YvWqRkJ` |
| 66 | `S4/both_para/LF+t` | 12 | `1eaab5fd452aaa60dfc1a20ae41af3ff` | `1PKfFJpT1oJgxfE9kGF6LauHHuppextnum` |
| 67 | `S4/both_para/CRLF` | 12 | `e0ef4e5ad41596a16e82e1c9201b67a6` | `1AhkUFKAz5jr6LGDtvVqeh9epCU8sRtoQ` |
| 68 | `S4/both_para/CRLF+t` | 12 | `f6e1502d0d959b1e8a35d5c79b263744` | `1DKfAdPd7vYBu6mwoErTqZYs1Do9v1aehc` |
| 69 | `S5/both/LF` | 6 | `cefce219da5a32a5b7af4f591ac061a1` | `1JBkEC9hpWjFHosh69gLEyd25dEvfH3Jxx` |
| 70 | `S5/both/LF+t` | 6 | `a4014f95b6123d279cfc3120979860ce` | `1HZkNYXpmivw6tGbHWUvagEoe9Yyvhfjwj` |
| 71 | `S5/both/CRLF` | 6 | `04e3eb314426a15cdcc9ad0866ee2b76` | `1DVkKMGJwMqATkiDeenQVQV77xHUfkzZQV` |
| 72 | `S5/both/CRLF+t` | 6 | `551c53b5667b54c7016083a3a7248242` | `1BLoP2YYNtxaxyuTyAy4a75ZNco1Bnmfsr` |
| 73 | `S5/down/LF` | 6 | `5dd5d5033215ba8a541f5234679c407c` | `1FsYZCtVejHkoW5qKwJZPKjXBWEw3WEe7b` |
| 74 | `S5/down/LF+t` | 6 | `00bf46a312b67b5cd073a15af9cdb06c` | `12mn2gBeAh8WYzWg4ntCQW3HsFMpPsbEZ2` |
| 75 | `S5/down/CRLF` | 6 | `2be9042baaaa2061485e11295f03930f` | `1PHvUBzkedohb99irMuXpjVEn7F5mSjkGC` |
| 76 | `S5/down/CRLF+t` | 6 | `8b05e28f8c974530b64a55cb57c3959b` | `1DZyijm9G8xnmzTjpK6jGv3XF6wd4SPSet` |
| 77 | `S5/up/LF` | 6 | `1a7db6cdb4a1396660dcc481ec7b777e` | `14iaiYbe5HYm2Ewr8NNrwhUXvnuTxREpBF` |
| 78 | `S5/up/LF+t` | 6 | `40911e707214244f12951ac9881f0f1c` | `1MWPy3HMFK9BFsuauqW7QRoUyK86AUNGTC` |
| 79 | `S5/up/CRLF` | 6 | `736d5f6d5f29eab555ae2eb196dfce7b` | `1NRL8kTFXJrWdrsZvSFeMd1CciEjzyh6gB` |
| 80 | `S5/up/CRLF+t` | 6 | `78f1328b34b8f037ea83341ec87fba70` | `18TUV7dky4HVVst9rSfhtVp5EKzoz1xmtt` |
| 81 | `S5/both_para/LF` | 6 | `f85252c354818e5b60be50ddc171829f` | `1KWgRiF4Vcpdudq7ihWBrtoomPhKyJmBRi` |
| 82 | `S5/both_para/LF+t` | 6 | `b41dbdeee50f7143e17c9bab0fcfb261` | `1G8zdW4JPWXkNGwsn9VXjAGCwomWBWvk9C` |
| 83 | `S5/both_para/CRLF` | 6 | `4041b0f4a40f6ecf5a92c112a75ae378` | `1pvSCZhRyNdGKU4TnoVifUSU6im8UcyR7` |
| 84 | `S5/both_para/CRLF+t` | 6 | `6ffadc875a9656f727cef6f5367f3a7c` | `19AFq2gBBRJfz4GUbLjQxDKpM9mje2hr2D` |

Every derivation used all nine indices; the full per-index address map is in
`blueprint_ladder_results.json`. No collisions between derivations: all 84 addresses at index 0 are
distinct.

## One open item closed on the way, which changes what the negative means

`DISCREPANCIES.md` §6 proposed that the author's `true` -> `real` substitution might mean the hashed
text differs from the live chapter. Wattpad's `data-p-id` is `md5(paragraph text)`, so it settles this
directly:

```
para 222 p-id   d6df7b89db018ad9c7c5f23bc395a6b9
md5 as written  d6df7b89db018ad9c7c5f23bc395a6b9   ("true identity")
md5 with real   5d1571a9e11d7704df8fd7555859f44c   (not the p-id)
para 243 p-id   fe288f1504837b3bf0d58185e1d9b059 == md5 of the paragraph as written
```

272 of 273 paragraphs match their p-id directly; the exception is ¶78, Wattpad's dedup hash for the
second `"What?"`. So ¶222 is byte-certified with **`true`**, and `real` exists only inside the
author's own quotation at ¶243, whose p-id also matches its bytes. **The substitution is a
quote-time paraphrase, not a text mutation.** The hashed text almost certainly contains `true`, the
`real` variant was never a live candidate, and that explanation for the negative is now closed rather
than open.

## What the negative excludes, precisely

Not the geometry. The flip rule reproduces the author's stated output exactly, so a failure cannot be
blamed on which edge is raised.

Not the serialization alone. All four forms miss on every set.

What remains, in order:

1. **The unit of selection is the word, not the paragraph.** `GRAMMAR_CONSTRAINTS.md` already observes
   that the demo's answer contains changes that are not at paragraph edges (`messaGe`, `vOIce`), while
   the demo's prose only ever says *"paragraphs where you recognize the signs"*. The text's own unit
   sentence is per-paragraph but its own solution is not. A word-level selection over the sign letters
   is the only lever the blueprint leaves untouched.
2. **The hashed bytes differ somewhere not covered by p-id certification**, which is paragraph text
   only. Separators, trailing spaces and any span the author edited wholesale remain outside it.
3. **The escrow is not derived from the chapter at all**, and the chapter is only the question.

## The next rung, if it is run

Word-level marking, still no sweeping: select occurrences, not paragraphs, and let the three windows
or the twelve "recognize the signs" paragraphs supply the positions. Bounded by construction: the
sign letters at word edges in those paragraphs are a few hundred positions, not millions.

