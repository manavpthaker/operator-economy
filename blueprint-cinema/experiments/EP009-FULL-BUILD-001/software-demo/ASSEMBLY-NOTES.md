# S13 software demonstration revision

The selected insertion is **[16704,17458)** on the unchanged r5 clock: **11:36.000 to 12:07.416667**, 754 frames. The original S13 question retains 95 frames before it; the closing retains 65 frames after it. The full episode remains 29,323 frames at 24 fps. Narration samples **[33408000,34916000)** continue unchanged from the locked master.

The entrance is in measured quiet (50 ms RMS −76.4 dBFS). The exit is immediately before “The drafting got cheap. The judgment didn’t.” (−56.76 dBFS). The apparent transcript gap at 12:03.875 is voiced, so it was not selected as a breath. `TIMING-CONTRACT.json` retains all 101 S13 word records and the original row boundaries.

The isolated builder uses the existing r4 source assembly graph. It does not flatten the r5 full movie into a new source or alter the previous assembly. Every existing presenter selection, P00/P08 limitation, film placement, cue, master, timing map and owner lock remains bound. Only new `assembly/r6-software-demo/` and `assembly/qa/r6-software-demo/` outputs are written.

## Source contract

Use a conformed **1280×720, 24 fps MP4** with consecutive timestamps from zero. Silent video is sufficient: all source audio is discarded. A single 754-frame reviewed plate is simplest; adjacent exact source intervals may also cover the entire range. Every output frame must map to exactly one selected source frame. No output gap, overlap, implicit freeze, fallback, generated, optical-flow, or speed-ramped picture is permitted. A VFR screen capture may be sampled onto the fixed 24 fps presentation clock only when `SCREEN-CONFORM.json` binds the untouched raw source, crop and pad, shown raw-time spans, omitted spans, source/output hashes, command, and no-interpolation constraint. That explicit delivery conform is not a claim that the raw capture was native 24 fps. Every source requires its file SHA256, full decoded-frame sequence SHA256 and a bound exact-range review.

The current r6 selection is `SELECTIONS-r2.json`. It binds existing F03 source frames **[96,144)** to the first 48 output frames and the 706-frame real Node-RED/OpenAI screen capture to the remainder. The associated `SCREEN-CONFORM.json` binds six shown raw-time spans and five disclosed idle or provider-latency ellipses. The assembler does not invent any state or fill the elided time.

## Selection records

The `--manifest` JSON belongs under `software-demo/` and contains:

```json
{
  "record_type": "ep009_software_demo_selections",
  "status": "selected_for_review",
  "base_build": {"path": "...r5...-BUILD.json", "sha256": "..."},
  "timing_contract": {"path": "...software-demo/TIMING-CONTRACT.json", "sha256": "..."},
  "master": {"path": "...narration-master-r3.wav", "sha256": "..."},
  "direction": {"path": "...selected-picture-direction.json", "sha256": "..."},
  "inserts": [{
    "id": "software-workflow",
    "kind": "real_software_capture",
    "output_frames": [16704, 17458],
    "source": {"path": "...reviewed-plate.mp4", "sha256": "..."},
    "source_start_frame": 0,
    "source_total_frames": 754,
    "decoded_frame_sequence_sha256": "...",
    "review": {"path": "...plate-review.json", "sha256": "..."}
  }]
}
```

The bound direction record contains `base_build`, `allowed_output_frames: [16704,17458]`, and `selected_inserts`, which copies each insert's `id`, `output_frames`, `source` and `source_start_frame` exactly. It may also bind the owner decision and plate edit manifest.

The bound review contains `source`, `source_frames`, `status: "reviewed_for_insertion"`, `errors: []`, `reviewer`, `method`, `limits`, and nonempty hash-bound `evidence`. Screen plates additionally require `real_software_capture`, `legibility_checked` and `workflow_sequence_checked` to be true. The review must disclose any illustrative establishing film separately and bind the actual capture/edit provenance; these flags do not make an illustrative shot evidence of software use.

`video_hashes(path, count)` imported from the existing look-transfer builder calculates the expected decoded frame sequence. The new builder checks it independently.

## Commands

Use the existing syncenv Python. From the episode build directory:

```sh
python software-demo/_tools/build_r6.py inspect
python software-demo/_tools/build_r6.py check --manifest software-demo/SELECTIONS-r2.json
python software-demo/_tools/build_r6.py render --manifest software-demo/SELECTIONS-r2.json --name ep009-r6-software-demo-review-r1
python software-demo/_tools/verify_r6.py assembly/r6-software-demo/ep009-r6-software-demo-review-r1-BUILD.json
```

`prepare` writes only a fresh BUILD and graph. Reusing any output name is refused. `render` is reserved for the later explicit root instruction after exact screen clips and directions are supplied.

Offline tests in `ASSEMBLY-PREPARATION-CHECK.json` cover all 754 source indices, the row boundary, retained question/closing frames, multiple adjacent inserts, and rejection of missing or conflicting ranges. No video was rendered by these tests. Final technical verification decodes the full episode, checks source/graph mappings and all locked audio samples; it does not grant creative, presenter-sync or release approval.
