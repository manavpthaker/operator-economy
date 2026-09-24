# R8 context coverage — 17-second review candidate

Date: 2026-09-08. Status: generated and mechanically checked; awaiting owner creative review. No canonical episode gate advanced, final delivery rendered, publication, commit or push.

Preview: http://localhost:3018/?review=r8#project/r8-context-coverage?v=1&t=0&tab=design&rc=0

## What this test contains

Unchanged master narration 10.920–27.920, 17 seconds / 408 frames at 24 fps. Reused R7 shared exchange, then two newly generated Kling close angles. No additional character audio, lip-sync claim, sketch, equation, avatar, meeting pre-roll, music or effects. These are illustrative synthetic characters, not case evidence.

| Shot | Record seconds | Source seconds | Purpose |
| --- | --- | --- | --- |
| A, preserved R7 | 0–3.833333 | 0.320–4.153333 | Shared rapport |
| B, new Kling | 3.833333–10.083333 | 0–6.250 | Buyer asking; attentive eyeline |
| C, new Kling | 10.083333–17 | 0–6.916667 | Owner's readiness, attempted answer and uninterrupted pause |

The context-sensitive film-direction skill selects narrated dramatization and motivated hard cuts here. It permits illustrative mouth movement but does not imply literal spoken dialogue. No decorative camera move or compulsory cut-frequency rule was added.

## Actual performance and editorial judgment

Both new source ins were adjusted from the drafted 0.750 seconds to 0.000 after inspecting the generated performances; record boundaries and locked narration did not change. B asks earlier than requested, so the earlier source in moves that behavior later against the narration. C's earlier source in retains readiness and places the lowered gaze closer to “stops.”

Timing is approximate, not exact lip sync. B's visible asking still partly precedes the complete narrated question. C settles her mouth before the narrated “stops”; her gaze lowers around source 5.5–6 seconds. No claim that she visibly says exactly four words.

**Review watchpoint:** around C source 3.5–4 seconds, the buyer moves out of the foreground. This may read as withdrawal rather than patient presence. Retained for this bounded review, not accepted as production-ready; no additional regeneration authorized or attempted.

The future four-second nonverbal meeting/sitting lead-in is recorded in the execution authorization but is not included in this test. The avatar introduction remains a later separately synchronized take.

## Verification and limits

- `node --check verify-r8.mjs` and `node verify-r8.mjs`: pass. Exact source hashes, contiguous frame windows, silent film, references and narration sample equality checked. Latest receipt: `renders/verification.json`.
- Both new MP4s decoded through FFmpeg without errors. Each is H.264, 1916×1080, 24 fps, with no audio stream. B delivered 8.041667 seconds and C 9.041667 seconds.
- HyperFrames check passed with zero lint, runtime and layout errors/warnings across 0.1, 3.791667, 3.875, 7, 10.041667, 10.125, 12, 14.5 and 16.958333 seconds. Motion-intent checking was disabled; contrast checked zero text elements. This is not a full creative pass.
- Inspected both source contact sheets at half-second intervals and generated composition frames, including opening, answer and last included frame.
- Live Chrome Studio initially held C while rewinding. A full page reload resolved it without composition changes. Subsequently verified correct A at 0, B at 7 and C at 12 seconds, and rewound to the opening. No browser error/warning entries were returned. Playback reached 17 seconds; the excluded exact endpoint displays white. Last included frame at 16.958333 is covered.
- Narration PCM equality is verified; an audio listening review is not claimed.
- Only the new project's HyperFrames pin changed from 0.8.30 to 0.8.31; final checks used 0.8.31. Repo-governed skill copies were preserved. HeyGen is not signed in and was not needed for retained Fal/Kling or existing locked audio.
- R7 composition hash remains `78d869c031297d453fde1f3439fda8e847d9fec250447ae3a21e4453d1c98f6b`.

## Generation receipt

Exactly two new Fal requests, `fal-ai/kling-video/v3/pro/image-to-video`, audio off, CFG 0.5, no retries. B requested 8 seconds; C requested 9. Provider request IDs, file hashes, reference hashes and selected windows are in `ASSET-MANIFEST.json` and the machine receipt. Full prompts are in `SHOT-B-PROMPT.md`, `SHOT-C-PROMPT.md` and `REFERENCE-RECORD.md`. Raw video responses remain in `renders/candidates/`.

Video-only current list estimate: $1.904 ($0.896 + $1.008), not invoice-verified spend. Reference-image generation cost is separate and unverified. The helper's “720p proof” wording is local metadata, not a Kling resolution control; actual output dimensions were probed above.
