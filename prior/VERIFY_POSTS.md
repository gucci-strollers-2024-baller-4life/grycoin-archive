# Blocks 78-150 do not exist; author posts verified instead

## Inventory check (blocks 78-150)

- `quizchain/calib/quiz1_blocks.py`: `Block(number=1..77)` - 77 published exact inputs (SHA-256)
- `quizchain/calib/quiz2_blocks.py`: `Block(number=1..77)` - 77 published exact inputs (MD5)
- Nothing anywhere in the workspace or the 91 author posts carries question text for block 78+
  (searched `block[ -]?(7[89]|8\d|9\d|1[0-4]\d|150)`); the single hit, "block 102", is the author's
  arithmetic in the block-25 post: run 1 had 77 blocks, so run-2 block 25 is overall block 102.
- The only unpublished block is the finale itself: the 777 mbtc Real Big Block at
  `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`, whose question is stage one's solution text.

So there is no 78-150 batch to verify against the chapter.

## Author posts vs chapter (91 posts in `grycoin_posts.json`)

Same engine (20-char anchors, exact extension). Posts sharing >= 40 chars with the chapter:

| post | block | LCS | paras | content |
|---|---|---|---|---|
| ca6jxv | Quizchain2 Block 77 (Stage One) | 279 | 221 | the Finney sentence "Today, Satoshi's true identity has become a mystery ... I recognize the signs." |
| c8lcsr | Quizchain2 Block 57 | 75 | 160 | "about how to reduce CO2 emissions from a widespread Bitcoin implementation" |
| cc5uka | Quizchain2 Block 66 | 65 | 29 | "a young woman of Japanese ancestry who is very smart and sincere" |
| civj2n | Grycoin Chain Block 1 | 42 | 148 | demo-era phrasing reused in the chapter |
| c78se0 | Quizchain2 Block 54 | 41 | 210 | "called Bitcoin and not Intercoin or some..." |

Everything else in the posts is unrelated to the chapter text.

## Two facts from the block-77 post worth keeping

1. "I will publish the complete solution as the Second stage of this block. This solution will in turn
   be the question for the Second stage, which will have the final 777 mbtc prize." -> stage one's
   solution text (`9dd2efb9...`) is *by design* the question for the finale. Confirms the pipeline.
2. Hint 1: "I already knew that 'Satoshi' was chosen as an anagram of 'Thomas'." Chapter para 168 says
   the same thing the other way round: Aoi Nakamoto is Satoshi's name with the consonants dropped.
   Thomas -> Satoshi -> Aoi is the author's own naming ladder.
