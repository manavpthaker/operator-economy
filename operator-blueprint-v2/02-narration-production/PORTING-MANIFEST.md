# Step 2 Reference Porting Manifest

Status: frozen v0.2 local-reference hashes with proposed v0.3 provider-selection additions.

No V1 source was moved or edited for this documentation pass. The sources below remain in place and are referenced rather than copied. SHA-256 values freeze the versions reviewed while designing Step 2.

| Source | SHA-256 | V2 treatment |
| --- | --- | --- |
| `docs/vo-first-production-flow.md` | `e8dd7d045c9416ec6dc99e113947b4172b6922feb8e217e80c147385c1221af8` | Reference-only production-order lesson. |
| `studio/ORIGINATE.md` | `dffddf82f1073ccd57e495154d4531e5320ef83e23d217e77972ddb6ba2c6b81` | Reference-only narration workflow history. |
| `studio/config/blueprint.json` | `1a1d691561a2aac703fa3532aed48cae3c36b4f68abcda227292762c98e326f8` | Reference-only configuration evidence. |
| `studio/scripts/originate/generate_vo.py` | `085c2941e18d987c406ce95c734f388cb5baa0b97c9be216bbdeff7d561a2186` | Reference-only evidence; V2 invocation/import is explicitly prohibited. |
| `studio/scripts/originate/build_v3_direction.py` | `f8a6abd5236158f750847ee6bd7a9a867a5f9ccdd7b9bc30e91d7f408c24e1a7` | Reference-only lexical-preservation evidence. |
| `studio/scripts/originate/ingest_recorded_vo.py` | `20cdcfadddac1f8abab0a0a908480ed65a1b8baa8e2677d6b384796db33bb992` | Reference-only human-recording parity evidence. |
| `studio/scripts/originate/master_vo_local.py` | `4fc3f62468e6703ecc63869639fec6dd9447095366a4a998db9e79c1608a855b` | Reference-only local mastering evidence. |
| `../content-os/voice.md` | `ec65d503a9973ec77919ca8edf37d37f18e6762c696d931690a86b179017574a` | Upstream Step 1 v1.5 editorial-language authority; not Step 2 narrator authority. |
| `../content-os/rubric.md` | `41f4468128061205285313e9cff6815d682e0e4bbe278a82697b3c700ba697fa` | Routes V2 video-script authority to approved Step 1; not Step 2 scoring authority. |
| `studio/config/speech-profile.md` | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` | Upstream Step 1 observed spoken-language authority; Step 2 may not use it to rewrite locked words. |
| `operator-blueprint-v2/01-editorial/STEP1-v1.5-APPROVAL.md` | `4eea77c5f3f8f5baf5862738f25e61cbef9afb48a0b76203acc1be673beba725` | Current Step 1 system and AI Visibility fixture boundary reviewed from commit `27c90fd`. |

## What was ported conceptually

- narration precedes visual translation;
- performance notation must not change approved words;
- raw audio and generation provenance must be preserved;
- human and synthetic paths need equivalent review rigor;
- word timings must describe the final narration edit; and
- downstream work needs a stable narration hash and duration.

## V0.3 additions are new doctrine, not a V1 port

The following controls were authored for the v0.3 proposal and do not inherit authority from V1:

- provider-agnostic performance envelope plus separately hashed provider adapters;
- the audit finding that the v0.2 Eleven transport space-joined canonical words without carrying
  the approved acting direction, so its creative revise is not a provider-comparison verdict;
- exact-one-original-sample provenance and retrieval gate;
- four separately authorized initial ElevenLabs/Hume external actions;
- UI-mediated Hume upload/clone receipt and the prohibition on treating Create Voice from a
  generation ID as a human-audio upload API;
- equal two-passage/two-generation candidates, sealed blind codes, six-dimension 100-point scoring,
  and hard gates;
- provider score from the mean of its highest hard-gate-passing P1 and P2 generation selects;
- short advancement at 80 points with the runner-up added only within 5.0 points;
- a separately authorized 3.5-to-4.5-minute continuity and several-hours-later pickup test; and
- pass/fail long-form/pickup confirmation with the asymmetric final rule applied only to frozen
  short scores: retain ElevenLabs within 5.0 points and adopt Hume only when it scores at least 80,
  leads by more than 5.0 points, and passes confirmation.

Live provider documentation is listed in `REFERENCE-MAP.md`. It is intentionally not assigned a
local SHA-256 in this manifest. Recheck it and the active account terms before each authorization.

## What was deliberately left behind

- provider lock-in and existing account-specific identifiers;
- obsolete state names and old folder contracts;
- MP3-first acquisition or master assumptions;
- fixed voice-generation settings treated as universal creative direction;
- final-program loudness targets applied prematurely to isolated narration;
- music and scene audio inside the narration-production stage; and
- any claim that successful generation, ASR, export, or technical pass equals creative approval;
- any V2 execution or import of legacy `generate_vo.py`; and
- any claim that Workflow Operations is a current positive Step 2 control.

## Retained narrator-profile comparison baseline

The current Studio voice ID and generation settings remain in
`02-direction/OE-NARRATOR-PROFILE.md` as the technically proven but creatively revised ElevenLabs
comparison baseline, not silently inherited authority. The v0.2 calibration receipts remain
frozen. V0.3 may not replay them, treat them as N4A approval, or infer sample retrieval, Hume clone,
short-bakeoff, long-form, full-capture, or Step 3 authority.

Recalculate the source hash and review the difference before relying on a newer V1 source revision.
