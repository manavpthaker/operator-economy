# QA — EP007 net-new opening, revision B

## Current status

- Test ID: `EP007-NET-NEW-UNFINISHED-ANSWER-002`
- Revision: `B`
- Intended duration: `59.86s`
- Current human-media form: generated still animatic plates
- Generated live-action video present: **no**
- Render path: `renders/EP007-NET-NEW-UNFINISHED-ANSWER-002-v001.mp4`
- Render SHA-256: `1b3046adf68abd43bd3648738990bb78c23fbef052dd3eb4094abfcd584fdbb0`
- HyperFrames check result: **passed** with zero errors and one nonfunctional file-length warning
- Encoded-media probe: **passed**; both streams also passed strict decode
- Status: draft opening test; not a gate approval and not publication-ready

This file records what revision B must prove. It does not carry forward the prior revision’s render hash or QA result.

## Visual acceptance checks

- [x] The workshop is bright, natural, functional, and held in open midtones.
- [x] Owner appears capable, comfortable, and at home in the business.
- [x] Buyer appears procedural, collaborative, and nonjudgmental.
- [x] Owner and buyer occupy adjacent sides of a table corner rather than a confrontational face-off.
- [x] Mineral binder, ivory sheet, graphite pencil, steel keys, pale maple table, wardrobe, lighting, and screen direction remain continuous across R1–R4.
- [x] Current human plates are labeled accurately as still animatic imagery, not live-action video or evidence.
- [ ] No generated dialogue, lip movement, reciprocal dialogue eyelines, random gaze, or “about to speak” posture appears.
- [x] No readable financials, operating records, page diagrams, captions, logos, watermarks, source IDs, or claim numbers appear.
- [x] The locked question card reads exactly: `WHAT HAPPENS HERE IF YOU ARE NOT AROUND FOR A MONTH?`
- [x] R3 crops faces out and makes the stopped pencil—not facial acting—the emotional event.
- [x] Four rough marks become four recognizable weeks or work units.
- [x] All four units route through the owner; one unit stalls under owner absence without implying total business collapse.
- [x] The localized stall expands into a legible full business model with enough breathing room.
- [x] One incomplete oxide practice path draws only during `00:44.50–00:46.70` and remains unresolved.
- [x] No oxide appears before the practice path.
- [x] `BUILD`, `OWN`, and `OPERATE` begin at `00:52.08`, `00:52.60`, and `00:53.16`.
- [x] The episode title cuts at exactly `00:56.04`.
- [x] No ambient drift, slow push, pan, tilt, rack focus, fake handheld movement, or slow motion is used to animate stills.

The unmarked human-performance item is intentionally still open. R1 is a still, so it contains no lip movement, but the owner's lips are slightly parted in the selected master. Only the later moving-plate test can establish whether the performance reads as narrated observation rather than unheard dialogue.

## Viewer-progression check

Review the encoded opening without reading these notes first. The intended progression is:

1. **Trust:** respected operator in a functioning business.
2. **Curiosity:** completed financial review gives way to a practical operating question.
3. **Quiet recognition:** the pencil stops and the model exposes repetitive owner routing.
4. **Constructive possibility:** one incomplete practice path appears.

Fail the revision if it instead reads as interrogation, crisis, shame, aimless pensiveness, buyer hostility, owner incompetence, or a promised fix.

## Mute test

- [ ] R1 reads as ordinary review, not missing dialogue.
- [x] R2 reads as an object-led task shift, not a spoken question.
- [x] R3 reads as action followed by cessation; no missing words are expected.
- [x] R4 reads as changed document hierarchy without readable content.
- [x] Graphics remain intelligible without audio.
- [ ] Narration remains intelligible without the graphics.

The first and final mute checks remain owner-review items. The encoded narration is the locked Step 2 derivative and decoded cleanly; no new independent intelligibility listen was performed here.

## Encoded result

The encoded review contact sheet is `qa/encoded-001/contact-sheet.png`.

| Property | Result |
| --- | --- |
| Container | MP4 |
| Video | H.264 High, 1920×1080, progressive, yuv420p, BT.709 |
| Frame rate | 30 fps |
| Video duration | 59.866667 seconds |
| Video frames | 1,796 |
| Audio | AAC-LC, 48 kHz, stereo |
| Audio duration | 59.861 seconds |
| File size | 4,977,719 bytes |
| Strict decode | exit 0; no decoder output |
| HyperFrames lint | 0 errors, 1 `composition_file_too_large` warning |
| HyperFrames runtime | 0 errors, 0 warnings |
| HyperFrames layout | 0 issues across 837 samples |
| HyperFrames motion | 0 errors, 0 warnings |
| HyperFrames contrast | 4/4 checks pass WCAG AA |

The lint warning is caused by duplicating the exact settled G3 drawing into G4 so the semantic objects survive the cut without recomposition. It does not affect the encoded result, but a production refactor should extract the shared static model rather than retain the duplication.

Encoded boundary review confirmed:

- the four physical marks carry into four slanted, broken, retraced pencil gestures;
- G3 and G4 preserve the same units, routes, handoff, stopped token, displaced owner, and business envelope across `00:44.50`;
- oxide begins after the boundary, completes its incomplete path by `00:46.70`, and holds;
- the mineral identity field begins immediately after `00:48.52`;
- BUILD, OWN, and OPERATE accumulate at the three locked narration-word starts;
- the episode title replaces the identity field immediately after `00:56.04`.

## Mechanical checks to run after render

1. Run the project’s full HyperFrames check and record errors, warnings, layout findings, motion findings, and contrast findings without summarizing them into a pass prematurely.
2. Probe the encoded video and audio streams; record codec, dimensions, frame rate, frame count, duration, sample rate, and channel layout.
3. Strict-decode both streams.
4. Inspect authored boundaries at `17.96`, `21.28`, `27.92`, `35.08`, `40.08`, `44.50`, `46.70`, `48.52`, `52.08`, `52.60`, `53.16`, `56.04`, and `59.86`.
5. Review the actual encoded frame sequence for continuity and the full opening for viewer progression.
6. Record the final render path and full SHA-256 only after the file exists.

## Generation provenance

Until a generation tool returns authoritative metadata:

| Field | Value |
| --- | --- |
| Provider | `UNKNOWN` |
| Model | `UNKNOWN` |
| Version | `UNKNOWN` |
| Request ID | `UNKNOWN` |
| Seed | `UNKNOWN` |

Prompts alone do not prove execution. File existence alone does not prove which model produced it. Do not backfill provenance from memory or visual appearance.

## Known boundary

Revision B’s current still plates can test composition, continuity, causality, emotional temperature, graphic language, and timing. They cannot test natural human motion, action performance, lip stability, prop behavior through time, or video-generation continuity. Those remain open until R1–R4 are replaced by verified one-action moving plates and the encoded result is reviewed.

Nothing in this QA record approves Step 3, a provider, a generation model, production footage, final sound, the full episode edit, or publication.
