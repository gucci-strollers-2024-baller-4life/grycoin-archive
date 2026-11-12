# Closed by exhaustive search: the eight-token address-decode answer

Space: every ordering of every legal 2-ciphertext + 2-plaintext split from the address decode
vocabulary, set 1 from {1A1, efi2DM, efiYDM, efiYNN} + {Hal, Finney, TOM}, set 2 from
{TS, mN, NmST} + {Satoshi, Nakamoto}, concatenated as `set1 set2`, six link fields, MD5, indices 0-2.

| quantity | value |
|---|---|
| strings | 31,104 |
| links x indices | 6 x 3 |
| derivations | 559,872 |
| coverage | 100 percent (112,752 + 450,000 + 127,872 across three passes) |
| hits | 0 |

Verdict: **the RBB answer is not a string of eight tokens drawn from the address decode.** This is the
first family closed by complete enumeration instead of sampling, so it can be struck from the board.

Machine note: the sandbox has 1 CPU core, so multiprocessing does not help; a full pass at
about 450 derivations per second costs roughly 20 minutes.

## What remains open

1. the copy/reference asymmetry: 231-235 is split by the `I` paragraph, the three seamless windows
   (5-8, 93-96, 168-171) are copies of it, and no test has yet used a copy as a rendering of the original
2. the flip selection itself, which every enumerated family has failed to reproduce
