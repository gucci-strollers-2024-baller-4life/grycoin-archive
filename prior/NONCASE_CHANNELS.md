# The channels that are not letter case (2026-10-31)

Every case family is now closed, so this pass attacks the bytes instead: what could differ between the
author's own copy and ours, in a way no case sweep can reach.

## 1. The four line-ending combinations

The repair gave ten paragraphs an internal single break. Until now only the *matched* pairings were
hashed — internal LF with paragraph LF-LF, internal CRLF with paragraph CRLF-CRLF. Her own description
("two line breaks between paragraphs", "13 10 13 10") plus single internal breaks implies the *unmatched*
pairings, which had never been hashed. None of the four md5s occurs anywhere in the repo's recorded
hashes:

| internal / paragraph | length | md5 |
|---|---|---|
| LF / LF-LF | 45,450 | `46a308c279540a33e977ea1f660e8458` |
| **LF / CRLF-CRLF** | 45,994 | `bd07e6ee209c5ab65d874bbbcfccda18` |
| **CRLF / LF-LF** | 45,460 | `52be2f2c6a51020960d50adb470230ea` |
| CRLF / CRLF-CRLF | 46,004 | `db11a7fdba7b4867a24445a7a30709b8` |

Each combination × {plain, all-paragraphs, non-ITASM, non-SATOI, the three FFWW windows, the reprint run,
the 14 "signs" paragraphs, the 13 trailing-space paragraphs, the 10 lowercase-initial paragraphs} ×
{first↓+last↑, last↑, first↓, first↓+first-sentence-final↑} at indices 0/1/2/44/76/77:
**696 derivations, zero hits.**

## 2. The typography channel: six non-breaking spaces

The chapter contains exactly six non-ASCII bytes, all `\xa0`, and every one sits immediately before a
normal space:

| paragraph | context |
|---|---|
| 90 | `as a\xa0 mechanism to extend` |
| 125 | `the exception of\xa0 transactions from coinbase` |
| 126 | `6.25 new\xa0 bitcoins under the address` |
| 126 | `on the Bitcoin network\xa0 because that address` |
| 196 | `in the anagram.\xa0 What might the third letter` |
| 257 | `heard about RPOW\xa0 in 2008` |

That is the signature of a copy-paste carrying both a NBSP and a space where the source had one space.
It is the one place where our bytes plausibly differ from hers, and it is enumerable: six sites, 2^6
subsets, two readings (NBSP deleted, NBSP turned into a plain space), four joins:

- plain: **3,072 derivations, zero hits**
- combined with the five main case sets × three edge modes: **720 derivations, zero hits**

## 3. What this leaves in the non-case space

- The six NBSP sites are also six *positions*: the words they separate are
  `a / of / new / network / anagram. / RPOW` before, and `mechanism / transactions / bitcoins / because /
  What / in` after. Their initials give `a o n n a R` / `m t b b W i`, which is not a message in either
  reading, so the sites are not a mark set.
- Untouched: punctuation edits (paragraph-final periods, the quotation-mark style), and the possibility
  that paragraph 78's `"What?"` is a substitution after all — both need either a wider enumeration or a
  source we do not have.
