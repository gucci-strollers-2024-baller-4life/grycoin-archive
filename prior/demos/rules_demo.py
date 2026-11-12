"""Demo (grycoin block 2): deterministic rule battery against the 3c6 oracle + escrow.

Why rules and not a sweep: the demo's blind spaces are closed up to four arbitrary flips
(hammered by a GPU hunt, >100B candidates) and five flips at word boundaries. What is left
needs five or more arbitrary positions, about 10^14 candidates, which no single-core run can
touch. A *rule* costs one candidate, so every rule the demo text itself implies is worth
checking.

Structural facts this uses (verified, not assumed):
  - all ten paragraphs end with '.', so a paragraph-*final letter* flip is impossible here;
    the last flippable letter of a unit is the final letter of its last word;
  - the demonstrated pair sits at byte 535 ('I', paragraph 5 initial) and byte 652 ('f' of
    "himself", the last word of paragraph 5's first sentence).

Usage: python3 demos/rules_demo.py
"""
import hashlib, re, sys, os, itertools

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import fast2

LIVE_H, OLD_H = fast2.h160(fast2.LIVE), fast2.h160(fast2.OLD)
DEMO_H = fast2.h160(fast2.DEMO)
IDX = (0, 1, 2, 3, 4, 5, 6)
ORACLE = "3c6"

T = open(os.path.join(HERE, "demo_base.txt"), encoding="utf-8").read()
BASE_MD5 = hashlib.md5(T.encode()).hexdigest()
assert BASE_MD5.startswith("7759227"), BASE_MD5


def spawn(text, sep="\n\n"):
    out, pos = [], 0
    for p in text.split(sep):
        out.append((pos, pos + len(p)))
        pos += len(p) + len(sep)
    return out


def sentences(text, paras):
    out = []
    for s, e in paras:
        cur = s
        for m in re.finditer(r"[.!?](\s+|$)", text[s:e]):
            out.append((cur, s + m.start() + 1))
            cur = s + m.end()
        if cur < e:
            out.append((cur, e))
    return out


def last_word_letter(text, s, e):
    w = re.findall(r"[A-Za-z]+", text[s:e])
    if not w:
        return None
    return s + max(m.start() for m in re.finditer(re.escape(w[-1]) + r"", text[s:e]))


def toggle(text, poss):
    b = bytearray(text.encode("utf-8"))
    for p in sorted(set(poss)):
        c = b[p]
        b[p] = c + 32 if 65 <= c <= 90 else c - 32
    return bytes(b)


def rules(text):
    P = spawn(text)
    SENT = sentences(text, P)

    def flip(pos, case):
        if pos is None or pos < 0 or pos >= len(text):
            return None
        c = text[pos]
        if not c.isalpha():
            return None
        if case == "d" and c.isupper():
            return pos
        if case == "u" and c.islower():
            return pos
        return None

    def lastletter(s, e):
        idx = [i for i in range(s, e) if text[i].isalpha()]
        return idx[-1] if idx else None

    def sig(paras):
        out = []
        for i in paras:
            s, e = P[i - 1]
            a = flip(s, "d")
            if a is not None:
                out.append(a)
            first = [x for x in SENT if s <= x[0] < e]
            if first:
                b = flip(lastletter(*first[0]), "u")
                if b is not None:
                    out.append(b)
        return out

    init = [text[s] for s, e in P]
    allp = list(range(1, len(P) + 1))
    R = {
        "sig_all": sig(allp),
        "sig_FWI": sig([i + 1 for i, c in enumerate(init) if c in "FWI"]),
        "sig_FW": sig([i + 1 for i, c in enumerate(init) if c in "FW"]),
        "sig_I": sig([i + 1 for i, c in enumerate(init) if c == "I"]),
        "init_down_only_all": [p for p in (flip(s, "d") for s, e in P) if p is not None],
        "caps_all_down": [i for i, c in enumerate(text) if c.isupper()],
        "sent_last_up": [p for p in (flip(lastletter(s, e), "u") for s, e in SENT)
                         if p is not None],
        "sent_init_down_last_up": (
            [p for p in (flip(s, "d") for s, e in SENT) if p is not None]
            + [p for p in (flip(lastletter(s, e), "u") for s, e in SENT) if p is not None]),
        "para_last_up": [p for p in (flip(lastletter(s, e), "u") for s, e in P)
                         if p is not None],
        "every_word_last_up": [p for p in (flip(m.end() - 1, "u")
                                           for m in re.finditer(r"[A-Za-z]+", text))
                               if p is not None],
        "signs_word_last_up": [p for p in (flip(m.end() - 1, "u")
                                          for m in re.finditer(r"signs", text))
                               if p is not None],
        "signs_word_init_down": [p for p in (flip(m.start(), "d")
                                            for m in re.finditer(r"signs", text))
                                if p is not None],
        "standalone_I_down_plus_sent_last_up": (
            [p for p in (flip(m.start(), "d") for m in re.finditer(r"\bI\b", text))
             if p is not None]
            + [p for p in (flip(lastletter(s, e), "u") for s, e in SENT) if p is not None]),
        "stated_pair": [535, 652],
        "stated_pair_swapped": [535, 652],
    }
    signp = [i for i, (s, e) in enumerate(P) if "signs" in text[s:e]]
    R["signs_paras_word_last_up"] = [
        p for p in (flip(m.end() - 1, "u")
                    for i in signp
                    for m in re.finditer(r"[A-Za-z]+", text[P[i][0]:P[i][1]]))
        if p is not None]
    return {k: v for k, v in R.items() if v}


def main():
    print(f"demo bytes={len(T)} md5={BASE_MD5} paragraphs={len(spawn(T))} "
          f"sentences={len(sentences(T, spawn(T)))}")
    hits = oracle = n = 0
    for join in ("\n", "\r\n"):
        text = T if join == "\n" else T.replace("\n", "\r\n")
        print(f"  base md5 for join={join!r}: {hashlib.md5(text.encode()).hexdigest()}")
        R = rules(text)
        print(f"join={join!r}: {len(R)} rules, flips="
              f"{ {k: len(set(v)) for k, v in sorted(R.items())} }")
        for name, poss in sorted(R.items()):
            variants = [(name, poss)]
            if set(poss) != {535, 652}:
                variants.append((name + "+stated", list(poss) + [535, 652]))
            for tag, pp in variants:
                try:
                    h = hashlib.md5(toggle(text, pp)).hexdigest()
                except ValueError:
                    continue
                n += 1
                if h.startswith(ORACLE):
                    oracle += 1
                    print(f"  ORACLE 3c6: {tag} join={join!r} flips={len(set(pp))} {h}")
                    for idx in IDX:
                        a = fast2.addr_from_key(
                            fast2.key_at(fast2.seed_from(bytes.fromhex(h)), idx))
                        if fast2.h160(a) in (LIVE_H, OLD_H, DEMO_H):
                            hits += 1
                            print("  *** ESCROW HIT", tag, join, idx, a, flush=True)
    print(f"candidates={n} oracle_hits={oracle} escrow_hits={hits}")


if __name__ == "__main__":
    main()
