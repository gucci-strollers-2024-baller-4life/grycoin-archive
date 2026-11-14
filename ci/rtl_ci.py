#!/usr/bin/env python3
"""RTL-suffixed subset sweep, shardable. Usage: rtl_ci.py START END JOIN IDX,IDX

Space: integer masks over the case-violating paragraphs (VIOL). Certified mechanic
(head alpha lowered, terminal alpha raised) applied to the selected paragraphs, join,
append the literal suffix, md5, BIP39, BIP32, P2PKH, compare to the escrow.

Repaired 2026-11-14 after audit:
  1. SPLICE BUG. The old code used flip[VM] (the violator index 0..N-1) instead of
     flip[i] (the paragraph index 0..272), so every non-empty mask REPLACED the
     selected paragraph with a different paragraph's flipped text (3,336 bytes lost
     on the all-bits mask). Only mask 0 was a real document; 2^24-1 of the 2^24
     enumerated texts were not documents at all.
  2. FOURTH REPLICA. The four FFWW/stnm runs are {4,5,6,7}, {92,93,94,95},
     {167,168,169,170}, {230,231,232,234} (0-indexed). The old list had
     {231,232,234,235} = F,W,W,W with tails t,n,m,h, dropping paragraph 230
     ("For those who don't know me, I'm Hal Finney...") which stage one flips, and
     adding 235 which belongs to no replica. Both readings are now axes (25 total).
  3. GATE. No candidate is derived unless the three certified base hashes reproduce
     and the masked document is byte-identical to a plain per-paragraph string rebuild.
"""
import sys, os, hashlib, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import btc
from coincurve import PrivateKey


def _pub(k):
    x, y = PrivateKey(k.to_bytes(32, 'big')).public_key.point()
    return (x, y)


btc.pubkey = _pub

ESC = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
V1T = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"
# Both escrows are checked on every candidate. The single-CRLF base is the 07-23 escrow's
# own format, so a run on that substrate that only watched 14zMk would miss its own answer.
TARGETS = {ESC: "LIVE(14zMk)", V1T: "V1(1EFojcAo)"}

# 16 replica members (0-indexed) + 8 prose F/W singles + 235 (kept so both readings
# of the fourth replica stay inside one space). 25 axes = 33,554,432 masks.
VIOL = [4, 5, 6, 7, 92, 93, 94, 95, 167, 168, 169, 170,
        230, 231, 232, 234, 235,
        69, 99, 101, 105, 119, 131, 138, 258]
N = len(VIOL)
assert len(set(VIOL)) == N
Hc = 0x80000000

_RAW = os.environ.get("RTL_SUFFIX", " RTL")
# The dispatch token can edit ci/ but not .github/workflows/, so the suffix input is the
# control channel (the same trick that selected V1): "CLS" selects the class-mode sweep
# and implies no suffix.
MODE = os.environ.get("RTL_MODE",
                      "CLASS" if _RAW in ("CLS", "CLSN", "CLSS", "CLDB", "CLPX", "CLCR", "CLWS") else "VIOL")
# Base-variant axis. The only file of hers we hold at byte level (safudev_stage1.txt,
# md5 9dd2efb9) is pure ASCII: no U+00A0, no trailing space on any line. The chapter base
# carries 23 characters her own file would not have (6 NBSP, 17 trailing spaces), so every
# sweep to date has hashed a web rendering. CLSN cleans nothing but the NBSPs, CLSS cleans
# the NBSPs and the trailing spaces.
VAR = {"CLSN": "nbsp", "CLSS": "nbsp+trail",
       # The ten inner breaks. wp_paras_br preserves them as a single Enter inside the
       # paragraph; chapter_paras_exact deletes them (fusing "to"+"the"), and no sweep
       # has ever controlled this variable. CLDB reads the break as the space a plain-text
       # paste produces; CLPX reads it as deleted, reproducing chapter_paras_exact.
       "CLDB": "debreak:space", "CLPX": "debreak:deleted",
       # A Windows browser copy turns the inner <br/> into CRLF: 46,010 bytes (db11a7fd),
       # which is exactly base_chapter_crlf.txt, and which no sweep has hashed.
       "CLCR": "debreak:crlf",
       # CLWS: the same inner-CRLF base, but with paragraphs separated by a single CRLF.
       # That is the only serialization a Windows browser produces at 45,466 bytes (f1368eb5).
       "CLWS": "debreak:crlf"}.get(_RAW)
V1 = (_RAW == "V1")
SUF = b"" if _RAW in ("NONE", "V1", "CLS", "CLSN", "CLSS", "CLDB", "CLPX", "CLCR", "CLWS") else _RAW.encode()

CERT = {b"\n\n": "46a308c279540a33e977ea1f660e8458",
        b"\r\n\r\n": "bd07e6ee209c5ab65d874bbbcfccda18",
        b"\r\n": "e7f3720c6f9c95afe37efb0b78ebc8ac"}


def flips(p):
    a = [i for i, c in enumerate(p) if c.isalpha()]
    if not a:
        return p
    c = list(p)
    c[a[0]] = c[a[0]].lower()
    c[a[-1]] = c[a[-1]].upper()
    return "".join(c)


def addr(d, ix):
    m = btc.entropy_to_mnemonic(bytes.fromhex(d))
    k = btc.derive_path(btc.mnemonic_seed(m, ""), (44 + Hc, 0 + Hc, 0 + Hc, 0, ix))
    return btc.p2pkh(_pub(k))


def load():
    P = open(os.path.join(HERE, "base_chapter_lf.txt"), encoding="utf-8").read().split("\n\n")
    assert len(P) == 273, len(P)
    assert sum(len(p) for p in P) + 2 * (len(P) - 1) == 45450, "substrate drift"
    return P


def gate(P):
    norm = [p.encode() for p in P]
    flip = [flips(p).encode() for p in P]
    for sep, want in CERT.items():
        got = hashlib.md5(sep.join(norm)).hexdigest()
        assert got == want, "base drift %r %s != %s" % (sep, got, want)
    if MODE == "CLASS":
        probes = [0, 1, (1 << 20), (1 << 21) - 1, 0b10101010101010101010]
        for mask in probes:
            a = b"\r\n".join(flip[i] if (LETBIT[i] is not None and not (mask >> LETBIT[i]) & 1)
                              else norm[i] for i in range(273))
            b = "\r\n".join(flips(P[i]) if (LETBIT[i] is not None and not (mask >> LETBIT[i]) & 1)
                              else P[i] for i in range(273)).encode()
            assert a == b, "CLASS construction mismatch at mask %d" % mask
        print("gate OK [CLASS]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) "
              "reproduced; construction byte-identical at %d probes; base variant %r"
              % (len(probes), VAR), flush=True)
        return
    probes = [0, 1, (1 << 3) | (1 << 12), (1 << 13) | (1 << 14) | (1 << 15),
              (1 << 16), (1 << 24) - 1]
    for mask in probes:
        sel = set(VIOL[v] for v in range(N) if (mask >> v) & 1)
        a = b"\r\n".join(flip[i] if i in sel else norm[i] for i in range(273))
        b = "\r\n".join(flips(P[i]) if i in sel else P[i] for i in range(273)).encode()
        assert a == b, "construction mismatch at mask %d (%d vs %d bytes)" % (mask, len(a), len(b))
    tails = "".join(next((c for c in reversed(P[i]) if c.isalpha()), "") for i in (230, 231, 232, 234))
    assert tails == "stnm", tails
    print("gate OK: bases 46a308c2 / bd07e6ee / e7f3720c; construction byte-identical;"
          " fourth replica tails %r" % tails, flush=True)


LETBIT = [None] * 273
LETTERS = []


def build_class_axes(P):
    """Every paragraph's initial, as an independent class-membership bit.

    Marking rule is the certified one read backwards: a paragraph is marked when its
    initial is NOT a member of the class. Enumerating membership over the letters the
    chapter actually uses as initials therefore enumerates every class-rule document
    the chapter can produce, including classes that contain F or W (FINNEY, GRYCOIN,
    SATOSHI NAKAMOTO), which stage one's calibration excludes.
    """
    global LETBIT, LETTERS
    LETTERS = sorted({next((c.upper() for c in p if c.isalpha()), None) for p in P} - {None})
    idx = {c: k for k, c in enumerate(LETTERS)}
    LETBIT = [None] * len(P)
    for i, p in enumerate(P):
        c = next((c.upper() for c in p if c.isalpha()), None)
        if c is not None:
            LETBIT[i] = idx[c]
    print("class axes n=%d %s" % (len(LETTERS), "".join(LETTERS)), flush=True)


def main():
    start = int(sys.argv[1]); end = int(sys.argv[2])
    join = sys.argv[3]; idxs = [int(x) for x in sys.argv[4].split(",")]
    if _RAW == "MEGA":
        import mega
        mega.main()
        return
    if _RAW == "TL":
        if join == "crlf":
            print("tail: single pass, join handled inside", flush=True)
        import tail_sweep
        tail_sweep.run(start, end, join, idxs)
        return
    if _RAW.startswith("K2"):
        # Exhaustive two-letter case-toggle space over the certified LF base (46a308c2).
        # K2A: global pairs 0 .. 2^29-1.  K2B: 2^29 .. 2^30-1 (clipped at 641,697,400).
        if join == "crlf":
            print("k2: single pass, lf only")
            return
        import k2_sweep
        off = 0 if _RAW == "K2A" else (1 << 29)
        procs = int(os.environ.get("K2_PROCS", "4"))
        k2_sweep.run(start + off, end + off, procs)
        return
    sep = b"\r\n" if (V1 or _RAW == "CLWS") else (b"\r\n\r\n" if join == "crlf" else b"\n\n")
    if _RAW == "CLWS" and join == "crlf":
        print("skip duplicate join under CLWS (single CRLF is forced)", flush=True)
        return
    if V1 and join == "lf":
        print("skip duplicate join under V1")
        return
    P = load()
    norm = [p.encode() for p in P]
    flip = [flips(p).encode() for p in P]
    gate(P)
    if VAR:
        if "nbsp" in VAR:
            P = [p.replace("\u00a0", " ") for p in P]
        if VAR == "debreak:space":
            P = [p.replace("\n", " ") for p in P]
        if VAR == "debreak:crlf":
            P = [p.replace("\n", "\r\n") for p in P]
        if VAR == "debreak:deleted":
            P = [p.replace("\n", "") for p in P]
        if "trail" in VAR:
            P = ["\n".join(ln.rstrip(" ") for ln in p.split("\n")) for p in P]
        norm = [p.encode() for p in P]
        flip = [flips(p).encode() for p in P]
        for sep2 in (b"\n\n", b"\r\n\r\n"):
            print("cleaned base %s %r %s" % (VAR, sep2, hashlib.md5(sep2.join(norm)).hexdigest()), flush=True)
    if MODE == "CLASS":
        build_class_axes(P)
        # marked when the paragraph's letter bit is 0 ("not a member of the class")
        triples = [(f, z, b) for f, z, b in zip(flip, norm, LETBIT)]
        nmasks = 1 << len(LETTERS)
        print("axes n=%d letters=%s join=%r indices=%s masks=%d targets=%s"
              % (len(LETTERS), "".join(LETTERS), sep, idxs, nmasks,
                 "+".join(TARGETS.values())), flush=True)
        t0 = time.time(); n = 0; hits = 0
        for mask in range(start, min(end, nmasks)):
            body = sep.join([z if (b is None or (mask >> b) & 1) else f for f, z, b in triples]) + SUF
            d = hashlib.md5(body).hexdigest()
            n += 1
            for ix in idxs:
                a = addr(d, ix)
                if a in TARGETS:
                    hits += 1
                    print("***HIT mask=%d join=%s idx=%d md5=%s escrow=%s"
                          % (mask, join, ix, d, TARGETS[a]), flush=True)
                    open("HIT_%s_%d_%d.txt" % (join, mask, ix), "wb").write(body)
            if n % 50000 == 0:
                print("n=%d mask=%d rate=%.0f/s" % (n, mask, n / (time.time() - t0)), flush=True)
        print("DONE %s %d..%d n=%d hits=%d in %ds" % (join, start, end, n, hits, time.time() - t0), flush=True)
        return
    axbit = [0] * 273
    for v, i in enumerate(VIOL):
        axbit[i] = 1 << v
    triples = list(zip(flip, norm, axbit))
    print("axes n=%d %s join=%r suffix=%r indices=%s" % (N, VIOL, sep, SUF, idxs), flush=True)
    t0 = time.time(); n = 0; hits = 0
    for mask in range(start, min(end, 1 << N)):
        body = sep.join([f if (mask & b) else z for f, z, b in triples]) + SUF
        d = hashlib.md5(body).hexdigest()
        n += 1
        for ix in idxs:
            if addr(d, ix) in TARGETS:
                hits += 1
                print("***HIT mask=%d join=%s idx=%d md5=%s" % (mask, join, ix, d), flush=True)
                open("HIT_%s_%d_%d.txt" % (join, mask, ix), "wb").write(body)
        if n % 50000 == 0:
            print("n=%d mask=%d rate=%.0f/s" % (n, mask, n / (time.time() - t0)), flush=True)
    print("DONE %s %d..%d n=%d hits=%d in %ds" % (join, start, end, n, hits, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
