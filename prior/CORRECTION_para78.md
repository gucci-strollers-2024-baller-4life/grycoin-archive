# Correction: paragraph 78 was never edited. All 273 paragraphs certify.

Source: floflo777 issue #39 (blue-horikon, 2026-10-24) via `ninjaops-puzzle-lanes/PROGRESS.md`
commit d9b1675. Wattpad stores a repeated paragraph with pid = **md5(previous_md5_hex + "1")** on
the second occurrence.

Checked against paragraph 78:

    md5('"What?"')                  = 184826be0ea6837abb5851807f7a9e2b
    md5("184826be...9e2b" + "1")    = 8b71bade9685d3388452bc4755b06a0d   <- the stored pid

Exact match. So 8b71bade is Wattpad's dedup hash for the *second* occurrence of `"What?"`, not the
hash of some pre-edit sentence.

## Full certification with the dedup rule

    paragraphs 273 | direct pid match 272 | dedup-rule match 1 | unmatched 0
    repeated paragraph hashes: 1 (paras 34 and 78, '"What?"')

**The chapter has no unmatched paragraph hash at all**, which means there is no edit anomaly
anywhere in the 273 paragraphs.

## What this corrects

1. Earlier note in this repo (README, RBB_DOSSIER line 23) said para 78's pid mismatch proved the
   author overwrote it with `"What?"` on 2019-07-23. **False.** The duplicate is original text.
2. BTCxanter's lead from 2026-10-10 - "the only anomaly in Second is line 78 ... we need to find the
   sentence that unlocks this MD5 hash" - is answered and dead. The hash is self-explanatory.
3. The 44-paragraph `"What?"` duplicate (paras 34 and 78) is therefore a *designed feature of the
   hashed text*, not an editing artifact. It keeps its full value as an index anchor, and it is
   present in whatever text was hashed.
4. Similarly, BTCxanter's later point that edited Wattpad stories show hash mismatches is true in
   general but has no application here: this chapter shows zero mismatches.

## Consequence for the hunt

Any reconstruction of the hashed text must keep paragraphs 34 and 78 identical, and must keep all
273 paragraph bodies as they are. The open variable is only the *serialisation* (join between
paragraphs), not the wording.
