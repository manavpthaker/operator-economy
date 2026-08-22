# Narration Technical QC

Template version: proposed Step 2 v0.1.

## Authority

- Episode:
- Narration master path:
- Narration master SHA-256:
- QC tool/version:
- Technical reviewer/date:

## File contract

| Measurement | Required | Observed | Result |
| --- | --- | --- | --- |
| Container/codec | WAV / PCM | | |
| Sample rate | 48 kHz | | |
| Bit depth | 24-bit | | |
| Channels | mono | | |
| Duration | matches lock candidate | | |
| True peak | at or below -3 dBTP | | |
| Clipping | none | | |

## Diagnostic measurements

- Integrated loudness:
- Loudness range:
- Peak sample level:
- Noise-floor observations:
- DC offset or phase issue:
- Dropouts or corrupt regions:

Integrated loudness is recorded for consistency and downstream planning. It is not the final program-loudness approval.

## Listening inspection

| Check | Result | Timecodes/findings |
| --- | --- | --- |
| Distortion or clipping | pass / fail | |
| Abrupt room-tone or timbre changes | pass / repair / pickup | |
| Audible edit joins | pass / repair / pickup | |
| Plosives, sibilance, mouth noise | pass / repair / pickup | |
| Over-denoising or processing artifacts | pass / fail | |
| Natural breaths and pauses | pass / revise | |
| No music, SFX, ambience, or final limiter | pass / fail | |

## Decision

- Result: pass / repair and rerun / pickup / blocked
- Required actions:
- Reviewer/signature/date:

This QC applies only to the exact master hash above. Any sample-level change requires a new report.
