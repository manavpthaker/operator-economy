# R76 S17 review assembly handoff

Prepared for root execution only. The assembler has **not been executed** by this agent. Python syntax compiles successfully and all five fixed source hashes were rechecked live. The current alignment selects restored frame **8**; the script reads that value from the live alignment file and requires 192 continuous source frames.

Run from any directory with Python 3 and ffmpeg/ffprobe on PATH:

```bash
python3 /Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R76-S17-REVIEW-BUILD/assemble_review.py
```

Only the Python standard library is required. The script discovers the canonical repository from its own path. Do not relocate it outside this checkout.

Inputs:

- Existing R62 context: first 192 video frames as S16 lead-in.
- Accepted R62 S17 P1: 711 frames.
- R76 provider/restoration/restored.mp4, selected_source_in_frame from provider/ALIGNMENT.json: 192 frames.
- Accepted R62 S17 P2: 708 frames.
- Original narration-master.v4.wav, with separately verified exact eight-second provider/audio/c.wav.

The script checks the fixed hashes before assembly and again afterward. When alignment includes source_sha256 or original_audio_sha256, it verifies those too. It binds the actual restored-media and alignment hashes in the generated report. An alignment without an explicit source hash is reported as such; root remains responsible for the measured alignment decision.

Root-run outputs:

- r76-s17-presenter/qa/s17-c.mp4 — 192 frames / 8 seconds / 1280×720 / 24 fps, with original master774.5–782.5 duplicated mono-to-stereo at unity.
- r76-s17-context/qa/context.mp4 — 1803 frames / 75.125 seconds, continuous master736.875–812.0, same stereo treatment.
- Exact master-derived PCM WAVs, command receipts, VERIFICATION.json in both QA folders.
- Presenter native stills at local frames0,96,191; full context and entry/return seam contact sheets in presenter/qa.
- r76-s17-context/index.html — review player starting33.5, with buttons at33.5,37.625,45.625 and complete review guidance.

The JSON retains the established status/scene/context/audio/blank-check schema, with additional per-channel and presenter-window checks. strict_check is null because this is ffmpeg assembly, not a new HyperFrames composition.

Verification performed only when root runs it:

- Exact source PCM slices and no added silence.
- Expected video dimensions,24fps and192/1803frame counts.
- Full decode of every output frame; near-uniform grayscale frame scan at64×36, failing at spatial standard deviation≤3.
- Zero-lag decoded-audio correlation>.999 and RMS level difference<0.1dB against master, independently for both stereo channels: isolated presenter, full context, and presenter within context.
- Input fingerprints stable across assembly.

Existing outputs are never overwritten. If execution fails after partial files are written, inspect them and explicitly move or remove only the new R76 outputs before rerunning. The script does not automatically clean up. It will reject insufficient source coverage or an unexpected source aspect ratio rather than freeze/pad/retime/crop.

Limits: syntax and input pins are verified, but media assembly remains unexecuted. Audio metrics do not establish perceptual lip sync, performance quality or owner acceptance. The blank-frame heuristic does not identify every visual defect. Output AAC is lossy; bit-exact claims apply to staged PCM. Accepted video is re-encoded for the review without changing cuts or timing. No provider calls, shared-source edits, decision-log mutations, canonical conform or release.
