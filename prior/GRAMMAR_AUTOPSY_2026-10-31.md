# Grammatical autopsy: the three syntactic layers, measured

**Date:** 2026-10-31
**Script:** `grammar_autopsy.py` (census, reproducible), `sweeps/sentence_geometry_probe.py` (oracle probe)
**Ledger:** `sentence_geometry_probe_results.json`
**Question asked:** does grammar carry the selection, or does it only carry geometry? Where does the
microscope go next: imperative/conditional shifts, or internal punctuation inside the windows?

## Short answer

Neither, as a *selector*. The demo is the only place the stage-two format is described, and it is also
a free 12-bit oracle. Every syntactic feature in this autopsy was run through the demo first. **Not one
of them returns the demo's own selected set {4, 5, 6, 8}.** The lexical predicate does, exactly. So the
selection mechanism is lexical and has been known since `GRAMMAR_CONSTRAINTS.md`; syntax is not where a
new paragraph set will come from.

The punctuation lane is not merely weak, it is empty: the chapter has **zero em-dashes and zero
en-dashes**, one semicolon, and nine colons (two of them inside film titles). The demo, the document that
*defines* the format, has **zero colons, zero semicolons, zero dashes** of any kind. A channel that does
not exist in the specification cannot be part of the format.

What the grammar does supply, and what has never been tested, is a **constraint on the mark's anchor**
(§7) and one new probe, run below, negative (§6).

---

## 1. Mood: thirteen sentence-initial imperatives, two of them mechanics

| ¶ | word | text | class |
|---|---|---|---|
| 30 | Want | "Want to try a half marathon, Tom?" | in-story question (not imperative) |
| 41 | Keep | "Keep around as many humans as possible. | **in-story command** (the AI to her captors) |
| 47 | Let | "Let me explain. | in-story |
| 58 | Want | "Want me to fix your real body like that?" | in-story question |
| 59 | Reverse | Reverse age?" | fragment of the same question |
| 60 | Want | Want to fix your body?" | in-story question |
| 71 | Reverse | Reverse Turing Test | heading, not a sentence |
| 73 | Tell | "Tell me more about your solution… | **in-story command** |
| 75 | Keep | Keep emissions in line with the carbon budget. | **design imperative** (the coin's purpose) |
| 155 | Start | Start the Central Internet Authority to control the native Internet currency? | rhetorical question |
| 162 | Show | Show me if you are smart enough to pass this reverse Turing test. | **frame imperative** (AI to humanity) |
| 245 | Take | Take the first words of that together… | **mechanics** |
| 246 | Take | Take the next three words together… | **mechanics** |

So the chapter contains **two** mechanics imperatives, and the recognised pair 245–246 is the complete
set at sentence level. There is no hidden eighteenth imperative waiting outside them.

**But the buried ones are real, and they are all operations.** These are commands whose subject is
suppressed inside a conditional, an interrogative or an infinitival complement, which is why a
sentence-initial detector misses them:

| ¶ | form | operation it orders |
|---|---|---|
| 102 | "GRY is what you get **if you do** an Atbash substitution on BIT and **rearrange** the letters" | Atbash + anagram |
| 186 | "the best anagram you can find **if you start out from** Thomas" | anagram search |
| 189 | "guess what you get **if you take** the two letters following that M and **spell it backwards**?TOM." | extract two letters, reverse |
| 193 | "it would be fun **if you could just choose** the nonces I and M" | choose nonces |
| 219 | "**Just remove** a couple of words and you get…" | elide |
| 236 | "We **are directed to look at** the last letter of each of these" | read final letters |
| 242 | "The first four and last four words of the paragraph **hinting at** the solution" | read word edges |
| 269–273 | closing argument | none |

**Result:** 9 operational instruction sites, and every single one of them lies in ¶102 or in
¶186–246. Outside that block the only imperatives in the whole 273 paragraphs are spoken by
characters. The imperative mood is therefore a **section marker**, not a distributed selector: it fires
once, in the unit where the author stops describing and starts instructing. Taking it as a per-paragraph
flag would select ¶75 and ¶162 into the answer, both of which are story prose.

## 2. Modality: the instruction register is the *least* modal part of the chapter

210 modal tokens in 7,968 words = **26.4 per 1,000**. Inventory: will 92, would 45, can 22, may 18,
could 12, should 11, might 8, must 2, **shall 0**.

155 of 273 paragraphs contain no modal at all. The mass sits in one place:

| part | paragraphs | modals | words | rate/1,000 |
|---|---|---|---|---|
| I. Second Life | 2–87 | 38 | 1,555 | 24.4 |
| II. Second Layer (the whitepaper pastiche) | 88–162 | 118 | 3,173 | **37.2** |
| III. Second Identity | 163–273 | 54 | 3,239 | 16.7 |
| mechanics block 236–246 | | 1 | 212 | **4.7** |
| Finney reprint 231–235 | | 2 | 279 | 7.2 |

Hot paragraphs: ¶107 (6), ¶126 (5), ¶135 (5), ¶146 (5), ¶218 (4). All five are hedged engineering
prose ("a user **might** burn", "someone **would** send", "it **will** certainly be").

The direction is the opposite of the hypothesis. Modal density spikes exactly where the text is
*speculative world-building*, and collapses to the chapter minimum in the block that actually contains
the instructions. There is no trapdoor: 24 of the 40 conditionals have a plain declarative consequent,
and every one of them is an economic "if the price overshoots, X follows".

Conditional inventory (40 sentences containing if/unless):

| consequent | n | notes |
|---|---|---|
| bare declarative | 24 | economics, rules of the imaginary system |
| modal consequent | 11 | all `would`/`will` predictions |
| interrogative / embedded (`wonder if`, `see if`) | 3 | ¶10, ¶82, ¶162 |
| **truncated, no consequent** | 1 | ¶63 "And if she chooses her first option…" — in-story ellipsis, deliberate |
| **imperative consequent** | 1 | ¶246 "if you want to know Satoshi's real identity, **recognize the signs**" |

That single imperative consequent is the author's own meta-instruction: the only conditional in 273
paragraphs whose consequent is a command. It is a *shape*, not a location: "if P, do Q" is how she
writes an instruction, and she does it once.

Tense strain, checked sentence by sentence: the only two sites are ¶193 ("If so, it **would** be fun if
you **could** just choose…", a counterfactual inside a counterfactual, followed by a missing space:
`meaning.There`) and ¶246's nested quotation (below). Neither is a logic trapdoor; both are ordinary
English for this author.

## 3. Punctuation: the equaliser channel does not exist

| mark | chapter (273 ¶) | demo (10 ¶) |
|---|---|---|
| em dash — | **0** | **0** |
| en dash – | **0** | **0** |
| semicolon ; | 1 | 0 |
| colon : | 9 | **0** |
| hyphen - | 19 (all compounds: proof-of-work, peer-to-peer, self-deprecating) | 1 |
| ellipsis … | 2 | 0 |
| ( / ) | 15 / 25 (10 of the closers are list markers a)–f)) | 0 |

The colon inventory, complete:

| ¶ | left | right | function |
|---|---|---|---|
| 72 | "I ask her" | (dialogue in 73) | quotative |
| 88 | "Second Layer" | "Grycoin - A Peer-to-Peer…" | title apposition |
| 94 | "most people will be able to understand" | "the purpose is to build a global currency" | **equative** |
| 184 | "The only differences are" | "An extra I and a missing M in Satoshi." | **equative, operational** |
| 195 | "2001 | An Odyssey in Space" | film title |
| 213 | "2001 | A Space Odyssey" | film title |
| 221 | "Hal writes this" | (quote in 222) | quotative |
| 230 | "Those paragraphs are (…)" | (quote in 231) | quotative |
| 271 | "As he writes in this post" | (quote) | quotative |
| 232 | "I was more idealistic" | "I have always loved crypto" | semicolon, plain coordination |

So: four quotatives, two equatives, two title colons, one coordination semicolon. The only equative
colon that carries an operation is **¶184**, and it equates THOMAS with SATOSHI via two letters:

> The only differences are: An extra I and a missing M in Satoshi.

which is the same pair ¶193 calls "the nonces I and M" and ¶189 spells backwards into TOM. The
punctuation channel's entire yield is one sentence, and the hunt has already mined it.

**The word-internal case markers do not align with syntax either.** The full interior-case inventory is
11 tokens in 10 paragraphs: `ppM` 73, `WorldWideAbsoluteCarbonBudget` 106/112, `FUCKFuck…` 107,
`AndrewYangForPresident` 107, two checksum demos 126, `VIrgin` 128, `BItcoin` 136, `BITcoin`/`AHScoin`
209. Eight of the eleven sit **inside quoted literals** (address strings, headline terms). The two in
free syntax are `VIrgin`/`BItcoin` at ¶136, both in the same preposed temporal slot ("Before X, there
were remailers"), both her known `i`→`I` slip. **None** of the eleven follows a colon, a dash or a
comma-introduced appositive. So the hypothesis "the case marker is governed by grammatical role,
e.g. the word after an em-dash" has no instances to be tested on: there are no em-dashes, and the
equative colons are followed by `Grycoin`, `the`, `An`, `A`.

## 4. The calibration gate: put every syntactic feature through the demo first

The demo's ten paragraphs are the only text where the author states which paragraphs are marked. The
certified set is {4, 5, 6, 8} (the paragraphs that say "recognize the signs"; ¶2 is excluded by C2, ¶5
included by C3). Any candidate feature must return exactly that set:

| feature | demo paragraphs selected | |
|---|---|---|
| lexical: contains "recognize the signs" | 4, 5, 6, 8 | **MATCH** |
| lexical: contains "sign" | 4, 5, 6, 8 | **MATCH** |
| modal present | 1, 3, 6, 7, 8, 9, 10 | fail |
| conditional (if/when/once) | 3, 6, 7, 8 | fail (drops 4 and 5) |
| second person you/your | 3, 6, 7, 8 | fail |
| quotation marks | 3, 4, 6, 7 | fail |
| internal punctuation : ; - | ∅ | fail |
| imperative sentence | ∅ | fail |
| negation | 4, 5, 9 | fail |
| more than one sentence | 5, 8, 9, 10 | fail |

This is the same argument `GRAMMAR_CONSTRAINTS.md` made against the sentence-initial sign set, applied
to three new channels. It costs nothing and it is decisive before any escrow derivation: **the modal,
conditional, imperative and punctuation channels each select the wrong demo paragraphs, including ¶3
and ¶7, which are pure exposition about the format.**

## 5. The one syntactic fact the layer does carry: three byte-identical windows

| window | initials | finals |
|---|---|---|
| 5–8 | F F W W | s t n m |
| 93–96 | F F W W | s t n m |
| 168–171 | F F W W | s t n m |
| Finney reprint 231–235 | F F W [I] W | s t n g m |

Three copies, one per part of the chapter, structurally identical. This is worth stating plainly
because it constrains the search: **no structural property can discriminate between the twelve
window paragraphs.** The three windows are interchangeable at signature level, so a rule that marks
"the four" marks twelve, and a rule that marks "one of the four" has no structural reason to prefer
any window. Only content can break the tie. (The reprint window differs in one place only: its
middle paragraph ¶234 opens on the `I` that the three chapter windows do not have, and ends on `g`
because Hal's sentence ends "fascinating" — the signature there is STNGM, not STNM.)

## 6. New probe: the trigger-sentence anchor (144 derivations, zero hits)

`WORDPLAY_RULES_CATALOG.md` §32 splits the author's device into two anchors that are **not the same
edge**: "a paragraph's **first** letter may move down" and "the letter that closes **the sentence
containing the sign word** may move up". Both exemplars live in demo ¶5, whose trigger sentence is its
first sentence, so every sweep to date has collapsed the second anchor into "first-sentence-final". In
the chapter they separate: five of the twelve trigger paragraphs carry the phrase in a sentence that
is not the paragraph's first, and two of those (¶222, ¶236) put the paragraph-initial and the
trigger-sentence-initial letters on different characters (`T`/`I` and `W`/`B`).

| mode | rule | md5s | hits |
|---|---|---|---|
| T1 | paragraph-first DOWN + trigger-sentence-last UP | 4 | 0 |
| T2 | paragraph-first UP + trigger-sentence-last DOWN | 4 (= the base, a no-op control) | 0 |
| T3 | trigger sentence's own edges, first DOWN + last UP | 4 | 0 |
| T4 | trigger-sentence-last UP only | 4 | 0 |

Serialisations LF/CRLF ± trailing, indices 0/1/2/5/6/7/44/76/77 against `14zMkTga…`:
**144 derivations, 12 distinct md5, 0 hits.** T2 returning `48d31820…` is the control that the
implementation is a no-op when it should be, which is the same consistency check the word rung used.

**Implementation validation.** Applied to the demo's four paragraphs, T1 reproduces the documented
eight changes character for character: `F→f`/`s→S` (¶4), `I→i`/`f→F` (¶5), `O→o`/`i→I` (¶6),
`W→w`/`s→S` (¶8), i.e. the repo's "f…S, i…F, o…I, w…S". So the negative is about the rule, not the code.

## 7. What the demo's own ¶6 says about the anchor (the live lead)

Look at what T1 does to demo ¶6:

```
in : On the other hand, if you were able to recognize the signs and thought that the "I" at the
     beginning of the previous paragraph was one of them, you would be expected to change that
     "I" as well to a "i".
out: on the other hand, … you would be expected to change that "I" as well to a "I".
```

The rule's own mark **undoes the change the sentence is instructing**. The sentence says: change that
"I" to a lowercase "i". The mechanical mark turns the final "i" back into "I", in the same sentence,
four words later. No reading of "apply the rule to this paragraph" survives that.

That is a genuine constraint, and it is not a negative. It says that in the demo either

1. **¶6 is not in the marked set** — the phrase there sits inside a conditional ("if you were able to
   recognize the signs"), i.e. it is *mentioned* in the scope of a hypothesis rather than *used*; or
2. **the second anchor is not sentence-final** — it is attached to the word carrying the sign, which
   in ¶5 is "himself" (sentence-final by coincidence) and in ¶6 would be something other than the
   final "i".

Reading (1) is the grammatical one, and it has a clean chapter counterpart: ¶230 uses the phrase
**negated** ("the only ones where we **don't** recognize the signs") to point at the FFWW four, and the
six mentions at ¶223, 225, 226, 236, 246 (twice) all sit inside quotation marks as objects of
*saying/reading*. Classifying the twelve trigger paragraphs by assertion scope:

| scope | paragraphs |
|---|---|
| asserted by the narrator/quote, unquoted | **20, 220, 222, 244, 273** |
| mentioned inside quotation marks | 223, 225, 226, 236, 246 ×2 |
| negated (the pointer to FFWW) | 230 |
| interrogative | 42 |

That gives a **new selection set of five paragraphs** — {20, 220, 222, 244, 273} — which no sweep in
the repo has used (S3 is all twelve).

**But it fails the demo before it can be tested on the chapter.** The demo's asserted-only set is
{4, 5, 8}, and under T1 it hashes to `0b530d67…` (LF) / `f359988c…` (CRLF), neither of which begins
`3c6`. Worse, the demo's paragraph-edge space is already provably exhausted: 1,048,576 edge-toggle
combinations, 0 hits (`WORDPLAY_RULES_CATALOG` §33). So the five-paragraph set has no future at
paragraph-edge geometry. It can only be rescued by a word-level anchor — which is reading (2), the
same conclusion `GRAMMAR_CONSTRAINTS.md` reached from the other side.

## 8. Verdict and next step

- **Imperative/conditional map:** done, and it is a dead end as a selector (a section marker, 9 sites,
  all in ¶102/¶186–246; zero modals in the instruction register; the demo gate rejects it).
- **Internal punctuation audit:** done, and the channel is empty (0 dashes, 1 semicolon, 2 operational
  colons, and the demo has none at all). Do not spend more time here.
- **Where the microscope goes:** the *anchor*, not the selection. The demo's ¶6 proves the second mark
  cannot be "the paragraph's or the sentence's last letter". The residue after that proof is word-level,
  attached to the word that carries the sign, and the chapter's asserted set {20, 220, 222, 244, 273}
  is the smallest, grammatically defensible set to run it on. That is a five-paragraph, word-level
  enumeration with the demo's `3c6` gate in front of it, not another paragraph sweep.

**Running total this session:** 144 oracle derivations, 12 distinct md5, zero hits, one no-op control
returning the base.

## 9. Postscript (after the parallel pass)

`safudev_stage1.txt` is the certified stage-one **preimage** (md5 `9dd2efb9…`), and it differs from
`hal_original.txt` by exactly eight characters: paragraph-initial DOWN, paragraph-final UP, on the four
paragraphs whose initial is not in {I,T,A,S,M}. See `BLOCK29_TEMPLATE_2026-10-31.md` §2.

That settles §7 of this file against my own reading: the second anchor is the **paragraph's last letter**,
certified by digest, not "the sentence containing the sign word". The trigger-sentence arm in §5-6 is
therefore a strict superset check that was already covered by the certified geometry, and the "anchor is
not sentence-final" lead in §7 is **retired**. What survives here is the negative: the census, the demo
gate in §4, and the fact that the three windows are byte-identical in signature (§5).

Corollary worth keeping: the demo's ¶6 self-contradiction still stands on its own. Under paragraph-edge
geometry ¶6's mark is its final `i`, which its own sentence says should be lower case — so the demo's
marked set and the paragraph-edge geometry do not coexist without a further rule, and that tension is
independent of which anchor wins.
