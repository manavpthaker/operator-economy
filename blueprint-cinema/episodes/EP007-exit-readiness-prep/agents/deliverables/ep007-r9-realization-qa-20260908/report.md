# EP007 R9 shot D: source and continuity QA

Reviewer: `qa_reviewer`, independent worker `r9_realization_qa`. Reviewed 2026-09-08.

## Recommendation

Use **source 0.416666667–7.583333333 seconds** as the candidate for the 7.166666667-second D slot: source frames **10–181 inclusive**, with out at frame 182, at 24 fps. This is 172 frames, leaves ten frames before and eleven after, preserves her lowered-eyeline entry, and finishes after the eyes lower again. The source is unchanged; this is a trim recommendation, not a selected-media mutation or approval.

The tighter scale and closed mouth make D a usable **review candidate** after C's answer has stopped. It does **not** exactly deliver the fixed-gaze performance in the prompt. No trim of the requested length can remove the middle eye lift. Do not describe it as a perfect silent-realization prompt match.

## Review evidence and limits

- Frozen D video, prompt, and response hashes matched before inspection and were checked again at packet validation.
- Inspected one full-frame eight-sample contact sheet already produced by root, a new 32-sample full-frame sheet using FFmpeg `fps=4`, all **193 decoded frames as mouth crops**, and a side-by-side C/D cut boundary.
- Boundary comparison: retained R8 C source **6.875 s** versus D source **10/24 s**.
- Display: local decoded PNG/JPEG images inspected through the image viewer; full-frame samples approximately 480 pixels wide each, boundary samples 958 pixels wide each, mouth crops 250 pixels wide each.
- **No continuous playback with the locked narration was performed by this reviewer.** Dense mouth inspection is frame review, not an audiovisual comprehension verdict. Emotional rhythm, temporal skin artifacts at speed, and the film-to-graphic handoff remain for root's assembled preview review.
- No competing server, source change, new generation, paid service, external write, canonical state change, final composition render, or owner approval occurred.

## Findings

| Finding | Severity | Evidence | Recommendation / owner |
|---|---|---|---|
| Fixed lowered gaze does not persist. The eyes lift toward screen-right/buyer around source 1.5–2 s, hold there through approximately 5 s, and lower by approximately 5.5–6 s. | Major against the literal performance prompt; not a technical media rejection | `proof/shot-d-4fps.png`, rows 2–7; root's contact sheet also catches a natural blink. Times approximate because full-frame review is sampled. | Root/director should judge with the actual narration whether this reads as a silent check of the buyer followed by inward recognition, rather than silently claiming the original held-gaze direction succeeded. Every possible 7.166667-second window includes the eye lift. Do not add a generation retry within this work order. |
| The mouth stays closed; slight lip/jaw tension changes do not form a speaking cycle. No fresh answer, open mouth, gasp, smile recovery, or exaggerated reaction was observed. | Observation | Every source frame represented in the two mouth-crop sheets, frames 000–192. | Keep the no-character-dialogue contract. Exact jaw-setting onset is subtle; do not claim a precisely timed emotional gesture from samples alone. |
| Character and spatial continuity survive the tighter cut. Gray hair, visible small stud, worn brown shirt, workshop window/tool palette, screen-right orientation, and lowered gaze match the incoming C frame. | Observation | `proof/c-to-d-boundary.png`: C left, D right. | Use the proposed frame-aligned in point. The crop is intentionally closer and clips the top of the hair; no added digital push is needed. |
| Camera/background appear stable. No buyer, hand, new object, text, role reversal, or side switch appears. Modest face/shoulder micro-motion remains. | Observation | Full-frame samples across the source. | Retain source framing. This is sampled visual evidence, not a measured optical-flow test or a guarantee against all temporal generation artifacts. |
| D is slightly more concentrated/serious at entry than C, so the cut itself supplies some pressure. The middle raised eyes can also read as listening. | Observation / interpretive risk | C/D boundary plus full-frame samples. | Review local 17–24.166667 against the locked arithmetic line. Do not overstate that the source unambiguously shows mental arithmetic or stress without the narration. |

## Technical and provenance facts

- File: `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r9-realization-model/renders/candidates/shot-d.mp4`.
- SHA-256: `c09986f249dcdfe365a9bbd56fef13b89760f71d0503b8a31e3745ff7715fa4c`.
- Container duration: **8.041667 seconds**. One H.264 video stream, **1916×1080**, **24/1 fps**, **193 frames**, `yuv420p`. **No audio stream.** Source color tags were absent from the requested probe fields; color-management identity is unknown.
- FFmpeg full-source decode completed with exit 0 and no reported errors.
- Response record: existing Kling v3 Pro image-to-video generation through fal.ai, request `01a081ec-17f8-7c60-8b31-e419124b6f6c`; `generate_audio: false`; requested duration `8`; CFG 0.5. This worker did not invoke it.
- The response's `resolution: 720p` is request-record/helper metadata, not the actual source dimensions; use the probe dimensions above.
- Generated people and scene are illustrative and non-evidentiary. Rights/disclosure acceptance and owner creative acceptance are not conferred by this review.
- Additional continuity source C SHA-256: `8293c4bcc201259cb4624c94673690c1ec1d34a0bcdfa63464eae0a91feda60e`. Root's extracted C continuity PNG SHA-256: `0bac55f9d1890a3ed1491fea6716dce4605f07675be8ff3b0cf97583e022d14f`.

## Proof index

- `proof/shot-d-4fps.png`: 32 full-frame samples, row-major, four columns. Each row spans approximately one source second. FFmpeg fps resampling means these are nominal quarter-second bins, not exact source-frame timestamp labels.
- `proof/c-to-d-boundary.png`: C 6.875 s on left; D 0.416666667 s on right.
- `proof/d-mouth-frames-000-095.png`: all source frames 0–95, row-major, 12 columns.
- `proof/d-mouth-frames-096-192.png`: all source frames 96–192, row-major, 12 columns; remaining bottom-row cells are padding, not black source frames.

## Remaining decision

Root should play the assembled C → D → model passage once with the actual VO and once muted. The question is whether the middle eye lift strengthens or distracts from quiet realization before the model explains the dependency. This packet completes the bounded source review; it approves no production gate or final shot selection. Canonical episode identity/input-lock files are absent, and the work-order gate label is an isolated-test placeholder only.
