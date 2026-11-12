# Pathway B audited: the archive is a Reddit post page, the modulo mapping is empty, and the real round-2 index rule is already in the repo

**Date:** 2026-10-31
**Files read:** `ca6jxv_arch.html`, `ca6jxv_full.html`, `corpus.json`, `wparts/`, `CLUES_CANONICAL` §9.
**Derivations this pass:** 480 (raw chapter and raw Finney post, both joins, with and without trailing
separator, indices 0–79). **Hits: 0.**

## 1. The Block 77 archive snapshot

`ca6jxv_arch.html`, 440,495 bytes, is a Wayback capture at `20200728154404` of a **reddit.com** post
page in r/Grycoin:

| field | value |
|---|---|
| title | `[77 mbtc] Quizchain2 Block 77 (Stage One) : Grycoin` |
| author | `AoiNakamoto` |
| subreddit | r/Grycoin, "Grycoin discussion", 35 members, created 2019-05-21 |
| capture | 2020-07-28 15:44:04, thread archived, 38 comments |

**What it does not contain:** no submission form, no input field, no textarea, no verification endpoint,
no regex, no expected input length, no hidden div carrying a target, no HTML comment beyond the Wayback
banner. The only `<form>` on the page is the site-wide Reddit search form, and the only `<input>` is that
search box. It is a discussion post, not a submission interface, so there is no parameter metadata to
recover from it.

**What it does contain, and this matters.** The post body was not captured *in this HTML*, but it is in
`grycoin_posts.json` (`ca6jxv`, 4,149 characters, quoted in `STAGE_TWO_POST_2026-10-31.md` §2), so the
archive's value here is the two captured comments:

- a player: *"I think it's impossible for this to be solved without a hint. We couldn't guess your
  thoughts when we only had some characters (the address in first block 77), so it is countless times
  harder now with a huge text with unlimited possibilities … the truth is that we don't know where to
  look."*
- the author: *"I am quite sure that it is impossible to write a script solving this block. Actually
  **there is a hint on how to solve this right in the post by Hal. Much like the Aa in the genesis block
  address hinted at the solution.**"*

Two things follow, in the author's own words. The solution is not scriptable, which is a direct argument
against every enumeration strategy in this repo, including the ones that returned zero. And the hint is
located *in Hal's post*, with the genesis address's case pattern named as the analogue, which is the same
reading the FFWW census reached from the other direction: case carries the payload.

`ca6jxv_full.html` is not a second capture. It is a 4,662-byte Wayback Machine landing/error page.

## 2. The 33-part corpus, enumerated

`corpus.json` holds 33 items in **ascending Wattpad id order**, which is publication order. `wparts/`
holds the same 33 as raw files. The sequence ends at id `762380140` *"Starting Up"*.

Part 10 and Part 11, by position in that order:

| part | id | title | paras |
|---|---|---|---|
| **10** | 721795188 | *Tragic Boating Accident* | 7 |
| **11** | 722270069 | *Satoshi's Stash* | 9 |

Openings:

- **¶10** — *"An explosion went off on my boat the other day. I was lucky to escape alive."* The post is
  the amnesia gag: the author claims to have lost her solution notebook and her memory, so block 44 has
  no solution from her. Its last paragraph: *"No solution for block 44 from me. For now."*
- **¶11** — *"There are all these rumors floating around that you will win a million of Satoshi's bitcoins
  if you stick around and solve block 77 first. These rumors are a Hoax."* The post argues there never
  were a million Satoshi coins, that he was a cypherpunk rather than a hoarder, and that the author is
  not Satoshi.

**Neither contains a question prompt, a `[solution] TOMI` format line, a `TOMI` token, a 4-unit set, or
any sign/replica structure.** Both are ordinary prose posts. The modulo mapping, run honestly, returns
nothing.

One coincidence is worth recording and then discounting. Part 10 names **block 76** and Part 11 names
**block 77**, which is exactly the pair the mapping selects. But the mentions are not unique: three parts
name block 76 ("Complete Quizchain", "Tragic Boating Accident", "End Phase of the Experiment") and nine
name block 77. So the correspondence is the author's habit of talking about the finale, not evidence that
part position encodes block number.

**Direct index fails structurally.** There are 33 parts and no Part 76 or Part 77. Ids are not
contiguous, so a post id cannot stand in for a block number either: the 33 ids run from `717956015` to
`762380140` with gaps, and the highest id is the last part.

## 3. The round-2 index rule is a derivation index, not a corpus position, and it is already in the record

`gh_leads.md` §4 carries the premise that the method confirmed on blocks 56–58 is "the block's own number
as a position index into a specific corpus (a numbered post … read in a specific order)". That premise
describes **round 1**. Round 2's own worked examples say something different, and they are in
`corpus.json` at `720895205` ¶708–715:

- **Round 2, Block 1** (¶710): solution `U2`, TOMI field `upside down`. *"And it was derived from the hint
  by reading M upside down and then W as UU, which is one step away from the solution."*
- **Round 2, Block 2** (¶714–715): *"This was just using the puzzle string in the latest Wattpad chapter
  on quizchain as a password manager in exactly the way it was described there and then pick the second
  private key under that puzzle string. **Second private key because this was block 2, or the second
  block.**"*

So in round 2 the block number selects a **derivation index under a puzzle string**, not a position in a
list of posts. This is not a new observation for the corpus: `FRESH_ANGLES.md` records the chain as
*"chapter phrase -> MD5 -> BIP39 wallet -> take the Nth private key (N = block number) as the strong
password -> MD5 that -> second wallet"*, `SESSION_2026-10-30.md` §12 verifies it end to end on round-2
block 2, and `FRESH_ANGLES.md` §C reports the sweep: 4 chapter variants × 2 joins × indices 0–77 × 2
target indices, **1,248 derivations, no hit**.

What that costs the modulo hypothesis is the reason it was ever attractive. There is no need to map block
numbers onto a 33-part list, because the author's own round-2 precedent maps them onto key indices
instead. The modulo-of-33 construction has no support from the series it was proposed for.

## 4. Re-run on the raw texts, for completeness

The chain above was swept on *chapter variants*. For the record, the unmodified documents were also run
at **every index 0–79**, which is wider than the 0–77 already covered and needs no variant selection at
all: chapter and Finney post, at `\n\n` and `\r\n\r\n`, with and without a trailing separator.

| text | md5 | idx 76 | idx 77 |
|---|---|---|---|
| chapter LF | `6bc77881b2eeb1298701d771f8330844` | `1NaFqoGKtjaxj3e5FU2ya19uyBZwjRXFC6` | `1JFXxtk7rfvmHyn6kRSoVydU5yaBWFnUei` |
| chapter LF + trailing | `d1b75e5db53b12252f35c461d6332d88` | `1KRAyVRYbR5g7N9vTddpjrgdoFCAeY9RQ1` | `12DpyKuEtzHJEsnKDaj4RK5ZtMA9hRk6V4` |
| chapter CRLF | `2979ce16480d92d5f229d7b3dc16aabb` | `17wNrgDLe6uaeWrpJeSjKjPj2QeyKKa95n` | `1PRhHCajyDWcscdv5Z67GHTWNiemUkGvJB` |
| chapter CRLF + trailing | `48f2adae7bbcc3a9b069824a8654e26e` | `1F7idUSRiEh3YgcKnMicQQzrGqWFHxZ5Em` | `1Etkhxod8M6V9NJwtvSCRrnXV1WspJvvSZ` |
| hal LF | `4f73b149adcfb54b606f6f0dbafd9d45` | `1PJPFWkwynDqvUgjnpKNHioMyLqJkW6EVr` | `1NtVLoQ3UiGkufyj1chH7vXAGJDSqWXF6H` |
| hal CRLF | `7b1203e2b4ebc6f7355b4b478ae1b942` | `16bFyr71jBoGgKZjX7FmSqo2nThaU4aKbF` | `1AjHmoWuGrNMcXpxXFsXei4o9An9UucCzd` |

480 derivations, **0 hits**. This overlaps the 1,248 already spent and adds only indices 78 and 79 and the
unmodified-baseline form; it does not change the picture. What remains open under the round-2 rule is not
the index but the **puzzle string**, since round-2 block 2's answer came from a *string in the chapter*,
not from the chapter. That is a selection problem of the same shape as the flip selection.

## 5. The terminal-vector argument, checked

The claim was that a hybrid sign set drawn from {20, 42} × {128, 136} × {220, 222} × {273} cannot reach
`stnm` on terminal letters. Verified directly:

| ¶ | initial | final | last word |
|---|---|---|---|
| 20 | I | **s** | signs |
| 42 | I | **s** | signs |
| 128 | V | **l** | fuel |
| 136 | B | **s** | emissions |
| 220 | A | **s** | signs |
| 222 | T | **s** | signs |
| 273 | A | **s** | signs |

The terminal multiset over the whole pool is `{s, s, s, s, l, s, s}`: only `s` and `l`. `stnm` needs `t`,
`n` and `m`, and **none of the three occurs as a terminal anywhere in the pool**, for any selection. So
the terminal channel is unreachable from this pool before derivation, which is a stronger statement than
a negative result: it is a letter-inventory obstruction. (The stated vector `slss` or `ssss` is right in
substance; the pool's actual terminals are `ssls` for {20, 42, 128, 136}.)

## 6. What this leaves

**Closed by this pass:** the archive-snapshot question (no submission metadata exists to recover), the
modulo-of-33 mapping (empty, and its one apparent hit is not unique), the direct index (no Parts 76/77),
and unmodified-text-at-every-index for both documents.

**Confirmed as already closed, not newly opened:** the round-2 rule *block number → derivation index under
a puzzle string* is documented, verified on round-2 block 2, and swept to 1,248 derivations. This pass
does not reopen it; it establishes that the corpus-position reading in `gh_leads.md` §4 is a round-1
convention, so the modulo construction is unnecessary rather than merely negative.

**Unchanged and still the only open variable:** `CLUES_CANONICAL` §9 lead 1, *which* paragraphs get
flipped.

**Also unchanged, and worth keeping in view:** the author's own statement on the archived post that the
block cannot be solved by script, and that the hint is in Hal's post with the genesis address's case
pattern as the precedent. Both point at the case channel, which is where the FFWW census arrived
independently.
