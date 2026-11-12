"""The dots image carries two ink intensities, split per glyph.

The address strip is not rendered in one colour. Glyph strokes are either near-black (cores ~40-55)
or mid-gray (~110), and the split is per character, not per stroke. This script recovers the
per-glyph tone, the bit string it implies, and the obvious decodings.

Glyph segmentation: blocks split at columns with <=1 ink pixel; blocks wider than expected are split
at their minimum-ink interior column until the count matches the 35 characters of the address. Five
of the 26 raw blocks are merged glyph pairs, so single-glyph boundaries carry +-1 uncertainty.

Reads:  ../assets/dots_tweet_1153435788626948097.jpg
"""
from PIL import Image
import numpy as np

ADDR = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa."


def segments(inkc, n):
    blocks, s, gap = [], None, 0
    for x in range(len(inkc)):
        if inkc[x] > 1:
            if s is None: s = x
            gap = 0
        else:
            if s is not None:
                gap += 1
                if gap >= 2:
                    blocks.append([s, x - gap]); s = None
    if s is not None:
        blocks.append([s, len(inkc) - 1])
    while len(blocks) < n:
        i = max(range(len(blocks)), key=lambda k: blocks[k][1] - blocks[k][0])
        x0, x1 = blocks[i]
        inner = range(x0 + 6, x1 - 5)
        if not inner: break
        xm = min(inner, key=lambda x: inkc[x])
        blocks[i] = [x0, xm]; blocks.insert(i + 1, [xm + 1, x1])
    return sorted(blocks)


def main():
    a = np.array(Image.open("assets/dots_tweet_1153435788626948097.jpg").convert("L")).astype(int)
    band = a[26:72, :]
    inkc = (band < 200).sum(axis=0)
    segs = segments(inkc, len(ADDR))
    tones = []
    for (x0, x1), ch in zip(segs, ADDR):
        b = band[:, x0:x1 + 1]
        d, g = int((b < 60).sum()), int(((b >= 78) & (b < 150)).sum())
        f = d / (d + g + 1e-9)
        tones.append("D" if f > 0.10 else "g")
        print(f"  {ch!r} x{x0:4d}-{x1:4d} dark {d:4d} gray {g:4d} f {f:.2f} -> {tones[-1]}")
    bits = "".join("1" if t == "D" else "0" for t in tones)
    print("\n" + ADDR)
    print(bits)
    print("dark :", "".join(c for c, t in zip(ADDR, tones) if t == "D"))
    print("gray :", "".join(c for c, t in zip(ADDR, tones) if t == "g"))

    print("\ndecodings")
    for w in (5, 7):
        for off in (0, 1):
            s = bits[off:]
            vals = [int(s[i:i + w], 2) for i in range(0, len(s) - w + 1, w)]
            txt = "".join(chr(v) if 32 <= v < 127 else "." for v in vals)
            print(f"  {w}-bit off{off}: {vals} -> {txt}")
    runs, cur, n = [], bits[0], 1
    for c in bits[1:]:
        if c == cur: n += 1
        else: runs.append(n); cur = c; n = 1
    runs.append(n)
    print("  runs:", runs)


if __name__ == "__main__":
    main()
