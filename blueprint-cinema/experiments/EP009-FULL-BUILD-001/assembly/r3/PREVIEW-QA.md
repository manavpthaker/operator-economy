# EP009 r3 assembly preparation and preview QA

The r3 master and timing revision are prepared. The full assembly waits for the six bound film selections. Original r2, master, shot plan and all source files remain retained. REVISION.json is immutable and is selected by the episode ACTIVE-REVISION pointer maintained by root.

## Current artifacts

- `narration-master-r3.wav`: 58,644,920 samples, mono 48 kHz PCM16.
- `TIMEMAP.json`: 29,323 picture frames at 24 fps, 1221.791667 seconds; final picture tail is 1,080 zero samples.
- `word-transcript-r3.json`: 3,367 words. Original IDs and timing shifts remain explicit outside the removed biography; 75 old words become 43 corrected words with new IDs. Pickup timings retain their approximate ASR limitations.
- `SOURCES.json`: all 75 rows, original source hashes/ranges, revised output ranges and source/output cues.
- `../qa/ep009-r3-review.html`: current review page, with all 75 mapped jumps. Full-video controls remain disabled until the new film is integrated.

Brand removal is exactly 78 frames / 156,000 zero samples. The corrected paragraph preserves all 684,339 selected audio samples and appends 1,661 zero samples to reach 343 frames. No time stretch, new gain change or fade is applied by the assembly builder. Every retained PCM section was verified byte-for-byte after writing. A separate agent independently confirmed the five PCM sections, all row boundaries and every retained word mapping.

## Preview checks

- `ep009-r3-brand-context-BUILD.json` and matching `-VERIFICATION.json`: 296 frames, 12.333333 seconds; complete video/audio checks pass. Per-channel audio correlation is 0.9999901.
- `ep009-r3-hospitality-context-BUILD.json` and `-VERIFICATION-r2.json`: 583 frames, 24.291667 seconds; complete video/audio checks pass. Per-channel audio correlation is 0.9999920.
- Root inspected the encoded hospitality context at 8 seconds and confirmed the L3 still and unobstructive pending-presenter label. This is not normal-speed audiovisual or voice acceptance.

The initial hospitality attempt failed before encoding because this FFmpeg has no drawtext filter. It remains preserved. The successful context uses a separate transparent technical label overlay; the locked L3 photograph remains an untouched input.

The initial brand preview exposed a one-frame concat branch with zero inferred duration. The current builder groups consecutive selections from the same source into one branch and assigns frame-based timestamps. The brand preview now retains exactly 296 frames, including the exact source selection across the approved cut. The earlier diagnostic remains retained.

The initial verifier required silent decoded AAC padding even for excerpts ending during speech. The current verifier permits at most one AAC frame of codec padding for excerpts, while checking every mapped program sample and exact container duration. Full-episode output still requires a silent final tail. No correlation, timing or frame-count threshold was relaxed.

## Full render when film selections are ready

Use the retained syncenv Python for Pillow and NumPy. From repository root:

```sh
python blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/_tools/build_r3.py render \
  --scope full \
  --film-selects blueprint-cinema/experiments/EP009-FULL-BUILD-001/film/r3-workflow/FILM-SELECTS.json \
  --name ep009-full-r3-review-draft
python blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/_tools/verify_r3.py \
  blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r3/ep009-full-r3-review-draft-BUILD.json
```

The renderer refuses missing film selections or existing output files. It uses retained source plates directly, never the already compressed full r2 movie. It writes a separate full build manifest and refreshes only the r3 review page. New film sources must be 1280x720 at 24 fps and cover their declared ranges at original speed.

Six film-map cases were tested in memory against independently computed expected coordinates, including both inserts in seg048: 823 total frames, all row lengths and selected source offsets preserved. Overlap with the brand removal or corrected paragraph is rejected. Actual new sources still require their hashes, encoded-frame checks and visual review.

Fourteen speaking presenter segments still use r1. Corrected P08 uses a visibly labeled still; it never places new words against the old speaking P08 picture. No owner, release, final mix or Resolve delivery acceptance is implied.
