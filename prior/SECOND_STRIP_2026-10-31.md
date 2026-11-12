# The "SECOND" strip: clean, no channel

**Date:** 2026-10-31
**Image:** `incoming_files/14132205c_image.png`, 1024 × 341, RGBA (alpha flat at 255), PNG with no
text chunks, RGB within 2/6 levels of grey.

## Layout

Two crenelated rules (y 19–66 and y 268–317, both spanning x 0–1016) with the word `SECOND` set
between them (x 361–815, y 121–210).

## The borders are periodic, not a barcode

Seventeen vertical connectors at x = 40, 99, 155, 214, 270, 329, 384, 444, 499, 558, 614, 673, 729,
788, 843, 903, 958. Step gaps alternate 59 / 56 px for a constant period of 115 px; the top-level
runs are 72–73 px, the bottom-level runs 69–70 px, the connectors 13–14 px. Top and bottom are
identical to the pixel. A message would break the period; nothing breaks it.

## The lettering is single-tone

Six components, all solid black: ink medians 19, 20, 20, 20, 21, 22 and core minimum 0 on every one.
This is the decisive difference from the address strip, whose glyphs were split 19 black / 16
mid-grey at ~110. There is no second tone here, so no per-glyph bit channel.

Widths 57, 57, 59, 67, 76, 66; heights 90 for the round letters (S, C, O) and 87 for the flat ones
(E, N, D), which is ordinary overshoot, not an offset code.

## The only irregular ink

A 1 px wide dashed rule at x = 1016–1017, marks at y = 8, 37–38, 51, 66, 95, 109, 124, 152–153,
210, 285, 297, 299, 326. Gaps 29, 14, 15, 29, 14, 15, 28, 58, 75, 12, 2, 27. It coincides with the
two rules and reads as the bleed edge of a vertical dotted rule just outside a right-hand crop, not
as a payload.

## Verdict

No hidden layer of any kind that I can detect: no alpha channel use, no metadata, no two-tone split,
no periodic break in the ornament. It is a title card.
