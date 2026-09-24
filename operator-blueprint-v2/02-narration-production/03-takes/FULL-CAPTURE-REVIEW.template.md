# N4B Full-Capture Review

Template version: proposed Step 2 v0.2.

## Authority

- Episode or fixture ID:
- Locked script path/SHA-256:
- Ordered `W`-token count/SHA-256:
- Current N4A calibration review path/SHA-256:
- Full-capture authorization ID/status:
- Frozen N3 configuration path/SHA-256:
- Capture batch or human session ID:
- Reviewer/date:

## Coverage and provenance

- Every `W` token has raw coverage exactly once or an explicitly reviewed alternate: yes / no
- Chunk map or session ranges are complete and ordered: yes / no
- Every raw file and provider job/session is registered and hashed: yes / no
- Every actual codec and audio origin is inspected: yes / no
- Any MP3 fallback is exactly `mp3_44100_192` with reason `pcm_capability_unavailable`: yes / no / not applicable
- No provider or human configuration drift from N3: yes / no
- No V1 `generate_vo.py` invocation or import: yes / no

## Interim diagnostic review

- Interim ASR artifacts and hashes:
- Every likely addition, omission, substitution, repeat, truncation, and pronunciation problem
  dispositioned: yes / no
- Interim ASR remains diagnostic and is not the final transcript: acknowledged / not acknowledged
- Required same-word pickups:

## Full-run continuity listen

| Check | Result | Timecodes/findings |
| --- | --- | --- |
| Narrator identity and timbre | pass / revise | |
| Pace and energy continuity | pass / revise | |
| Pronunciation consistency | pass / revise | |
| Chunk or session boundaries | pass / revise | |
| Lossy-source artifacts, if applicable | pass / fail | |
| Complete-episode fatigue and credibility | pass / revise | |

## Gate N4B decision

- N4B gate result: pending / passed / failed / invalidated
- Workflow outcome: in_progress / blocked
- Return gate when failed: N3 / N4A / N4B
- Required pickups or wider regeneration:
- Unresolved authorization or continuity issue:
- Reviewer/signature/date:

N4B accepts acquisition coverage only. It does not establish the final edit, lexical conformity,
`technical_pass`, `creative_approved`, or narration lock.
