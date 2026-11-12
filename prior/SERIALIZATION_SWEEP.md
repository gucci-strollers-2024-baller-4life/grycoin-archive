# Serialisation and format-field sweep, 2026-10-29 late

Every candidate below is hashed, converted through BIP39 to m/44'/0'/0'/0/{0..3} and compared with
the live prize address `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`. Nothing matched.

## 1. Byte-state / serialisation forms (19) - the "subtle hashing mistake" angle

| form | bytes | MD5 |
|---|---|---|
| raw `chapter_single.txt` | 45,161 | 057787061e |
| raw `chapter_lf.txt` | 45,433 | df281d0c1f |
| raw `chapter_crlf.txt` | 45,977 | 3be071d7c5 |
| `<p data-p-id="...">text</p>` joined by newline | 59,370 | eaf4260b85 |
| same, concatenated without newline | 59,098 | bcef12c2c7 |
| `<p>text</p>` newline / concatenated | 47,085 / 46,813 | 7b807943b2 / 29923b5dd8 |
| `<br><br>` and `<br/><br/>` separators | 47,078 / 47,622 | 453457dd05 / 1a99451907 |
| pid + tab + text; pid + space + text; pid newline text | 54,183 | 56065705a9 / d1043ee855 / 967e1425d8 |
| text only, newline joined | 45,174 | 6a9d61b74c |
| HTML-escaped (`&quot;`), escaped inside tags | 46,614 / 48,525 | 5e512a7d91 / 2f57781ac7 |
| typographic quotes | 45,658 | 392f015927 |
| UTF-8 BOM prefix | 45,177 | 8bdce9293b |
| headings dropped (paras 4-273) | 45,135 | 4302be9991 |
| trailing newline added | 45,175 | c7b3169289 |

## 2. Appended answer fields - the `[solution] TOMI omit TOMI [link]` format

Bases: chapter in five flip states (plain, all-edge-flipped, not-FFWW, FFWW-only, the three windows)
and the demo text in both states. Fields appended after a space or nothing: the prize address, the
demo escrow, both funding transactions (`f11eca99...`, `ccf5ad64...`), `TOMI`, `STNM`, `HAL`,
`Satoshi`, `signs`, `777`, `Grycoin`, `Aoi`, `Aoi Nakamoto`, `Thomas`, `himself`, `himselF`, `i`,
`Second Life`, `Second Coming`, `44`, `44:44`, `second`, `Second`, `upside down`, `MasK`, `U2`,
`Jesus`, `Easter TOMI Second Life`. 1,176 derivations. No match against either escrow.

## 3. The paragraph-id chain as the hashed object

pids concatenated, newline-joined, comma-joined, upper-cased, sorted, duplicated at the end, and both
pid-then-text orders. 32 derivations. No match.

## 4. Sentence-edge flips (new rule variant)

First letter of every sentence lowered and/or last letter raised, applied to: all paragraphs, the
three FFWW windows, all FFWW-signature paragraphs, the story part (1-87), the non-story part (88-273).
90 derivations. No match.

## Reading of the result

The obvious serialisations of the chapter are now excluded, so the missing variable is not the
encoding. It is the flip set (which paragraphs, which edges) and the appended field. The log makes the
second point unavoidable: 23 blocks append "the last three digits of the previous block's private key",
and round-2 blocks append a TOMI field naming the method. Both are unknowable from the published text
alone, which is why bare-text sweeps of the chapter keep failing while the demo - which the author says
uses no TOMI field - stays the only clean oracle.
