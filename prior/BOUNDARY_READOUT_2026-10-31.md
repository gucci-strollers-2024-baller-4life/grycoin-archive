# The boundary read-out: 24 words, and they carry one block of information three times

**Date:** 2026-10-31
**Base:** `wp_paras_br.json`, mixed, md5 `bd07e6ee…`, self-check clean, 273 spans.
**Script:** `sweeps/boundary_readout.py`, results in `sweeps/boundary_readout_results.json`.
**Derivations run:** none. Nothing here touches the case-inversion results.

## M1: the 12 + 12 boundary words

| window | ¶ | initial word | BIP39 | terminal word | BIP39 |
|---|---|---|---|---|---|
| W1 | 5 | First | ✔ | keys | – |
| W1 | 6 | For | – | that | ✔ |
| W1 | 7 | When | ✔ | again | ✔ |
| W1 | 8 | When | ✔ | them | – |
| W2 | 93 | For | – | purposes | – |
| W2 | 94 | Fairly | – | budget | ✔ |
| W2 | 95 | When | ✔ | emission | – |
| W2 | 96 | When | ✔ | them | – |
| W3 | 168 | For | – | this | ✔ |
| W3 | 169 | Face | ✔ | object | ✔ |
| W3 | 170 | While | – | Dorian | – |
| W3 | 171 | While | – | them | – |

```
initials  : First For When When For Fairly When When For Face While While
terminals : keys that again them purposes budget emission them this object Dorian them
```

**BIP39: 6/12 initial, 5/12 terminal, 11/24 combined.** Neither 12-word set is a legal mnemonic
(6/12 and 5/12 are far below the 12/12 a real seed needs). 24 is a legal *length*, but an illegal
word list, so the checksum never even gets computed.

The acrostics are the whole answer, and they are degenerate:

```
initial acrostic  : F F W W F F W W F F W W
terminal acrostic : s t n m s t n m s t n m
```

So the three-window read-out is **one four-letter string, repeated three times.** That is the reason
the tri-coordinate model cannot produce a seed: it has four letters of content and twelve words of
output. Three copies of `stnm` are three confirmations of the same quad, not three coordinates.
Whatever `stnm` + `I` is worth in ¶236–¶239, W1–W3 add no second, third or fourth letter to it, and
no amount of re-reading the three windows will make them.

## The one word-level echo worth having

Position 4 closes on the literal word **"them"** in all three windows *and* in the source:

| position | W1 | W2 | W3 | source |
|---|---|---|---|---|
| 1 | keys | purposes | this | activities |
| 2 | that | budget | object | it |
| 3 | again | emission | Dorian | reaction |
| 4 | **them** | **them** | **them** | **them** |

Positions 1–3 share no word with the source. Position 4 shares the *word*, not just the letter. That
is a small but real upgrade to the mimicry claim: at that slot the author reproduced the token, not
the termination class. It also means the 24-word read-out contains "them" three times, which is not
a BIP39 word at all.

## M2: the deltas are one interval short and one assumption long

| quantity | value |
|---|---|
| W1 start → W2 start | **88** |
| W2 start → W3 start | **75** |
| W3 start → ¶231 (the reprint) | 63 |

Three novel windows give **two** intervals: 88 and 75. The third number, 63, is measured to ¶231,
which is the reprint. So the triple `88, 75, 63` only exists if ¶231 counts as a coordinate alongside
W1–W3, which is exactly the uniform 16-paragraph-pool assumption the same message retires. The model
needs the anchor it just eliminated.

Independently: 88, 75 and 63 all exceed 44, so none of them can index the 44-character solution
string. As character offsets into the chapter they are worse than useless: all three land inside ¶4,
within 25 characters of each other.

```
offset 63 -> " I'd write about my seco"
offset 75 -> 'bout my second coming, a'
offset 88 -> 'd coming, an unusual eve'
```

## M3: the book-cipher model was already executed

Nothing in this read-out tests it. Worth stating plainly though: stage one *was* an external payload
(`hal_original.txt`), and that is the version of the rule that worked. Running the rule on the chapter
is the version that has now failed 2^16 and 131,071 times. The read-out above gives no reason to
prefer a third external target over the one that already produced a key.

## The lead-in paragraphs

| window | ¶ | initial | first word | closing word |
|---|---|---|---|---|
| W1 | 4 | I | I | in |
| W2 | 92 | I | I | now |
| W3 | 167 | I | I | years |

Closing letters: `n`, `w`, `s`. No relation to `stnm`, and the source's lead-in (hal ¶1, "…Bitcoin and
me.") closes on `e`, so `n/w/s` is not the template's property.

Their real feature is simpler: **all three windows are led in by an I-initial paragraph immediately
before them.** The source has the same shape, hal ¶1 being `I`-initial and immediately preceding ¶2.

That produces the structural version of the correction already made on evidential grounds: W4 is
`¶231, ¶232, ¶233, ¶235` and its immediate predecessor is ¶230, *"Having seen the signs before…"*,
initial `H`. W4 has no I lead-in because the chapter's reprint starts at hal ¶2 and drops hal ¶1. So
the shape is:

```
I-paragraph, then F F W [I] W with tails s t n m   ->  W1, W2, W3, and the source
                                                    ->  not W4
```

This is the ¶238 claim ("the I as the first letter in the paragraphs close to that") holding on all
four true instances and failing on the reprint. The caveat that keeps it honest: 47 of 273 paragraphs
are I-initial, so an I-lead-in is a 17% feature, not a locator on its own. It discriminates W4 from
W1–W3 and it does not name anything new.

## 118 vs 121: neither, and it does not matter

Every convention I can reproduce:

| convention | out of `{I,T,A,S,M}` |
|---|---|
| first **alphabetic** character, case-folded, all 273 | **119** |
| first **alphabetic** character, case-sensitive | **121** |
| raw character at index 0 | 149 |
| body only, 27 headings excluded | 103 |

The 119/121 gap is exactly two paragraphs, ¶176 `a) Satoshi's birthday` and ¶250 `a) ALS Condition`,
where the lowercase `a` folds into the class. Raw index 0 is much larger because **63 of 273
paragraphs open with a straight quotation mark** (the chapter is dialogue-heavy) and 10 open with a
lowercase lettered subheading, so a `^([A-Z])` anchor silently misreads a quarter of the chapter.

No convention gives 118. The most likely explanation is a one-paragraph difference in which headings
are counted, and I am not going to defend a number I cannot reproduce from the certified base. What
matters is the range: 103 to 149, against a hypothesis that needs exactly 4. The conclusion is
unmoved by the ambiguity, which is the only reason it is safe to leave the discrepancy open.

## Verdict

The read-out question is answered and the answer is negative. The boundary words carry `stnm` three
times, 11/24 are BIP39, neither 12-word array validates, and the deltas are two numbers plus a
retracted third. M1 and M2 both close.

What the read-out does hand over is a cleaner statement of the thing that actually distinguishes the
three witnesses from the reprint: **an I-initial paragraph immediately before the block.** That is a
structural predicate, not a statistical one, it holds 4/4 including the source, it fails on W4, and
it is the same predicate ¶238 names. If anything is to be swept next it should be that, on external
documents, where a block can be found rather than asserted.
