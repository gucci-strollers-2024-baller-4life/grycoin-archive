# Web research, 2026-10-29: what the public record adds

## 1. There are no missing blocks 78-150

The community census (floflo777/open-crypto-puzzles, `1-big-prizes/aoi-nakamoto-quizchain-0-854btc`)
and the author's own logs agree: roughly 147 blocks over two rounds, every one solved and swept by
readers **except two**:

- Real Big Block stage 2, 0.777 BTC at `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` - open.
- Quizchain2 Block 76, 0.077 BTC at `13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd` - **solved and swept
  2026-08-17** (tx `2e271ac2f63f488cd14112bceeed56f159ecd98cb3ce753f08e2d94bb62714a3`).

So the only outstanding item is the finale we are already working. There is no unpublished block
range to verify against the chapter.

## 2. The target text is confirmed

The stage-two post links `wattpad.com/720888559-second`; that part is titled "Second" and holds
**273 paragraphs** - byte-identical in count and content to our `wp_paras.json` copy. The story
`184148284` has 33 parts; part 2 is the puzzle text, part 1 is "Welcome to the Quizchain".

## 3. The serialisation is now documented by the author (this is new and decisive)

From the author's own comments in the Real Big Block discussion thread (`as_chn8un.json`):

- "When I posted the real big block at the Wattpad site, I added extra line breaks between paragraphs.
  This information is needed to solve the block."
- "I have line breaks in the chapter between all paragraphs. And there are two line breaks there now,
  since Wattpad would not display them correctly with only one each. I analyzed them with the tool at
  asciivalue.com and that shows one 13 and one 10 for each of the line breaks. The solution you need to
  hash with has only one line break between paragraphs, which is one 13 and one 10 in ASCII."
- Then, after the refund and re-funding: "I took back the prize for a moment and sent it again to a new
  address, hashing with a slightly different solution ... It has multiple paragraphs and two line
  breaks between each of them."
- "I mean the second one. Hit enter twice. This displays in Ascii as 13 10 13 10."

**Conclusion: the hashed text is the 273 paragraphs joined with `\r\n\r\n` (13 10 13 10), not `\n\n`.**
Every sweep we ran with `\n\n` (including the demo-derived conventions) was hashing the wrong bytes.

Consequence that matters: the flip set did not change between the two fundings. The July-22 version
(single `\r\n`, escrow `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC`) and the July-30 version (`\r\n\r\n`,
escrow `14zMk...`) hash the *same* flipped text under *two* joins. So there are two oracles for one
unknown flip set, and a candidate must match one of them under its own join.

## 4. Cross-checks from the public material

- Author hint 6: "Once someone figures out the format for the first stage, they will also have a big
  hint for the format of this second stage." Stage-one format is certifiably: paragraph firsts F,F,W,W
  lowered, paragraph lasts s,t,n,m raised.
- The 2019 "lucky address" narrative (a 7 near the middle, Fibonacci, "Ao" at digits six and seven)
  is the author's own apophenia note, not a hint.
- July 2026 thread revival: players ask each other for a copy of the July-2019 chapter; nobody has one
  in public. Our copy is nevertheless trustworthy: all 273 paragraph ids certify (272 direct hashes +
  1 Wattpad dedup hash for the `"What?"` duplicate), so nothing was edited after upload.

## 5. Re-run of the flip families with the documented join

1,248 derivations: 13 selection rules (all, ITASM, not-ITASM, the three FFWW windows, FFWW signature,
the four Finney paragraphs, all-but-those-four, first 44, last 44, both, story part, stride 44, the
end-quadruples) x 6 edge modes (first-down, last-up, both, first-up, last-up-only, last-down) x
`\r\n\r\n` and `\n\n` x with and without a trailing break x indices 0-3, checked against both the live
prize and the lucky address. **No hit.**

## 6. What this narrows it to

The encoding is settled by the author's own words, and the text is certified. What remains is exactly
one unknown: which letters were flipped. Her format line for block 77 - "eight items in two sets of
four. Two items ciphertext and two items plaintext each, 44 read from left and 44 read from right" -
should therefore be read as a description of the *selection*, and it is the only thing left to decode.
