#!/usr/bin/env python3
"""The chapter plants Hal's full signature three times, not just his initials.

Window firsts/lasts (wp_paras_br.json):
    5-8     FFWW / stnm
    93-96   FFWW / stnm
    168-171 FFWW / stnm
    231-235 FFWIW / stngm   <- the Finney reprint, natural, I between the W's

Chance of one window spelling stnm in order is ~2e-4, so the three exact replicas are
deliberate. Her 2019-08-03 reply says the letters to change are "obvious if you know the
solution to Satoshi's bitcointalk puzzle": in Hal's post those are the F,F,W,W paragraphs,
firsts lowered and lasts raised.

This sweep applies exactly that, on certified bases, to:
  - each window alone, all three together
  - the same widened by the paragraphs either side of it (never in any 2^16 closure)
  - every paragraph in the chapter whose (first,last) completes the signature
    F->s, F->t, W->n, W->m (29 paragraphs, incl. the quoted dialogue lines)
Usage: python3 sweep_signature.py
"""
import itertools, json, sys
import rbb_probe as R

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

CERT = {
    ("wp_paras_br.json", "crlf2"): "bd07e6ee209c5ab65d874bbbcfccda18",
    ("wp_paras_br.json", "lf2"): "46a308c279540a33e977ea1f660e8458",
    ("chapter_paras_exact.json", "crlf2"): "f74e8e0122e114fe13c89a3bba25294a",
    ("chapter_paras_exact.json", "lf2"): "48d318202691ffb873e00b63196eaf36",
}
PAIRS = {"F": "st", "W": "nm"}


def load(path):
    return ["\n".join(p) if isinstance(p, list) else p for p in json.load(open(path, encoding="utf-8"))]


def edge(t, last=False):
    rng = range(len(t) - 1, -1, -1) if last else range(len(t))
    return next((j for j in rng if t[j].isalpha()), None)


def flip(t, down=True):
    s = list(t)
    for last in (False, True):
        j = edge(s, last)
        if j is not None:
            s[j] = s[j].lower() if down else s[j].upper()
    return "".join(s)


def first_alpha(t):
    j = edge(t)
    return t[j] if j is not None else ""


def last_alpha(t):
    j = edge(t, True)
    return t[j] if j is not None else ""


def main():
    assert R.addr_at(bytes.fromhex("9dd2efb9bc976c2095bd534d7b8d431c"), 0) == R.STAGE1, "stage-one selftest FAILED"
    bases = []
    for fn in ("wp_paras_br.json", "chapter_paras_exact.json"):
        ps = load(fn)
        for jn, j in (("crlf2", "\r\n\r\n"), ("lf2", "\n\n")):
            t = j.join(ps)
            if R.md5b(t).hex() != CERT[(fn, jn)]:
                sys.exit("base certification FAILED %s/%s" % (fn, jn))
            bases.append((fn, jn, j, ps))
    print("base certification PASS", flush=True)

    paras0 = bases[0][3]
    sig = [i + 1 for i in range(len(paras0))
           if first_alpha(paras0[i]) in PAIRS and last_alpha(paras0[i]) in PAIRS[first_alpha(paras0[i])]]
    print("signature-completing paragraphs:", sig, flush=True)

    W = [(5, 8), (93, 96), (168, 171)]
    allw = [i for a, b in W for i in range(a, b + 1)]
    sets = {
        "w1": list(range(5, 9)), "w2": list(range(93, 97)), "w3": list(range(168, 172)),
        "w123": allw,
        "w1+prev": [4] + list(range(5, 9)), "w2+prev": [92] + list(range(93, 97)),
        "w3+prev": [167] + list(range(168, 172)),
        "w1+next": list(range(5, 10)), "w2+next": list(range(93, 98)), "w3+next": list(range(168, 173)),
        "w123+both": sorted({4, 9, 92, 97, 167, 172} | set(allw)),
        "signature_all": sig,
        "signature_no_dialogue": [i for i in sig if not paras0[i - 1].lstrip().startswith('"')],
    }
    print("sets:", {k: len(v) for k, v in sets.items()}, flush=True)

    seen = {}
    for fn, jn, j, ps in bases:
        for name, st in sets.items():
            for down in (True, False):
                out = list(ps)
                for p in st:
                    out[p - 1] = flip(out[p - 1], down)
                seen.setdefault(R.md5b(j.join(out)), (fn, jn, name, down))
    print("unique preimages:", len(seen), flush=True)

    hits = []
    for h, meta in seen.items():
        for i in (0, 1, 2, 76, 77):
            got = R.addr_at(h, i)
            if got in (R.LIVE, R.OLD):
                print("HIT!!", meta, "idx", i, got, h.hex(), flush=True)
                hits.append({"meta": [meta[0], meta[1], meta[2], meta[3]], "idx": i, "addr": got, "md5": h.hex()})
    print("DERIVATIONS:", len(seen) * 5, "HITS:", len(hits), "DONE", flush=True)
    json.dump(hits, open("sweep_signature_hits.json", "w"), indent=1)


if __name__ == "__main__":
    main()
