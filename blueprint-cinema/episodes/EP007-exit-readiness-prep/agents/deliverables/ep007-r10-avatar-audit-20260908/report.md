# R10 avatar availability audit: Test Q

Read-only audit, 2026-09-08. Work order `ep007-r10-avatar-audit-20260908`; QA reviewer. The work order's original M objective is superseded for selection by the parent's explicit task update and the user's current answer, **“use test Q.”** No presenter files, provider state, or episode gates were changed.

## Result

**Use Q's source and request recipe for a new exact-introduction take. Do not reuse Q's existing mouth footage:** that file speaks the 5.600-second scope excerpt, not the introduction. No generated exact-introduction video was found in the presenter or current net-new experiment during this audit. The exact introduction WAV is already prepared and independently matches the locked master PCM.

Q is in `blueprint-cinema/experiments/EP007-PRESENTER-001/repair-r18/`. No `repair-r19/` existed at inspection. Q is rendered, not an observed in-flight request. No new request was submitted or provider queried by this reviewer.

The local Q status still records `rendered_qa_pending` and `performance_owner_accepted: false`; its README still names M as the accepted baseline. Those records predate the user's current selection of Q. That selection supports using the Q recipe for this introduction test, not a full-episode or release approval. The top presenter README has not caught up with P/Q and is not current selection authority.

## Exact Q recipe

Read `repair-r18/video-request.json`; comparison with `repair-r14/video-request.json` confirms **only `image` and `title` changed from M**. The motion prompt is byte-identical.

```json
{
  "type": "image",
  "image": {
    "type": "asset_id",
    "asset_id": "c3d34de484624626864053cb3dbe11cb"
  },
  "audio_asset_id": "f5e2f0c3d9b341e893e15201e326aab1",
  "expressiveness": "low",
  "motion_prompt": "The presenter speaks with a neutral, matter-of-fact expression. His head stays upright and centered, chin level, shoulders relaxed and still. Small precise lip movements articulate the audio, with a relaxed jaw and eyebrows. Natural blinking.",
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "fit": "cover",
  "title": "EP007 - Test Q - M direction visible hands"
}
```

The recorded route is **direct-image Avatar IV**. The image is O's visible-hands study source, not a saved talking-avatar look or M's tighter source. For the introduction, the scope `audio_asset_id` above **must be replaced** with the newly uploaded exact introduction WAV. The title can identify the introduction. Preserve the other Q settings; the new generated performance cannot be guaranteed to duplicate Q's motion.

All paths below are relative to `blueprint-cinema/experiments/EP007-PRESENTER-001/` unless stated otherwise.

| Artifact | Verified identity |
|---|---|
| `media/repair-r16/study-visible-hands-source.png` | SHA256 `2abb05079084198c21a33802e6e0aa6373027a65f2163ea5a9114f77c1c4da24`; image asset `c3d34de484624626864053cb3dbe11cb` |
| `media/repair-r18/test-q-m-direction-visible-hands-1080p.mp4` | SHA256 `8675571508e53e3f57ecefe42994b71f9b710e7e3603f1ad1c9a454c66574950`; video ID `9ae293a0f1b4938d070d21b1b0a07651` |
| `media/repair-r2/scope-two-sentences.wav` | SHA256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`; audio asset `f5e2f0c3d9b341e893e15201e326aab1` |
| `media/presenter-01-introduction.wav` | SHA256 `0604f9d4bf455970500d606a36778e9f9d0b9e4e61ec01ce4b930ada2b002201`; no intro upload or generated video ID found in the inspected records |

## Introduction timing and audio identity

- Locked words: **W000118–W000190**, 73 words, first “This” at master **48.520**, final “all.” ends at **74.000**. The transcript tokens exactly match the presenter manifest's introduction text.
- Prepared WAV source range: master **48.270–74.250**, **25.980 seconds**, 48 kHz, mono, signed 16-bit PCM. Speech starts at clip **0.250** and ends at **25.730**.
- Master samples: **2,316,960–3,564,000**, exclusive out; **1,247,040 samples**. Independently decoded PCM is byte-equal to that exact master slice.
- Master SHA256 independently matches the pinned manifest: `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9`.
- Preserve the continuous locked master as final audio authority. Trim the generated picture using its measured audio alignment and the recorded handles, without changing narration speed. Q's measured delay is **not** a guaranteed delay for a newly generated introduction.

## Q technical / audio checks

Q probes as H.264, **1920×1080**, **25 fps**, **140 frames / 5.600-second picture**; AAC audio, 48 kHz stereo, **5.612 seconds**. Full decode to FFmpeg null completed without errors.

The input scope WAV independently matches master **591.050–596.650** exactly in decoded PCM. Q's returned audio has normalized correlation **0.9992925** against the scope input after a measured **23 ms delay**, using mono 4 kHz decoded float PCM and a ±100 ms lag search. This supports scope-audio identity; it does **not** judge lip-sync, mouth/head motion, acting, or visual quality.

Q's status records an observed right-hand lift during each sentence, with the left mostly resting. That is an inherited observation, not a fresh visual performance review by this worker. No moving-picture creative pass was performed because the work order concerns identity, availability, and recipe provenance.

## Source pins and inspection limits

The three issued work-order inputs matched before inspection and again before packet handoff. Auxiliary Q records were live evidence, permitted by the parent's task update, not retroactively added to the issued work order:

| Auxiliary source | Observed SHA256 |
|---|---|
| `README.md` | `3376f3a8baa1e2c1a8167da664a2cbd41cf961f1f6cae17a56822772b9472227` |
| `repair-r14/video-request.json` | `848877f9226ca3114cafab6664cd91c8959d945741c82fb3dab8be3126ab0d1a` |
| `repair-r18/README.md` | `5d275b3f299c3b632e96c5a90bf8ed5ca2b09467614cd831dce9cec12491c8d2` |
| `repair-r18/video-request.json` | `211ed64d9be57879a8298fa4392cf7817778660b4dcff4a1b2f274078469ed31` |
| `repair-r18/status.json` | `a42b31c106ac2a59001309f76c1999659afead75823503d31ef2e6ab6cf6f925` |

Discovery covered the presenter experiment's local media, manifests, readmes, request/status records and exact intro/Q references in the net-new experiment. It was not a provider-account inventory. A separate task could create a new intro after this snapshot; the orchestrator should coordinate before submitting one to prevent duplication. No credentials, account status, billing, or remote jobs were inspected.

The canonical episode has no top-level `README.md`, `episode.json`, or input lock at the inspected location; this is an isolated wave-zero audit, not a claim that any canonical visual gate exists or has passed. The generic packet CLI assumes canonical episode state and Blueprint-root-relative input paths; this work order uses repo-relative cross-boundary inputs. JSON Schema and explicit current-hash/ownership checks are therefore the applicable checks here, not a fabricated canonical-state validation.
