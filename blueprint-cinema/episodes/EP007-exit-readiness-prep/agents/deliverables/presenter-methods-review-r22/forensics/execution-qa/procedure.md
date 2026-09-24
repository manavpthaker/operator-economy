# Native-output QA for the four-sample photo/audio benchmark

Status: all four native outputs received and technically checked, with sampled-frame observations recorded. Full-speed audiovisual review and owner acceptance remain unverified; see four-output-observations.md and review-records.json.

## Fixed inputs and controls

- Image: [existing O/Q photo](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/media/repair-r16/study-visible-hands-source.png), SHA256 `2abb05079084198c21a33802e6e0aa6373027a65f2163ea5a9114f77c1c4da24`.
- Audio: [original 5.600s WAV](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/media/repair-r2/scope-two-sentences.wav), SHA256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`; 268,800 samples at 48kHz. Exact text: “I will be straight with you about my own position. I have never sold a business.”
- Same-image control: [Q](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/media/repair-r18/test-q-m-direction-visible-hands-1080p.mp4), SHA256 `8675571508e53e3f57ecefe42994b71f9b710e7e3603f1ad1c9a454c66574950`.
- Historical mouth/head reference only: [M](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/media/repair-r14/test-m-direct-study-image-steady-head-1080p.mp4), SHA256 `dc6d9f8e6421fda85f56ddbb6c08e588695dce8ae434c0bf18855b4c59d3e526`. Its different framing prevents a raw-pixel motion comparison or inherited acceptance.
- Four anonymous review labels A1/A2/B1/B2 map to two independent samples per parent-selected model. Populate the exact model/version, run ID, request path and native output hash from the parent's handoff. The labels make no claim about a completed generation.

## 1. Verify untouched native files

Hash the delivered file; bind the request, fixed-input hashes and result ID. Preserve the native output bytes. Probe codec, dimensions, aspect, sample rate, channel layout, frame rate, frame timestamps and stream duration. Run a complete decode and check for corrupt or missing frames, truncated speech, frozen spans or unexpected audio absence.

New models may return another native frame rate, resolution or duration. Do not require Q's 25fps/140 frames or silently convert them to match. Assess source-audio coverage and actual timestamps. Padding is a recorded result; no trimming, respeeding, frame replacement, optical-flow repair or geometric correction is part of this review. No new old-clip renders.

## 2. Check audio provenance and timing separately from lips

Compare decoded output audio against the original WAV. A lossy provider encode need not have the same file or PCM hash. Measure the candidate's own lag with adequate nonsilent windows across both sentences and record alignment quality, clock-rate/drift evidence, audible wording/prosody changes, pause coverage and final-word picture coverage. Do not inherit Q's 23.021ms lag or treat correlation alone as proof of sync.

Decode/resample only in disposable diagnostic data for comparison, preserving native media. If the native result lacks audio or contains altered speech, record that fact immediately. A separately authorized original-audio remux must be distinctly labeled and independently aligned; it must never be passed off as the untouched native result.

## 3. Conduct full-speed audiovisual review first

An actual observer watches each entire native clip at 1x, with its audible track, without seeking or face stabilization. Record artifact hash, observer, player/display, playback rate, audio enabled, start/end, date and findings. Judge before showing model names or movement metrics.

Review each criterion independently:

| Criterion | Required observation |
|---|---|
| Mouth/word match | Both sentences articulate the spoken syllables; inspect especially the second sentence rather than assuming the new model fixes it. |
| Visual emphasis | “Straight” and “never” do not trigger an unwanted large jaw opening, nod, thrust or brow accent. |
| Head/body connection | Natural residual motion; no head-size pulse, detached neck, neck stretching or pose snap. |
| Hands/arms | Restrained plausible movement, supported arm continuity, no repeated emphatic lift, finger mutation or face crossing. |
| Pause/end | Plausible resting mouth and expression between sentences; no continuing false speech; final word and settling pose complete. |
| Identity/room | Face/glasses/wardrobe consistent with source; shelf and room do not bend or pulse. |

Compare Q at its native framing for the actual same-image improvement. Use M only to show the historical mouth/head preference. Judge at a practical normal display size; inspect enlarged details afterward.

## 4. Diagnose specific concerns

After the 1x pass, use native-PTS stills or short contact strips around actual “straight,” “never,” the inter-sentence pause, and first/final speech. Map source events through each candidate's independently measured audio offset; transcript word ranges are not phoneme labels. Add slow playback only to identify onset/closure errors or edge defects. Frame-aligned strips support diagnosis and cannot certify continuous naturalness.

When there is no continuous audiovisual observer, report `full_speed_playback_performed: false`, `visual_lip_sync: unverified`, and `naturalness: unverified`. Report only the actual sparse observations. A browser's play/pause state, elapsed-time progression, successful decode, video embed, or screenshot sequence does not establish that an agent perceived the full motion with sound.

Tool discovery in this session found local image/file/UI inspection but no exposed local continuous audiovisual analysis tool. An external scene-analysis service exists but requires an upload/provider call; it is outside this read-only work order and is not a substitute used here. No such call was made.

## 5. Decide and stop

Keep integrity, sampled observations, continuous playback judgment and owner acceptance as separate fields. Native output that passes technical checks remains a candidate. Explicit owner playback determines acceptance; do not average away a mouth-sync or unnatural-motion failure with good metrics.

Review all four returned results once. Report model samples individually: two good samples is promising but not a reliability estimate; one good sample is an isolated candidate. If none meets the owner's standard, stop this benchmark. Do not add prompt retries, image edits, head stabilization, audio alteration, new recordings or reference videos. No longer-passage expansion until one exact short candidate is accepted.

The prepared [review records](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/review-records.json) contain four empty candidate slots; pending and unverified fields must remain so until corresponding evidence exists.
