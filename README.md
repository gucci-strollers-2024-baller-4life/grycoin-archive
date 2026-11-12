# Grycoin Block 77 stage two — hunt archive

Consolidated record of the attempt to solve stage two of Aoi Nakamoto's
Grycoin "block 77" (the 0.777 BTC escrow, address `14zMkTga…USG9W`).

The escrow is **unclaimed**. Nothing in this repository contains the answer.

## What is settled

- **Substrate.** The chapter *Second* is 273 paragraphs, 45,450 characters, LF join,
  md5 `46a308c2…`. Confirmed byte-identical to Wattpad's stored data via pid checks,
  and confirmed identical to the only surviving April 2019 copy.
- **Serialization.** Live escrow join is CRLF CRLF, author-confirmed in his own words.
- **Pipeline.** MD5 → BIP39 entropy → `m/44'/0'/0'/0/i`. Certified against two
  published vectors and against an independent community tool.
- **Stage one.** Reproduced: `19TbyN5…`, and flipping the four F/F/W/W paragraphs
  regenerates `9dd2efb9…` → stage one's escrow.

## What is not settled

The selector: which characters the author capitalised. Everything above is
arithmetic; this one step is a judgement, and the author says so himself:
*"It is for 77, but you will not see it if you let a script solve the block."*

Roughly 400M+ candidates across two independent efforts have returned zero.

## Layout

| Path | Contents |
|---|---|
| `corpus/` | All 33 Wattpad publications, one file each, plus INDEX.md |
| `analysis/` | `grycoin_legend.md` (lexicon/compass/mapping), `reprint_analysis.md`, `leads.md` |
| `data/` | Author's Reddit footprint (posts + 418 comments), thread dumps, HTML captures |
| `scripts/` | Sweep scripts and logs from this session |
| `prior/` | The earlier `grycoin-rbb-hunt` repository, preserved intact |
| `history/` | Session log of the investigation |

## Standing rules observed

Never use sub-agents. Never spend credits without explicit confirmation.
Prioritise exhausted negatives and arithmetic verification over speculation.
Maintain the certified substrate.
