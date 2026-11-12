# Container probe: 63 division spans, 756 derivations, zero hits

**Date:** 2026-10-31
**Scripts:** `container_probe.py` (ledger `container_probe_results.json`), single-break probe inline
(`singlebreak_probe_results.json`)
**Target:** `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` (live). Old refunded escrow and drained demo escrow
also checked on every candidate.

## What was tested

The container question: is the hashed object a division of the document rather than all 273 paragraphs?

Section boundaries come from `STRUCTURE_MAP.md`; the exact heading paragraphs come from the live part,
where each heading is the only paragraph whose content is wrapped in `<b>` (28 of them). Every
heading-to-heading span is a container, under two boundary conventions:

- `body` heading+1 .. next_heading-1  (what a human copying the section copies)
- `head` heading .. next_heading-1  (the document's own serialization, heading included)

Plus part-level and composite spans that heading-to-heading cannot express (`PART-I/II/III`, their
bodies, `III-2/Satoshi-Code`, `III-2d/Outing`, and `WHOLE/no-title`, which drops the `<b>Second</b>`
title paragraph).

**63 containers**, three marking rules (`plain`, `geom` = the validated paragraph-initial down plus
first-sentence-final up on recognized signs inside the container, `win` = the STNM terminal words
raised), four serializations (`\n\n` and `\r\n\r\n`, each with and without trailing separator),
nine indices each.

**756 derivations, 485 distinct byte strings, 0 hits.** The 271 collapse cases are small containers
where a marking rule has nothing to mark and reproduces `plain`.

New ground relative to the repo's earlier `fresh_sweep.py` (22 segment definitions x paragraph-final
flips x 3 joins x 4 indices): the sub-subsections 2a-2d and 3a-3f, the `body`/`head` convention, the
trailing-separator variants, indices 5/6/7/44/76/77, and both marking rules applied inside containers.

## The container answer, plain rule, `\n\n` join

| container | paras | md5 | addr @0 |
|---|---|---|---|
| `WHOLE` | 1-273 | `48d318202691ffb873e00b63196eaf36` | `14isnRimk9qAzpm85qwiFgLjzxL1387TXL` |
| `head/1/Second` | 1-1 | `c22cf8376b1893dcfcef0649fe1a7d87` | `1FkVuq38ZWu6YXs62H4WH8vhCqaLGQD7L2` |
| `head/2/I-Second-Life` | 2-2 | `78fb210102221169f1559fc51d6088e2` | `1DqKkFDnGNXgvPPSqwEs6xsSjgyKQvHczd` |
| `body/3/1-Second-Coming` | 4-53 | `e41f3e97213af51ec06d6ed29d305d16` | `1DYGgPWz4yXoTfmgyYXwejkuhcj6HDVB5n` |
| `head/3/1-Second-Coming` | 3-53 | `3ee139e4300f8d5f96fbc64ddbb3796d` | `1PA83soP64gy9gyeyDa6bqXn9buxPSaY5B` |
| `body/54/2-Running` | 55-70 | `74b56f23b547a6f8c226e5c9d6551a6b` | `16dP5aEsgEg8ofwrsXLo7ftLWeasMqQdhE` |
| `head/54/2-Running` | 54-70 | `dae2a68eaddbb2750231ff254e2e9362` | `1Uo7r5AfEa2Cfn4Ysg7mv8GdYc6YDard2` |
| `body/71/3-Reverse-Turing-Test` | 72-87 | `a270340e5c73cd2882287ed36a9f817f` | `1N1JDqHXs4NwpGzdx2ka9x7TMVDA3g12jS` |
| `head/71/3-Reverse-Turing-Test` | 71-87 | `da2554fb31f4fe30ae822d6f45041507` | `16bBfDtBZqVM7sKP79CVaneVmgoxoNcUYM` |
| `head/88/II-Second-Layer-Grycoin-A-Peer-to-` | 88-88 | `3afbf003f96b1a205f9d76a174e44bbc` | `1GqLEqyFixszrDSB4vBBteoE1onVxFfAkP` |
| `body/89/Abstract` | 90-90 | `136ae34c6b09fe71d84d3876e5e82915` | `1Amhz15DV2PzP86ikhaYfjcbNBukv5NAGo` |
| `head/89/Abstract` | 89-90 | `da8f27e0d811d9ae66848ca589e07698` | `151WCNAc6kd73JoZcVCaSDXvn7QSD8kgt8` |
| `body/91/1-Purpose-of-Grycoin` | 92-114 | `7047bf2058e6d420ad89289d15d7086a` | `1EQSG3uxkQnSwpU9zdPc1zSYt2dLiis54b` |
| `head/91/1-Purpose-of-Grycoin` | 91-114 | `59c89752a6f0d0bd86827b21f026cdd3` | `1C5Fsj3qhPEKMxrogdq5X7xEMATuvDHQ5c` |
| `body/115/2-Bitcoin-With-Two-Changes` | 116-129 | `7c2fe010a330f8095fa3a0d3cfb250e3` | `1GptgCtvsycgj8JrqamvDcPftjokfyBynw` |
| `head/115/2-Bitcoin-With-Two-Changes` | 115-129 | `996f8160f0d745c35eb89587cf543ed2` | `1Dz4eQsW553gnf1y2wGUXQRPJBt326pddE` |
| `body/130/3-Incentives` | 131-151 | `86835c9f3849231c71d1eaa5ba44c8cb` | `18qV4qfKZ36hNYwAJdBLpQpU7oiEyHDbnF` |
| `head/130/3-Incentives` | 130-151 | `158f51b4c82c157037846c49cccc52dc` | `1A3zE4kq1TM3A42ETjuBVq14MW5xmn6Nm7` |
| `body/152/4-Why-Blockchain` | 153-156 | `566b2c032ab5a9068a9e1e00d7c78156` | `1Vbakis6ctxkVoaDqzE43vTYadZfL48gY` |
| `head/152/4-Why-Blockchain` | 152-156 | `5795c42fae60ae00696864944a8363c3` | `16yuj7oyQLLpej7Pux2DxAw2WjPDYAnRVB` |
| `body/157/5-What-Grycoin-can-do-for-Bitcoin` | 158-160 | `f03a59cbcfd3cc0356a14ad7c108b19c` | `1KpAEL67iAuiHEgN6AzeC1DALhoqN4Z3LW` |
| `head/157/5-What-Grycoin-can-do-for-Bitcoin` | 157-160 | `d276929cc1f9c02952257e8edb86749c` | `1BnxJhru7Acd3gh3r6CzCth9qCVswNPxEY` |
| `body/161/6-Conclusion` | 162-162 | `3aa1eeeec4bf91cee5db0f852119cd4e` | `1GfZ57PCMRbNkLZkykdGjwpD2XfzJsnayg` |
| `head/161/6-Conclusion` | 161-162 | `90b762e4bb21e136a30ae666838cbf7b` | `1BMAyizTVv1SMo95BRKs2UL8GaNJX89dbT` |
| `head/163/III-Second-Identity` | 163-163 | `2fcd152de29c5509cf9ab39345cd309d` | `13JBD7deKDFgQsPBairT1EuKHisbAT94TJ` |
| `body/164/1-My-Identity` | 165-174 | `d17dd282bdcbb0f099af8bcc9976bec6` | `1NyzydS8uPcKEYW65674zUUpfzP1WTyD99` |
| `head/164/1-My-Identity` | 164-174 | `9b56aeea9fe973c5e9d46adec81871b6` | `14W8DskcQ5KJsELKfsRZYhcZpkFbT7zEyY` |
| `head/175/2-The-Satoshi-Code` | 175-175 | `3064087408d4dee3b0dfb6f14511b5bc` | `1CpwEDfFrsEUNHWgA1GBykDtKWRZQ1sNwb` |
| `body/176/a-Satoshi-s-birthday` | 177-181 | `25f20e572d692214d734445274d00e7a` | `1qtJ4qnmEwffXpANAhE3uNaHHu2Drspc1` |
| `head/176/a-Satoshi-s-birthday` | 176-181 | `54ecb67b61da8e8d1f5f59f10e842533` | `1McuVNU8Edpf8BttZRJ3JQqjWxNNTP5HXn` |
| `body/182/b-THOMAS-and-Satoshi` | 183-208 | `d2fc38689f6a5499bd695d933b69513d` | `1JpHpbFF7UhJdLYj5QCmGKpzvLsz4YcUtC` |
| `head/182/b-THOMAS-and-Satoshi` | 182-208 | `cdbff9dc7422d6b940c893650a21fc0f` | `12rR837tocWC8f9bnNRLmEbvGJk43a94sX` |
| `body/209/c-BITcoin-is-actually-AHScoin` | 210-214 | `0936e89378654977f727c052bc4c3d69` | `16G6bFgvkgVbnz7PPRre1V7nW9apWXHPJc` |
| `head/209/c-BITcoin-is-actually-AHScoin` | 209-214 | `bc19fe73d9b444e375f523c8f7b86da1` | `1CJxgKaRrWdmiaGXagEBTZU7sZ7Lfkudmb` |
| `body/215/d-Outing-himself-as-Satoshi-on-Bit` | 216-246 | `550618b635e3e078a83c62adec0abb47` | `1Ke8KCds3RTbAbtstLTRghUwd124KXG2dd` |
| `head/215/d-Outing-himself-as-Satoshi-on-Bit` | 215-246 | `b4ef200c3bfa45db787717066e6a5af0` | `18pF7G37ks5WFzmeVqKPPX9kYHEGk75fYp` |
| `body/247/3-Other-evidence` | 248-249 | `ab20fd057392c9ee6989ff5de7f47966` | `14PwKiJbgmDeh1BCopvfyd9xGYw35LxvLa` |
| `head/247/3-Other-evidence` | 247-249 | `f70f79d6dadd3ff4405c54586ba26a15` | `1325tGrEzAapqYnrCofJrNRmX7u9YwVAUV` |
| `body/250/a-ALS-Condition` | 251-251 | `c9e9e65e736c9e36cb5cfe44785bdad1` | `19d3GTtEQwFeW8GtfXSkmS6gGnrj4DeQWb` |
| `head/250/a-ALS-Condition` | 250-251 | `4ad03afbdadd74272ebb5bb345d4a3fd` | `19JWfn2pQbn8sr1EzkyEiFVkXbWZUjTnic` |
| `body/252/b-Previous-Experience` | 253-253 | `cb7c94638497d9e55318b3bd51f14e7e` | `18bPvPMR2JrJGhyrWKP61KUKUcNsv99eY1` |
| `head/252/b-Previous-Experience` | 252-253 | `938ae3ed48e5478a373ea205ef88d1e5` | `1EVXmR7hKUsVFVV1Qqx6fWhb2STKypBSXU` |
| `body/254/c-Mail-Conversation-With-Himself` | 255-255 | `63d202b15c4c39cece8c4a17dba464d8` | `16TA4uhFc8QuFeB7XJ854WQ8AV8C8gGNWQ` |
| `head/254/c-Mail-Conversation-With-Himself` | 254-255 | `946cd2847a5a237d31a49fc00e7a3b37` | `17rbnAH9DbYZJkKw4o15MZqcJ2BUsWgsmi` |
| `body/256/d-Not-Citing-RPOW-in-the-Whitepape` | 257-257 | `162b08f57287bc176d407346142ed60c` | `1LLk46MD5zZCxs1MX7kKgcHxx7iR2hrCbK` |
| `head/256/d-Not-Citing-RPOW-in-the-Whitepape` | 256-257 | `529dab579322f663d69bcfe100a24aa4` | `18aVoFDp77tJHru9UCfwFvAGq3NNrYkJvs` |
| `body/258/e-Coding-Style` | 259-259 | `da020ca3b5d70015b1152663a9f9f07a` | `1MiA9BZWNxyJJYBmtKGx3sfCUCz788dXQG` |
| `head/258/e-Coding-Style` | 258-259 | `013bf4ce6bbd5ec8a1e31f672afcd91a` | `1FATTq4AxUeLQK9wLSmXCDKHehdwxTg3h2` |
| `body/260/f-Overheating-Computer` | 261-264 | `59a618907b3aaa61876a7d2f12a5d105` | `12pEKR1uDwE1ugSnEqwEft7GAoQPHgCUxd` |
| `head/260/f-Overheating-Computer` | 260-264 | `bc42ccc88dd3c1e9edebf1d051bba8e2` | `1JqhoDkN2HWzTkdTW5VTw45eRzXXZG4BzT` |
| `body/265/4-What-Does-it-Mean` | 266-273 | `5e963d92c637ec0d03c425e766e6cc6a` | `17qYtUfZ1SKGC8nGZmwAo8HrtcfPGYZCs5` |
| `head/265/4-What-Does-it-Mean` | 265-273 | `64ed056bb0009a2cb9a2ab630f71e19d` | `172RijmynJYTMsH4Z2E1XRhvHw73PR9yE4` |
| `PART-I` | 2-87 | `4496de9cf236047874ab31a92a924fa4` | `1M718gRxZNNTDVxSZoa4ACVmnothPxjDa7` |
| `PART-I/body` | 3-87 | `1832d2b440b555b087d7004c8d148516` | `19JCx4oHLrCJq9LkomThQEkgNmUazeLB5T` |
| `PART-II` | 88-162 | `dc202558f5cca6107df1484ddbb1feda` | `1DmVZtcbHcyd4D1NepHcUqw18kjeHMn2Rq` |
| `PART-II/body` | 89-162 | `1ef6389c6e031fb1d32299949ddb6a77` | `1A6ThJPpxMhiEuU18XnKNCrCSgaFLNXNCC` |
| `PART-III` | 163-273 | `ca6194546a73141698589d1557784d55` | `13CQHyZySh2nqVhAzqonpkwrd9wm6kv914` |
| `PART-III/body` | 164-273 | `dcf4005ebbfeab71ba3d71a8811ab1e7` | `1CM8dphUTGZiJNwGzZoVeiapWnrqzoQtwh` |
| `III-2/Satoshi-Code` | 175-246 | `6be0fcd27ba850110f32e75ba57cb461` | `1DKgzXNnnmdiJ6fFrvwmQ1Q58RVKn9Brvo` |
| `III-2/Satoshi-Code/body` | 176-246 | `0267708ec7cf53c4fc96572c61ba2eb4` | `17QstRfsfqeDYzYdzgZ5oJJKfYkF8VcxmK` |
| `III-2d/Outing` | 215-246 | `b4ef200c3bfa45db787717066e6a5af0` | `18pF7G37ks5WFzmeVqKPPX9kYHEGk75fYp` |
| `III-2d/Outing/body` | 216-246 | `550618b635e3e078a83c62adec0abb47` | `1Ke8KCds3RTbAbtstLTRghUwd124KXG2dd` |
| `WHOLE/no-title` | 2-273 | `e64623ea6ed214bbe9eb9aa57140776a` | `19sirtfu7EtbtVZ8NRp688xubxwpfkPAvF` |

Full matrix (marking variants, `\r\n\r\n`, trailing separators, all nine indices) is in
`container_probe_results.json`.

## The single-break question, which the author's own sentence raises

Her 2019-07-30 update reads *"It is also hashed with two line breaks between paragraphs now."* The
word `also` and the word `now` together state that a **single**-break form preceded it. That reading is
not in `SERIALIZATION.md`, which treats single breaks as "not the author's form". It is worth four
serializations, so it was run on the seven containers that matter:

| container | rule | serialization | md5 | addr @0 |
|---|---|---|---|---|
| `WHOLE` | plain | LF1 | `6a9d61b74cffbaef1bfa36cd73157472` | `1JQ4JdSYrnGASSwHruiaguhvPPuY3qj179` |
| `WHOLE` | geom | LF1 | `bf4e4c1844c1010b44bf6310b5b89d42` | `13W8MDK5PiKrhVr46z9hTYWEQeAEyvAvNP` |
| `WHOLE` | plain | LF1+t | `c7b316928948671e255a58ec7fbe3541` | `1E7TKUQoQvxH1YAVdXSqmvz6dZR1qupkKc` |
| `WHOLE` | geom | LF1+t | `3bc1e6a2823559094bef9564b7238500` | `1Brfip351WxHiPpDMmJ3Yt5SataRFg6HrU` |
| `WHOLE` | plain | CRLF1 | `892f502b083423612cbcc746d4667ac4` | `18AkiLrqea8ntvAjQK6HjZaBiQEg2MEYeh` |
| `WHOLE` | geom | CRLF1 | `3493c3bb5d306e81d1a8d869c6b26832` | `1Q7j6iVA6bXyMRLtarpsReLNVtpRtxitKP` |
| `WHOLE` | plain | CRLF1+t | `c96187e54ecd5a139bc1438700bd456d` | `1NpT5EaCeHxi6xGtUe8gZrBNWd4QDc59UE` |
| `WHOLE` | geom | CRLF1+t | `f53973b6382df73e0d3ad1ef347563e4` | `137Lf1Nn3ohmetyVySHEnKAMAPfnKZpyC5` |
| `WHOLE/no-title` | plain | LF1 | `4a9634fe58f1d7f7703807ec5c95a3fe` | `12FAKqrgDmN11LxYGyVhyeZZDUTep6yANu` |
| `WHOLE/no-title` | geom | LF1 | `6f0e0a4d52015686d9f16a7b8ddb8656` | `1Bnut8jg31v2mGBgJbBXvcruVP5LpsNSpJ` |
| `WHOLE/no-title` | plain | LF1+t | `6193c56793cbdd8d43793dce17a268d6` | `1GmCz7KZGuzKF4D1CGu6VXsNPCHwL6X6Jq` |
| `WHOLE/no-title` | geom | LF1+t | `faaa2cb328c60ba51b03a8a37d1c9afc` | `16hxuvzTpS8zz97kx6oaezFiBgZuPcQkRB` |
| `WHOLE/no-title` | plain | CRLF1 | `cfca998d21262dc790da551a4392875e` | `1EwBiBqqZbNgpkQZp4SoBf6KjcXovsx28Q` |
| `WHOLE/no-title` | geom | CRLF1 | `a0d4630d8838577873546eb11d8864b8` | `14LnUNm4pudgbLKdKhYH9rp9ckn5CpvtmP` |
| `WHOLE/no-title` | plain | CRLF1+t | `fd48deabd4e318419d305c99550f2029` | `1MsAZAKUJ76rdrt2qSoNRpXBurTWn28mNd` |
| `WHOLE/no-title` | geom | CRLF1+t | `93d1e22523356ca13664b122694c826c` | `14R3cFQDsfrUDt3gLbK9CjbCEVHnMeK5eZ` |
| `PART-III/body` | plain | LF1 | `9ece40eb2bbeb1b6727a4b7f080ebc86` | `16WEiEKXbKLrrZu8CYRBmq2twcLzWRxu9S` |
| `PART-III/body` | geom | LF1 | `fb7127475a50389c17746cc818dc0866` | `1K8pje64b6vycKjYh9RhppU2AXG4QcxfSV` |
| `PART-III/body` | plain | LF1+t | `af8939bc0210f8d31305948bc52d42b9` | `18ca1MFh4qKA68TY28dHPdzbUYUMAz4zHw` |
| `PART-III/body` | geom | LF1+t | `d9b4a7a9ce210b60f9768f0b9a5a1ddc` | `1A93pkA73SE9tMWUQ1c6e62SpEM1p8Vot9` |
| `PART-III/body` | plain | CRLF1 | `7f41e0530ed099f8787f98e3456a148b` | `1CC4yP1AuDqCZ2pvZnpE1HHchus5k8ARdk` |
| `PART-III/body` | geom | CRLF1 | `0e8e193b1ef16871cda2dba8062594da` | `1QsCs67DRBmSRxDEF5Pqkd4Nh1ExPbNAp` |
| `PART-III/body` | plain | CRLF1+t | `b94b1c4cd59299d3778d399b7f98f8ee` | `16oCYmqCANAmP8U7F8jZ4KGGZuwgR18mjJ` |
| `PART-III/body` | geom | CRLF1+t | `bc3ef6f3bb49e426c29e8cbb14d507d3` | `15h1mHwLsK2BZgTKJ8n6fTSYs3rciERMon` |
| `III-2/body` | plain | LF1 | `bd9c7dc26eae7620514cec99e9a3615b` | `14kdWFXXhNLi595FTDmJVtcVVNZhavpwWt` |
| `III-2/body` | geom | LF1 | `70260c1baef39e39fc07dd8432d45e16` | `1FM4RJ1EKeAyagJebcdhSrB9tjts16ktEm` |
| `III-2/body` | plain | LF1+t | `725fe72ce6952b3d836fa21346bb6f85` | `13fQqMuUzJgL5GDzLxdwULvjStGNxcTvxi` |
| `III-2/body` | geom | LF1+t | `ccb1213ff2fcd5db4375cb17d43c93f0` | `1FAspzdBtWC1dxK4bJMTC9oS2VWKXVCAon` |
| `III-2/body` | plain | CRLF1 | `13409b63867ad2ae6c5a5175f85d68a0` | `1NU6QBi6Nwsoyyf4EzovznGV5gUkM27Hkh` |
| `III-2/body` | geom | CRLF1 | `fd13ebb10d88f997a1e4f2303445f6da` | `1MUhFbvqhk1N22CeaHDrG7hPLoJKZeWffo` |
| `III-2/body` | plain | CRLF1+t | `dccc77cfab1e35c331f110770ebe9c25` | `13FeY6L7hgfvxtir13ZhEFYR1kkVpkTaqd` |
| `III-2/body` | geom | CRLF1+t | `0e9e241c0326fe0e280920455dbfbb12` | `1K4ChDWaBdWLzHtBpADaFkVMy1ZD6Gmgr6` |
| `III-2d/Outing` | plain | LF1 | `c64f6ee3f02d7f427eeb8a13866429a3` | `1PdnzPGhiGcTPqVWduMbU2QSGGuMDXfbin` |
| `III-2d/Outing` | geom | LF1 | `b5e39f6114f1f2cafd3d26b1acf2cd18` | `1EMZtqHrQaBjJG7mwrZr2yxDqYaRFJyoNc` |
| `III-2d/Outing` | plain | LF1+t | `324da63d59ded9f04f758c7b1717d05c` | `12ErCTBRiu52oJgt3LEAN51uMAwB7ytpa2` |
| `III-2d/Outing` | geom | LF1+t | `fc7c3e20a7d53ff307093a4510da135a` | `18Nvwy54rNGPtXr9jcWQob2W4FV1ANaSar` |
| `III-2d/Outing` | plain | CRLF1 | `6c45d5b74ddace8032c5f569fb774197` | `17zReUKpojDtEMivUEN4XqkwPrFBg8EB8X` |
| `III-2d/Outing` | geom | CRLF1 | `d5cadce86cbb107be8256da8ca6dae01` | `1LqYTWXtYuKjqPg1jGMjGyj5EQkYRdivzf` |
| `III-2d/Outing` | plain | CRLF1+t | `76e8e58874c6a0c2d47db075e3726f3d` | `1GEsXFmU87rVTyDzAWi2sxY7B1UoFhHgZi` |
| `III-2d/Outing` | geom | CRLF1+t | `851a7096d8e17f8acc90e9c939ceef30` | `1PHNKSWVaXWB875WaawuCXGqrGs1KHxncd` |
| `III-2d/Outing/body` | plain | LF1 | `fd8db86ae5f62ec298f7c5823ea5d483` | `18zQrWECfgN911wRyLsN4u8H4RCcLfKxu` |
| `III-2d/Outing/body` | geom | LF1 | `e80ba611b4a81d067b6d88b296fd5404` | `1Bcz1MTWd8QUFr29oSbY91Jpf26Xc4FeDB` |
| `III-2d/Outing/body` | plain | LF1+t | `60e1a236cfce2d0c9bb4e2db5a47c5d3` | `1A6toPX6xud129btnxetHVo17shfxBjDyH` |
| `III-2d/Outing/body` | geom | LF1+t | `f976a26cecfa57144af1a482d33d0419` | `1BGuuKrLjradBF5rFpL5VQWf83se1QEh2Y` |
| `III-2d/Outing/body` | plain | CRLF1 | `5a39939222a9670a7b0a18ffecb8885a` | `1NHiKDbhQaPBfgX6qbrRi4KJSeqCWattpT` |
| `III-2d/Outing/body` | geom | CRLF1 | `f144ef04da3fe3d70d6d065a48318981` | `1KpF77to4Ki6GHfcpvu9NZxVTGZuQnU7eS` |
| `III-2d/Outing/body` | plain | CRLF1+t | `749c3444b5d034803c3dee885b9b1490` | `1Dc7Qx7Qoo9c85dEbppKn3vMkdxv6N9yLz` |
| `III-2d/Outing/body` | geom | CRLF1+t | `f8a2efe67efa96568c431fee7500ee43` | `12JsAFziS7RwJ3sKjCY5L2HGw7HDgjRNoB` |
| `RULEBOOK` | plain | LF1 | `4e78766e3cac8a48780c9f0e5e1c7167` | `12nAyJ8GNVmkinZPnPTXKeWC7huAdQJzqX` |
| `RULEBOOK` | geom | LF1 | `edfd3699cda5b094ded86289d84e183b` | `13whX7nwSNNdJGJtXiQ4Wiie8f8T1YjrBS` |
| `RULEBOOK` | plain | LF1+t | `0d81269f03a2e990145e6fd513cae7fc` | `1QB8Hfzf2yS4JyGWv6ihKuwkeU7ommWyFb` |
| `RULEBOOK` | geom | LF1+t | `a8f984a2a86bd870e5d62117efed13e2` | `1CTt5FivnydHXxj9VzeL8z1wxfCDu4afmM` |
| `RULEBOOK` | plain | CRLF1 | `440f07664eed8adfe6849e7c26852a3c` | `1NjjrC8DHE4iogXccTMusJr21fTALiJcbt` |
| `RULEBOOK` | geom | CRLF1 | `74edd741f2a771df2df3764eb7cdccbb` | `1CX57d5VVWgUCfcj1v5787d7rzWJUyVvPn` |
| `RULEBOOK` | plain | CRLF1+t | `666ec06f80a600a3460bb17fc9248c01` | `15Kmv9r7UvLjuczwsJwFxg6EcTAvhsFofT` |
| `RULEBOOK` | geom | CRLF1+t | `6f699f20f266ea4aff4c375b1a6bf8c8` | `1L3hUK6VWR8muRxRXQ9c67B2P8ZiK3GEqR` |

**56 derivations, 0 hits.**

## Polarity check: the published chapter is not the already-marked version

If the chapter were published in its *marked* state, the answer would be the unmarked text, and the
marks would be visible as case anomalies. Scanned both ways:

- Paragraphs whose first alphabetic character is lowercase: **10**, and all ten are the lettered
  subheadings `a)` through `f)` at 176, 182, 209, 215, 250, 252, 254, 256, 258, 260. Typography, not
  marks.
- All-caps tokens: 22 distinct, every one accounted for by an acronym the prose defines (`PGP`, `OPEC`,
  `IBM`, `RPOW`, `CPU`, `PETM`, `UTXO`, `GRY`, `ALS`), a heading numeral (`II`, `III`), the author's own
  marker lines (`STNM`, `FF`, `WW`, `UUUU` at 237-241), or the anagram wordplay the text explains
  (`THOMAS`, `BIT`, `AH`, `TOM`, `HAL`). One emphasis `NOT` twice.

So there is no hidden set of pre-applied flips to reverse. The chapter is plain text.

## Verdict

The container hypothesis is dead in the structural sense. Every division the document names, under
both boundary conventions, in four serializations and nine indices, with and without the two marking
rules, is negative. Section isolation does not rescue the derivation.

## Running total for the day

| rung | derivations | hits |
|---|---|---|
| paragraph-level (5 selection sets x 4 modes x 4 serializations) | 84 | 0 |
| word-level (7 rules x 4 serializations) | 36 | 0 |
| intra-paragraph break layer (4 renderings x serializations) | 17 | 0 |
| containers (63 spans x 3 rules x 4 serializations) | 756 | 0 |
| single-break serialization (7 containers) | 56 | 0 |
| **total** | **949** | **0** |

Three independently validated marker implementations, a pipeline certified on three vectors, and the
author's own worked example reproduced character for character. Every structurally named object in the
document has now been tried with the rule the document states.

## What is left, stated plainly

The remaining possibilities are not more spans or more rules:

1. **The escrow is not derived from this text.** The chapter is introduced in her own post as
   *"Question: Final version of the second chapter of Wattpad story"*. A question is not necessarily
   the preimage, and the RBB has stood unclaimed since 2019 while both other escrows were drained, which
   is consistent with an object that is not reachable from the obvious text at all.
2. **The rule the chapter states is the rule for the PREVIOUS block.** Paragraphs 228-246 explain the
   Hal Finney post, in the section that reprints it. Reading them as instructions for this chapter may
   be the category error behind 949 negatives: the document teaches stage one and does not state its
   own marking rule anywhere. If that is right, the chapter's marks have to be inferred from her other
   blocks' documented rules (`WORDPLAY_RULES_CATALOG.md` R1/R3), not from this text.
3. **A byte layer that is neither paragraph text nor separators.** Trailing spaces (13 paragraphs carry
   them), the `<br>` renderings (probed), and any span she edited wholesale.

Of these, (2) is the one this session changed the evidence for, and it is the one I would take next.
