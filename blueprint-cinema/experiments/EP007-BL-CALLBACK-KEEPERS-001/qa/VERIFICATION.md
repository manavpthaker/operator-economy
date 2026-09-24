# EP007 silent keeper assembly

Status: **rendered and technically verified for internal review. This is not a gate pass,
production select, Step 4 authorization, or publication approval.**

## What this test asks

Do the generated owner-buyer moments that survived the owner's review work as intermittent human
anchors when the aimless looks, unclear employee beat, recycled callbacks, and legible generated
paperwork are removed?

This is deliberately silent. It tests source selection and performance continuity, not narration
fit, sound, or the full episode edit.

## Review artifact

- Film: `../hyperframes/renders/EP007-BL-CALLBACK-KEEPERS-001.mp4`
- SHA-256: `2cdd1d2405e6c0b63e9116cf870d2c17471779c5b3fe10fdb70054915a8864de`
- Size: 45,285,150 bytes
- Picture: H.264 High, progressive YUV 4:2:0, limited-range BT.709, 1920×1080, constant 24 fps,
  929 frames, 38.708333 seconds
- Sound: no audio stream
- Manifest: `../render-manifest.json`
- Manifest SHA-256: `063bd7c13b721f1f0f9aabc75a3876662ae9347e072cbdede13358c174dc6e4d`

## Exact assembly

| Assembly frames | Time | Source from the reviewed callback reel | Purpose |
| ---: | ---: | ---: | --- |
| `[0,192)` | 0.000–8.000 | 0.000–8.000 | ordinary conversation introduction |
| `[192,288)` | 8.000–12.000 | 8.000–12.000 | owner demonstrates operating knowledge |
| `[288,354)` | 12.000–14.750 | 12.000–14.750 | short operating exchange |
| `[354,449)` | 14.750–18.708333 | 14.750–18.708333 | conversation before the stray look-away |
| `[449,641)` | 18.708333–26.708333 | 20.333333–28.333333 | full answer-and-stop close-up |
| `[641,785)` | 26.708333–32.708333 | 52.250–58.250 | binder-wide action |
| `[785,929)` | 32.708333–38.708333 | authored placeholder | missing over-the-shoulder binder shot |

The final six seconds are not proposed episode content. They state the only replacement generation
still needed: the buyer pulls the binder closer, opens one tab, and settles into reading. The binder
stays low or soft; the contents are withheld; there is no pointing, page close-up, legible paperwork,
or approval performance.

## Verification

The exact current composition passed HyperFrames 0.8.29 `check`:

- lint: 0 errors, 0 warnings
- runtime: 0 errors, 0 warnings
- layout: 0 issues across 7 samples
- motion: 0 errors, 0 warnings
- contrast: 3/3 text checks pass WCAG AA

The encoded MP4 then passed:

- strict decode of all 929 frames
- one video stream and no audio stream
- no black interval of 0.04 seconds or longer
- frame-by-frame seam inspection at frames 192, 288, 354, 449, 641, and 785
- source-frame comparison for every outgoing last frame and incoming first frame
- frame 784 matches the intended final binder source frame
- frames 927 and 928 are the same paper placeholder, so there is no terminal flash

Encoded-render contact sheet:
`../hyperframes/qa/encoded-samples/final-contact-sheet.jpg`

Cut-adjacent contact sheet:
`../hyperframes/qa/seams/final-contact-sheet.jpg`

## Defects caught before this freeze

The initial slate used a legacy near-match palette while calling itself Boundary Ledger. It was
rebound to the canonical 2.0 color values: paper `#F5F0E6`, mineral `#173530`, oxide `#B5482F`, and
steel `#586D74` / `#33464C`.

The first encoded edge audit also found two 1/24-second timing defects hidden by broad sampling: the
last binder boundary frame was wrong and the final frame flashed mineral. Six-decimal timing was
replaced with exact 24-fps rational values. A temporary stacking workaround was removed. The final
render now has the intended half-open frame ranges with no gap, overlap mask, or end flash.

## Provenance and limitations

The source is the preserved `EP007-BL-CALLBACK-ARC-001` review reel. Its render is unchanged. Its
HyperFrames package command pin was upgraded from 0.8.28 to 0.8.29 and the parent composition passed
the upgraded check.

The copied generation response records remain verbatim and retain absolute paths back to the parent
experiment. That preserves the original record, but those sidecars require path rebasing outside
this checkout. Five source clips are 1280×720 and `operational-master` is 1024×576, so all footage is
upscaled to the 1920×1080 review output. No footage grade, speed change, post camera move, narration,
music, sound effects, captions, claim IDs, or source annotations were added.

The file's embedded `hyperframes_version` tag says `0.0.0-dev`. That tag is incorrect renderer
metadata; the invoked and package-pinned CLI was 0.8.29.

## What still requires the owner

Machine checks cannot answer whether the acting feels credible in motion or whether the jump from
the pensive close-up to the binder-wide shot carries enough narrative causality. Watch the reel once
at normal speed and judge only:

1. Which moments deserve to recur as human anchors in the full episode?
2. Does the pensive-close-to-binder-wide cut read as a useful before/after leap, or merely a jump?
3. Is the generated look acceptable when it appears intermittently among the rough illustrations
   and talking-head avatar?

If the selection passes, the next bounded test is to generate only the missing over-the-shoulder
binder action, replace the final slate, and distribute these keepers against the locked narration.
The rough Boundary Ledger model carries the invisible operating logic; the generated humans carry
observable action, not evidence.

No gate changed, nothing was committed, and V4 was not advanced.
