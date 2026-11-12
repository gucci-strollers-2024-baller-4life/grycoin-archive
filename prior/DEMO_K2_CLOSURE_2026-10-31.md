# The demo block cannot be reproduced at one or two letters, so the inversion rule is uncalibrated

**Date:** 2026-10-31

## 1. What the author says the demo solution is

`demo_base.txt` (1,549 chars, md5 `7759227d…`) is the certified hashed slice: first `I` of the question to
the period after the last "method". In ¶7 the author writes the answer out himself:

> When you do that, you would end up changing "I" to "i" and "himself" to "himselF".

Both characters are in ¶5, so the solution is demo_base with ¶5's endpoints inverted: exactly **two**
characters change, `I→i` at the head and `f→F` at the tail of "himself".

    ¶5 flipped, LF    md5 731aee6b14fb9865f52d854635ffbf8c   addr0 1C38QnE5dFnPtF6D43zk7uD3X3RPRq9ET3
    ¶5 flipped, CRLF  md5 0a896c73724dc98145b9663fdf8ca734   addr0 1ErrmAAqjNvjaXPKzRBMp2tYDnrm8vYRTW

**Neither begins `3c6`.** Derived at indices 0 through 5, neither reaches the demo escrow
`1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` either.

## 2. The space around it, exhausted

Every one- and two-character case flip of the whole text, 1,197 alphabetic positions,
`1197·1198/2 = 717,003` candidates, screened on the published 12-bit oracle:

| | count |
|---|---|
| candidates | 717,003 |
| begin `3c6` | 162 (~175 expected at chance) |
| derive to the demo escrow at indices 0, 1, 2 | **0** |

The 162 survivors are positional garbage, e.g. flipping `g` at offset 6 and `t` at 1,032 gives `3c62edfd…`.

So the demo is not reproducible by the rule the demo describes, at k ≤ 2, anywhere in its own text, at any
of the three lowest indices. This compounds `DEMO_PARADOX` with a hard bound rather than a suspicion.

## 3. What that means for the chapter

Every chapter sweep in this repository is an application of the same rule: select paragraphs, invert their
endpoints. The demo is the only instance in the family where the answer is published, the hashed object is
certified, and the escrow is known — and the rule fails on it at the only cardinality the author names
("a couple of letters").

That does not prove the chapter's escrow is unreachable, but it does mean the inversion family is
uncalibrated: it has never once been shown to produce a correct answer on a known-answer instance.
Running the 36,856 two-paragraph pairs on the chapter would be 36,856 more trials of a rule whose single
ground-truth case is already negative.

## 4. Three smaller answers

- **¶75–¶80** are the "So what is the problem?" / "What?" exchange inside section 3, quoted in the session
  log; ¶78 sits between Aoi's "two ways to make sure of adoption" line and her Turing-test explanation.
- **The single newline in `safudev_stage1.txt`** is inside ¶16, not between paragraphs:
  `"…I'm comfortable with my legacy.\n[edited slightly]"`. A `<br>` in the Bitcointalk post renders as one
  LF. That certifies the `<br> → \n` treatment used at the chapter's ten break sites.
- **¶254** is `c) Mail Conversation With Himself`. Its head `c` is already lowercase, and its last
  alphabetic character is the `f` of "Himself", so the standard rule changes exactly **one** character
  (`HimselF`). My "no-op" in the previous turn was wrong.
