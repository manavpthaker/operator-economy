# Look-transfer review builder

`build_review.py` is a separate, inactive assembly path. It reads the frozen r4 candidate and source audit, and writes only new files under `assembly/r5-look-transfer/` and `assembly/qa/r5-look-transfer/`. It never changes current clips, narration, review pages, presenter indexes, execution plans or owner locks. Nothing has been rendered.

Full mode requires exactly these 15 replacements: `seg009, seg012, seg019, seg021, seg028, seg035, seg037, seg044, seg055, seg059, seg071, seg072, seg073, seg074, seg075`. P00 and films cannot be selected. A missing, stale, malformed or flagged replacement blocks the entire full build. The original 29,323-frame timeline, P00 opening, all films, word cues and frozen narration remain intact. Only the P08 picture-description field changes to describe its new speaking picture.

Pilot mode accepts exactly one existing moving presenter segment and creates a separate **original-left / candidate-right** comparison at 2560×720, with the unchanged master excerpt. It may retain pending performance review; it does not establish full-build eligibility. P08 is excluded from pilot mode because its current picture is a still, not the performance being preserved.

## Selection manifest

All bindings are `{ "path": "repository/relative/file", "sha256": "full hash" }`. Supply a new file with:

```json
{
  "record_type": "ep009_look_transfer_review_selections",
  "status": "selected_for_review",
  "base_build": { "path": ".../assembly/r4/ep009-full-r4-opening-candidate-BUILD.json", "sha256": "fad999994483aa029f045a4b1ac6286ca42e7aef91b43fcb454822e5363bec02" },
  "source_audit": { "path": ".../presenter-look-transfer/SOURCE-AUDIT.json", "sha256": "77d1300b3f52841209013af3523124bbca9568061f6cac35fb6026de0184224d" },
  "master": { "path": ".../assembly/r3/narration-master-r3.wav", "sha256": "0f0d5d326262813cb5ff5392fb263f15f6a8e871ad22e54c1274ff974037ca85" },
  "look_reference": { "path": ".../presenter-regen/look/L3-chambray.png", "sha256": "0b529748f457774986e661dcfe31e916ad9507c8f7cf4803171cb602a012d7c5" },
  "replacements": [{
    "segment": "seg074",
    "kind": "look_only_existing_performance",
    "source": { "path": ".../presenter-look-transfer/NEW-VERIFIED-CLIP.mp4", "sha256": "FULL_HASH" },
    "verification": { "path": ".../NEW-VERIFICATION.json", "sha256": "FULL_HASH" },
    "output_frames": [28849, 29137],
    "source_start_frame": 0,
    "frames": 288
  }]
}
```

The shortened paths above are illustrative; use complete repository-relative paths from `SOURCE-AUDIT.json`. Full mode requires all 15 records. Each replacement must be a separate MP4 under `presenter-look-transfer/`, with exactly the selected segment's frame count, 1280×720, consecutive 24 fps timestamps from frame zero, and no added hold or fallback source.

## Required verification carrier

Each verification JSON must bind `segment`, `replacement`, `original_source`, `output_frames`, `master` and `look_reference` to the exact selection/source-audit values, and contain:

```json
{
  "record_type": "ep009_look_transfer_replacement_verification",
  "status": "verified",
  "technical_complete": true,
  "errors": [],
  "master_sample_range": [57698000, 58274000],
  "master_pcm_sha256": "6d4cd5d81f23c21deaeab4aadfb4b1038965c05127778c24f78d05451dd831b2",
  "original_frame_sequence_sha256": "cba737f0d1135cf591d43ac4044076bcb66de044bedce8e51b9ba3f03f69bc83",
  "replacement_frame_sequence_sha256": "COMPUTED_FROM_ACTUAL_REPLACEMENT",
  "scoped_review": {
    "status": "complete",
    "flagged": false,
    "reviewer": "ACTUAL_REVIEWER",
    "method": "ACTUAL_METHOD",
    "limits": "ACTUAL_LIMITATIONS",
    "target_appearance_matches": true,
    "identity_preserved": true,
    "change_scope_confirmed": "outfit_and_environment_only",
    "preserved": {
      "hands": true,
      "facial_expressions": true,
      "head_and_body": true,
      "camera_and_crops": true,
      "timing": true
    },
    "evidence": [{ "path": "ACTUAL_REVIEW_ARTIFACT", "sha256": "FULL_HASH" }]
  }
}
```

The sample audio/frame hashes are the real original **seg074** values, verified offline. They are not replacement evidence. Obtain other values using the helper's read-only `audio_digest(master_path, output_frames)` and `video_hashes(video_path, expected_frames)` functions. Frame hashing decodes yuv420p frames in order with FFmpeg SHA-256, then hashes the newline-delimited frame hashes, including a final newline. Exact PCM hashing includes only the fixed 1,080-sample final silence when a range reaches the episode end. These hashes bind reviewed pixels/audio; they do not prove performance preservation.

For a pilot comparison, technical verification and hashes are still mandatory, but `scoped_review` may be `pending` or flagged. Full mode requires the complete unflagged scoped review above. A positive technical result never creates those review judgments automatically.

**P08:** use `kind: "corrected_P08_performance_exception"`, the exact 343-frame slot `[15920,16263)`, and add `corrected_script` bound to `narration-revisions/r3-hospitality/paragraph.txt` plus `old_P08_speaking_picture_used: false`. Its scoped review must include `corrected_dialogue_reviewed: true`, target appearance and identity checks. Existing-performance preservation fields do not apply to the superseded P08 speaking take; that exception remains explicit.

## Invocation

From the repository root, using system Python 3 and installed FFmpeg:

```sh
python3 blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/_tools/build_review.py check --manifest ACTUAL-MANIFEST.json
python3 blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/_tools/build_review.py prepare --manifest ACTUAL-MANIFEST.json --name ep009-r5-look-transfer-review-r1
python3 blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/_tools/build_review.py render --manifest ACTUAL-MANIFEST.json --name ep009-r5-look-transfer-review-r2
python3 blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/_tools/build_review.py render --mode pilot --segment seg074 --manifest ACTUAL-PILOT-MANIFEST.json --name pilot-seg074-look-r1
```

`check` writes nothing. `prepare` writes a new BUILD and graph only. `render` prepares and encodes under a **fresh name**; it refuses existing artifacts, so a prior prepared name cannot be reused. The output remains `encoded_unverified_review_only` until separate full decode, unchanged-master audio comparison, source mapping, joins and performance review are completed. There is no automatic page publication, plan activation, owner acceptance or release promotion.

Preparation validation is recorded in `presenter-look-transfer/SKELETON-QA.json`: seven negative inventory checks, exact required/full and one-item pilot inventory, real seg074 decoded-frame sequence and master PCM hashes. No replacement has been fabricated and no media has been rendered by this task.
