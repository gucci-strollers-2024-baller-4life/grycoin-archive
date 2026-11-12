# The demo fails calibration, but the casing paradigm does not

**Date:** 2026-10-31 **Base:** `demo_base.txt` (md5 `7759227d7406d8230d7e3a8f7b9846d7`).
**Targets:** prefix `3c6`; escrow `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi`. Indices 0, 1, 2.

## 1. The premise needs one correction

The demo names `I`→`i` and `himself`→`himselF`, but its own next clause is *"which would be the solution,
once you do that for all the paragraphs where you recognize the signs."* Those two characters are the
worked illustration, not the answer. A two-flip search cannot falsify the rule, because the rule's own
statement says the answer is a *set* of recognised signs. The earlier 717,003-candidate pass over one- and
two-character flips is therefore a test of the illustration, not of the mechanism.

## 2. The second named flip is not a paragraph endpoint

In `demo_base.txt`, "himself" sits at ¶5, mid-paragraph: *"…in Satoshi's Bitcointalk post outing himself.
Even after I explained the method used…"*. It is the last letter of a **sentence**, not of a paragraph. So
the demo's two signs are a sentence-initial `I` and a sentence-final `f`, and the demo teaches
sentence-boundary selection rather than paragraph-boundary selection. That has never been calibrated, and
it matters: the chapter has 273 paragraphs but roughly fifteen hundred sentences.

## 3. What the boundary rules produce on the demo

| rule | md5 | prefix | index 0 |
|---|---|---|---|
| stated two flips | `932fe1a55110f95b60bbbfc4ca548f85` | `932` | `17kFBYuenWHKLnz7FS7S6cEGFd12vWsqoA` |
| stated two flips + trailing `\n` | `510d367c0fd33a64ee28076c5842362c` | `510` | `1JNWbEBmpVX8hr7K3ZZJtvfWNTpFK1uoaq` |
| all paragraph-initial down + final up | `a37126a89e9485a562d1ea9a73fb4a52` | `a37` | `1PeMiMhMLErQJKuVuE9QtPVi3aJmXv4dKW` |
| all paragraph-initial down | `b31ad58e261d3869b3fcb072a12981a4` | `b31` | `1H6nLzWPuzEZqDgykp3nAJRb4KmDMp8sS8` |
| all paragraph-final up | `079a767878f163491a4fbc1ffa52adf2` | `079` | `1LgUEUjjASh1XPYcKfAbwkEcNEEA6HmPRn` |
| all sentence-initial down + final up | `9ba6e7b795a2470950f4745a9d672689` | `9ba` | `12bZez2S1KxuSpxkGzy43azA8hcvt2S2KS` |
| all sentence-initial down | `f2d3ff7619b79d4734eccf05db4e238a` | `f2d` | `13WXR85bPq5mH4MKabo1fNM8Ci2rQnHvbv` |
| all sentence-final up | `60203051ad21f295eb385750f3a2fa17` | `602` | `12RFHRH7N2xhw9R5cpgpnW84dtJvcQZBWM` |
| all word-initial down + final up | `70e418db71d424033a08ad622a3d1fc7` | `70e` | `1KJQaaLv5ZUaFT5SzKRTHVvkqNFH8n15dm` |

None begins `3c6`, and none reaches `1tzieUf…` at indices 0–2. So the demo's published prefix is not
reproduced by any boundary rule tested, including the one its own example instantiates.

## 4. Why that does not falsify case flipping

Stage one is a verified known-answer for exactly this mechanism. `safudev_stage1.txt` is the bitcointalk
post with eight characters' case flipped, four paragraphs, both ends each: `F→f`, `W→w`, `s→S`, `t→T`,
`n→N`, `m→M` across ¶2, ¶3, ¶4 and ¶6. Its md5 `9dd2efb9bc976c2095bd534d7b8d431c` derives
`19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` at index 0, re-derived in this sandbox at every index 0–80.

That is the only fully verified preimage-to-escrow chain in the entire puzzle, and it is a case flip. If
case flipping were a decoy, the author could not have built stage one that way. So the demo is best read as
a **replica problem or an author typo**, not as a refutation: either `demo_base.txt` is not byte-identical to
the span she hashed, or `3c6` is wrong. Both readings are testable and neither licenses abandoning the
mechanism that stage one certifies.

## 5. The question as asked

*"What operation could relate the raw chapter text to the MD5 without changing cases?"* On the evidence,
none is needed, and none is motivated. The author states that both phases use the demo's format, that format
is case edits on retained text, and the one verified instance of it works. The open variable remains
selection: which units count as signs. The demo points at sentences, stage one used paragraphs.
