"""Builds the corrected RBB base text from Wattpad's authoritative paragraphs.

wp_paras_br.json holds each paragraph as a list of segments split on the chapter's internal <br>
line breaks (10 paragraphs: 63, 73, 121, 124, 146, 160, 184, 189, 193, 213). Wattpad's own
`length` (45,451) equals sum(chars) 44,896 + 10 breaks + 2*272 separators + 1 trailing newline,
so the segment model reproduces the stored text exactly.
"""
import json, hashlib, sys

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

SEGS = json.load(open('wp_paras_br.json'))
VARIANTS = {
    'base_chapter_lf.txt':    ('\n\n',    '\n',   ''),     # browser copy / Wattpad export
    'base_chapter_crlf.txt':  ('\r\n\r\n','\r\n', ''),     # Windows draft throughout
    'base_chapter_mixed.txt': ('\r\n\r\n','\n',   ''),     # Windows paragraph breaks, LF inside
}
if __name__ == '__main__':
    sys.path.insert(0, 'harness')
    for name, (join, ibr, trail) in VARIANTS.items():
        text = join.join(ibr.join(s) for s in SEGS) + trail
        open(name, 'w', newline='').write(text)
        h = hashlib.md5(text.encode()).hexdigest()
        addr = ''
        try:
            import btc; addr = btc.addr_from_md5hex(h)
        except Exception:
            pass
        print(f"{name:26s} bytes={len(text.encode()):6d} chars={len(text):6d} md5={h} {addr}")
    print("Wattpad stored length: 45,451 (= text chars + 1 trailing newline)")
