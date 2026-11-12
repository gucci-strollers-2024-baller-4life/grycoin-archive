# State of the hunt, 2026-10-31

## Certified base
- Text: Wattpad part 720888559 "Second", 273 paragraphs, 45,450 chars in the LF build. All 273 paragraph pids
  verify (272 direct, 1 by Wattpad's dedup rule `md5(md5_hex + "1")`, paragraph 78).
- Join in force for the live 0.777 escrow: `\r\n\r\n` (author, 2019-08-01: "Hit enter twice ... 13 10 13 10").
  The July-28 "one 13 and one 10" note belongs to the refunded 1EFoj oracle.
- Pipeline: md5 -> 12 words, empty passphrase -> m/44'/0'/0'/0/i -> P2PKH. Stage one reproduces exactly
  (9dd2efb9 -> 19TbyN5 at index 0). Alternate paths (m/0'/0'/i) do not reproduce it, tested today.
- Demo oracle: question hash 7759227d7406 only under LF join; escrow 1tzieU... still unreproduced.

## Closed families (all negative)
case flips of every enumerated selection; sentence/paragraph/clause edges; the 44-residue lattice;
eight-token address-decode space (559,872 derivations, exhaustive); serialisation (19 byte forms, pid tags,
NBSP/zero-width/smart quotes, BOM, the 10 in-paragraph <br> breaks, 12,288 derivations); appended format
fields and link candidates; chained keys and the round-2 password-manager pipeline; segment and part
permutations; numeric rewrite axis; sign-location demo rule (1,062 today); demo under SHA-256 (80 today).

## Open
1. the flip selection for the chapter; every enumerated candidate fails
2. the demo answer, which is the only clean oracle left and is not a case change of its own text up to k=4
3. whether the July-22 chapter differed in *paragraph set* (pids certify text, not addition date)
4. the unit that carries the signs: paragraph, sentence, or neither — 2^664 as a free sentence subset,
   and no rule naming the units exists anywhere in the corpus
5. `H` membership in the sign alphabet: `{A,I,M,O,S,T}` (103 out) or with `H` (92 out), decided at ¶230
   if anywhere

## Operational
- `demo_oracle.py` wordlist repointed to `harness/bip39_english.txt`; verify on first use.
- Quizchain calibration (`quiz1_blocks.py`, `quiz2_blocks.py`) is absent from this workspace; the 153
  published exact inputs must be re-supplied before any block-level verification runs again.
- Sandbox has 1 CPU core; budget ~450 derivations/second.
- Prize protocol if a candidate key ever appears: pre-sign a sweep with a high fee, broadcast once, never
  publish the WIF, never send a test transfer.

## 2026-10-31 second pass — sign-unit scan and the shifted quadruples (negative)

Hal's post: 16 paragraphs, exactly four openers outside I,T,A,S,M (F,F,W,W at 2,3,4,6), the
I-paragraph 5 between the two W's, and those four are the certified flips. The chapter has
**121** such paragraphs, so the phrase in para 229 cannot be a property of the whole chapter:
the stage-one sign test has no chapter-wide transfer. That is a structural result, not another
negative, and it explains why every ITASM/SATOSHI sign-set sweep was doomed rather than merely
unlucky.

`sign_unit_scan.py` returns the only spans that do satisfy "all paragraphs except four":
the three known windows, the Finney reprint 231-235 (the only F,F,W,[I],W replica), and three
shifted quadruples that mix window and non-window paragraphs — {94,95,96,100} FWWF,
{95,96,100,102} WWFF, {232,233,235,236} FWWW. The order-free reading of "F F and W W" licenses
the first two.

`sweep_signunit.py`: 896 sign sets (every subset of {94..236} pool touching 100/102/236), 6 edge
modes, 2 bases x 2 joins, 64,536 derivations at indices 0,1,2,44,76,77 — **0 hits**.

Harness repair made this pass: the first run used `.strip()` on paragraphs and hashed a base that
matched none of the four certified values (3be071d7 instead of f74e8e01). The script now refuses to
run unless the plain text of all four serialisations matches the certified digests, so a wrong-base
negative cannot recur silently.

## 2026-10-31 third pass — class-3 slips and paste bases (negative)

Fresh sandbox, harness rebuilt from zero and re-certified (stage-one at index 0, all three base
digests, Wattpad length arithmetic, live hash160), 560-580 derivations/s.

Two families that `SLIP_PATTERNS.md` §8.2-8.3 named as never enumerated are now closed:

- `sweeps/class3_slips.py` — an accepted sign set with exactly one paragraph's direction inverted
  (155 candidates), and with exactly one stray capital inside the set (23,907 candidates);
  120,310 derivations, 0 hits.
- `sweeps/slip_extension.py` — the same inversion logic over twelve accepted sets in both
  directions, on four bases (two certified, two claimer's-paste) at indices 0,1,2,44,76,77;
  33,768 derivations, 0 hits.

A per-paragraph direction is outside every earlier closure (those applied one mode to a whole set,
or arbitrary subsets under a fixed mode), which is why this was an open shape at all. Totals this
session: **154,078 address-verified derivations, 0 hits.** Details in `SESSION_2026-10-31_third.md`.

## 2026-10-31 fourth pass — the sign alphabet folded in, the sentence unit closed, and the payload question answered

Folds `d6675c3` (sign alphabet) and `dce5ae2` (sentence unit) into the record, plus
`PAYLOAD_AUDIT_2026-10-31.md` for the external-payload question.

**The sign alphabet is `{A,I,M,O,S,T}`.** SATOSHI's letters leave five anomalies on the Finney post
(¶11 opens on `M`); `{I,T,A,S,M}` leaves five on the grycoin demo (¶6 opens on `O`). The minimal fixed
alphabet that gives exactly four `FFWW` on both is `{A,I,M,O,S,T}`, and dropping any one of the six
breaks one of the two documents. `H` is *undetermined* by that calibration — neither demonstrated
document has an `H` initial — so it is carried as a parameter, and it is worth 11 paragraphs:
¶44, 64, 74, 205, 216, 221, **230**, 251, 253, 255, 261. The exact boundary:

| alphabet | out of class | with letters |
|---|---|---|
| `{A,I,M,O,S,T}` | 104 | **103** |
| `{A,H,I,M,O,S,T}` | 93 | **92** |

¶230 *"Having seen the signs before"*, the paragraph that introduces the reprint, is a sign under the
six-letter set and a carrier under the seven-letter one, which is the only place the ambiguity is
load-bearing.

**The sentence unit is closed for every alphabet rule.** The demo's worked example is sentence-level:
demo ¶5 sentence 1 `"I expected…himself."` → `"i expected…himselF."`, two moves, asserted in
`sweeps/sentence_signs.py` before anything runs. Applied at chapter scale — 664 sentences, 2.43 per
paragraph, max 7 — five alphabets × in-class and out-class × three unit definitions × four joins ×
nine indices: 120 texts, 1,080 derivations, **0 hits**. A free "which sentences" selection is 2^664 and
is not a sweep; no rule naming the sentences exists anywhere in the corpus.

**No external payload exists here.** Nothing in the repository contains the 2008 announcement, the v0.1
release post, the genesis coinbase headline or its scriptSig hex, or the whitepaper. The genesis
artefact is present only as an address *string quoted in prose*. Two external primary documents exist:
`hal_original.txt` and `hal_post.html`. Pathway A therefore needs a capture it does not have, and
contradicts `CLUES_CANONICAL` §5, which names the hashed object as the chapter at `720888559`.
For Pathway B, `gh_leads.md` §4's only untried candidate that is also in-repo is the author's own
numbered posts — and `corpus.json` holds all 33 of them, including "Complete Quizchain" (766 ¶) and
"Complete Second Round" (367 ¶). That method targets a block's *question*, not stage two's payload.

**Section-level four-anomaly codes do not discriminate.** Sliding 6–24-paragraph windows over the
chapter give 81 distinct four-anomaly codes; `FFWW` occurs 82 times, `HCDH` 55, `FFGF` and `CDHH` 36,
`WVWB` 16, `GFVE` 2. Any window can be made to produce a four-letter code by choosing its edges, so a
section-level claim needs a section definition justified independently of the code it yields. `GFVE` and
`WVWB` appear nowhere else in the repository and no section boundaries are recorded, so those two
negatives are honest but non-discriminating.

**Two corrections.**
- The `14z` collision is **1 in 1,580**, not 1 in 262,144: P2PKH addresses always begin `1` and `14`
  occurs at 4.2%, measured over 30,000 derivations. Expected count at 120 texts is 0.076. Noise, by a
  wider margin than the bits-per-character estimate implies.
- The join is **CRLF for the chapter and LF for the demo**. The demo's question hash reproduces only
  under `\n\n`; the live `14zMkTga…` escrow's join is `\r\n\r\n` per the author's 2019-08-01 note. Every
  sweep ran both, so nothing moves, but the earlier generalisation of the LF result to the chapter was
  wrong.

**Pruned:** the `§13.9` citation in `SAT_SET_TRANSPORT_2026-10-31.md` §5 pointed at a section that does
not exist (§13 runs 13.1–13.5). Replaced with §13.5 and with the sentence-scale statement above.

## 2026-10-31 fifth pass — the act census folded in, and what it corrects

`ACT_CENSUS_2026-10-31.md`, `sweeps/act_census.py`, `act_census_results.json`. Four act ranges as given
(1–92, 93–167, 168–230, 231–273), 245 prose paragraphs after removing 17 headings, 10 `a)`–`f)` labels
and ¶237.

**Confirmed.** `sign*` tokens in Act I = 2 (¶20, ¶42), in Act II = **0**. Case-odd tokens in Act III and
IV prose = **0** and **0**. The semantic directive channel and the planted orthographic channel do not
overlap in prose, which is the reason every single-channel macro-filter failed.

**Corrected.** Prose counts are 85/68/58/34 (245), not 83/68/58/35 (244), and 244 is unreachable under
any consistent rule. Sentences over prose are 621 (quote-splitting) or 614 (conservative); 664 counts
headings too. The stated 627 is none of these. `sign*` tokens are 13 over 10 paragraphs in Act III and 6
over 5 in Act IV, not 11 and 7. Case-odd tokens in Act II are 9 raw, of which only `VIrgin` (¶128) and
`BItcoin` (¶136) are internal-capital plants, the rest being the author's camel-case identifiers and her
alphabet strings.

**Inverted.** ¶128 opens on **V** (*"VIrgin bitcoins are the only source of grycoins."*) and closes on
**l**; ¶136 opens on **B** (*"Before BItcoin, there were remailers."*) and closes on **s**. `V` and `B`
are both outside `{A,I,M,O,S,T}`, so both paragraphs are **anomalies**, not carriers. Act II therefore
*does* have anomaly-class, plant-bearing paragraphs available as sign units, which is the routing the
orthographic channel needs. The stated conclusion that neither is an anomaly is the reverse of the text.

**Leaked.** The orthographic exclusion is a prose-only result. ¶209 *"c) BITcoin is actually AHScoin"* is
in Act III and carries two internal-capital tokens; it is a label, which the prose filter drops. Case-odd
paragraphs including headings and labels: 73, 106, 107, 112, 126, 128, 136, **209**.

**Observed, not derived.** The three genuine plants sit in paragraphs with edge signatures (T,t) ¶73,
(V,l) ¶128, (B,s) ¶136. Only ¶73 is edge-matched, which is the `F…f` / `W…w` / `s…s` shape where head and
tail are the same letter in opposite case.

**The partition itself is imposed, not declared.** The chapter has part headings `I. Second Life` (¶2) and
`III. Second Identity` (¶163) and **no `II.` heading at all**; the 1–92 / 93–167 line falls inside the
Grycoin spec between ¶92 and ¶93. The exclusion result holds for the partition as imposed, but the
boundaries are not the author's, and `PAYLOAD_AUDIT_2026-10-31.md` §5 remains the record on section-level
codes (81 distinct four-anomaly codes, `GFVE` and `WVWB` non-discriminating).

## 2026-10-31 sixth pass — Pathway B audited: archive, modulo mapping, and the round-2 rule

`PATHWAY_B_AUDIT_2026-10-31.md`. Citation in `SAT_SET_TRANSPORT` §5 re-anchored from the nonexistent
`§13.9` to `CLUES_CANONICAL` **§9 lead 1** ("The only open variable is which paragraphs get flipped").

**The Block 77 archive is a Reddit post page, not a submission interface.** `ca6jxv_arch.html` is a
Wayback capture (20200728154404) of `[77 mbtc] Quizchain2 Block 77 (Stage One) : Grycoin` by
`AoiNakamoto` in r/Grycoin. No form, no input field, no regex, no endpoint, no expected length, no hidden
target. `ca6jxv_full.html` is a Wayback landing page. Two comments were captured, and the author's reply
is the useful part: *"I am quite sure that it is impossible to write a script solving this block.
Actually there is a hint on how to solve this right in the post by Hal. Much like the Aa in the genesis
block address hinted at the solution."*

**The modulo-of-33 mapping is empty.** 33 parts in ascending Wattpad-id order, ending at `762380140`.
Part 10 = *Tragic Boating Accident* ("An explosion went off on my boat the other day…"), Part 11 =
*Satoshi's Stash* ("There are all these rumors… you will win a million of Satoshi's bitcoins"). Neither
has a question prompt, a `[solution] TOMI` format line, a `TOMI` token, or a 4-unit set. Part 10 names
block 76 and Part 11 names block 77, but three parts name block 76 and nine name block 77, so the
correspondence is the author's habit of discussing the finale. Direct index fails: no Parts 76/77 exist.

**The round-2 convention is a derivation index, not a corpus position.** `corpus.json` `720895205`
¶714–715: *"pick the second private key under that puzzle string. Second private key because this was
block 2, or the second block."* Already documented (`FRESH_ANGLES.md`), already verified end to end on
round-2 block 2 (`SESSION_2026-10-30.md` §12), already swept (1,248 derivations, none). So
`gh_leads.md` §4's corpus-position reading is a round-1 convention and the modulo construction is
unnecessary rather than merely negative. Round-2 block 1 is worth remembering for its wordplay: solution
`U2`, *"reading M upside down and then W as UU"*, TOMI field "upside down".

**New negative.** Unmodified chapter and Finney post, both joins, with and without trailing, at every
index 0–79: 480 derivations, 0 hits. Adds indices 78–79 and the unmodified baseline; it does not reopen
the chain, it closes the raw-baseline form of it.

**Terminal-vector obstruction, verified.** The hybrid pool {20, 42} × {128, 136} × {220, 222} × {273} has
finals `s s s s l s s` — only `s` and `l`. `stnm` requires `t`, `n` and `m`, none of which occurs as a
terminal anywhere in the pool, under any selection. That is a letter-inventory obstruction, not a
negative result.

## 2026-10-31 seventh pass — Hal's post screened for an `Aa` pair: none exists, the polarity is the hint

`HAL_BOUNDARY_2026-10-31.md`. Triggered by the author's preserved comment on the archived stage-one post:
*"there is a hint on how to solve this right in the post by Hal. Much like the Aa in the genesis block
address hinted at the solution."*

**The screen is negative, in six scopes.** `hal_original.txt` has 16 paragraphs and zero non-ASCII bytes;
heads run `I F F W I W T A T S M A T I A T`, tails run `e s t n g m s s s g t n s n o y`. Screened for an
`Xx` pair with chance expectations computed from the post's own letter frequencies: **self-matching within
a paragraph 0 of 16** (0.88 expected), **global endpoints `I…y`** not a pair (last char `]`, from
`[edited slightly]`), **adjacent head→tail 0 of 15** (0.88 expected), **adjacent tail→head 1 of 15**
(0.75; ¶9 tail `s` → ¶10 head `S`), **bookend mirror head→tail 0 of 8** (0.13), **bookend mirror
tail→head 2 of 8** (0.50; ¶6 `m`→¶11 `M`, ¶7 `s`→¶10 `S`, P≈0.09 and dissolved by the six comparisons).
The one asymmetry that survives: no paragraph ends on `f` or `w`, so the four anomalous heads are dead
ends while three of four anomalous tails resolve to heads. No symmetric edge-pairing marker exists.

**What transfers is polarity.** The genesis `A…a` is capital head, lowercase tail, and the four anomalies
are exactly that shape. The certified diff shows the operation inverts both ends and nothing else: 8
single-character replacements at offsets 85, 480, 484, 713, 717, 924, 1299, 1691, plus one deleted
newline. `F…s → f…S`, `F…t → f…T`, `W…n → w…N`, `W…m → w…M`.

**The resolution matrix is asymmetric.** No paragraph in the post ends on `f` or `w`, so all four
anomalous heads are dead ends; three of four anomalous tails point at heads (`s`→¶10, `t`→¶7/9/13/16,
`m`→¶11), and `n` points at nothing. `n` is the one `STNM` letter the post's heads cannot supply, so no
symmetric head-to-tail chaining exists across the 16 paragraphs.

**Two texts, not one.** `hal_original.txt` has `facinating` (¶5 tail) and `moter` (¶12); the chapter's
reprint ¶231–235 has them corrected while keeping the same edge geometry. `hal_original.txt` is the
certified stage-one base (`9dd2efb9` → `19TbyN5`); the reprint is a different byte stream. Do not
substitute one for the other in a sweep.

**The post mentions no key, no address, no code.** `signs` occurs once (¶7), `signals` once (¶12), wallets
at ¶9 and ¶14. Under the census rule `signals` is not a `sign*` token, so the post's directive count is 1.

**Index narrowed.** `corpus.json` ¶714–715 ("second private key because this was block 2") is a 0-based
`block − 1` rule, so block 77 is **index 76**, not 77. This does not unblock the hunt: both indices are in
the standard set and the raw texts were swept at every index 0–79 tonight (0 hits). The unknown remains the
string, and this pass removes the post itself from the `Aa`-pair reading.

## 2026-10-31 eighth pass — the two Block 77 posts were in the repo all along

`STAGE_TWO_POST_2026-10-31.md`. Triggered by a proposal that stage two might hash a Reddit post envelope.
It does not, and the correction is to our own inventory.

**Correction.** `grycoin_posts.json` holds **91 r/Grycoin posts with full `selftext`** (retrieved
2019-07-25 to 2019-08-29), and `agntn/` holds 15 as markdown. `PAYLOAD_AUDIT_2026-10-31.md` §2 said the
repo held "two external primary documents" and `PATHWAY_B_AUDIT_2026-10-31.md` §1 said the post body "was
not captured". Both were wrong and are fixed in place. The narrower finding survives: no byte stream of
the 2008 announcement, the v0.1 post, the genesis coinbase parameter or the whitepaper exists here.

**Stage two's announcement is `cgkpbb`** (*"[777 mbtc] Quizchain last block"*, 2019-07-22): *"Question:
Final version of the second chapter of Wattpad story"*, link `720888559-second`, and on the refund from
`1EFojcAo…` to the live escrow: *"because I wanted to remove one of the twists I had. The block is now
slightly easier. It is also hashed with two line breaks between paragraphs now."* No format, no TOMI, no
prefix, no payload text. A post envelope has no paragraphs to put breaks between, so the container
hypothesis is dead on the author's own sentence.

**Stage one hashes the linked bitcointalk post, not the submission.** `ca6jxv` (4,149 chars) contains no
Finney text at all; it says *"Question: https://bitcointalk.org/index.php?topic=155054.0"*. The 5,362-char
preimage is the bitcointalk text, ending `…my legacy.\n[edited slightly]` with no trailing newline. So
`[edited slightly]` travels with the document, not with Reddit.

**No stage-two oracle exists.** 44 of the 91 posts publish a three-digit MD5 prefix (block 76 = `f8e`,
demo = `3c6`, Chain Block 1 = `4c4`). The two block-77 posts are the only pair that withholds it: *"no
first digits of MD5 hash, nothing"* and *"You are on your own completely with this one."* The escrow
address is the only oracle, and it is exact.

**Index 0, measured.** `md5(safudev_stage1.txt) = 9dd2efb9…` re-derived at every index 0–80 returns
`19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` at **index 0 and nowhere else**. The earlier narrowing to index 76 is
withdrawn; the measurement beats the inference for the one lane that can be verified.

**The hint question is answered by the author, in the repo.** The stage-one post's Hint two quotes ¶7 and
says: *"This is Satoshi's hint right in the post on how to decode it. After removing the misdirecting part,
I will rearrange the first four and last four words a bit"* → *"Today I come out. If you want to know
Satoshi's true identity, recognize the signs."* The sub-paragraph unit is the sentence group, and the
mechanism named is the first four and last four words of ¶7. ¶7's edges are `T…s`, and its `s` is the one
that resolves to ¶10's head `S`.

**Wattpad framing.** Story description *"Hint for block 77."*, tag `#hintforblock77`, and the body is
exactly 273 `<p data-p-id>` paragraphs with no note, header or footer inside it.

## 2026-10-31 ninth pass — the envelope measured, not argued: 48 derivations, 0 hits

`CONTAINER_TEST_2026-10-31.md`. The claim under test was that stage two hashes a Reddit post envelope
because stage one supposedly hashed one.

**The premise is checkable and fails.** `ca6jxv`'s `selftext` is **4,149** characters, contains no title
line, no `[edited slightly]`, and no Finney text beyond seven quoted sentences used as hints. The 5,362
characters hashed in stage one are the **linked bitcointalk document**, and the post's Question line is a
URL to it. So the convention is *document-as-preimage*, not submission-as-preimage, which is precisely why
stage two lands on the Wattpad part. `CLAIM_FORMAT_717956015_2026-10-31.md` and
`STAGE2_POST_AND_PART_2026-10-31.md` both stated this loosely and are corrected in place.

**Then it was measured.** 16 candidate preimages × indices 0, 76, 77 = **48 derivations, 0 hits**: both
Reddit selftexts with and without their titles, the chapter in both joins, and six framing variants
(`Second` prefix, `1. Second Coming` prefix, `Hint for block 77.` as prefix and as suffix, full title
stack) in both serialisations. One near-miss, `D_hint_pre_crlf` → `14rdtyix…`, differs at the third
character and is not a hit.

**Also note the record already closed this.** `44b32e7` (`STAGE2_POST_AND_PART_2026-10-31.md`) came one
commit after `afe6ea4` (`CLAIM_FORMAT…`) and refuted the same speculation with the author's own sentence
about two line breaks between paragraphs. What this pass adds is the arithmetic.

**No stage-two oracle exists.** 44 of 91 posts publish a three-digit MD5 prefix; the two block-77 posts
are the only pair that withholds it. The escrow is the only filter, and it is exact.

## 2026-10-31 tenth pass — the `<br>` axis is already closed, and the edge-class census needed one fix

**Inventory re-verified.** The payload has exactly **ten** `<br>` tags, one each in ¶63, 73, 121, 124, 146,
160, 184, 189, 193, 213 (`wp_paras_br.json` segment lists; `SERIALIZATION.md`). Skip-wraps: ¶63 "…one
bullet to | the brain…", ¶121 "…impossible to | forge them…", ¶160 "And it | will be an answer…", ¶189
"…if you take | TOM.", ¶213 "…playing around wit | And again…". Between-sentence breaks: ¶73, ¶124, ¶146,
¶184, ¶193.

**Serialization settled by the certified stage-one text, not by inference.** `safudev_stage1.txt` has
exactly **one** internal single newline, in ¶16: `legacy.\n[edited slightly]`. `demo_base.txt` has **none**
(10 clean paragraphs). So the author's pipeline renders a single `<br>` as `\n` and `</p><p>` as `\n\n`.
That is precisely `base_chapter_lf.txt`: 273 paragraphs, 45,450 chars, 10 internal newlines at exactly the
ten indices above, md5 `46a308c279540a33e977ea1f660e8458`, idx0 `1DGrEwbRwANU28BgCnp6HeNhPzB2HbiyUL` —
already swept, alongside the 1,238,662-candidate mixed-base closure. Negative.

**¶78.** `"What?"`, unique 32-hex id `8b71bade9685d3388452bc4755b06a0d` like all 273, duplicating ¶34, and
fifteen paragraphs before W2's lead-in at ¶92. `REBUILD_2026-10-31.md` §3 already records that it is the one
paragraph whose stored id fails to match its content under every transform tried. The July-23 edit reading
is plausible (chapter `modifyDate` 2019-07-23T23:12:04Z is one day after the re-funding post) but the repo
records a mismatch, not a proven edit.

**Correction to the "zero false positives in either direction" claim.** Census of the four edge classes
across all 273 paragraphs, first ASCII letter capitalised, last ASCII letter lowercased:

| class | members |
|---|---|
| `F…s` | 5, 93, **100**, 168, 231 — one outlier |
| `F…t` | 6, 94, 169, 232 — **exact, no outliers** |
| `W…n` | 7, 52, 95, 139, 152, 157, 170, 233, 265 — five outliers, several of them headings |
| `W…m` | 8, 30, 96, 171, 235 — one outlier |

So only the `F…t` row is exactly four and exactly the four window-second-paragraphs. Caveat against
over-reading it: eight different edge classes have exactly four members (`A…e`, `A…s`, `G…s`, `I…t`,
`O…e`, `S…e`, `W…t`, `F…t`), so cardinality alone is not evidence. What distinguishes `F…t` is that its
four sit at identical structural positions, gaps 88/75/63.

## 2026-10-31 eleventh pass — solo, paired and whole-chapter inversions all negative

`ANCHOR_INVERSION_2026-10-31.md`. **¶187 is `I…m`** (*"It also has the added value of misdirection… this
anagram."*), so it is not a case-pair site. "For those who don't know me" occurs at **¶6, ¶168 and ¶231**
(the reprint, opening on a quotation mark), not twice; "young man of Japanese ancestry" occurs at **¶187 and
¶222**; "recognize the signs" occurs **twelve times**. ¶187 is therefore neither unique nor a marker.

39 derivations, 0 hits: ¶6 solo (both ends, head only, tail only), ¶168 solo, ¶187 solo, {6,168},
{6,168,231}, {6,168,187}, the `F…t` quad {6,94,169,232}, the `F…s` quad {5,93,168,231}, and the whole-chapter
inversion in three modes. So neither the anchor-only reading nor the 273-paragraph reading produces the
escrow; the open variable is the selector, not the scope.

## 2026-10-31 twelfth pass — isolated extraction dead; Atbash contradicted by the author

`SUBSET_EXTRACTION_2026-10-31.md`. The 2^16 closure covered flip *subsets within* the 16 window paragraphs.
Untested until now was the inverse operation, **dropping** the other 257 paragraphs and hashing only the
marked ones. 20 texts (W1, W2, W3, the `F…t` anchors, W4, the full reprint, four sign paragraphs, W123,
W1234, each raw and inverted, plus two Atbash variants) × indices 0/76/77 = **60 derivations, 0 hits**.

**Atbash is contradicted by the author**, in the demo post: the block's format is *"the format used in both
phases of block 77"*, where solvers *"keep the whole long text and change only a couple of letters in their
capitalization."* Substitution, bisection and reordering are all excluded by that sentence. Round-1 part
761570746 is not held in this repo, so the Atbash claim about round 1 cannot be checked here.

**Shape, but no selector.** The demo's two illustrative flips are explicitly not the answer (*"that 'n' is
not part of the solution"*), so it certifies the mechanism and not a count. The only certified answer shape
is stage one's: four paragraphs, both ends, `\n\n` join, index 0. Remaining unknown: *which* paragraphs, i.e.
the selector. Scope is no longer the variable.

## 2026-10-31 thirteenth pass — `data-p-id` is a content hash, and it certifies the base

`DATA_PID_AUDIT_2026-10-31.md`. All 273 paragraphs hashed against their stored `data-p-id` under a cross
product of `<br>` handling, trailing character and NBSP handling.

**272/273 match** under: tags stripped, `<br>` **deleted**, nothing appended, **NBSP kept**. So no paragraph
requires a trailing space (the premise that one did is not borne out), the six U+00A0 sites must stay
U+00A0 (converting them breaks ¶90, 125, 126, 196, 257), and Wattpad's own id hash **deletes** the ten
`<br>` breaks rather than turning them into newlines. The author's certified stage-one text keeps a single
`<br>` as `\n` (`legacy.\n[edited slightly]`), and Wattpad's stored length counts a char per break, so
`base_chapter_lf.txt` is the right serialisation and is now verified per paragraph rather than assumed.

**¶78 is the one scar, sharply.** ¶34 and ¶78 are byte-identical (`"What?"`), ¶34's id **is** md5 of that
text, ¶78's is not, and a 168-variant probe finds no match. The field is content-derived, so ¶78's id is a
leftover from different content: she edited that paragraph and the id did not follow. Since `modifyDate` is
2019-07-23T23:12:04Z, the present text is the final one, i.e. the edit precedes the hash. The pre-edit
wording is unrecoverable and not needed.

**Net:** the baseline is byte-exact at 272/273 by hash. The claim that every document-level sweep ran on a
corrupted baseline is false, and this is settled by arithmetic rather than argument.

## 2026-10-31 fourteenth pass — the demo fails calibration; that does not kill the paradigm

`DEMO_CALIBRATION_2026-10-31.md`. Two corrections to the reasoning in play:

**The two named flips are an illustration, not the answer.** The demo's own next clause reads *"which would
be the solution, once you do that for all the paragraphs where you recognize the signs."* So a one- and
two-flip search tests the example, not the mechanism.

**The second flip is not a paragraph endpoint.** "himself" sits mid-¶5 in `demo_base.txt`, as the final
letter of a *sentence*. So the demo teaches **sentence-boundary** selection: a sentence-initial `I` and a
sentence-final `f`. That has never been calibrated, and the chapter has roughly 1,500 sentences against 273
paragraphs.

Battery run on the demo, indices 0–2: stated two flips `932fe1a5`, +trailing newline `510d367c`, paragraph
ends `a37126a8` / `b31ad58e` / `079a7678`, sentence ends `9ba6e7b7` / `f2d3ff76` / `60203051`, word ends
`70e418db`. **None begins `3c6`, none reaches `1tzieUf…`.**

**But case flipping is not falsified.** Stage one is a certified known-answer: eight case flips on the
bitcointalk text, md5 `9dd2efb9…` → `19TbyN5…` at index 0, re-verified across 0–80. That is the only
verified preimage chain in the puzzle and it is a case flip. So the demo is a replica or typo problem
(`demo_base.txt` may not be the exact span she hashed, or `3c6` may be wrong), not a decoy. Abandoning the
mechanism would discard the one thing the record actually certifies.

Open variable, unchanged: **selection** — which units are signs. Demo says sentences, stage one used
paragraphs.
