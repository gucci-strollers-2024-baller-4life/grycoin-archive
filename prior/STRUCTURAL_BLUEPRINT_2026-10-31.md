# Structural blueprint of "Second" (live-source verified)

**Date:** 2026-10-31
**Object:** Wattpad part 720888559, chapter "Second", 273 paragraphs.
**Provenance:** read live from `https://www.wattpad.com/apiv2/storytext?id=720888559` in a browser
session on 2026-10-31. 59,613 bytes, 273 `data-p-id` paragraphs, every `p-id` identical to
`wp_paras.json` in this repo. Paragraph numbers below are 1-indexed over those 273.

**Status vocabulary used throughout:** `VERIFIED` = mechanically checked against the live bytes in
this session. `INFERRED` = a reading consistent with the text, not forced by it. `OPEN` = undecided.

**This file supersedes four earlier hypotheses.** The self-referential-header reading of ¶242, the
"arity fracture / swallowed comma", the "`Like,` register break", and the "¶243-244 scar" are each
falsified below, with the check that falsifies it, so they are not re-proposed.

---

## 1. VERIFIED: ¶242 is an external pointer, not a self-description

¶242 does not describe its own container. The paragraph it names is ¶222, twenty paragraphs back,
and the two extracts are printed immediately after it at ¶243 and ¶244.

```
222  "Today, Satoshi's true identity has become a mystery. But at the time, I thought I was dealing
     with a young man of Japanese ancestry who was very smart and sincere. I've had the good fortune
     to know many brilliant people over the course of my life, so I recognize the signs."   [51 words]

242  The first four and last four words of the paragraph hinting at the solution.
243  "Today, Satoshi's real identity"
244  "I recognize the signs."
245  Take the first words of that together and you get "Today, I". Like, "today I come out as Satoshi".
246  Take the next three words together and you get "Satoshi's real identity, recognize the signs".
     Like, "if you want to know Satoshi's real identity, recognize the signs (at the end of the
     relevant paragraphs).
```

Checks:

- ¶222 opens `Today, Satoshi's` and closes `so I recognize the signs.` Its first four words are
  `Today, Satoshi's, true, identity` and its last four are `I, recognize, the, signs.`
- ¶222 is a verbatim reprint of ¶7 of Hal Finney's "Bitcoin and me" (`hal_original.txt`, 16
  paragraphs, this text at line 13), so the hinted paragraph is Hal's words, not the narrator's.
- ¶242 itself contains a finite-less imperative with elided verb, exactly parallel to ¶245 and ¶246
  which both begin with `Take`. Three consecutive instructions: 242 states the operand set, 243-244
  supply the operands, 245-246 the two operations.

**Consequence:** the eight words do not need to be reconstructed or counted off any other paragraph.
They are given. Any procedure that reads ¶242's *own* first four and last four words is reading the
instruction instead of its target.

---

## 2. VERIFIED: ¶243 is not a verbatim extract (`true` -> `real`)

¶222 and ¶243 disagree in exactly one word, the third of four.

| source | words 1-4 |
|---|---|
| ¶222 and `hal_original.txt` | `Today, Satoshi's **true** identity` |
| ¶243 | `Today, Satoshi's **real** identity` |

¶244 is exact. `real identity` occurs nowhere in ¶222 and nowhere in Hal's post.

This is the only self-quotation in all 273 paragraphs that is not verbatim, and it is the only place
where the narrator quotes a source and silently improves it. **VERIFIED** as a fact about the bytes.
**INFERRED** as intent: the substitution is thematic (the chapter's whole frame is simulation versus
the real, ¶9 `I wonder if I live in the real world right now`), so it may be a deliberate marker
rather than an error. Not settled, and it does not need to be settled to use the rule.

**Doctrine this establishes:** the author paraphrases when she quotes herself. Quotations in this text
are evidence of intent, never evidence of bytes. Every preimage built from her quoted strings is
therefore unverified by construction, which is a sufficient explanation for that whole family of
certified negatives.

**Corroborating instance, same class.** In the demo block (`demo_base.txt`, 10 paragraphs) she writes
*"if the letter 'n' at the end of the last paragraph was part of the solution, you would be expected to
change it to 'N' and write 'capitalizatioN'"*. The word `capitalization` ends **¶2 of 10**, not the
last paragraph. So her positional deictics are also unreliable: she indexes a paragraph by a trait
that identifies it, not by where it sits. That is consistent with ¶242 naming its target by definite
description (`the paragraph hinting at the solution`) rather than by index.

---

## 3. VERIFIED: the marker geometry is paragraph-initial down, first-sentence-final up

The demo block fixes the geometry in its own worked example, and it is asymmetric in a way the corpus
sweeps did not test.

- ¶5 of the demo begins `I expected otherwise, but actually not many people do recognize the signs…`
- ¶6 refers to *"the 'I' at the beginning of the previous paragraph"*: that is ¶5's paragraph-initial
  `I`.
- ¶7 states the result: *"you would end up changing 'I' to 'i' and 'himself' to 'himselF'"*.
- `himself` is not ¶5's last word. It is the last word of ¶5's **first sentence**. ¶5 then continues
  `Even after I explained the method used and the result in detail.`

So the pair is **paragraph-initial lowered, first-sentence-final raised**. Not paragraph-final.

**Polarity, also from the demo (¶8):** *"once you do that for all the paragraphs where you recognize
the signs. And keep the rest completely unchanged."* The marked set is the **in-class** set. The
out-of-class paragraphs are read, not modified: in Hal's post the four paragraphs that do not begin in
the sign class are ¶2, ¶3, ¶4, ¶6, and it is their final letters that spell `S T N M`.

Verified against `hal_original.txt`: paragraph initials are `I F F W I W T A T S M A T I A T`. Twelve
paragraphs begin in `{I,T,A,S,M}`; the four that do not are ¶2 (`F`), ¶3 (`F`), ¶4 (`W`), ¶6 (`W`),
matching ¶229 *"All paragraphs except for four, which start with F F and W W"* and ¶230's *"with one
paragraph starting with I in between"* (¶5). Final letters of ¶2/3/4/6: `activities`→s,
`it`→t, `reaction`→n, `them`→m.

**Consequence:** previous edge-inversion masks paired paragraph-initial with paragraph-final, or
sentence-initial with sentence-final. The author's own example pairs paragraph-initial with
first-sentence-final. That pairing is the one the text licenses.

---

## 4. VERIFIED: the chapter carries the STNM signature three times at word level

Three runs of exactly four consecutive paragraphs beginning `F, F, W, W`, one per major division.
The final letters of their terminal words spell `STNM` in each case.

| window | division | terminal words | letters |
|---|---|---|---|
| ¶5-8 | I. Second Life | keys, that, again, them | s t n m |
| ¶93-96 | II. Grycoin | purposes, budget, emission, them | s t n m |
| ¶168-171 | III. Second Identity | this, object, Dorian, them | s t n m |

Full evidence:

- ¶5 `…All the words I need to use my keys.` → s
- ¶6 `…more people know me under the name I created from that.` → t
- ¶7 `…Feels good to be alive again.` → n
- ¶8 `…And of course I believed them.` → m
- ¶93 `For starters, define the project's purposes.` → s
- ¶94 `…the purpose is to build a global currency for the carbon budget.` → t
- ¶95 `…It will be up to the users to set parity rates of grycoins to CO2 emission.` → n
- ¶96 `…set a relation that is approximately correct between them.` → m
- ¶168 `…the most simple and elegant solution for this.` → s
- ¶169 `…it makes sense to object.` → t
- ¶170 `…some media circus like in the case of Dorian.` → n
- ¶171 `…If you want your privacy protected, you need them.` → m

Two properties matter more than the reading itself.

1. **The unit is the last letter of the last word, not the last character of the paragraph.** All
   twelve paragraphs end in a full stop, so a character-level edge read returns nothing but `.` in
   every position. A word-level read returns `STNM` three times. This is the same unit ¶242 names
   (`words`), and it is the reason character-edge masks over these windows were empty.
2. **The signature matches ¶237 (`STNM`) and ¶239 (`I STNM.`), which sit inside the rulebook at
   ¶228-246, inside section 2d, the section that quotes the text the rulebook explains.** The document
   states its own signature and then carries it three times.

`OPEN`: whether the three windows are decorative self-endorsement (marking divisions) or the payload
channel. Nothing in the text yet forces one reading; the answer bears on whether any window is a
substrate for a case flip.

---

## 5. Falsified hypotheses, with the check that kills each

| hypothesis | status | falsifying check |
|---|---|---|
| ¶242 is a self-referential container header for a 2x4 grid | **falsified** | ¶243/244 are extracts of ¶222 (§1); the eight words are supplied, not to be derived from ¶242 |
| ¶246's numeral/quote mismatch is an intentional arity fracture forcing a multidimension read | **falsified** | ¶245 fixes the convention one paragraph earlier: `the first words of that` yields **two** words, one per half. `next three words` in ¶246 therefore yields six by the same rule. Consistent distributive arithmetic, no fold forced |
| the comma in ¶246 is a structural separator swallowed into a quoted span | **falsified** | the comma exists nowhere in ¶222; she inserted it while assembling her own two 3-word groups. ¶246 also opens a metalinguistic quotation mark it never closes. Both are composition marks, not quotation marks |
| `Like,` marks a localized register break and a syntactic beacon | **falsified** | exactly **2** occurrences in 273 paragraphs, one per decoding paragraph, because there are two decoded fragments. Voice is continuous across the whole stretch: ¶225 `So what's up with that`, ¶238 `I wonder what that could mean`, ¶240 `That's a fun coincidence`, ¶241 `I leave it as an exercise for the reader` |
| ¶243-244 is the scar where the removed twist lived, detectable as broken anaphora | **falsified** | ¶243/244 are the operands of ¶242. The scar is elsewhere: §2 (word substitution) and the July 30 2019 note (serialization) |
| out-of-class paragraphs receive the case marker | **falsified** | demo ¶8: mark the paragraphs where you **recognize** the signs, `keep the rest completely unchanged`; and in Hal's post the out-of-class four are read for `STNM`, not modified (§3) |

### Where the removed twist actually lives

Author's own words, 2019-07-30 (`agntn/aoinakamoto-2019-07-22-cgkpbb.md`):

> Took back the funds from the address above and sent them to a new address, funding transaction below,
> because I wanted to remove one of the twists I had. The block is now slightly easier. **It is also
> hashed with two line breaks between paragraphs now.**

That is a statement about the **serialized byte stream**, not about prose. A twist removed at that
layer leaves no broken anaphora and no missing antecedent. It leaves a difference in separators. And
the certification we hold covers paragraph **text** only: `p-id` = MD5(paragraph text), 272 of 273
direct plus one Wattpad dedup hash. Separators are outside what that certifies, on either side of the
change. **Any hunt for the removed twist belongs in the line-ending and blank-line layer, not in the
grammar of ¶243-244.**

---

## 6. What this fixes for the final run

1. **Channel:** case only, at word edges. Anything that lowercases, case-folds, strips punctuation or
   normalizes whitespace before hashing destroys the only channel the author used.
2. **Unit:** the word, not the character stream. ¶242 says `words`; the three STNM windows only resolve
   at word granularity (§4).
3. **Geometry:** paragraph-initial lowered, **first-sentence-final** raised (§3). Not paragraph-final.
4. **Selection:** by a trait the text names (`paragraphs where you recognize the signs`), not by index.
   The author's own positional deictic is wrong in the demo (§2), so index arithmetic derived from
   her prose is not trustworthy.
5. **Serialization is a live variable**, stated by the author, and uncertified by `p-id` (§5). Two line
   breaks between paragraphs is her stated post-2019-07-30 form.
6. **Quoted strings are not bytes** (§2). Derive from the live paragraph text, never from her quotes.

---

## 7. Status ledger

| # | claim | status |
|---|---|---|
| 1 | ¶242 indexes ¶222, twenty paragraphs back | VERIFIED |
| 2 | ¶243 substitutes `real` for `true`; only non-verbatim self-quote in 273 paragraphs | VERIFIED (fact); INFERRED (intent) |
| 3 | marker = paragraph-initial down + first-sentence-final up | VERIFIED against demo ¶5-¶7 |
| 4 | marked set is the in-class set; out-of-class is read, unchanged | VERIFIED against demo ¶8 |
| 5 | Hal's post: 12 of 16 paragraphs begin in `{I,T,A,S,M}`; exceptions ¶2,3,4,6 = F,F,W,W | VERIFIED |
| 6 | three `FFWW` windows at ¶5-8, ¶93-96, ¶168-171 spell `STNM` at word level | VERIFIED |
| 7 | the three windows are division markers vs. payload channel | OPEN |
| 8 | location of the twist removed 2019-07-30 | OPEN; serialization layer per author's note |
| 9 | `real` substitution is deliberate and load-bearing | OPEN |
