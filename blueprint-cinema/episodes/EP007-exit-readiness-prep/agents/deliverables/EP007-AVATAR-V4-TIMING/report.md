# EP007 avatar V4: question crop timing

Status: completed timing proposal for the orchestrator; no new video, edit, approval, or episode-state change.

Recommend one picture-only hard cut from the wider master to a closer crop at **master 17.833333 seconds, zero-based frame 428 at 24 fps (00:00:17:20)**. Keep the same continuous source take and uninterrupted original narration. Hold the closer crop through the entire question and the final settle.

## Exact locked passage

| Word ID | Token | Master start | Master end |
|---|---|---:|---:|
| W000050 | question. | 16.32 | 16.76 |
| W000051 | What | 17.96 | 18.08 |
| W000052 | happens | 18.18 | 18.48 |
| W000053 | here | 18.58 | 18.70 |
| W000054 | if | 18.76 | 18.93 |
| W000055 | you | 18.96 | 19.02 |
| W000056 | are | 19.06 | 19.18 |
| W000057 | not | 19.20 | 19.38 |
| W000058 | around | 19.44 | 19.80 |
| W000059 | for | 19.82 | 19.95 |
| W000060 | a | 19.96 | 19.98 |
| W000061 | month. | 20.04 | 20.34 |

Preceding sentence: “Then he asks her one more question.” W000044–W000050, master 14.77–16.76. The pause map marks 16.76–17.96 as a 1.20-second intentional pause. The complete question is “What happens here if you are not around for a month.” The next word is W000062 “And” at 21.28, outside this test's 0–20.9-second audio.

These are exact values from the locked forced-alignment file, not sample-accurate phoneme boundaries. In the actual original audio, the 16.7–16.8-second window still has substantial energy. The nominal pause also contains a low-level event around 17.3–17.4 seconds and quieter sound through 17.8–17.9. Preserve it. Waveform inspection cannot determine the precise phoneme or prove that this event is a breath.

## One cue, explicit clocks

| Clock or quantity | Value |
|---|---|
| Original narration/master range | 0.0–20.9 seconds |
| Transcript “What” onset | 17.96 seconds |
| Proposed master-clock cut | 428 / 24 = 17.833333 seconds |
| Lead before aligned “What” | 0.126667 seconds |
| Verified accepted V3 audio placement | +0.04725 seconds in its container |
| V3-container “What” mapping | 18.00725 seconds |
| Equivalent V3-container cut | 429 / 24 = 17.875 seconds; 00:00:17:21 |
| V3-container original audio endpoint | 20.94725 seconds |
| Accepted V3 video extent | 505 frames / 24 = 21.041667 seconds |
| V4-container audio placement | Unknown until the actual V4 restoration is measured |

General cut rule for a source whose original narration begins at offset delta: take the last 24 fps frame boundary at or before (17.96 + delta - 0.125). Equivalently, frame = floor((17.96 + delta) × 24) - 3. Zero-based indexing throughout. With delta = 0 this is frame 428; with V3 delta = 0.04725 it is frame 429.

For a review edit carrying the original WAV from timeline zero, use frame 428 on that timeline. Map picture source time using the actual generated clip's independently measured placement. For a review that preserves the restored clip's own container/audio clock, calculate its crop cue from that clip's delta. Do not apply both corrections or assume V4 will repeat V3's offset.

The cut keeps most of the anticipation in the wider view, then makes the question more direct just before its opening word. The roughly three-frame lead is an editorial proposal, not an alignment fact. A cut at the nominal 17.96-second onset could enter after preparatory mouth movement; a long animated push would add a second movement variable to this hands/framing test. An uninterrupted wide hold remains the simpler alternative if the actual crop reads as an abrupt visual bump.

## Protected continuity and end

- Mode remains presenter_address with presenter_delivery and the exact approved voice. This is a crop of the same speaking take, not another angle or a buyer character.
- The source must advance continuously through the crop boundary. Do not restart, duplicate, freeze, or retime the video/audio there.
- One cue owns both outgoing-wide visibility and incoming-close visibility. Keep the eyes at a compatible screen position; preserve glasses, identity, light and body position.
- Keep all original 20.9 seconds, including the question's final articulation and original tail. Do not trim at the forced-alignment “month.” end of 20.34.
- With audio at timeline zero, at least 502 frames (20.916667 seconds) are needed to include 20.9 seconds on a 24 fps boundary. The authorized approximately 21-second test supplies useful extra picture time. With nonzero insertion, the available source end must cover delta + 20.9 before any frame rounding. Check actual V4 output rather than copying V3's 505-frame count.

## Narrow V4 QA

1. Verify new source hashes, resolution, frame rate and duration, then original-audio overlap, placement and early/middle/late similarity. Accepted V3 rerun: 20.9 seconds overlap, correlation 0.998346, placement +0.04725; this is waveform alignment, not a measured lip-sync error.
2. Review full opening at normal speed with the actual original track. At the crop, inspect frames immediately before/after and a continuous 16.5–18.5-second playback. Check for a source-time jump, clipped opening word, framing bump or hand gesture cut mid-action.
3. In the wide view, inspect complete fingers/wrists, support/contact with the desk, hand crossings and return to rest. In the close view, check actual encoded face detail and articulation; a large portrait or upscaled source does not prove useful crop resolution.
4. Protect the new question and tail, approximately master 17.96–20.9. Check the last spoken word and final settling at speed; a closed-mouth still alone cannot prove complete audio or perceptual sync.

## Evidence and limits

Both assigned media hashes matched. The word transcript and pause map matched the narration lock. Audio placement was recomputed by importing the existing read-only audio_qa.py, overriding its in-memory reference to the pinned WAV, and printing its comparison; no script/source file was changed. Probe: accepted MP4 video H.264, 1280×720, 24 fps, 505 frames; embedded audio AAC mono 48 kHz.

Authoritative inputs and exact hashes are in deliverable.json. The Blueprint Cinema episode directory currently contains agents/review but no README.md, episode.json or input-lock.json; this bounded experiment uses the upstream narration-lock.md and 03-visual-translation/input-lock.json plus the explicit V3 acceptance. The upstream episode README has stale Step 1 status; its newer hash-bound narration lock is the relevant timing authority.

No browser, provider, upload, generation, canonical timeline edit, or approval write occurred. No full audiovisual playback or new V4 output was reviewed in this timing pass. The accepted V3 delivery is retained, not reopened.

Scope exception disclosed to the orchestrator: importing the read-only QA script appears to have created the incidental 6,106-byte Python cache /Users/brownmanbrain/Downloads/avatar-naturalness-review/seedance-v3-opening/__pycache__/audio_qa.cpython-312.pyc. The source script and media are unchanged. The cache is outside the owned packet and is left in place under the no-delete rule; the manifest is partial pending orchestrator disposition of this side effect. The timing proposal itself is complete.

Work-order display ID: EP007-AVATAR-V4-TIMING. The manifest uses ep007-avatar-v4-timing to satisfy the existing lowercase work_order_id schema; owned folder remains exactly as assigned.
