#!/usr/bin/env python3
"""chapter_tumble.py - systematic tumble of join x flip-rule variations on RBB chapter.

Oracle: md5(text) -> BIP39 12 words -> BIP32 m/44'/0'/0'/0/i -> P2PKH
Targets: LIVE 14zMkTga... (unspent), OLD 1EFojcAo... (pre-2019-07-30 escrow)

Families (flip selection sets over the 273 certified paragraphs):
  all, first-letter classes, last-letter classes, complements, mod-44 residues,
  anchor sets around the duplicated "What?" para 34 & 78 (0-based 33/77), and
  stride-44 repeated patterns.

Each paragraph flip = case op on its first alpha char and/or last alpha char.
"""
import json, hashlib, sys, time, itertools, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from demo_oracle import derive
# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)

LIVE = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
OLD = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"

WP = json.load(open(os.path.join(HERE, "wp_paras.json")))
T = [t for _, t in WP]
N = len(T)
BASES = {"exact": T, "strip": [t.rstrip() for t in T]}
JOINS = ["\n\n", "\r\n\r\n", "\n", "\r\n"]
OPS = [None, "swap", "lower", "upper"]
TRANS = [(f, l) for f in OPS for l in OPS if (f, l) != (None, None)]

LEDGER = os.path.join(HERE, "tumble_ledger.txt")
LOG = os.path.join(HERE, "tumble_log.txt")


def alpha_idx(s):
    return [i for i, c in enumerate(s) if c.isalpha()]


def first_alpha(s):
    return next((c for c in s if c.isalpha()), "")


def last_alpha(s):
    for c in reversed(s):
        if c.isalpha():
            return c
    return ""


def s1_end(p):
    for i, c in enumerate(p):
        if c in ".!?" and (i + 1 >= len(p) or p[i + 1] in " \n"):
            return p[: i + 1]
    return p


def apply_op(ch, op):
    if op == "swap":
        return ch.swapcase()
    if op == "lower":
        return ch.lower()
    if op == "upper":
        return ch.upper()
    return ch


def build(sel, base, join, trail, level, fop, lop):
    out = []
    for i, p in enumerate(base):
        if i in sel:
            seg = s1_end(p) if level == "s1" else p
            ai = alpha_idx(seg)
            if ai:
                np = list(p)
                np[ai[0]] = apply_op(np[ai[0]], fop)
                np[ai[-1]] = apply_op(np[ai[-1]], lop)
                out.append("".join(np))
                continue
        out.append(p)
    txt = join.join(out)
    if trail:
        txt += join
    return txt.encode()


def make_sets(which="singles"):
    """Return dict name -> frozenset of 0-based paragraph indices."""
    sets = {"all": frozenset(range(N))}
    letters = "abcdefghijklmnopqrstuvwxyz"
    for L in letters:
        fs = frozenset(i for i in range(N) if first_alpha(T[i]).lower() == L)
        ls = frozenset(i for i in range(N) if last_alpha(T[i]).lower() == L)
        if len(fs) > 1:
            sets["first-" + L] = fs
            sets["not-first-" + L] = frozenset(range(N)) - fs
        if len(ls) > 1:
            sets["last-" + L] = ls
    for r in range(44):
        s = frozenset(i for i in range(N) if i % 44 == r)
        if 0 < len(s) < N:
            sets["mod44-" + str(r)] = s
    # anchor sets around the duplicated "What?" pair (0-based 33 and 77)
    anchors = {
        "anchor-pair": {33, 77},
        "anchor-33+44k": {33 + 44 * k for k in range(7) if 33 + 44 * k < N},
        "anchor-77+44k": {77 + 44 * k for k in range(7) if 77 + 44 * k < N},
        "anchor-44-block-heads": {44 * k for k in range(7) if 44 * k < N},
        "anchor-44-block-tails": {44 * k + 43 for k in range(6) if 44 * k + 43 < N},
        "anchor-33-to-77": set(range(33, 78)),
        "anchor-34-to-78": set(range(34, 79)),
        "what-dups": {33, 77},
        "what-dups-plus": {33, 77, 121, 165, 209, 253},
    }
    sets.update({k: frozenset(v) for k, v in anchors.items()})
    return sets


class Runner:
    def __init__(self):
        self.seen = set()
        if os.path.exists(LEDGER):
            with open(LEDGER) as f:
                self.seen = set(l.split()[0] for l in f if l.strip())
        self.tested = 0
        self.derived = 0
        self.t0 = time.time()

    def check(self, data, cfg, idxs=(0, 1, 2)):
        h = hashlib.md5(data).hexdigest()
        if h in self.seen:
            return
        self.seen.add(h)
        with open(LEDGER, "a") as f:
            f.write(h + " " + cfg + "\n")
        self.tested += 1
        for idx in idxs:
            words, addr = derive(bytes.fromhex(h), "m/44'/0'/0'/0/%d" % idx)
            self.derived += 1
            for esc, nm in ((LIVE, "LIVE"), (OLD, "OLD")):
                if addr == esc:
                    msg = "!!!!!! %s MATCH !!!!!! cfg=%s idx=%d md5=%s\nwords=%s\n" % (
                        nm, cfg, idx, h, words)
                    print(msg, flush=True)
                    open(os.path.join(HERE, "RBB_SOLUTION.txt"), "wb").write(data)
                    with open(os.path.join(HERE, "RBB_SOLUTION_INFO.txt"), "w") as f:
                        f.write(msg)
                    sys.exit(0)

    def report(self, tag):
        el = time.time() - self.t0
        print("%s: %d texts, %d derives, %.0fs (%.0f derives/s)"
              % (tag, self.tested, self.derived, el, self.derived / max(el, 1e-9)), flush=True)


def stage_singles(r):
    sets = make_sets()
    names = list(sets)
    print("singles: %d sets x %d transforms" % (len(names), len(TRANS)), flush=True)
    for name in names:
        sel = sets[name]
        for bn, base in BASES.items():
            for join in JOINS:
                for trail in (False, True):
                    for fop, lop in TRANS:
                        cfg = "%s|%s|%r|t%d|para|%s/%s" % (name, bn, join, trail, fop, lop)
                        data = build(sel, base, join, trail, "para", fop, lop)
                        r.check(data, cfg)
        r.report("singles:" + name)
    # first-sentence level for the exact base only
    for name in names:
        sel = sets[name]
        for join in JOINS:
            for trail in (False, True):
                for fop, lop in TRANS:
                    cfg = "%s|exact|%r|t%d|s1|%s/%s" % (name, join, trail, fop, lop)
                    data = build(sel, T, join, trail, "s1", fop, lop)
                    r.check(data, cfg)
    r.report("singles-s1")


def stage_pairs(r, maxpairs=None):
    base_sets = make_sets()
    keys = [k for k in base_sets if k not in ("all",)]
    print("pairs: %d base sets" % len(keys), flush=True)
    cnt = 0
    for a, b in itertools.combinations(keys, 2):
        sel = base_sets[a] | base_sets[b]
        if not sel or len(sel) == N:
            continue
        for join in JOINS:
            for fop, lop in TRANS:
                cfg = "PAIR %s+%s|exact|%r|t0|para|%s/%s" % (a, b, join, fop, lop)
                data = build(sel, T, join, False, "para", fop, lop)
                r.check(data, cfg, idxs=(0,))
        cnt += 1
        if maxpairs and cnt >= maxpairs:
            break
    r.report("pairs")


def stage_stride44(r, kmax=2):
    """Repeated flip pattern with period 44: flip positions r mod 44 for r in pattern."""
    print("stride44: patterns up to %d residues" % kmax, flush=True)
    for k in range(1, kmax + 1):
        for pat in itertools.combinations(range(44), k):
            sel = frozenset(i for i in range(N) if i % 44 in pat)
            if not sel or len(sel) == N:
                continue
            for join in JOINS:
                for fop, lop in TRANS:
                    cfg = "STRIDE44 %s|exact|%r|t0|para|%s/%s" % (pat, join, fop, lop)
                    data = build(sel, T, join, False, "para", fop, lop)
                    r.check(data, cfg, idxs=(0,))
        r.report("stride44-k%d" % k)


def stage_mods(r, mods=(7, 11, 13, 77), pairs_for=(7, 11, 13, 77)):
    for m in mods:
        classes = {}
        for k in range(m):
            s = frozenset(i for i in range(N) if i % m == k)
            if 0 < len(s) < N:
                classes[k] = s
        keys = sorted(classes)
        print("mod%d: %d classes" % (m, len(keys)), flush=True)
        for k in keys:
            for join in JOINS:
                for fop, lop in TRANS:
                    cfg = "MOD%d %d|exact|%r|t0|para|%s/%s" % (m, k, join, fop, lop)
                    r.check(build(classes[k], T, join, False, "para", fop, lop), cfg, idxs=(0,))
        r.report("mod%d-singles" % m)
        if m in pairs_for:
            for a, b in itertools.combinations(keys, 2):
                sel = classes[a] | classes[b]
                for join in JOINS:
                    for fop, lop in TRANS:
                        cfg = "MOD%d %d+%d|exact|%r|t0|para|%s/%s" % (m, a, b, join, fop, lop)
                        r.check(build(sel, T, join, False, "para", fop, lop), cfg, idxs=(0,))
            r.report("mod%d-pairs" % m)
        if m == 7:
            for a, b, c in itertools.combinations(keys, 3):
                sel = classes[a] | classes[b] | classes[c]
                for join in JOINS:
                    for fop, lop in TRANS:
                        cfg = "MOD7 %d+%d+%d|exact|%r|t0|para|%s/%s" % (a, b, c, join, fop, lop)
                        r.check(build(sel, T, join, False, "para", fop, lop), cfg, idxs=(0,))
            r.report("mod7-triples")


def stage_words(r, words=("gycoin", "aoi", "nakamoto", "rbb", "second", "satoshi",
                          "what", "big", "real", "block", "hint", "final")):
    for w in words:
        ls = set(w)
        sel = frozenset(i for i in range(N) if first_alpha(T[i]).lower() in ls and first_alpha(T[i]))
        if not sel or len(sel) == N:
            continue
        for join in JOINS:
            for fop, lop in TRANS:
                cfg = "WORD %s|exact|%r|t0|para|%s/%s" % (w, join, fop, lop)
                r.check(build(sel, T, join, False, "para", fop, lop), cfg, idxs=(0, 1, 2))
    r.report("words")

def stage_structure(r):
    import re
    classes = {}
    def add(name, pred):
        s = frozenset(i for i in range(N) if pred(T[i]))
        if 0 < len(s) < N:
            classes[name] = s
    add("end-q", lambda p: p.rstrip().endswith("?"))
    add("end-dot", lambda p: p.rstrip().endswith("."))
    add("end-bang", lambda p: p.rstrip().endswith("!"))
    add("start-quote", lambda p: p.lstrip()[:1] in ('"', "\u201c"))
    add("short", lambda p: len(p.strip()) < 40)
    add("long", lambda p: len(p.strip()) > 200)
    add("has-what", lambda p: "What?" in p)
    add("no-words", lambda p: len(p.strip()) < 25)
    add("has-digit", lambda p: any(c.isdigit() for c in p))
    add("comma", lambda p: "," in p)
    add("colon", lambda p: ":" in p)
    add("dash", lambda p: "-" in p or "\u2014" in p)
    for m in (2, 3, 5, 22, 88, 132):
        for k in range(m):
            s = frozenset(i for i in range(N) if i % m == k)
            if 0 < len(s) < N:
                classes["mod%d-%d" % (m, k)] = s
    print("structure: %d classes" % len(classes), flush=True)
    for name, sel in classes.items():
        for join in JOINS:
            for fop, lop in TRANS:
                cfg = "STRUCT %s|exact|%r|t0|para|%s/%s" % (name, join, fop, lop)
                r.check(build(sel, T, join, False, "para", fop, lop), cfg, idxs=(0,))
    r.report("structure-singles")

    # global word-level rules (no selection)
    for join in JOINS:
        for trail in (False, True):
            for where in ("first", "last"):
                for op in ("swap", "lower", "upper"):
                    out = []
                    for p in T:
                        np = list(p)
                        for m in re.finditer(r"[A-Za-z]+", p):
                            k = m.start() if where == "first" else m.end() - 1
                            np[k] = apply_op(np[k], op)
                        out.append("".join(np))
                    txt = join.join(out) + (join if trail else "")
                    cfg = "WORDRULE %s/%s|%r|t%d" % (where, op, join, trail)
                    r.check(txt.encode(), cfg, idxs=(0, 1, 2))
    r.report("wordrules")

def stage_windows(r, lengths=(7, 11, 22, 44, 77, 88)):
    """Contiguous paragraph windows: flip all paragraphs inside one window."""
    for L in lengths:
        for start in range(0, N - L + 1):
            w = frozenset(range(start, start + L))
            for join in JOINS:
                for fop, lop in TRANS:
                    cfg = "WIN L%d s%d|exact|%r|t0|para|%s/%s" % (L, start, join, fop, lop)
                    r.check(build(w, T, join, False, "para", fop, lop), cfg, idxs=(0,))
            if L == 44:
                comp = frozenset(range(N)) - w
                for join in JOINS:
                    for fop, lop in TRANS:
                        cfg = "WINNOT L44 s%d|exact|%r|t0|para|%s/%s" % (start, join, fop, lop)
                        r.check(build(comp, T, join, False, "para", fop, lop), cfg, idxs=(0,))
        r.report("windows-L%d" % L)


def stage_excluded(r, maxset=3):
    """Stage-one generalization: flip paras whose first letter is NOT in letter set S, |S|<=maxset."""
    import string
    letters = string.ascii_uppercase
    for k in range(1, maxset + 1):
        for S in itertools.combinations(letters, k):
            Ss = set(S)
            sel = frozenset(i for i in range(N) if first_alpha(T[i]) and first_alpha(T[i]).upper() not in Ss)
            if not sel or len(sel) == N:
                continue
            for join in JOINS:
                for fop, lop in TRANS:
                    cfg = "EXCL %s|exact|%r|t0|para|%s/%s" % ("".join(S), join, fop, lop)
                    r.check(build(sel, T, join, False, "para", fop, lop), cfg, idxs=(0,))
        r.report("excluded-k%d" % k)

if __name__ == "__main__":
    stage = sys.argv[1]
    r = Runner()
    if stage == "singles":
        stage_singles(r)
    elif stage == "pairs":
        stage_pairs(r, int(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif stage == "stride44":
        stage_stride44(r, int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    elif stage == "words":
        stage_words(r)
    elif stage == "mods":
        stage_mods(r)
    elif stage == "structure":
        stage_structure(r)
    elif stage == "windows":
        stage_windows(r)
    elif stage == "excluded":
        stage_excluded(r, int(sys.argv[2]) if len(sys.argv) > 2 else 3)
    r.report("DONE " + stage)
    print("no match in stage", stage, flush=True)
