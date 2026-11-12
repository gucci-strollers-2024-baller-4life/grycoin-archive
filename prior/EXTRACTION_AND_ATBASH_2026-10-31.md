# Isolated extractions and document-scale Atbash: both negative

**Date:** 2026-10-31

## 1. The four requested extractions, joined by `\n\n`, index 0

| subset | raw md5 | index 0 |
|---|---|---|
| W3 ¶168,169,170,171 | `cc9113dd…` | `13FAAeUEXa9oMjbgrzcjnbpGARNew3YLa9` |
| `F…t` quad ¶6,94,169,232 | `753fdc86…` | `16BYgcywdwWfhaN7YDazaVDGGW1b4KG3X2` |
| W4 ¶231,232,233,235 | `e476b4f1…` | `1FZXKz93je81ZDGZsrBD3i5iNHaXstMnYU` |
| signs ¶20,42,220,273 | `81fb80bd…` | `1P3jC7bPiZaDo5Uq2QEAodiC16L76j7tvq` |

Eight subsets in total — those four plus W1 ¶5–8, W2 ¶93–96, all five reprint paragraphs ¶231–235, and
all sixteen window paragraphs — each in five transforms (raw, head-lowered, tail-uppered, both, and the
duplicate tail) with and without a trailing LF: **80 derivations at index 0, zero hits.**

## 2. Atbash and foldover, document scale

The author's own text does support Atbash as the `Aa` meaning — ¶47 of `761570746` says "the first `Aa` as
pointer to the fact that Atbash is needed to read this code", the word appears 72 times in the corpus,
and ¶114 describes the bisection: "we can devide it into two halfs. The first one is the first sixteen
digits from 1 to M, then a capital P, then the last sixteen digits."

Nine document transforms, each with and without a trailing LF, all at index 0:

| transform | md5 | index 0 |
|---|---|---|
| full Atbash | `0d99381298…` | `1FB7QEhKVfqjDDqcPG7b6PNw6wZz1p2bS4` |
| full reversal | `aa0a8b7aff…` | `14hMZcNhfWUfvm4bf1f5HcDY14PrBtEtQo` |
| half swap | `fd97a4137d…` | `1NenrpCN2oJ6Ki8jYxmGzCC2ahKbeADDpy` |
| fold: first + reversed second | `31fbcfeab2…` | `1CXBD9FPwNXfWXpD7SRPEpJvKCMHs9Lba5` |
| fold: reversed first + second | `847c9ec0de…` | `19dMG52rb2KKwPSLnCBinNvDzmwWrpUaoW` |
| Atbash fold | `4f824d191b…` | `1Kap4MfPvjG4wzf6t1Qh1NybPXzgLxqP7p` |
| reversed paragraph order | `1ed0be9822…` | `1E3etTEevNMhbaoubnZ7kbf4tahSvXf1Nu` |
| Atbash + reversal | `eedc89007f…` | `19D3Zij7GLNiTjMSu1dTY5jZPQPkXDpgfD` |
| Atbash + reversed paragraph order | `1f34bd0825…` | `1NTKjzCJjH5Wsj6uMNtxkMEdxAxtHszaJf` |

Eighteen candidates, zero hits.

## 3. Why document-scale Atbash was never going to work

In round one the fold was applied to a **34-character base58 address** — a short, structured carrier whose
letters spell the message once folded and Atbash'd. That is what "two halves" and "the capital P" describe:
a property of the address string, not of the prose. The prose was the *question*, and its md5 produced the
address.

For stage two the address is the **output**. There is no carrier to fold between the text and the hash, so
importing the bisection is a category error: the text goes to md5 directly, and whatever encodes the
message has to be *in the text* (the FFWW marking), not in a downstream string.

## 4. Census corrections, confirmed

- "For those who don't know me" — ¶6, ¶168, ¶231. The third is the reprint, opening on a quotation mark.
  My "the chapter never uses that clause a third time" was wrong; the shingle scan had counted ¶231 as a
  full reprint and I read only its top matches.
- "young man of Japanese ancestry" — ¶187 and ¶222. ¶222 carries both this phrase and "recognize the
  signs", so the two anchors coincide there.
- "recognize the signs" — ¶20, 42, 220, 222, 223, 225, 226, 230, 236, 244, 246, 273, twelve sites.
- Hal ¶2 "I got my **start** in crypto"; Hal ¶7 "has become a mystery". Both confirmed verbatim.
