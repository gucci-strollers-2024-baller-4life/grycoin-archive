# Compare and brainstorm: where the missing link can still be (2026-10-31)

## 1. Comparison with other work

**Outside.** Searches for the Grycoin reverse-Turing-test block return nothing about this puzzle:
only generic Bitcoin-puzzle threads and unrelated quizzes. No writeup, no partial solution, no claim.
That matches the chain: the escrow `14zMkT…` has received one transaction ever, in block 587833, and
has never been spent. So there is no other solver's answer to compare against. The only external
benchmarks are her own three solved examples: round-one block 77 (the genesis puzzle), demo block 2
(`grycoin`), and round-one block 29 (AOI marked by case).

**Inside ours.** Five lanes, what each rests on, and where each stands:

| lane | core claim | certified by | status |
|---|---|---|---|
| sign-set (case flips on paragraphs) | the answer is her 12 letters applied to the chapter | stage one reproduces `19TbyN5…` from `9dd2efb9…` | swept, negative |
| serialization (how the bytes join) | 13 10 13 10 between paragraphs | hint 7 + her 08-01 clarification | now swept over joins, internal breaks and tails |
| structural (windows, islands, voices) | the flip set is the FFWW/stnm windows | three exact replicas in her voice | closed, no data channel |
| dialogue / voice | signs live only in her voice | 39% vs 62% sign density | closed |
| cryptography | the key is not reverse-derivable | no nonce reuse; live key never signed | closed permanently |

## 2. What the lanes share, and which shared assumption is load-bearing

The most important thing this comparison shows is which assumption is *already proven* and which is
not, because a proven assumption is not where a missing link can hide.

**The wallet pipeline is certified, not assumed.** `md5 -> BIP39 entropy -> m/44'/0'/0'/0/0 ->
address` reproduces her published stage-one address from her published stage-one solution. A wrong
pipeline could not do that. So the pipeline is right, and every negative sweep is a negative about the
*bytes* or the *selection*, not about the derivation.

What remains assumed:

1. case-only edit of the chapter (strong: "change only the capitalization of letters in solution");
2. flip unit = first and last letter of each selected paragraph (strong: stage-one certification);
3. the hashed object is the whole part, title included (moderate: "final version of the second
   chapter" could exclude the title line);
4. the flip set is a subset of paragraphs (this is the one still doing all the work);
5. no other edit anywhere in the text.

Since 1, 2 and the pipeline are proven, and 5 is contradicted by nothing, **the missing link has to
be 3 or 4.**

## 3. Closed today

Three grids, all on the certified base and all checking both escrow addresses (`LIVE` and `OLD`) so
that a hit on the earlier solution would also be caught:

| grid | derivations |
|---|---|
| joins {LF, CRLF, single, double} x internal {LF, CRLF} x tails {"", LF, CRLF} x 9 flip sets | 2,160 |
| derivation indices 0-20, 44, 76, 77 (hint 4 mentions the 7th key) x 9 sets x 3 serializations | 1,224 |
| doubled internal breaks (she doubled every break, not just paragraph breaks) x tails x 24 indices | 9,216 |

Total **12,600 derivations, 0 hits.** Index 6 is now covered, which the earlier sweeps' index set
{0,1,2,76,77} did not cover.

## 4. Brainstorm: candidate missing links, ranked

1. **The hashed object excludes the title line.** Paragraph 1 is the single word "Second". If the
   solution begins at "I. Second Life", every sweep so far is off by one paragraph and its separator.
   Cheap to test: drop paragraph 1, re-run the two certified serializations against the same sets.
2. **The hashed object ends before the closing paragraph.** The last paragraph is the echo line
   "At least for those of us who are able to recognize the signs." An author who quotes her own
   instruction last may have hashed the text without it.
3. **The set is not a subset of paragraphs but a rule on letters.** Stage one's flips were at edges of
   paragraphs *of a post*, where every paragraph is a sentence or two. In the chapter some paragraphs
   carry ten sentences. The untested variant is edge-of-*sentence* rather than edge-of-paragraph.
4. **"All paragraphs except for four" was about the chapter after all.** The chapter has exactly four
   paragraphs in a voice that is not hers in section III (222, 231, 243, 244) and exactly four
   narrative paragraphs in each of scenes 2 and 3. If the rule is "the chapter, except four", the four
   are structural, and the flip set is the *rest* — which is a set no sweep has used because it is
   269 paragraphs long, most of them already starting with a sign letter.
5. **The two escrows used different sets.** "Slightly different solution" may mean a different flip
   set, not just a different separator. If so, `OLD` is an oracle for a set we can only guess, and any
   single-set sweep is structurally unable to hit it. This is not a test but a reason to keep testing
   both addresses (already done).

Options 1 and 2 are minutes of compute each and are the only places where the whole corpus could be
off by a boundary rather than by a rule. Option 3 is a large but bounded space. Option 4 reframes the
selection problem instead of extending it.

## 5. Boundary hypotheses, tested

Options 1 and 2 above, run against the same four flip sets and three serializations, both escrow
addresses, indices 0/1/2/6/44/76/77:

| variant | meaning |
|---|---|
| `title_out` | hash from paragraph 2 ("I. Second Life") to the end |
| `last_out` | hash paragraphs 1-272, without the closing echo line |
| `both_out` | both removed |

**504 derivations (72 preimages x 7 indices), 0 hits.** So the boundaries are not where the corpus is wrong: the object does
begin at "Second" and does run to the closing paragraph. That leaves the selection (option 4) and the
edge unit (option 3) as the live hypotheses.
