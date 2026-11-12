# The sentence unit: calibrated on the author's own worked example, then swept. Negative.

**Date:** 2026-10-31
**Script:** `sweeps/sentence_signs.py`, results in `sentence_signs_results.json`.
**Fast lane validated** against `harness/btc.py` before the run (standing rule).
**Derivations:** 1,080 (120 texts × 9 indices). **Hits: 0.**

## 1. Calibration first, because the unit is the open question

`CLUES_CANONICAL` §13.4 is explicit that the demo's worked example is sentence-level: *"I expected…"* is
the first sentence of demo ¶5 and *"himself"* is that sentence's last word. So before sweeping anything,
the sentence machinery has to reproduce the author's own quoted pair. It does, as a hard assertion in
the script:

```
demo ¶5 sentence 1  "I expected…himself."
        after       "i expected…himselF."       2 moves
```

Both quoted changes fall out, and nothing else in the sentence moves. Anything below is the same
operator at chapter scale.

## 2. The chapter at sentence scale

| | |
|---|---|
| paragraphs | 273 |
| sentences | **664** |
| mean | 2.43 per paragraph |
| max | 7 in one paragraph |

Which matters for the variable in question. **"Which sentences carry signs, and how many" is a free
subset of 664 units: 2^664.** That is not a sweep and never can be. The variable as stated has no
tractable exhaustive form; it becomes sweeppable only when a *rule* names the sentences, and no rule has
been specified anywhere in the corpus. What follows is therefore not that variable closed. It is the
tractable part: every alphabet-rule selection, at sentence granularity, in three unit definitions.

## 3. Sentence counts per alphabet

| alphabet | sentence-initial in class | out of class |
|---|---|---|
| `{I,T,A,S,M}` | 377 | 287 |
| `{S,A,T,O,H,I}` | 427 | 237 |
| `{A,I,M,O,S,T}` | 413 | 251 |
| `{T,H,O,M,A,S}` | 311 | 353 |
| `{T,H,O,M,A,S,I}` | 439 | 225 |

Note these are sentence-initial sets, so they are not the paragraph sets and the paragraph counts do not
transfer.

## 4. The sweep

Three units, because "sentence-level" is ambiguous at chapter scale:

- `st` — sentence head down, sentence tail up (the unit the demo demonstrates)
- `pt_st` — paragraph head down, **first sentence** tail up (what the demo's ¶5 example becomes when
  generalised, and the reading `CLUES_CANONICAL` §13.4 supports)
- `st_pt` — sentence head down, paragraph tail up

× five alphabets × in-class and out-class × four serialisations × nine indices
(0, 1, 2, 5, 6, 7, 44, 76, 77), screened against `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`.

**120 texts, 1,080 derivations, 0 hits.** Full md5 and index-0 table in the results file. Every
selection moves real capitals: the smallest is 412 moves, the largest 1,290.

One near-miss worth naming so it is not mistaken for signal later: `SATOSHI`, out-class, `st`, index 0
is `14z8tsJTqoyur67FvDyaTT51ewVDXfGcrf`, which shares the first three characters with the escrow
`14zMkTga…`. At 120 texts the expected count of `14z` prefixes is ~0.1, so it is noise. It is not a hit
and should not be treated as one.

## 5. Scope note, and one correction

**What is not new.** `SATOMI` and `THOMAS` are both already in the `CLUES_CANONICAL` §13.3 family table
(1,408 candidates, 0 hits), and `{A,I,M,O,S,T}` is SATOMI's letter set. So the paragraph-level
carrier/anomaly selection under this alphabet was already swept before `fb3cb47`, at index 0 and on two
derivation paths. What `fb3cb47` and this entry add is the **minimality argument** (why six letters and
which six, with `H` undetermined) and the **sentence unit**, not the alphabet as a family name.

**What is still open, per the corpus rather than per recollection.** There is no `§13.9` in
`CLUES_CANONICAL`. That section runs §13.1 to §13.5 and stops. The sentence *"The variable §13.9 names is
untouched: which sentences carry signs, and how many"* is your own line in `SAT_SET_TRANSPORT_2026-10-31.md`
§84, so the citation is circular: it points at itself. The forward-looking text is §13.5, whose open
items are:

1. demo name-marking with the C flipper for `FINNEY` (92.1M in-order embeddings), `THOMAS` (177.1M),
   `GRYCOIN` (123.6M), `NAKAMOTO` (1.05e9), `SATOMMI` (0.92e9);
2. re-run the chapter's sign-set families with the SATOSHI set instead of ITASM.

Item 2 is now done twice over (`e3b32b3`, `b8b6f32`, and `fb3cb47`/`d6675c3` here). Item 1 is the only
cheap decisive-looking thing left in §13.5 and it is demo-side, not chapter-side. The sentence variable
is real as a question, but it is not a named item in the canonical record, and as §2 shows it is not
sweepable as posed.

## 6. State

Closed this pass: sentence-granularity alphabet selection under five alphabets, three unit definitions,
four joins, nine indices.

Standing negative list: window payloads, the 61 scattered sites, pentads and `I`-target readings, lexical
and directive selectors, the 44-char string, the `FFWW` locator reading, paragraph-level transport of
every carrier and anomaly set (strict, forced, nine lanes), and now sentence-level selection.

The two things that would change the shape of this are a rule for *which* sentences are signs, or
evidence that the transport unit is neither paragraph nor sentence. Both are specification problems, not
search problems, and neither is anywhere in the corpus yet.
