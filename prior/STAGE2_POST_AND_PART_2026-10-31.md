# The stage-two post body and the live part markup: the envelope theory is closed

**Date:** 2026-10-31

Question raised: is the stage-two preimage the announcement post body, complete with title,
preamble and Reddit tags, the way stage one's preimage was the posted question text?

## Answer, in the author's own words

The post is already archived at `agntn/aoinakamoto-2019-07-22-cgkpbb.md` (cgkpbb, 2019-07-22
23:22:14 UTC, last edit 2019-07-30 23:51:31 UTC, from Arctic Shift with pullpush agreeing). It says
what the question is:

> **Question: Final version of the second chapter of Wattpad story, which I will publish in a moment.**

and, in the update that re-funded the block:

> Took back the funds from the address above and sent them to a new address … because I wanted to
> remove one of the twists I had. The block is now slightly easier. **It is also hashed with two line
> breaks between paragraphs now.**

So the hashed object is the chapter body, not the post. The announcement's title, preamble, the
address-apophenia paragraphs, the expiry conditions, the `[shutting down...]` line and the update
text are all outside the hash. Stage one was text-as-preimage because its Question line pointed at a text
document, the bitcointalk post; stage two's Question line points at a Wattpad part, so the same reading
lands on the part. (It was never submission-as-preimage: the stage-one post body is a URL and seven quoted
sentences, not the document.)

## No framing in the part either

`curl "https://www.wattpad.com/apiv2/storytext?id=720888559"` returns 59,613 bytes containing
exactly 273 `<p data-p-id="…">` paragraphs and **nothing else**: stripping them leaves an empty
string. No author's note, no title, no dedication, no timestamp, no navigation text.

Our corpus matches those 273 paragraphs character for character (0 differing paragraphs).

## Fidelity is closed by the timestamps

| object | modifyDate |
|---|---|
| part 720888559 "Second" | 2019-07-23T23:12:04Z |
| story 184148284 | 2019-07-23T23:24:07Z |

Both last modified the day after the post went up, and never since. The live text **is** the text
he hashed. The thread's worry that "nobody has the July 2019 copy" is answered by that alone.

Corpus-wide check against Wattpad's own stored `length` (`text + 2×(n−1) + 1` trailing newline):
32 of 33 parts match exactly; part 720895205's story-level `length` is stale by 17 but its text
also matches when fetched directly. The corpus is faithful everywhere.

## There is no stage-two hash oracle

The 2026 thread is explicit. Asked for more hash digits:

> Not going to do more hash digits for 76, would make it too easy to script the block. But there
> will be hints for that one, not always declared as such...

No 3-hex prefix for block 77 stage two appears anywhere in the 34 comments. `9dd` is stage one's
only published prefix. Candidates must therefore be fully derived; there is no MD5-only filter.

## Serialization, unchanged

The part's stored length is **45,451** = 44,896 text + 10 internal `<br>` + 2×272 separators + 1
trailing newline, which is the figure `SERIALIZATION.md` already certifies. The built base files are
45,450 (no trailing newline); trailing `{"", LF, CRLF}` was already run as a 72-candidate family,
zero hits.

## Two small findings worth keeping

1. **¶78 is the one paragraph whose stored id doesn't match its own text.** Ten paragraphs carry an
   internal `<br>` (63, 73, 121, 124, 146, 160, 184, 189, 193, 213), and hashing their rendered text
   with `\n` reproduces their `data-p-id` apart from reconstruction detail. ¶78, which is exactly
   `"What?"`, is different: **no** variant of its text reproduces `8b71bade…`. It is the single
   paragraph whose stored text was changed after its id was minted, i.e. the only visible edit scar
   in the chapter.
2. **The chapter's own skeleton is 28 bold headings**, which fixes the section boundaries the sweeps
   have been inferring: `I. Second Life` ¶2, `1. Second Coming` ¶3, `2. Running` ¶54, `3. Reverse
   Turing Test` ¶71, `II. Second Layer: Grycoin…` ¶88, `Abstract` ¶89, `1. Purpose` ¶91, `2. Bitcoin
   With Two Changes` ¶115, `3. Incentives` ¶130, `4. Why Blockchain?` ¶152, `5. What Grycoin can do
   for Bitcoin` ¶157, `6. Conclusion` ¶161, `III. Second Identity` ¶163, `1. My Identity` ¶164,
   `2. The Satoshi Code` ¶175, `a)` ¶176, `b)` ¶182, `c)` ¶209, `d)` ¶215, `3. Other evidence` ¶247,
   `a)`–`f)` ¶250/252/254/256/258/260, `4. What Does it Mean?` ¶265.

The four known window anchors sit one per subsection in four different acts' subsections: ¶6 in
`1. Second Coming`, ¶94 in `1. Purpose of Grycoin`, ¶169 in `1. My Identity`, ¶232 in `d) Outing
himself as Satoshi on Bitcointalk`.

## Consequence

Nothing here reopens the derivation. The payload question is unchanged and narrow: the case edit, on
a base whose text and serialization are now pinned by three independent sources (our own corpus, the
part's stored `length`, and the two certified sibling preimages).
