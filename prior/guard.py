"""Runtime guard for sweep scripts. One import plus one call, at the top of the file.

    from guard import install
    install(__file__)

What it does before the script is allowed to transform anything:

1. **Certified corpus parity.** Finds every chapter corpus the script mentions and re-derives its
   canonical digests. If a canonical source no longer matches its certified value, it raises. Base
   identity is checked by hash, never assumed.
2. **Drift-pattern refusal.** Statically rejects the char/byte mixing bug that voided sweeps on
   2026-10-31: an offset accumulator built with `len(<str>)` in a file that mutates bytes. Byte
   accumulators (`len(x.encode())`) pass.
3. **Non-canonical corpus notice.** `chapter_paras_exact.json` and `wp_paras.json` are legitimate
   objects but are NOT the published chapter. A script that builds its base from them gets a loud
   notice, because its result cannot be read as a test of the RBB base.

Set GUARD_QUIET=1 to suppress the success line. Failures always raise.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

CANONICAL = {
    "wp_paras_br.json": {
        "mixed": "bd07e6ee209c5ab65d874bbbcfccda18",
        "lf": "46a308c279540a33e977ea1f660e8458",
    },
}
OTHER = {
    "chapter_paras_exact.json": {
        "mixed": "f74e8e0122e114fe13c89a3bba25294a",
        "lf": "48d318202691ffb873e00b63196eaf36",
    },
    "wp_paras.json": {
        "mixed": "f74e8e0122e114fe13c89a3bba25294a",
        "lf": "48d318202691ffb873e00b63196eaf36",
    },
}
# the ten internal line breaks collapse in these two, so they are 10 chars short of the published text
NONCANONICAL_NOTE = ("is NOT the published chapter: the ten internal line breaks are collapsed, "
                     "10 characters short. Results apply to that object only.")

_DONE = set()


def _join(kind):
    return ("\r\n\r\n", "\n") if kind == "mixed" else ("\n\n", "\n")


def _digest(path, kind, indexed):
    S = json.load(open(os.path.join(HERE, path), encoding="utf-8"))
    if indexed:      # wp_paras.json records are [paragraph_md5, text]
        S = [r[1] if isinstance(r, list) and len(r) > 1 else r for r in S]
    join, ibr = _join(kind)
    segs = [ibr.join(p).encode() if isinstance(p, list) else p.encode() for p in S]
    return hashlib.md5(join.encode().join(segs)).hexdigest()


# scripts read line by line and confirmed to work entirely in character space (2026-10-31). They
# keep offsets and their offsets' consumers on the same str, so there is nothing to drift.
REVIEWED_CHARSPACE = {
    "verify_blocks.py": "fmap, SequenceMatcher and both corpora are str throughout",
    "verify_corpora.py": "casefolded str LCS, no byte indexing at all",
    "pal2.py": "paragraph coverage map, str throughout",
    "verify_full.py": "paragraph coverage map, str throughout",
    "verify_posts.py": "paragraph coverage map, str throughout",
    "harness/sweep1.py": "scans a str with isalpha(); no encoded base in the file",
}

ACC = re.compile(r"^\s*[\w\.\[\]]+\s*\+=\s*(.+)$")
ASSIGN = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*(.+?)\s*$")
FORLOOP = re.compile(r"^\s*for\s+([A-Za-z_]\w*)\s+in\s+([A-Za-z_]\w*)\s*:")
BYTE_SIGNAL = (".encode(", "bytes(", "bytearray(", 'b"', "b'")
STR_SIGNAL = ("join(", ".read(", "json.load", "'", '"')


def _classify(src):
    """tiny dataflow: which names hold bytes, which hold str"""
    kind = {}
    for line in src.splitlines():
        if line.lstrip().startswith("#"):
            continue
        m = FORLOOP.match(line)
        if m and m.group(2) in kind:
            kind[m.group(1)] = kind[m.group(2)]
            continue
        m = ASSIGN.match(line)
        if not m:
            continue
        name, rhs = m.group(1), m.group(2)
        if any(sig in rhs for sig in BYTE_SIGNAL):
            kind[name] = "byte"
        elif any(sig in rhs for sig in STR_SIGNAL):
            kind[name] = "str"
    return kind


def check_source(source_path):
    """Static checks on the script's own text."""
    src = open(source_path, encoding="utf-8", errors="replace").read()
    problems = []
    touches_chapter = any(k in src for k in list(CANONICAL) + list(OTHER))
    if not touches_chapter:
        return problems
    kind = _classify(src)
    for i, line in enumerate(src.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if "len(" not in line:
            continue
        offsetish = ("+=" in line or "pos + len(" in line or "pos+len(" in line
                     or "pos +len(" in line)
        if not offsetish:
            continue
        if re.search(r"\b\w+\s*\+=\s*\d+\s*$", line):
            continue
        if os.path.basename(source_path) in REVIEWED_CHARSPACE:
            return problems
        for m in re.finditer(r"len\(\s*([A-Za-z_]\w*)\s*(\.encode)?", line):
            name, encoded = m.group(1), m.group(2)
            if encoded:
                continue
            if kind.get(name) == "str":
                problems.append(
                    f"{os.path.basename(source_path)}:{i} offset accumulator built from the "
                    f"character length of {name!r}: {line.strip()!r}. The chapter holds six U+00A0 "
                    f"characters; encode first or use harness/corpus.py.")
    return problems


def install(source_path=None, quiet=None):
    """Called from the top of a sweep script. Raises on any integrity failure."""
    if quiet is None:
        quiet = os.environ.get("GUARD_QUIET") == "1"
    path = os.path.abspath(source_path or sys.argv[0])
    if path in _DONE:
        return True
    src = open(path, encoding="utf-8", errors="replace").read() if os.path.exists(path) else ""
    notes = []

    for corpus in CANONICAL:
        if corpus not in src:
            continue
        for kind, want in CANONICAL[corpus].items():
            got = _digest(corpus, kind, indexed=False)
            if got != want:
                raise SystemExit(
                    f"GUARD: {corpus} {kind} digests to {got}, certified is {want}. "
                    f"The corpus changed; every sweep built on it is void until resolved.")
        notes.append(f"{corpus} certified")

    for corpus, digests in OTHER.items():
        if corpus not in src:
            continue
        for kind, want in digests.items():
            got = _digest(corpus, kind, indexed=(corpus == "wp_paras.json"))
            if got != want:
                raise SystemExit(
                    f"GUARD: {corpus} {kind} digests to {got}, recorded is {want}.")
        msg = f"GUARD NOTICE: {corpus} {NONCANONICAL_NOTE}"
        print(msg, file=sys.stderr)
        notes.append(f"{corpus} non-canonical")

    problems = check_source(path)
    if problems:
        raise SystemExit("GUARD: drift pattern refused:\n  " + "\n  ".join(problems))

    _DONE.add(path)
    if not quiet and notes:
        print(f"GUARD ok ({os.path.basename(path)}): " + ", ".join(notes), file=sys.stderr)
    return True


if __name__ == "__main__":
    digests = {"canonical": {}, "other": {}}
    for corpus, kinds in CANONICAL.items():
        for kind, want in kinds.items():
            got = _digest(corpus, kind, indexed=False)
            digests["canonical"][f"{corpus}:{kind}"] = {"want": want, "got": got,
                                                        "ok": got == want}
    for corpus, kinds in OTHER.items():
        for kind, want in kinds.items():
            got = _digest(corpus, kind, indexed=(corpus == "wp_paras.json"))
            digests["other"][f"{corpus}:{kind}"] = {"want": want, "got": got, "ok": got == want}
    print(json.dumps(digests, indent=2))
    bad = [k for group in digests.values() for k, v in group.items() if not v["ok"]]
    sys.exit(1 if bad else 0)
