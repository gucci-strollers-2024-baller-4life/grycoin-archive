"""Single canonical loader for the chapter, in BYTE space.

Why this file exists: the chapter contains six U+00A0 characters, so `len(text)` and
`len(text.encode())` disagree (45,994 vs 46,000 in the CRLF form). Any script that took paragraph
offsets from the decoded string and then indexed the encoded bytes silently toggled the wrong
letters from character 9,084 onward. That invalidated sweeps before it was found on 2026-10-31.

Rules this module enforces:
  * the base is BYTES, and every offset handed out is a byte offset
  * every certified digest is asserted before a caller gets a base
  * every toggle position is asserted to be an ASCII letter byte
  * the non-ASCII census is explicit and stable; a new odd character fails loudly

Use:
    from corpus import chapter, toggle, drift
    b, spans = chapter("mixed")            # bytes, byte spans, md5 asserted
    b2 = toggle(b, [spans[4][0], ...])     # asserts each position is a letter
"""
import hashlib
import json
import os

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEGS_PATH = os.path.join(HERE, "wp_paras_br.json")

CERT = {
    "mixed": "bd07e6ee209c5ab65d874bbbcfccda18",   # \r\n\r\n between, \n inside
    "lf": "46a308c279540a33e977ea1f660e8458",      # \n\n between, \n inside
}
EXPECTED_NONASCII = {0x00A0: 6}                     # six non-breaking spaces, no more

# corpora that are NOT the certified chapter base. Scripts using them are sweeping a different
# object, whatever their digest assertion says.
OTHER_CORPORA = {
    "chapter_paras_exact.json": {
        "lf": "48d318202691ffb873e00b63196eaf36",
        "crlf": "f74e8e0122e114fe13c89a3bba25294a",
        "note": "same paragraphs, the ten internal line breaks collapsed; 10 chars shorter",
    },
    "wp_paras.json": {
        "note": "raw scrape: every paragraph is prefixed with its own md5, ~9,000 extra chars",
    },
}


def seeds():
    return json.load(open(SEGS_PATH, encoding="utf-8"))


def _join(kind):
    return ("\r\n\r\n", "\n") if kind == "mixed" else ("\n\n", "\n")


def chapter(kind="mixed", verify=True):
    """Return (bytes, [(start, end), ...]) with all offsets in bytes."""
    if kind not in CERT:
        raise ValueError(f"unknown base {kind!r}; use one of {sorted(CERT)}")
    join, ibr = _join(kind)
    segs = [ibr.join(p).encode() if isinstance(p, list) else p.encode() for p in seeds()]
    b = join.encode().join(segs)
    if verify:
        got = hashlib.md5(b).hexdigest()
        if got != CERT[kind]:
            raise AssertionError(f"{kind}: md5 {got} != certified {CERT[kind]}")
    spans, pos, j = [], 0, len(join.encode())
    for s in segs:
        spans.append((pos, pos + len(s)))
        pos += len(s) + j
    return b, spans


def is_letter(byte):
    return 0x41 <= byte <= 0x5A or 0x61 <= byte <= 0x7A


def toggle(b, positions):
    """Flip the case of each byte. Refuses to touch anything that is not a letter."""
    a = bytearray(b)
    for p in positions:
        if not is_letter(a[p]):
            raise AssertionError(
                f"toggle at byte {p} hits {bytes(a[p:p+1])!r}, not a letter: the offsets are "
                f"probably character offsets from the decoded string")
        a[p] ^= 0x20
    return bytes(a)


def drift(kind="mixed"):
    """[(byte_offset, char_index_of_same_neighbourhood)] for every non-ASCII char."""
    b, _ = chapter(kind)
    join, ibr = _join(kind)
    text = join.join(ibr.join(p) if isinstance(p, list) else p for p in seeds())
    out, extra = [], 0
    for i, ch in enumerate(text):
        if ord(ch) > 127:
            out.append({"char_index": i, "byte_index": i + extra, "codepoint": hex(ord(ch)),
                        "drift_after_this": extra + len(ch.encode()) - 1})
            extra += len(ch.encode()) - 1
    return out


def census(kind="mixed"):
    """codepoint -> count, over the decoded base. UTF-8 continuation bytes are not counted."""
    b, _ = chapter(kind)
    seen = {}
    for ch in b.decode("utf-8"):
        if ord(ch) > 127:
            seen[ord(ch)] = seen.get(ord(ch), 0) + 1
    return seen


def self_check(verbose=True):
    """Everything a sweep needs to be trustworthy. Raises on the first failure."""
    report = []
    for kind in ("mixed", "lf"):
        b, spans = chapter(kind)
        join, ibr = _join(kind)
        for i, (s, e) in enumerate(spans):
            want = ibr.join(seeds()[i]).encode() if isinstance(seeds()[i], list) else seeds()[i].encode()
            assert b[s:s + len(want)] == want, f"{kind}: span {i+1} misaligned"
        report.append(f"{kind}: {len(b)} bytes, {len(spans)} spans aligned, md5 ok")
        # drift must equal the census of multi-byte chars before each point
        d = drift(kind)
        report.append(f"{kind}: {len(d)} non-ASCII chars, total drift {d[-1]['drift_after_this'] if d else 0}")
    cen = census("mixed")
    if cen:
        for byte, n in cen.items():
            exp = EXPECTED_NONASCII.get(byte)
            assert exp is not None, f"unexpected non-ASCII byte {hex(byte)} x{n}"
            assert n == exp, f"expected {exp}x {hex(byte)}, found {n}"
    if verbose:
        for line in report:
            print(line)
    return True


if __name__ == "__main__":
    self_check()
    print("census:", {hex(k): v for k, v in census("mixed").items()})
    for row in drift():
        print("  ", row)
