# Narration Technical QC

Template version: proposed Step 2 v0.2.

## Authority

- Episode:
- Narration master path:
- Narration master SHA-256:
- Native-source register path/SHA-256:
- Source-format conversion record path/SHA-256:
- Audio origins present: `native_pcm` / `lossy_mp3` / both
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

## Acquisition and conversion truth

- Actual native codecs were inspected rather than inferred from filenames: yes / no
- Native PCM was requested first for synthetic capture: yes / no / human path
- Every `lossy_mp3` source is exactly `mp3_44100_192`: yes / no / not applicable
- Every fallback reason is `pcm_capability_unavailable`: yes / no / not applicable
- Every fallback passed audible artifact review: yes / no / not applicable
- Each fallback was decoded/resampled exactly once into 48 kHz, 24-bit, mono PCM: yes / no / not applicable
- No lossy intermediate entered the chain afterward: yes / no
- Master is truthfully labeled native PCM or PCM delivery derived from lossy source: yes / no

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
| Lossy-codec swirls, watery tails, pre-echo, smeared sibilance, or damaged consonants | pass / fail / not applicable | |
| Natural breaths and pauses | pass / revise | |
| No music, SFX, ambience, or final limiter | pass / fail | |

## N6 technical decision

- Lexical-conformity report is current and passes: yes / no
- Word transcript and pause map match this master hash/duration: yes / no
- Complete provenance and edit decision list are current: yes / no
- `technical_pass`: true / false
- N6 gate result: pending / passed / failed / invalidated
- Workflow outcome: in_progress / returned_to_editorial / blocked
- Required actions:
- Reviewer/signature/date:

`technical_pass` applies only to the exact master hash above. It is not creative approval. Any
sample-level change invalidates this report and every later state.
