# Voice and Capture Lock

Template version: proposed Step 2 v0.1.

## Identity and authorization

- Episode:
- Lock revision:
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
- Output format/sample rate/bit depth/channel:
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

## Calibration decision

| Passage | Source file/job | Performance | Lexical | Technical | Decision |
| --- | --- | --- | --- | --- | --- |
| Cold open | | | | | |
| Dense evidence | | | | | |
| Economics/uncertainty | | | | | |
| Pronunciation/numbers | | | | | |

## Gate N3 approval

- Configuration frozen: yes / no
- Authorization complete: yes / no
- Calibration approved: yes / no
- Owner:
- Voice custodian:
- Approval date:
- Exceptions:
