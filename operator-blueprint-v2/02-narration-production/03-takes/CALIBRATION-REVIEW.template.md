# N4A Calibration Review

Template version: proposed Step 2 v0.3.

The two-passage provider bakeoff is N3 method-selection evidence, not this N4A review. Use this
template only after one method is selected and separately authorized for N4A.

## Authority

- Episode or fixture ID:
- Step 1 script path/SHA-256:
- Ordered `W`-token count/SHA-256:
- Performance-direction path/SHA-256:
- N3 configuration path/SHA-256:
- Calibration authorization ID/status:
- Provider batch or human session ID:
- Review date:

## Frozen configuration check

- Narrator/voice ID matches N3: yes / no
- Provider/model/settings or human chain match N3: yes / no
- Pronunciation and context methods match N3: yes / no
- Native PCM requested first: yes / no / human capture
- If PCM unavailable, actual fallback is exactly `mp3_44100_192`: yes / no / not applicable
- Fallback reason is `pcm_capability_unavailable`: yes / no / not applicable
- Every raw source is immutable, registered, and hashed: yes / no
- No V1 `generate_vo.py` invocation or import: yes / no

## Passage reviews

| Passage | `W` range | Raw take/job and SHA-256 | Audio origin | Interim ASR finding | Lexical disposition | Technical result | Performance result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cold open and promise | | | | diagnostic only | | | |
| Dense evidence | | | | diagnostic only | | | |
| Economics and uncertainty | | | | diagnostic only | | | |
| Names, numbers, acronyms, pronunciation | | | | diagnostic only | | | |

## Source-format audible review

Complete for every `lossy_mp3` source.

| Check | Result | Timecodes/findings |
| --- | --- | --- |
| Swirling, watery tails, or pre-echo | pass / fail | |
| Harsh or smeared sibilance | pass / fail | |
| Damaged transients or consonants | pass / fail | |
| Intelligibility loss | pass / fail | |
| Pickup/chunk source consistency | pass / fail | |

## Calibration technical decision

- Exact `W` passages preserved: yes / no
- Technical quality acceptable: yes / no
- Continuity across the four modes acceptable: yes / no
- Diagnostic ASR findings fully dispositioned: yes / no
- Technical recommendation: pass / revise / return to N3 / blocked
- Technical reviewer/signature/date:

## Owner calibration creative decision

- Sounds like the intended OE narrator: yes / no
- Argument modes are usefully distinct: yes / no
- Dense proof and numbers remain understandable: yes / no
- Performance feels human, credible, and sustainable for the full episode: yes / no
- Owner decision: approve / revise / return_to_N3 / blocked
- Owner statement/signature/date:

N4A gate result: pending / passed / failed / invalidated

Workflow outcome: in_progress / blocked

N4A passes only when the technical recommendation passes and the owner approves the calibration.
This decision does not authorize full capture; a separate full-capture authorization is required.

A result of technical `pass` and owner `revise` is valid evidence but leaves N4A unpassed. Route a
performance-only revision through N2/N3 without reopening Step 1.
