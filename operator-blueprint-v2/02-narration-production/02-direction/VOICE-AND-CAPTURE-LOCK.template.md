# Narrator Identity and Acquisition Configuration Freeze

Template version: proposed Step 2 v0.2.

This is the N3 configuration freeze. It makes calibration reproducible; it does not approve a
performance and does not authorize an external provider call.

## Identity and authorization

- Episode:
- Configuration revision:
- Locked script SHA-256:
- Ordered `W`-token count/SHA-256:
- Approved narrator-profile path:
- Approved narrator-profile revision and SHA-256:
- Primary narration path: human / synthetic
- Narrator or authorized voice identity:
- Identity owner:
- Consent/rights basis and record path:
- Third-party imitation or cloning: no / yes, block pending explicit approval
- Voice custodian:

If the episode uses the approved OE narrator profile, copy its frozen values into this episode lock and verify them. Do not read mutable Studio configuration during generation without recording the exact reviewed source identity.

## Human capture profile

Complete when the narration path is human.

- Room/location:
- Acoustic treatment:
- Microphone and pattern:
- Microphone placement and approximate distance:
- Interface/preamp:
- Recording software/version:
- Sample rate: 48 kHz unless exception approved
- Bit depth: 24-bit unless exception approved
- Channel: mono
- Input-level target:
- Monitoring method:
- Room-tone file/path/hash:
- Session naming rule:

## Synthetic capture profile

Complete when the narration path is synthetic.

- Provider:
- Model/version:
- Authorized voice ID or internal alias:
- Settings and seed, when exposed:
- Context/chunking method:
- Pronunciation-alias method:
- Requested native acquisition: PCM
- Permitted fallback: `mp3_44100_192` only
- Permitted fallback reason: `pcm_capability_unavailable` only
- Actual audio origin vocabulary: `native_pcm` / `lossy_mp3`
- Delivery working/master format: PCM WAV / 48 kHz / 24-bit / mono
- Provider job-ID capture method:
- Terms or rights record path:
- Local raw-output preservation rule:

Do not place credentials or secret keys in this file.

## Continuity contract

- Approved narrator reference sample path/hash:
- Tone and pace reference:
- Pronunciation dictionary revision/hash:
- Maximum session gap or drift rule:
- Recalibration triggers:
- Prohibited substitutions or fallback voices:
- Material configuration changes that return to N3:
- Full-run continuity-listen requirement:

## Source-format and raw-evidence contract

- Actual returned codec will be inspected rather than inferred: yes / no
- Native output will be preserved byte-for-byte before processing: yes / no
- Fallback MP3 will receive an audible codec-artifact review: yes / no
- Fallback will be decoded/resampled exactly once to the PCM working path: yes / no
- Lossy intermediates after native acquisition are prohibited: acknowledged / not acknowledged
- A PCM WAV derived from MP3 remains labeled lossy-origin: acknowledged / not acknowledged

## External-action boundary

- Calibration authorization record required separately: yes / no
- Full-capture authorization record required separately: yes / no
- Legacy `studio/scripts/originate/generate_vo.py` invocation/import prohibited: acknowledged / not acknowledged

## Gate N3 configuration decision

- Configuration frozen: yes / no
- Rights basis verified for calibration: yes / no
- This document grants provider-call authority: no
- N3 gate result: pending / passed / failed / invalidated
- Workflow outcome: in_progress / blocked
- Owner:
- Voice custodian:
- Approval date:
- Exceptions:
