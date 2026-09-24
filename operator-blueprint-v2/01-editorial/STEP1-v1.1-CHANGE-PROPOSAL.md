# Step 1 v1.1 Change Proposal: Editorial Voice Enforcement

Status: rejected by owner on 2026-08-22; never canonical

Opened: 2026-08-21

Requested by: Manav Thaker

Owner instruction: `yes go back to step 1 and make these fixes and then test again we need to add the voice profile to the test criteria and make sure that the script soujnds like that`

Previous approved version: `operator-blueprint-v2-step1-v1.0`

Proposed version: `operator-blueprint-v2-step1-v1.1`

Owner rejection: v1.1 removed report language but remained too safe, too hedged, too dependent on explicit hypothetical disclaimers, insufficiently opinionated, and unlike the intended Gawdat/Mulaney/Maher craft blend with a Last Week Tonight-style research-and-comedy engine. Superseding proposal: `STEP1-v1.2-CHANGE-PROPOSAL.md`.

## Problem

Step 1 v1.0 routed `content-os/voice.md`, but its lock and tests did not independently prove editorial-voice conformity. The Step 2 proposal then incorrectly treated that writing authority as a narration-performance authority.

The observed Manav spoken-language profile in `studio/config/speech-profile.md` was also absent from the Step 1 authority map. That creates a dangerous gap: a script can be clear, accurate, and technically speakable while still sounding like a polished report that Step 2 would have to rewrite to sound like Manav.

## Proposed correction

- Define editorial voice as a Step 1 word-level responsibility.
- Separate editorial voice from Step 2 narrator identity and audio performance.
- Route both Content OS house voice and the observed Manav speech profile into script authorship.
- Record both source hashes in the script package and editorial lock.
- Add a dedicated E5V editorial-voice conformity gate.
- Add an independent editorial-voice reviewer distinct from the performance reviewer.
- Add voice-profile failure and recovery to the Step 1 regression set.
- Re-run the two full Step 1 script fixtures without altering their historical v0.2 artifacts.
- Remove self-hash fields and downstream-review hash cycles exposed while adding the new conformity artifact: hashes are calculated only after each artifact is complete and recorded by dependent artifacts plus the editorial lock. The narration handoff is created only after that lock exists.

## Calibration source identities

| Source | SHA-256 | Proposed role |
| --- | --- | --- |
| `../content-os/voice.md` | `ff7886abc18c5c815bcc045e0e5dca625cdd0b61e649e518eada8e26f508a1b9` | Live house editorial-voice authority. |
| `studio/config/speech-profile.md` | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` | Live observed Manav spoken-language authority. |

## Expected regression behavior

1. The previously accepted GEO v0.2 script should fail E5V if its report register dominates despite evidence integrity.
2. The previously accepted workflow-reliability v0.2 script should fail E5V for the same reason if applicable.
3. Revised scripts must recover through actual word changes in Step 1, not Step 2 performance instructions.
4. Claims, qualifications, Canvas logic, narrative function, entry wedge, and aspirational scope must not drift during recovery.
5. A deliberately mannered script should fail the non-caricature dimension even when it contains recognizable Manav phrases.

## Closure

The proposal completed its planned regression and froze the identities below, but the owner rejected the editorial result. V1.1 never became canonical and cannot now be approved through this closed record. Any recovery belongs to the v1.2 proposal and must receive its own tests, hashes, and explicit owner decision.

## Rejected v1.1 authority identities

Frozen after regression completion on 2026-08-21:

| Authority file | SHA-256 |
| --- | --- |
| `README.md` | `d38d428f8930b8ab0309345947299dc5207b4241d5a68173c3366db854b9428f` |
| `EDITORIAL-STANDARD.md` | `b7096f09bbe07e089cadf3b87a861dfbd9345c9a89306342e7f4e13633afcf27` |
| `EDITORIAL-VOICE-STANDARD.md` | `bad4759ddb40069cfa3daba6d6efa8632600f65fa21386104e6327eeeb12a9c2` |
| `STAGE-GATES.md` | `63faa7a6660c1c97276e7d23bd2219d15961fd40306afc9a574a3dbb50da796b` |
| `TEAM-WORKFLOW.md` | `bc34f07d8b14707485e21ac65523d1e6f3a5f7ac93ca746e6c2362892d7fe792` |
| `01-handoff/STEP0-HANDOFF-CHECKLIST.md` | `590d2766d76d8175999c2d90422aa614c286a2e6b9e48695fe53e457852e6e39` |
| `02-contract/EDITORIAL-CONTRACT.template.md` | `517a3a3d3fe5bf5ad46bcaa84bf08a55dced05ce71e3719e17fad76f776bb6b2` |
| `03-canvas/OPERATOR-CANVAS.template.md` | `ba3e9ebc83dd998e951e669b08fc5c605a50993ef179be3dbd57d57d50b85242` |
| `04-narrative/NARRATIVE-SPINE.template.md` | `1174707023203eef2e4a8b8f790f6ff085f4302723f4e70d4a694a1ebc334c2d` |
| `04-narrative/EPISODE-OUTLINE.template.md` | `2bfa38f8b60939830853b4d528b859f86fd9b6c99d8003bc8ff90e7104c3e6c8` |
| `05-script/CLAIMS-MAP.template.md` | `f706a048ba2bacd9ccaddc14af55e68c682153ba58181592ed20e4776a4e37d4` |
| `05-script/EDITORIAL-VOICE-CONFORMITY.template.md` | `a94880710e584f74f724e8b1a0776564acc3a6e29872f5ecd2be8516fff059ab` |
| `05-script/PERFORMANCE-READTHROUGH.template.md` | `712aefc2c75a953169a8ac98a8b77e3e022f4ecdec6e367b9d721c466b7f367d` |
| `05-script/REVIEW-DISPOSITION.template.md` | `ef38dc6ab9cd5e7ec3d1272284a87fe77dfe9bff5b7511021a419c19946dd5e9` |
| `05-script/SCRIPT-STANDARD.md` | `ecf7666a5aed2c0f668852dcdf049b976a88f6979c15c00fc251bd94d4f4d75e` |
| `05-script/SCRIPT.template.md` | `e2137cfe9a070fc6532b2f828569c5ffd6d3817dc9c4aa0ec18228762b88b9ca` |
| `05-script/STEP0-AMENDMENT-REQUEST.template.md` | `fc875be85bf4eef6c975818c39eeb212401843c3dcbf7060af8960e1be5d6469` |
| `06-approval/EDITORIAL-LOCK.template.md` | `3bf977a346c341de9b86d1720d498c4318b2d886e43b228ae10dfcab6084d756` |
| `06-approval/NARRATION-HANDOFF.template.md` | `f1934a63d7143ffd4b5346341f37498a6f0fff5b524e8deeb61424a92577767f` |
| `REFERENCE-MAP.md` | `93171e0f6451d48d1aae43c317bf827536e6780840587921781aa9e325d933f5` |
| `PORTING-MANIFEST.md` | `e42b00a8e18b03300f6ca1755cccf912dfcb8e4b5d29fc9f449e474a41a0c27d` |

Fixtures and result reports are evidence, not authority files.
