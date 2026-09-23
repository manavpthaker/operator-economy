# R80 4K plates: PREFIX leaf map (R79 frames 0–13376)

Full data: `PREFIX-LEAF-MAP.json` (next to this file).

## How the prefix was built

R79 frames 0–13376 are an unchanged copy of R58 `full.mp4`. R58 is R56 (frames 0–12481) followed by the S13 context (895 frames). R58's level fix changed audio only. R56 joined 12 section encodes, and each of those only trimmed and joined scene renders or an earlier full-project render. None of these steps scaled, cropped, color-corrected or overlaid the picture. The only picture changes were re-encodes.

## Leaves: 21 in total, covering frames 0–13376 with no gaps or overlaps

| R79 frames | Leaf | Source frames |
|---|---|---|
| 0–5872 | HF `r36-buyer-demand` (0.8.34) | 0–5872 |
| 5872–6408 | HF `r39-question-performance` (0.8.34) | 5872–6408 |
| 6408–6895 | HF `r46-revenue-machine` | 0–487 |
| 6895–7164 | HF `r47-transfer-criterion` (presenter inside) | 0–269 |
| 7164–7983 | HF `r48`, `r49`, `r50`, `r51` (full scenes) | full |
| 7983–8131 | media: R52 `handshake-v5/native.mp4` | 0–148 |
| 8131–8163 | media: R52 `walkout/native.mp4` | 112–144 |
| 8163–8351 | media: R53 `presenter-a/restoration/restored.mp4` | 15–203 |
| 8351–8897 | HF `r53-s10-evidence` | 0–546 |
| 8897–9104 | media: R53 `presenter-c-v2/resync-shift/restored.mp4` | 12–219 |
| 9104–10824 | HF `r54-s11a`, `r54-s11b`, `r54-s11cd` | full; s11cd 0–564 of 573 |
| 10824–11089 | media: R55 `s12a-pickup/restoration/restored.mp4` | 0–265 |
| 11089–13376 | HF `r55-s12bc`, `r55-s12d`, `r57-s13ab`, `r57-s13cd` | full |

"HF" means a HyperFrames project. Projects without a version in brackets are pinned to 0.8.36 through `npx` in `package.json`.

To confirm each range, the leaf's own reference render was compared with R79 frame by frame using SSIM, a 0–1 image-similarity score. Motion graphics scored 0.9987–0.9994 and presenter or film clips 0.988–0.994. Moving any presenter or film leaf by one frame lowers its score.

## Feasibility probe

Two projects were rendered at 4K from copies in the scratch folder, then shrunk to 720p and compared with R79:

| Project | Frames | Render time | Speed | SSIM vs R79 | PSNR (48 frames) |
|---|---|---|---|---|---|
| `r49-concentration` (motion graphics) | 163 | 13.4 s | 12.2 fps | 0.9947 | 37.9 dB |
| `r47-transfer-criterion` (presenter) | 269 | 24.6 s | 10.9 fps | 0.9884 | 42.8 dB |

The render has no frame-range option, so every composition renders in full. The whole prefix is about 19,100 frames, around 30 minutes or more; R36 and R39 will be slower because they carry more video. In a zoomed comparison, the 4K line work and text are clearly sharper than R79.

## Risks

1. **R39 presenter clip is only 720p (blocks sharpness, not rendering).** `compositions/owner-dependency.html` plays `public/media/question-r39-aligned.mp4`, a 1280x720 proxy. Re-make it from `provider/restoration/restored.mp4` (1920x1080) with the same trim: frames 10–136 inclusive at 24 fps, per `provider/PICTURE-CONFORM.json`. Point only the scratch copy at it.
2. **Presenter and film clips top out at 1080p.** These are the five media leaves plus the video inside R36, R39 and R47, including 1916x1080 Kling plates. 4K adds no detail to them, and a 1080p master needs none. The R52 plates are 1916 px wide, so filling 1920 needs a 0.2% horizontal stretch. The review builds stretched them the same way.
3. **R36/R39 punch-ins are softer.** Crops of 1916x1080 plates at 2395x1350, and the post-title push up to 1.32x, enlarge the source beyond its size even in a 1080p master.
4. **R50 source drift.** The original `index.html` is lost and the current file is a rebuild. Its render differs from the accepted bytes by up to 1.23/255, which is very small (see event `r50-records-source-rebuilt-v1`).
5. **Two HyperFrames versions.** R36 and R39 use 0.8.34 with no lockfile; everything else uses 0.8.36. Both versions support `--resolution landscape-4k`, and each project should be rendered with its own pinned version. R36 was originally rendered at quality "draft", so a "standard" 4K render may differ slightly in how video frames are pulled.
6. **R47 source clip has keyframes about 10 s apart.** The renderer warned this can make seeking fail. The probe still matched.
7. **Frames 5872–5943 exist in two projects.** The S07 tail is in both R39 and R36; R79 used the R39 re-encode. Either project works.
8. **No picture effects to rebuild.** No filters, overlays or color changes need re-creating in ffmpeg or Resolve. The review encodes only added small losses, for example about 1.26/255 darker on the S07 tail.
9. **Owner sign-off gaps carried over.** These frames are unchanged from R79 but still lack separate owner verdicts: the R39 callback and animation (R79 6117–6408) and the R47 presenter performance (6895–7164).
10. **Missing build scripts.** Recipes for the media leaves come from event records plus SSIM checks; no build scripts exist for them.
