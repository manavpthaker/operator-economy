# Source-Format Inspection and Conversion Record

Template version: proposed Step 2 v0.2.

One record covers one immutable native source and its first PCM derivative. A later edit or master is
not another source conversion.

## Source identity

- Episode or fixture ID:
- Take/chunk/pickup ID:
- Native source path/SHA-256:
- Provider job or human session ID:
- Inspection tool/version:
- Inspected by/date:

## Requested and observed format

- Requested first format: native PCM
- Actual container:
- Actual codec:
- Actual sample rate:
- Actual bit depth, when meaningful:
- Actual channel count:
- Actual duration:
- Audio origin: `native_pcm` / `lossy_mp3`
- Fallback reason: none / `pcm_capability_unavailable`

Fail when a synthetic source is not native PCM and is not exactly `mp3_44100_192` with the permitted
fallback reason. A renamed extension does not change the observed codec.

## Audible fallback review

Complete when audio origin is `lossy_mp3`.

| Artifact | Result | Timecodes/findings |
| --- | --- | --- |
| Swirling or watery tails | pass / fail | |
| Pre-echo or transient smear | pass / fail | |
| Harsh or damaged sibilance | pass / fail | |
| Consonant or intelligibility loss | pass / fail | |
| Unacceptable mismatch with adjacent sources | pass / fail | |

## Single PCM conversion

- Conversion required: yes / no
- Conversion tool/version and exact recorded invocation identity:
- Conversion count from this native source: `0` only when already exact working format / otherwise `1`
- Output path/SHA-256:
- Output contract: PCM WAV / 48 kHz / 24-bit / mono
- Output inspected and contract matched: yes / no
- Any lossy intermediate after native acquisition: no / yes, fail

## Truthful labeling decision

- Delivery lineage: native PCM / PCM derived once from `mp3_44100_192`
- Native-lossless claim permitted: yes only for inspected `native_pcm` / no
- Result: passed / failed / blocked
- Reviewer/signature/date:
