"""The single edit in the Finney reprint: 'facinating' (Hal, and her certified stage-one text)
-> 'fascinating' (chapter). One letter inserted, 1,289 letters into the quotation.

Two readings tested here:
  (a) the answer's preimage keeps Hal's spelling, i.e. the stage-two solution restores the typo;
  (b) the restore is inert and the edit means nothing positionally.

Costs one derivation per candidate, so every plausible mask is layered on top of the restored
text as well.
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import fast2

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)

LIVE_H, OLD_H = fast2.h160(fast2.LIVE), fast2.h160(fast2.OLD)
IDX = (0, 1, 2, 76, 77)
SEGS = json.load(open(os.path.join(HERE, "wp_paras_br.json")))
CERT = {"lf": "46a308c279540a33e977ea1f660e8458", "mixed": "bd07e6ee209c5ab65d874bbbcfccda18"}
n = hits = 0


def base(kind):
    join, ibr, step = ("\n\n", "\n", 2) if kind == "lf" else ("\r\n\r\n", "\n", 4)
    text = join.join(ibr.join(p) for p in SEGS)
    assert hashlib.md5(text.encode()).hexdigest() == CERT[kind]
    spans, pos = [], 0
    for p in SEGS:
        t = ("\n".join(p)).encode()          # BYTE spans: six U+00A0 chars shift offsets
        spans.append((pos, pos + len(t)))
        pos += len(t) + step
    return text, spans


def check(blob, tag):
    global n, hits
    h = hashlib.md5(blob).digest()
    for idx in IDX:
        n += 1
        addr = fast2.addr_from_key(fast2.key_at(fast2.seed_from(h), idx))
        if fast2.h160(addr) in (LIVE_H, OLD_H):
            hits += 1
            print("*** HIT", tag, idx, h.hex(), addr, flush=True)
    return h.hex()[:8]


def toggle(text, poss):
    a = bytearray(text.encode())
    for p in poss:
        a[p] ^= 32
    return bytes(a)


def edges(text, spans, paras):
    out = {}
    for p in paras:
        s, e = spans[p - 1]
        f = next((i for i in range(s, e) if text[i].isalpha()), None)
        seg = text[s:e]
        m = re.search(r"[.!?](?=\s|$)", seg)
        cut = s + (m.end() if m else len(seg))
        ls = [i for i in range(s, cut) if text[i].isalpha()]
        out[p] = (f, ls[-1] if ls else None)
    return out


for kind in ("mixed", "lf"):
    text, spans = base(kind)
    restored = text.replace("fascinating", "facinating")
    assert len(restored) == len(text) - 1
    print(f"--- {kind}: published {hashlib.md5(text.encode()).hexdigest()[:8]}  "
          f"restored len {len(restored)} prefix {check(restored.encode(), 'restore_only')}")
    sp2, pos = [], 0
    step = 2 if kind == "lf" else 4
    for p in SEGS:
        t = ("\n".join(p)).replace("fascinating", "facinating").encode()
        sp2.append((pos, pos + len(t)))
        pos += len(t) + step
    for name, paras in (("finney4", [231, 232, 233, 235]),
                        ("finney5", [231, 232, 233, 234, 235]),
                        ("reprint+222", [222, 231, 232, 233, 235])):
        E = edges(restored, sp2, paras)
        variants = {
            "down_up": [(f, "d") for f, _ in E.values()] + [(l, "u") for _, l in E.values()],
            "down_down": [(f, "d") for f, _ in E.values()] + [(l, "d") for _, l in E.values()],
            "fin_up": [(l, "u") for _, l in E.values()],
            "init_down": [(f, "d") for f, _ in E.values()],
        }
        for vname, spec in variants.items():
            pos_list = []
            for q, mode in spec:
                if q is None:
                    continue
                c = restored[q]
                if (mode == "d" and c.isupper()) or (mode == "u" and c.islower()):
                    pos_list.append(q)
            if not pos_list:
                continue
            tag = f"{name}/{vname}/{len(pos_list)}f"
            print(f"  restored+{tag}: {check(toggle(restored, pos_list), tag)}")
print(f"derivations={n} hits={hits}")
