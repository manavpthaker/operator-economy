# EP007 R80 4K leaf map: S14–S26

This map traces R79 output frames [13376, 27241) back to their original sources (the "leaves"). The full detail is in `S14-S26-LEAF-MAP.json`.

The range breaks into 33 leaves:

- **19 HyperFrames leaves.** These can be re-rendered at 4K.
- **14 media leaves.** These are the presenter takes, the Kling film clips and the screen recordings.

A script checked that the leaves cover every frame, with no gaps and no overlaps.

| Scene | R79 frames | Leaves |
|---|---|---|
| S14 | 13376–15146 | Presenter A, C1, C3 (`r59-s14-presenter/provider/*/restoration/restored.mp4`, 1080p) + HyperFrames `r59-s14b`, `r59-s14c2`, `r59-s14d` (0.8.36) |
| S15 | 15146–16514 | HyperFrames `r60-s15-p1` [0,600), `r60-s15-p2` [0,8) and [292,768) + ChatGPT recording (R77 raw 3840x1946 VFR), cropped by R78 |
| S16 | 16514–17807 | HyperFrames `r61-s16-p1` [0,213), return still p1 frame 866 (10 frames), `r61-s16-p2` [0,417) + 4 Sheets recording stretches |
| S17 | 17807–19418 | HyperFrames `r62-s17-p1` [0,711), presenter `r76-s17-presenter/provider/restoration/restored.mp4` [8,200) (1080p), HyperFrames `r62-s17-p2` [0,708) |
| S18 | 19418–20198 | HyperFrames `r63-s18` [0,780) |
| S19 | 20198–21314 | HyperFrames `agents/deliverables/R64B-S19-TITLE-SWAP` [0,1116) (0.8.46) |
| S20 | 21314–23588 | HyperFrames `r65-s20-economics` [0,2274) |
| S21 | 23588–25060 | HyperFrames `r66-s21-hard-part` [0,1472) |
| S22 | 25060–25584 | 4 Kling clips (1916x1080) placed full-frame by `r69-s22-film` |
| S23–S26 | 25584–27241 | HyperFrames `r70-s23-payoff`, `r71-s24-verdict`, `r72-s25-first-action`, `r75-s26-boundary-close` (0.8.46, vector only) |

## Probe

Two leaves were rendered at 4K from copies in the scratchpad. Each 4K render was scaled back down to 720p and compared frame by frame with the matching R79 frames:

- **S20 (0.8.46):** 2274 frames in 151 s. Average SSIM 0.9974, lowest 0.9954. PSNR 43.3 dB.
- **S15 P1 (0.8.36):** 600 frames in 18 s. Average SSIM 0.9972, lowest 0.9948. PSNR 44.7 dB.

Shifting either comparison by one frame lowers the score, so the frame alignment is correct. The picture matches R79, apart from differences at the level of compression noise.

## Risks

1. **Disk space blocks the default render.** A normal 4K render of S20 needs about 75 GB of temporary space, and the machine has about 11 GB free. `--low-memory-mode`, which streams frames instead of storing them, works. Otherwise, free up disk before rendering.
2. **Some sources are below 4K.**
   - The presenter shots (S14 A/C1/C3 and S17 C) are only available at 1080p, including the lip-synced versions, so they need a 2x upscale. True 4K would need newly generated takes, which is a paid step the owner must approve.
   - The Kling clips in S22 are 1916x1080, so about 2x upscale.
   - The screen recordings are 3840x1946, but only part of each is used. The S15 area needs a 1.8x upscale and the S16 area needs 3.3x, which is the worst in this range.
3. **Some steps happened in ffmpeg, not HyperFrames.** Each one has to be redone at 4K:
   - the R77 frame-rate conversion to a steady 24 fps and its crop;
   - the R78 moving crop and Lanczos scale into the 1216x630 box, with 1280x720 pixel sizes written into the layout;
   - the S15 seam-hold still and the S16 return still, which were taken from the 720p renders;
   - the presenter trim and downscale.
4. **HyperFrames versions differ.** r59–r63 are pinned to 0.8.36 in `package.json`, but the S14 renders carry the tag `0.0.0-dev`, and there are no render logs for r60–r63. R78 uses 0.8.50. R64B and S20–S26 use 0.8.46. The S15 P1 probe on 0.8.36 matched closely.
5. **S19 was a full re-render, not an overlay.** R64B is a modified copy of the r64-s19 project with two edits. The heading is hidden and "The risk" appears at leaf frame 703 (R79 frame 20901). One line on the final card was also darkened for contrast. Its `public/` folder is a link to r64-s19. The owner lock pins the video's checksum but not `index.html`'s.
6. **The locked look includes a known bug.** Some S14 labels render grey instead of the accent colour. A faithful re-render keeps that.
7. **Other risks:**
   - **Low-res stand-ins:** `autoProxy` is on in S22, so the render must be checked to confirm it used the original clips, not lower-res copies.
   - **Slow seeking:** the S22 establishing clip has keyframes far apart, which can cause frozen frames.
   - **Between-frame image:** R79 frames 17380–17381 show an in-between image at the S16 return join.
   - **No build records:** there are no build commands for `r59-s14-full-context`, `r63-s18-context` or the S17 `native-trim.mp4`. The mapping was rebuilt by comparing frames.
   - **Not in git:** the r59 folders and R64B are untracked, so back them up before relying on them.
8. **Stale entry in SEGMENTS.** The S15/S16 `pending_overrides` there were resolved by `r78-owner-s15-s16-mobile-lock-v1`.
9. **Output quality setting.** At quality `standard`, the 4K output is only about 0.45 Mb/s. Masters for Resolve should use `--quality delivery`, a low `--crf`, or `--format png-sequence`.
