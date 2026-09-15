# EP007 narration-first B6 verification

Status: **technically passed; exact action contract failed; editorial review candidate only.**

## Source and provenance

- Asset: `hyperframes/assets/video/source/shot-01-buyer-close-b6-veo-fast.full-generated.mp4`
- SHA-256: `17e8bbdc01de479ee3a227b063aa9a2eedf08c549e534b9f3408587fa56394c0`
- Generator/model: `fal.ai` / `fal-ai/veo3.1/fast/first-last-frame-to-video`
- Request: `01a06f6a-5526-7ad1-bcf2-e53101562c0a`
- Prompt: `direction/shot-01-buyer-close-b6-veo-fast.prompt.md`
- Prompt SHA-256: `efb26121f230eb1503cf91052fb7d6835c50abddc6bba7aa89b92d25f561b8e8`
- Response record: `hyperframes/assets/video/source/shot-01-buyer-close-b6-veo-fast.full-generated.response.json`
- Response SHA-256: `9d7e65a27413de53336ce50ced0cb2a8c27ca2ce7d103217f6fe8f8f626b8d03`
- First frame SHA-256: `0d1e68a9ed6f83c1e4b6318ea5a29fecff5dde7fc1aa41c21b9e720f5ec46430`
- Last frame SHA-256: `47acad223d893dda2985765eb347080b479ebba27d67b4d70531a14f124ee5a3`
- Seed: `1528090608`; audio off; auto-fix off; 720p; 16:9; four seconds.

Seedance B5 produced no reviewable asset. Its result endpoint returned a provider policy block that
classified the synthetic human references as possible real-person likenesses. B6 is therefore the
last executable model comparison, not a visual revision selected from B5.

## Predeclared action check

| Frames | Required | Result | Evidence |
| --- | --- | --- | --- |
| `0–30` | Calm owner eyeline holds | Pass | Pose and eyeline remain stable through frame 30. |
| `31–40` | Eyes shift before the head | Fail | Motion begins around frames 32–34, but the eyes close around frames 34–39 as the head begins turning. |
| `41–52` | Chin follows only 3–5° | Fail | The move grows into an approximately 30–40° profile turn. |
| `53–61` | Settle on visible operation | Pass | The buyer holds on shelves and equipment through the cut. |

The buyer does not look into the lens, raise his brow, speak, articulate his jaw, nod, or move his
torso. The owner remains a still, faceless foreground edge. Camera, focus, identity, wardrobe, and
workshop geometry remain stable. The larger turn communicates person-to-operation clearly, but it
is not the microaction that was specified. Passing it would require changing the action contract,
not relabeling this generation.

## Technical source check

- H.264 High, 1280×720, progressive 8-bit `yuv420p`, true 24 fps CFR.
- 96/96 frames decode over exactly 4.000 seconds; no audio stream.
- No black frames, repeated frames, exact duplicates, or 0.5-second freezes.
- All 96 decoded frame hashes are unique; `repeat_pict=0` throughout.
- The background moves at most one horizontal pixel transiently; no meaningful camera or focus
  drift is measurable.
- The selected range is frames `[0,62)` / seconds `[0,2.583333)`. `2.56` is not on the 24 fps grid.
- Frame 61 is a coherent B-frame. A standalone trim must decode and re-encode; the composition uses
  a frame-accurate timeline trim rather than keyframe-dependent stream copy.

## Rendered comparison

- Isolated B6: `hyperframes/renders/EP007-BL-NARRATION-FIRST-006.mp4`
  - SHA-256: `09d71108708b630d55bb28b066d5013df499f0f7ef0e427bbd52ec2d861377e1`
  - 9,226,153 bytes; 1920×1080; 24 fps CFR; 186/186 frames; 7.750 seconds.
- Shared-context B6: `hyperframes/renders/EP007-B6-NARRATION-FIRST-context-17.5-27.5.mp4`
  - SHA-256: `5e778cb24c1caf897160f87a75fad037d594967ea75f8f16238a230423988f75`
  - 6,150,440 bytes; 1920×1080; 24 fps CFR; 240/240 frames; 10.000 seconds.
- Both files decode without error and contain no black interval.
- Isolated B6 contains no consecutive exact duplicate. The two duplicate transitions in the
  context file end at frames 10 and 11, inside the unchanged pre-roll rather than B6.
- The context file copies Variant A's original AAC stream. Its decoded PCM SHA-256 matches A's
  context exactly: `35bfb83d2c0e8205044ac5e101c133bfe0b3a1d7b4810290d084dc8bb4e67b49`.
- HyperFrames `0.8.28` strict check: zero lint, runtime, layout, motion, or contrast findings.

The shared-context transform is recorded before execution in
`hyperframes/scripts/build-b6-context.sh`. It retains A frames `0–15`, inserts all 186 B6 program
frames, retains A frames `202–239`, and copies A's ten-second audio stream.

## Boundary

B6 is generated live-action-style `humanContext`, not evidence or documentary footage. It does not
depict a sale, price, contract, handshake, incompetence, resolved outcome, or real owner or buyer.
This test does not approve the generated take, Shot 2, V4, Step 4, production, publication, or any
platform disclosure.
