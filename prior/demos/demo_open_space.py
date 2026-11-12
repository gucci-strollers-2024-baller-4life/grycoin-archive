"""Demo block 2: the first genuinely open, affordable slice of the 5+ flip space.

Closed already (dossier, not repeated here): every subset of paragraph/sentence units, all
2^33 boundary subsets, word-edge k<=3, up-to-4-anywhere, and 5 flips at word boundaries.

Two families here are provably outside that:

  A. every subset of the demo's 25 capitalised letters. Subsets of size <=4 are inside
     "4-anywhere", size 5 is inside "5-boundary"; sizes 6..25 are open. Gray-code walk, one
     byte toggled per step, 2^25 = 33,554,432 candidates.
  B. four capitals plus one letter anywhere in the text: C(25,4) x 1197 = 15,140,000. Five
     flips, one of them not at a word boundary, so outside both closed families.

Oracle is the certified 12-bit prefix 3c6 on md5 of the edited text (the demo's solution hash),
then address derivation at indices 0-2 against the demo escrow and both chapter escrows.

Usage: python3 demos/demo_open_space.py [A|B|AB] [--max-min N]
"""
import hashlib, math, os, sys, time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "harness"))
import fast2

LIVE_H, OLD_H = fast2.h160(fast2.LIVE), fast2.h160(fast2.OLD)
DEMO_H = fast2.h160(fast2.DEMO)
IDX = (0, 1, 2)

T = open(os.path.join(HERE, "demo_base.txt"), encoding="utf-8").read()
BASE = hashlib.md5(T.encode()).hexdigest()
assert BASE.startswith("7759227"), BASE
BA0 = bytearray(T.encode())
CAPS = [i for i, c in enumerate(T) if c.isupper()]
LETTERS = [i for i, c in enumerate(T) if c.isalpha()]
assert len(CAPS) == 25, len(CAPS)
CAPSET = set(CAPS)
FREE = [i for i in LETTERS if i not in CAPSET]
print(f"demo {len(BA0)} bytes, md5 {BASE}, capitals {len(CAPS)}, free letters {len(FREE)}",
      flush=True)


def oracle(d):
    return d[0] == 0x3C and (d[1] >> 4) == 0x6


def derive(h):
    ent = bytes.fromhex(h)
    for idx in IDX:
        a = fast2.addr_from_key(fast2.key_at(fast2.seed_from(ent), idx))
        if fast2.h160(a) in (DEMO_H, LIVE_H, OLD_H):
            print(f"  *** HIT idx={idx} {a} md5={h}", flush=True)
            return True
    return False


def run_A(t0, cap):
    """all 2^26 subsets of the capitals, Gray code"""
    n = 0
    hits = []
    ba = bytearray(BA0)
    prev = 0
    for i in range(1 << len(CAPS)):
        g = i ^ (i >> 1)
        diff = g ^ prev
        j = diff.bit_length() - 1
        ba[CAPS[j]] ^= 32
        prev = g
        d = hashlib.md5(ba).digest()
        n += 1
        if oracle(d):
            h = d.hex()
            print(f"  oracle 3c6 | caps mask={g:026b} {h}", flush=True)
            hits.append(h)
            derive(h)
        if (i & 0xFFFFF) == 0:
            el = time.time() - t0
            print(f"  A {i:,}/{1<<len(CAPS):,} {i/max(el,1e-9):,.0f}/s "
                  f"hits={len(hits)}", flush=True)
            if cap and el > cap:
                return n, hits, "time"
    return n, hits, "done"


def run_B(t0, cap):
    """four capitals + one free letter"""
    n = 0
    hits = []
    ba = bytearray(BA0)
    cap_list = list(CAPS)
    for a in range(len(cap_list)):
        for b in range(a + 1, len(cap_list)):
            for c in range(b + 1, len(cap_list)):
                for dd in range(c + 1, len(cap_list)):
                    quad = (cap_list[a], cap_list[b], cap_list[c], cap_list[dd])
                    for p in quad:
                        ba[p] ^= 32
                    for q in FREE:
                        ba[q] ^= 32
                        d = hashlib.md5(ba).digest()
                        n += 1
                        if oracle(d):
                            h = d.hex()
                            print(f"  oracle 3c6 | quad={quad} free={q} {h}", flush=True)
                            hits.append(h)
                            derive(h)
                        ba[q] ^= 32
                    for p in quad:
                        ba[p] ^= 32
                    if n and (n % 5_000_000) < len(FREE):
                        el = time.time() - t0
                        print(f"  B {n:,} {n/max(el,1e-9):,.0f}/s hits={len(hits)}",
                              flush=True)
                        if cap and el > cap:
                            return n, hits, "time"
    return n, hits, "done"


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "AB"
    cap = None
    if "--max-min" in sys.argv:
        cap = 60 * float(sys.argv[sys.argv.index("--max-min") + 1])
    t0 = time.time()
    total = 0
    allhits = []
    for w in which:
        fn = run_A if w == "A" else run_B
        n, hits, st = fn(t0, cap)
        total += n
        allhits += hits
        print(f"family {w}: candidates={n:,} oracle={len(hits)} status={st} "
              f"elapsed={time.time()-t0:.0f}s", flush=True)
    print(f"TOTAL candidates={total:,} oracle_hits={len(allhits)} escrow_hits=0 "
          f"elapsed={time.time()-t0:.0f}s")
