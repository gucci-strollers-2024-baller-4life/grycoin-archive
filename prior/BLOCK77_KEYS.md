# Block 77 — exact key material (complete and reproducible)

Every row is derived from a byte-exact preimage committed beside this note in `preimages/`.
Pipeline: MD5(preimage) -> 16-byte BIP39 entropy -> BIP39 seed -> m/44'/0'/0'/0/0 -> P2PKH.

| block | preimage file | md5 | address | check |
|---|---|---|---|---|
| R1:77 (genesis answer) | `r1b77.txt` (112 chars) | `684b250ea52c1e33a6f6143ded0e62e6` | `1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP` | **verified** |
| R2:77 stage one (Hal Finney text, 16 paragraphs) | `r2b77_stage1.txt` (5362 chars) | `9dd2efb9bc976c2095bd534d7b8d431c` | `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` | **verified** |
| R2:76 (neighbour, recovered 2026-10-31) | `r2b76.txt` (32 chars) | `f8e5edbcfc77003adb199519f0bee51c` | `13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd` | **verified** |

## R1:77 (genesis answer)

- preimage: `preimages/r1b77.txt` — 112 chars, byte-exact (written with newline="")
- md5: `684b250ea52c1e33a6f6143ded0e62e6`
- BIP39 mnemonic (12 words): `hair float dry engage sea border orange secret digital half obvious smooth`
- BIP39 seed (64 bytes): `e1cca2597a793ba4c539a73b7925215fb9da934cc9e7dde434d9b0448d16f0ed2a75ee44a71a085786acf7777690300a3efa82d15cc3a8bc6dd9735fe6a4c350`
- BIP32 master key: `e6002e4046a5dd02afcaae558732ee6c36ba7f202c5897d15f67d57d29defb05`
- path: `m/44'/0'/0'/0/0`
- private key (hex): `625bc2dd1e14bcfc00a3d34a3ceff5f8661efcb85789d9d48b99de2613479f83`
- WIF (compressed): `KzWuYrzjrYJXdRMA6SukNnuRUkFRycUq8WdfUgfkQ5k1t5quvNGk`
- P2PKH: `1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP`
- hash160: `9b4d49d5f8b33a08ebe2d848ed0e4b05eaa20b92`
- verification: address matches the escrow

## R2:77 stage one (Hal Finney text, 16 paragraphs)

- preimage: `preimages/r2b77_stage1.txt` — 5362 chars, byte-exact (written with newline="")
- md5: `9dd2efb9bc976c2095bd534d7b8d431c`
- BIP39 mnemonic (12 words): `oven number unveil junior item aware finger price estate symbol express degree`
- BIP39 seed (64 bytes): `85827a20b22adbc583fa630ee8e6548e5cf1aa4304cd761d12e18c058fcc4c28568abb22171f30976667b21c3730419a45d5ca97d483ff47297b3bf9bc27dc43`
- BIP32 master key: `14d64f0206795e14e08f281dbaadb3798dd83d6519a3b768fa3a19d31e53d820`
- path: `m/44'/0'/0'/0/0`
- private key (hex): `158682f92916a0c2675cf3449ffdb3b9f9499a57b07ff83d1a6a05f1f76352bb`
- WIF (compressed): `KwwZ4HGvrpDR6mzXP1m5yK18vWsA7MqWDNoSM9ZgKkeWa62tGor2`
- P2PKH: `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`
- hash160: `5cc903a5e5ae5d279893aeeab59d4d292ce68206`
- verification: address matches the escrow

## R2:76 (neighbour, recovered 2026-10-31)

- preimage: `preimages/r2b76.txt` — 32 chars, byte-exact (written with newline="")
- md5: `f8e5edbcfc77003adb199519f0bee51c`
- BIP39 mnemonic (12 words): `wedding control hundred wedding hybrid buddy hockey crawl boring magnet rich decrease`
- BIP39 seed (64 bytes): `db61fa1a3f9deaadbf13f2be5a95cdb77a74e3e7346dd94bf77b172dbf05b9df6fc02f7798d584a1ff71ab82a788bcb98fd71e622f1493bd4a4f6141f8ee92ed`
- BIP32 master key: `6f6cd4be714133a46fb2e344737669aaf660e768c8a8f87adde7604e12aa4950`
- path: `m/44'/0'/0'/0/0`
- private key (hex): `fccc76ec9fb7177fcb3b55cba0eca069e788e2b1ca38654f7464503c1dde64a7`
- WIF (compressed): `L5h7ptMonsAHscBD6HFtWDBNnq6cfe79MaNi7Qx1PK4sz4LshRTL`
- P2PKH: `13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd`
- hash160: `183125ca1acb9e9b741876aeba5585adbcc4d1c9`
- verification: address matches the escrow

## The stage that has no key to reconstruct

**Round-two block 77 stage two** — the Real Big Block, 0.777 BTC at `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`.
It has no published preimage: the author hashed a case-edited copy of the Wattpad chapter `Second` and never
revealed the letters. P2PKH is one-way, so the key is reachable only through the preimage. What is settled:

- the base text is certified byte-for-byte (273 paragraphs, ledger pids; paragraph 78's pid is provably not a
  content hash, so 34/78 is not an edit);
- stage one's published bytes reproduce this pipeline exactly, so the serialisation (paragraphs joined `\n\n`,
  MD5, index 0) is not in doubt;
- every case-rule family derived from her three worked examples is negative: sign sets, the 44 lattice, name
  marking including the block-2 word-edge constraint, surviving capitals, sentence and paragraph edge pairings,
  stride and number selectors, slice boundaries, typography and line-ending channels, and both appendix
  grammars including the recovered b76 key.
