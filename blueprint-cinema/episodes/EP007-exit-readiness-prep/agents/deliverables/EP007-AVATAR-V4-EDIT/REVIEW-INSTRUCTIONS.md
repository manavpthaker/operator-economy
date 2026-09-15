# Bind and render the actual restored take

From this deliverable directory, run:

```sh
python3 build_review.py --source project/assets/source8bit-before-edge-cleanup.mp4 --audio-insertion-offset 0.04725 --wide-scale 1.004 --crop-scale 1.30
```

This reproduces the verified V4 binding. Its measured original-WAV insertion offset is +0.04725 seconds. Do not substitute another take or a different offset without new source QA. The staged 8-bit derivative still contains the source edge defect; the explicit 1.004× wide overscan removes it. The script checks locked hashes, 1920×1080 resolution, constant 24 fps, audio presence, and approved-audio tail coverage. It stages a local copy, records its full probe/hash, then generates the deterministic composition. It preserves time zero and playback rate for both picture and the restored soundtrack.

Review moving frames around the question and at the tail. The default 1.30× crop is top anchored; adjust it only within 1.30–1.40 after checking actual eyes/hair/headroom. A passing layout check does not establish likeness, gesture naturalness, or audiovisual sync.

Run canonical HyperFrames proof and render. The script preserves an existing final output and refuses to overwrite it; use a new owned revision directory for further edits:

```sh
cd project
npx --yes hyperframes@0.8.34 snapshot . --at 17.75,17.875,19.5,21.0
cd ..
./render_review.sh
```

The keyframes --shot diagnostic does not resolve this zero-duration hard set; its --ghost fallback requires canvas. Use canonical snapshots for the two visible poses. Proof times should bracket the cut time printed by `build_review.py`, especially if the measured insertion offset changes that time. Final output: `EP007-avatar-v4-wide-to-close-review.mp4` in this deliverable directory. `render_review.sh` refuses to render the still study as a finished review. After the HyperFrames render it stream-copies the original restored mono AAC into the final output and enables faststart; neither audio nor rendered picture is re-encoded during that remux.

After rendering: probe resolution/FPS/frame count/audio duration; inspect the last wide frame, first close frame, representative closer frames, and final frame; compare the output waveform against the approved WAV at early/middle/late windows; listen to the complete result for continuity and watch mouth/gesture motion. Root owns audio and independent naturalness QA. Preserve the complete pause and audio tail.

This work order forbids browser UI, uploads, publishing, new provider calls, and canonical-project mutations. Canonical CLI snapshots/checks are local composition diagnostics. No Studio session or public feedback submission has been started.
