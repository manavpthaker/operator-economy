# Exact source slices with disposable end guards

Use `guarded-r1/DELIVERY.json`. It binds each original r1 source, exact source range, immutable uploaded MOV bytes, decoded frame hashes, source PCM, Fal storage URL and verified upload receipt. The unguarded local files are retained preparation evidence and were **not uploaded**.

Every MOV uses lossless H.264 CRF 0 at the original 1280×720 / 24 fps and stereo 48 kHz float PCM. Every original decoded frame and audio sample within each source range compares exactly. The final eight frames repeat the last original frame; the corresponding 16,000 audio samples are zero. All five guarded inputs are between 3 and 15 seconds and below 200 MB.

| Input | Original source frames | Guarded input frames | Select local frames | Original frames reconstructed |
|---|---:|---:|---:|---:|
| seg019a | [0,333) | 341 | [0,333) | [0,333) |
| seg019b | [288,394) | 114 | [45,106) | [333,394) |
| seg071a | [0,120) | 128 | [0,97) | [0,97) |
| seg071b | [97,449) | 360 | [0,352) | [97,449) |
| seg071c | [418,514) | 104 | [31,96) | [449,514) |

The retained boundaries coincide with existing crop cuts at seg019 frame 333 and seg071 frames 97 and 449. Selection reconstructs all 394 / 514 original frames once, in order, with no added edit seams or retiming. Existing earlier crop changes remain inside the relevant source slice.

Keep the disposable guards through **both** wardrobe and background edits. Select only the listed original ranges afterward; never incorporate guard frames or provider audio into the episode master. Provider temporal quantization remains a risk to check in returned media; eight guards do not guarantee any returned output length.

The [official Kling edit schema](https://fal.ai/models/fal-ai/kling-video/o3/pro/video-to-video/edit/api) accepts MP4/MOV, 3–15 seconds, 720–3840 pixels, max 200 MB. Prompts refer to the moving source as `@Video1` and the appearance reference as `@Image1`. No generation request is part of these scripts or receipts. Storage upload performs initiate, PUT and downloaded-byte hash verification only.
