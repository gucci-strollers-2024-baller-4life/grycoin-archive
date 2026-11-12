#!/usr/bin/env python3
"""Resumable sweep: chapter 'AOI marked inside one sentence' family.

Candidate = chapter text with the three letters spelling AOI (uppercased) inside a
single sentence (the block-29 'vOIce' mechanic). Each candidate: MD5 -> BIP39 ->
m/44'/0'/0'/0/{0,1,2} -> P2PKH, compared with both escrows.

Resumable: progress in aoi_chapter_progress.json, hits appended to aoi_chapter_hits.txt.
Usage: python3 aoi_chapter.py [budget_seconds]
"""
import json, re, hashlib, sys, time, os
# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

sys.path.insert(0, '.')
try:
    from demo_oracle import derive            # needs bip_utils
except Exception:                             # dependency-free fallback (audit 2026-10-31)
    sys.path.insert(0, 'harness')
    import fast2

    def derive(h, idx):
        return fast2.addr_from_key(fast2.key_at(fast2.seed_from(bytes.fromhex(h)), idx))

T1 = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"   # live RBB escrow (2 line breaks version)
T2 = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"   # original escrow (1 line break version)
PROG = "aoi_chapter_progress.json"
HITS = "aoi_chapter_hits.txt"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0

P = [x[1] for x in json.load(open('wp_paras.json'))]
JOINS = ['\n\n', '\r\n\r\n']

prog = json.load(open(PROG)) if os.path.exists(PROG) else {"join": 0, "span": 0, "done": 0}
t0 = time.time()
stop = False

for ji in range(prog["join"], len(JOINS)):
    join = JOINS[ji]
    txt = join.join(P)
    base = txt.encode()
    # AUDIT GUARD (2026-10-31): this script used wp_paras.json element [1], which is the
    # chapter_paras_exact object (LF md5 48d31820...), ten characters short of the published
    # text (the ten internal line breaks are collapsed). It also indexes these (character)
    # offsets into the encoded bytes, and the chapter holds six U+00A0 characters. Both make a
    # candidate set meaningless. Refuse to run until re-pointed at wp_paras_br.json with byte
    # spans from harness/corpus.py.
    CERT_MD5 = {"bd07e6ee209c5ab65d874bbbcfccda18", "46a308c279540a33e977ea1f660e8458"}
    assert hashlib.md5(base).hexdigest() in CERT_MD5, (
        "aoi_chapter: base is not the published chapter "
        f"(md5 {hashlib.md5(base).hexdigest()[:8]}); rebuild from wp_paras_br.json")
    spans = [(m.start(), m.end()) for m in re.finditer(r'[^.!?]+', txt)]
    start_span = prog["span"] if ji == prog["join"] else 0
    for si in range(start_span, len(spans)):
        s, e = spans[si]
        pA = [i for i in range(s, e) if txt[i].upper() == 'A']
        pO = [i for i in range(s, e) if txt[i].upper() == 'O']
        pI = [i for i in range(s, e) if txt[i].upper() == 'I']
        if pA and pO and pI:
            for a in pA:
                for o in pO:
                    if o <= a:
                        continue
                    for i in pI:
                        if i <= o:
                            continue
                        b = bytearray(base)
                        for x in (a, o, i):
                            c = chr(b[x])
                            if c.islower():
                                b[x] = ord(c.upper())
                        h = hashlib.md5(bytes(b)).hexdigest()
                        prog["done"] += 1
                        for idx in range(3):
                            w, addr = derive(bytes.fromhex(h), f"m/44'/0'/0'/0/{idx}")
                            if addr in (T1, T2):
                                rec = f"HIT join={join!r} pos={(a,o,i)} idx={idx} addr={addr} words={w} md5={h}\n"
                                open(HITS, 'a').write(rec)
                                print("!!!!!! CHAPTER SOLVED " + rec, flush=True)
                                json.dump(prog, open(PROG, 'w'))
                                sys.exit(0)
                        if time.time() - t0 > BUDGET:
                            stop = True
                            prog["join"] = ji
                            prog["span"] = si
                            json.dump(prog, open(PROG, 'w'))
                            print(f"paused at join {ji} span {si}, tested {prog['done']} candidates in {time.time()-t0:.0f}s", flush=True)
                            sys.exit(2)
        prog["join"] = ji
        prog["span"] = si + 1
        if si % 200 == 0:
            json.dump(prog, open(PROG, 'w'))
    prog["join"] = ji + 1
    prog["span"] = 0
    json.dump(prog, open(PROG, 'w'))

print(f"COMPLETE: {prog['done']} candidates tested, no match", flush=True)
