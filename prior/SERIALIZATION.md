# RBB base-text serialization (canonical, verified 2026-10-31)

Source: `https://www.wattpad.com/apiv2/storytext?id=720888559` (chapter "Second", part 720888559,
groupId 184148284). 273 `<p data-p-id>` paragraphs. Ten of them contain an internal `<br>`:
paragraphs 63, 73, 121, 124, 146, 160, 184, 189, 193, 213.

`wp_paras_br.json` stores each paragraph as a SEGMENT LIST split on those breaks.
`build_base.py` emits the three variants; all three regenerate byte-identically:

| file | paragraph join | internal break | trailing | chars | md5 | idx0 address |
|---|---|---|---|---|---|---|
| base_chapter_lf.txt    | `\n\n`     | `\n`   | none | 45,450 | 46a308c279540a33e977ea1f660e8458 | 1DGrEwbRwANU28BgCnp6HeNhPzB2HbiyUL |
| base_chapter_crlf.txt  | `\r\n\r\n` | `\r\n` | none | 46,004 | db11a7fdba7b4867a24445a7a30709b8 | 1Ph7YoXiFDJtX7nRRArjmYoNhFv2NjYmjC |
| base_chapter_mixed.txt | `\r\n\r\n` | `\n`   | none | 45,994 | bd07e6ee209c5ab65d874bbbcfccda18 | 1BGh8btgbCSPDfjyESjnkjYyYvoB7xnDDb |

Certification of the segment model: 44,896 chars + 10 breaks + 2x272 separators + 1 trailing newline
= 45,451 = Wattpad's own stored `length`. The built files omit the trailing newline; trailing
{"", LF, CRLF} was tested as a 72-candidate family set (zero hits).

## Coverage ledger (so nothing is re-run blind)
- LF base: full 2^16 window closure, mode first-down+last-up - zero hits.
- mixed base (bd07e6ee): spans 9,867; signs-subset 32,766; window-subset 131,071; complete 2^20
  mechanism closure 1,048,575. Indices 0/1/5/6/7/76. Total 1,238,662 - zero hits (`harness/fast.py`,
  coincurve, self-tested on stage one 9dd2efb9 -> 19TbyN5K).
- all-CRLF base (db11a7fd): only the 72-candidate family set previously. 2^17 window closure x 2
  indices x 3 modes launched 2026-10-31 (see sweep_bfull.log).

## Certified answer format for the sibling block (proof the conventions are right)
`1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN TOMI Omit TOMI L4VdZUDY2BXa7VVkjuYkmaLvi8P5qNZaARwwB9wjqkDa6Sn4JLV4`
md5 684b250ea52c1e33a6f6143ded0e62e6 -> BIP39 -> m/44'/0'/0'/0/0 -> 1FAAKpzFc2CGU6Yt51kAZv5f6dXZckRsMP
(on-chain: funded 7,700,000 sats, spent 2019). Conventions proven by it: eight items, literal
`TOMI Omit TOMI` (capital O), single spaces, no leading/trailing whitespace, full-key link, index 0.

## Correction (2026-11-11): the certified demo hash is the LF join

`7759227d7406d8230d7e3a8f7b9846d7` is the ten paragraphs of `demo_base.txt` joined with
`\n\n` (1,549 characters). Joined with `\r\n\r\n` they are 1,567 characters and hash to
`e997007971f6f17c8775d83f30edb4c6`. The author's "13 10 13 10" sentence describes how Reddit
stores the post, not his hash input. The LF base is the certified one.

Also closed: the full 2^16 window-subset closure on the **45,451-character** trailing-newline
substrate, which every earlier closure had missed (they all ran on 45,450). Zero hits.
