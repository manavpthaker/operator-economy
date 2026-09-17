# EP009 presenter regeneration helper review

Reviewed 2026-09-17 before the regenerated presenter batch. Scope: `_tools/regen.py` only. No provider requests, production ledger writes, plan changes, prompt changes, or existing media changes were made during this review.

## Fixes

- **Native trim timing:** The helper previously counted input video frames as 24 fps and only converted to 24 fps afterward. A 30 fps native therefore trimmed picture and audio at different times. It now converts picture to 24 fps before applying the shared trim offset. The trim record binds native video, narration, and offset-measurement hashes.
- **Gate before paid Sync:** Trimming and Fal submission now require three valid native-offset windows, matching video and narration hashes, and drift no greater than 0.30 seconds. Fal submission additionally verifies the trim and its input hashes before loading the provider transport or uploading media. A clip shorter than its narration is rejected.
- **Completion accounting:** Repeated completed-result retrieval no longer appends duplicate charged completion rows. Completion writes use an exclusive ledger lock and reject conflicting request IDs or amounts. Totals charge the latest state of each unique item once, so reconciling an uncertain submission to completed does not count the estimate twice. Retakes still require distinct item IDs.
- **Media preservation:** Downloads and restored results are staged, then installed without overwriting an existing file. Matching bytes are an idempotent success; differing bytes fail with the original preserved. Trimming reuses an existing output only when its input and output hashes match the recorded provenance.
- **Restored frame rate:** Alignment now rejects restored video that is not 24 fps rather than silently applying 24 fps frame arithmetic to it.

## Local verification

Seven isolated checks passed using temporary fixture directories and a fake Fal transport; no network or paid provider calls were used:

1. A synthetic 30 fps native with frame-coded luminance was trimmed by 12 frames on the 24 fps timeline. Its first output frame had luminance **61**, matching source frame 15 at **0.5 seconds**. The old ordering would have selected source frame 12 at 0.4 seconds, luminance 52.
2. Repeating a trim preserved its existing output hash.
3. A drifted native failed before transport initialization, upload, submission intent, or spend.
4. Stale native-offset provenance failed closed.
5. Two completed-result fetches produced one completion entry, with an earlier uncertain charge reconciled to a single **$0.25** total.
6. A changed remote result could not replace existing restored media.
7. A second completion with a conflicting amount was rejected.

Python syntax parsing passed. This is a helper correctness review, not a presenter performance or lip-sync acceptance. Native correlation and mouth metrics remain diagnostic; normal-speed playback with the locked narration is still required for the generated clips.

## Resume notes

Run `native` before `trim` so `NATIVE-OFFSETS.json` includes the newly required narration hash. Existing measurement records without that hash must be recomputed. Drifted parts stop before paid restoration and need a recorded production decision or a new bounded take; this helper does not silently waive that gate.

The helper still keeps final conform and QA outputs in their existing working paths. This review protects provider native/restored media and the validated trim; it does not introduce an episode-wide artifact versioning system.

## Active execution provenance and review readiness

The later resume uses different prompt, behavior reference, upload and job artifacts. `take` now requires a per-part `EXECUTION.json` instead of assuming that the original unnumbered files describe the executed request. All paths are repository-relative, and every artifact is bound by SHA-256:

```json
{
  "record_type": "presenter_part_execution",
  "part_id": "P01",
  "job_id": "actual-provider-job-id",
  "base_plan": {"path": "path/to/TAKE-PLAN.json", "sha256": "hash"},
  "artifacts": {
    "prompt": {"path": "path/to/active-prompt.txt", "sha256": "hash"},
    "higgsfield_job": {"path": "path/to/active-job.json", "sha256": "hash"},
    "higgsfield_upload": {"path": "path/to/active-upload.json", "sha256": "hash"},
    "native": {"path": "path/to/P01/native.mp4", "sha256": "hash"}
  },
  "generation": {
    "model": "seedance_2_5",
    "mode": "omni_reference",
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "generation_seconds": 11,
    "generate_audio": true,
    "est_credits": 71.5,
    "medias": [
      {"role": "image", "value": "actual-image-media-id"},
      {"role": "video", "value": "actual-behavior-media-id"},
      {"role": "audio", "value": "actual-guidance-audio-media-id"}
    ]
  }
}
```

The helper checks the bound paths/hashes, the selected job ID, provider generation parameters, exact prompt text and media IDs, and the uploaded audio ID. `TAKE.json` retains the original values under `base_plan`, records executed values under `plan` and `execution`, and nests review notes so they cannot overwrite provenance.

`gate` now records its input hashes and `status: diagnostics-complete`. Before a final segment can become `review-ready` or `review-ready-flagged`, its parts need a current `TAKE.json`, gate and `NOTES.json`. Notes require:

```json
{
  "review_status": "complete",
  "reviewer": "named reviewer",
  "method": "what was inspected",
  "review_limitations": "what was not judged",
  "flagged": false,
  "execution_sha256": "hash of EXECUTION.json",
  "restored_sha256": "hash of restored.mp4",
  "sync_gate_sha256": "hash of SYNC-GATE.json"
}
```

Generate `TAKE.json` after those notes. Missing or stale evidence leaves the segment `pending-review`. False weak diagnostic signals preserve a flag even when notes do not add one; they are neither automatic rejection nor creative acceptance. Every eligible index entry explicitly records `owner_accepted: false` and `technical_complete: true`.

The contact-sheet command no longer uses the failing drawtext escape sequence. It renders the sampled sheet and writes a neighboring JSON record with the source hash, duration, sampling rate, row/column count, reading order and output hash.

Seven additional temporary-fixture checks passed: active r2 provenance and a 12-second execution overriding the preserved 13-second base plan; pending review with missing evidence; ready but unaccepted state with complete evidence; weak-signal flag retention; stale restoration invalidation; stale execution refusing to replace TAKE; and successful contact-sheet rendering. No production media or conform writes were used in these checks.

## Reused provider prefix provenance

P01a reuses the original P01 provider result at its original speed. It is not a new generation using the shorter restoration audio. `resolve_execution` now accepts this explicit, bounded derivation:

```json
{
  "derivation": {
    "method": "prefix-frame-selection-no-retime",
    "source_native": {"path": "path/to/P01/native.mp4", "sha256": "hash"},
    "source_frames": [0, 108],
    "source_fps": 24,
    "source_frame_count": 265,
    "derived_native": {"path": "path/to/P01a/native.mp4", "sha256": "hash"},
    "restoration_audio": {"path": "path/to/P01a/audio/narration.wav", "sha256": "hash"}
  }
}
```

The original prompt, generation parameters, job receipt, and full guidance-audio upload remain bound under the existing execution fields. The derived native must match `artifacts.native`; the restoration audio must match the current part's WAV. All three file hashes are validated. The range must be a nonempty prefix inside the recorded source frame count. Read-only ffprobe checks require both files at 24 fps, the source count matching its declaration, and the derived count matching the selected prefix. The existing active-plan hash selection and `selected_plan` binding are preserved.

`TAKE.json` now records `provider_source` with the original provider job, guidance upload, and source native, plus a separate `restoration_audio` binding for the current narration slice. No equality between these audio sources is asserted. The derivation method remains a recorded production operation; frame counts and hashes do not by themselves prove visual identity after re-encoding. `P01a/NATIVE-DERIVATION.json` retains the executed selection commands and source bindings.

One isolated temporary fixture passed the valid derived case and verified the distinct TAKE fields, unchanged direct-generation path, and rejection of stale source/native/restoration hashes, non-prefix or out-of-bounds ranges, incorrect source or derived frame counts, a changed derived frame rate, and a different active plan. Each failure preserved the prior TAKE. Read-only checks of the actual production files confirmed **P01: 265 frames at 24 fps; P01a: 108 frames at 24 fps**. Python syntax parsing passed. No provider calls, renders, production media writes, gate changes, or production TAKE writes were performed.
