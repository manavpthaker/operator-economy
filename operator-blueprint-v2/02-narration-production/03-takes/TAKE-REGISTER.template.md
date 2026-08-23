# Raw Take Register

Template version: proposed Step 2 v0.2.

Raw files are immutable. Cleaned, edited, or mastered files receive new paths and records.

## Session

- Episode:
- Locked script revision/hash:
- Ordered `W`-token count/SHA-256:
- Voice-and-capture lock revision/hash:
- Capture phase: calibration / full / pickup
- Provider authorization ID, when synthetic:
- Human session or provider batch ID:
- Session date:
- Operator:

## Takes

| Take ID | `W` range | Raw file path | SHA-256 | Duration | Session/job ID | Actual codec/rate/channels | Audio origin | Fallback reason | Known defects | Review state |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | `native_pcm` / `lossy_mp3` | none / `pcm_capability_unavailable` | | unreviewed |

## Completeness

- Every locked section has coverage: yes / no
- Every raw file is registered and hash-verified: yes / no
- Raw files preserved without destructive processing: yes / no
- Actual codec inspected rather than inferred from extension: yes / no
- Every `lossy_mp3` source is exactly `mp3_44100_192`: yes / no / not applicable
- Every fallback passed audible artifact review: yes / no / not applicable
- No legacy `generate_vo.py` path used: yes / no
- Missing or corrupt material:
- Gate decision: N4A / N4B / pickup evidence
- Reviewer/date:
