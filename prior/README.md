# Grycoin RBB hunt snapshot (private)

Working tree for the RBB / Grycoin puzzle: demo block (cleczc), the 273-paragraph chapter,
stage-one solution, pipelines and elimination sweeps. Full narrative: `RBB_DOSSIER.md`.

## Verified byte conventions (do not re-derive)

| Object | Convention | Hash |
|---|---|---|
| Demo question base (`demo_base.txt`, 10 paras) | paragraphs stripped, joined with a blank LF line (`\n\n`), no trailing newline | MD5 `7759227d7406...` (author-confirmed) |
| Same text, `\r\n\r\n` join | NOT the author's form | `e9970079...` |
| Same text, single `\r\n` join | NOT the author's form | `fc3c7a66...` |
| Same text, single `\n` join | NOT the author's form | `7d6f7387...` |
| Chapter base (`wp_paras.json`, 273 paras) | byte-certified by Wattpad `data-p-id` = MD5(paragraph text); 272/273 match | - |

Stage-one solution: Hal Finney "Bitcoin and me" (bitcointalk topic 155054), 16 paras,
flips = paras 2,3,4,6 first-letters F,F,W,W down + paragraph-lasts s,t,n,m up (STNM);
that MD5 derives the certified stage-one escrow.

Pipeline: solution text -> MD5 -> BIP39 12 words (empty passphrase) -> m/44'/0'/0'/0/i -> P2PKH.

## The "What?" anchor (verified 2026-10-28)

- Paragraphs **34** and **78** (1-indexed) are byte-identical: `"What?"`
- That is the **only** exactly repeated paragraph string in all 273.
- 0-indexed these are 33 and 77; index delta is 44 (43 paragraphs between them).
- Stable across all three line-ending variants (`chapter_single.txt`, `chapter_lf.txt`,
  `chapter_crlf.txt`): 273 non-empty paragraphs, identical sequence, anchor immovable.
- Provenance: para 34 matches its Wattpad pid (`184826be` = MD5 of `"What?"`).
  Para 78's pid `8b71bade...` is Wattpad's **dedup hash** for the second occurrence:
  md5('"What?"') = 184826be..., and md5("184826be..."+"1") = 8b71bade... exactly. So the
  duplicate is original text, not an edit; all 273 paragraphs certify (272 direct + 1 dedup).
- Caveat: 13 paragraphs carry trailing spaces (86, 108, 122, 128, 139, 147, 165, 166, 192,
  201, 209, 220, 267) and must keep them.

## Open threads

- Demo: remaining hypothesis is 5+ flips at word-internal positions (stated-pair-anchored k=4).
- Chapter: 4-before/4-after rule around hint para 222 (paras 218-221, 223-226).
- Anchor use: 44 as stride/modulus, or (34,78) as a coordinate pair.
