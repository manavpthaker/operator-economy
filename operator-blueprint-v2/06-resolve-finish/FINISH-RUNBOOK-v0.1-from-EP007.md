# Step 6 runbook v0.1: from locked cut to delivery masters

Status: **approved v0.1 (owner, 2026-09-24).** Derived from EP007 / public №001 and updated 2026-09-24 to point presenter work at `blueprint-cinema/references/PRESENTER-RECIPE.md`. Authoritative for its stage; a record still wins where it disagrees on EP007 facts.
Every step below was done for EP007; the pointers are the record. Public number for EP007 is №001.

Input: an owner-locked whole-episode reference (EP007: R79, 1280×720, 27,241 frames at 24 fps) plus
its segment/timing map. Output: a verified 1080p upload master, an archive master, a -14 LUFS mix,
an English SRT, a Resolve project, interchange files and a delivery report.

## 0. Preconditions

- Owner has locked the whole cut (EP007: `r79-owner-whole-episode-lock-v1`).
- Disk: check `df -h ~`. EP007 ran on ~10 GB free; the method below needs < 3 GB of working space
  at a time. Media never goes in git (`.gitignore` covers nested renders, frames, audio, provider
  payloads); it lives under `~/Movies/OE/<EPxxx>-*`.
- Tools: DaVinci Resolve 21 (free edition is enough), ffmpeg 8, Python venv with numpy/requests,
  HyperFrames (each project pins its own version), whisper.cpp (`whisper-cli`, ggml-medium.en).

## 1. Trace the cut to its leaves (why: review encodes are nested and low-res)

The locked reference is usually assembled from 720p review encodes that are themselves nested
(EP007: R79 ← R58 ← R56 ← R36 …). Map every output frame to a **leaf**: a HyperFrames project +
composition frame range, or a native media file + exact recipe (trim, offsets, crop, stretch).

- Split the work: one agent per half of the timeline. Deliverable per half: `LEAF-MAP.json`
  covering every frame with no gaps/overlaps + a risks note.
- EP007 result: 54 leaves (35 HyperFrames, 19 media) —
  `blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r80-4k-plates/leafmap/`.
- Verify each mapping by comparing the leaf's own reference render to the locked cut (SSIM) and
  confirm a one-frame shift scores lower (proves alignment).

## 2. Re-render every leaf at 4K, keep only 1080p (why: sharp graphics, tiny disk)

- HyperFrames can only scale by integers: 1280×720 → `--resolution landscape-4k` (3×).
  `--quality high --crf 12 --low-memory-mode --frames-cache-dir off`, each project with its pinned
  version, rendered from a **scratch copy** (never inside the repo).
- Immediately downscale each 4K render (lanczos) to a 1920×1080 H.264 CRF 14 plate, BT.709 tv,
  24 fps CFR, no audio; delete the 4K file before the next leaf. Disk guard: stop if free < 4 GB.
- Media leaves (presenter, film, screen recordings): rebuild from the highest-res original with the
  recorded recipe, straight to 1080p. Replace any 720p proxy embedded in a project (EP007: R39).
- Verify each plate: downscale to the reference size, per-frame SSIM vs the locked cut
  (pass: mean ≥ 0.985, no frame < 0.95, one-frame shift scores lower). Record every failure; never
  silently accept.
- Tool: `…/r80-4k-plates/_tools/render_plates.py`; manifest `…/r80-4k-plates/PLATES-MANIFEST.json`.
- EP007: 54 plates, 185 MB total. 4 flagged; owner ruled 3 acceptable and R50 kept the locked
  frames upscaled because its rebuilt source drifted ~1 frame (`ep007-r80-plates-owner-review-v1`).

## 3. Owner review of the plates

Build a full 1080p review (concat plates + locked PCM) and side-by-side clips of every flagged
section (top = locked, bottom = new), served on the private tailnet review page
(`http://100.101.49.30:3116/`, `http-server` via `launchctl submit`, range requests verified).
Ask the owner to rule on each flag. Timing fixes: test a uniform shift first; if drift varies,
use the locked frames upscaled.

## 4. Resolve conform (free edition, in-app scripting)

- Free Resolve blocks **external** scripting. Use **Workspace → Console (Lua)**: `dofile("<abs path>")`.
  The console must be on the current macOS Space for background input; if it is not, reopen it
  from the menu. Lua `io` is unavailable: verify results by **exporting OTIO** and parsing it.
- Project settings before import: 24 fps, 1920×1080. Import plates + PCM, build the timeline with
  `AppendToTimeline({mediaPoolItem, startFrame, endFrame, recordFrame, trackIndex, mediaType})`.
  **`endFrame` is exclusive.** EP007's first pass used inclusive and left 54 one-frame gaps; the
  OTIO check caught it.
- Export `timeline.otio` / `.edl` / `.fcpxml` and compare clip-by-clip to the plate manifest
  (0 gaps, 0 mismatches, full-length audio). Scripts: `…/r80-4k-plates/_tools/resolve_*.lua`.

## 5. Editorial changes after lock (only on explicit owner direction)

Record the reopening as a decision. Cut in digital silence on both sides (check per-frame RMS).
A hard cut inside a talking avatar shot reads as a glitch because the avatar never holds still;
moving the cut does not help. Bake a **4-frame centred cross-dissolve** into the plate using
2 handle frames each side, keeping the audio hard cut in silence (no length change).
EP007: removed "I have never sold a business." (51 frames) → R81
(`ep007-r81-cut-never-sold-v1`, `…/r81-cut-never-sold/EDIT-LIST.json`).

## 6. Mix, captions, masters

- **Mix:** dialogue only unless the owner asks for music. Target -14 LUFS integrated, true peak
  ≤ -1 dBTP: straight gain + 4×-oversampled limiter (`volume=…dB,aresample=192000,alimiter,
  aresample=48000`), 24-bit WAV. Measure with `ebur128=peak=true`. Avoid `loudnorm` dynamic mode.
- **Captions:** map the locked narration word timings through the timing map and any post-lock cut,
  group into cues (≤ 42 chars/line, 2 lines, break on sentence/pause), write SRT. Verify against a
  whisper.cpp transcript of the final mix: word match rate, median offset, no drift across cuts.
  Tool: `…/r81-cut-never-sold/finishing/_tools/build_captions.py`.
- **Masters:** Resolve render queue from the console: H.264 MP4 1080p24 + AAC (upload) and
  ProRes 422 + LPCM 24-bit (archive) into `~/Movies/OE/<EPxxx>-masters/`.
  Script: `…/finishing/_tools/resolve_render_masters.lua`.
- **QC:** frame count, full decode, loudness/true peak on each master, SSIM vs the plate concat,
  luma mean diff, hashes → `DELIVERY-REPORT.json`; log a verification event.

## 7. What to hand to Step 7

Upload master path + hash, SRT, chapters recomputed for any post-lock cut, the delivery report.

## Lessons from EP007

- Check disk and API quotas before planning, not after.
- A second session can sweep your staged files into its own commit — stage and commit in one command.
- Verify from exported data (OTIO, ffprobe, SSIM), never from the app's console text.
- Budget: 4K plate render ~1 h for 19 min; Resolve masters render in minutes.
