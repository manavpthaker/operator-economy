# BC-REHEARSAL-001 — edit and Resolve handoff

## Control

- Handoff version: `1`
- Experiment: `BC-REHEARSAL-001-missed-call-recovery`
- Picture stage: `directed animatic`
- Directed-animatic reference: `hyperframes/renders/BC-REHEARSAL-001-directed-animatic-final.mp4`
- HyperFrames CLI: `0.8.4`
- Status: `resolve-ready reference package; not imported or conformed`
- Resolve launched: `no`
- OTIO/FCPXML claim: `none`
- Public delivery: `blocked`

## Timeline standard

- Resolution: `1920x1080`
- Frame rate / time base: `30/1`, `1/30`
- Start timecode: `01:00:00:00`
- Rendered extent: frames `0–1842`; exclusive end `1843`
- Audio sample rate: `48 kHz`
- Current reference color: tagged Rec.709 SDR, video range
- Proposed future mixed-source timeline: DaVinci Wide Gamut / Intermediate with Rec.709 Gamma 2.4 SDR output
- Current alpha: none; reference is opaque H.264

The canonical narration and shot boundaries retain exact source seconds. `timeline-events.json` separately starts each non-frame-aligned cut on the first rendered frame at or after the authored source second. This ceiling conversion was assembled and checked manually; it is not a shared Blueprint Cinema exporter.

## Package inventory

| Item | Path | Classification | Notes |
| --- | --- | --- | --- |
| Animatic reference | `hyperframes/renders/BC-REHEARSAL-001-directed-animatic-final.mp4` | implemented and validated | 61.433333s, H.264 + AAC, hash-pinned |
| Locked VO | `inputs/vo.wav` | implemented and validated | 61.411354s, 48 kHz mono PCM |
| Word timings | `inputs/words.json` | implemented and validated | 158 words, source-time authority |
| Media probe | `handoff/media-probe.json` | implemented and validated | resolution, fps, codecs, audio, duration, black-frame test |
| HyperFrames outputs | `handoff/hyperframes-output-manifest.json` | implemented and validated | render and contact-sheet hashes |
| Timeline events | `handoff/timeline-events.json` | manually assembled and structurally checked | seven adjacent events, exact source seconds plus frame conform |
| Markers | `handoff/markers.csv` | manually assembled and structurally checked | seven shot markers |
| Placeholder assets | `handoff/placeholder-asset-manifest.json` | manually assembled and structurally checked | exact ticket links and public-delivery blocks |
| Track map | `handoff/track-map.json` | documentation-only | Resolve behavior not tested |
| Sound plan | `handoff/sound-plan.json` | documentation-only | VO exists; ambience/SFX ticketed only |
| Color proposal | `handoff/color-management.json` | documentation-only | Resolve behavior not tested |
| Alpha/plate behavior | `handoff/ALPHA-PLATE-BEHAVIOR.md` | documentation-only | no separate plates rendered |
| Round-trip rules | `handoff/ROUND-TRIP-RULES.md` | documentation-only | governance only |
| Captions | `handoff/CAPTIONS.md` | blocked | timing source exists; no sidecar/import path |
| OTIO / FCPXML | none | blocked | no supported validated exporter found; no fabricated interchange |
| Resolve project/conform | none | blocked | prohibited in this rehearsal |

## Track map

- `V1 picture_primary`: complete directed animatic reference; future reality master after conform.
- `V2 picture_reality`: approved reality/operator pickups only.
- `V3 graphics_opaque`: future opaque HyperFrames system plates.
- `V4 graphics_alpha`: future declared-alpha plates.
- `V5 evidence`: approved evidence only; the rehearsal fixture is prohibited from public use.
- `V6 titles_identity`: unused in this bounded mid-episode sequence.
- `V7 captions`: future validated caption artifact.
- `A1 voiceover`: locked `inputs/vo.wav`.
- `A2 music`: none.
- `A3 ambience`: future `AST-AMBIENCE-005`.
- `A4 sound effects`: future `AST-SFX-006`.

## Timeline events and markers

The complete event list is `handoff/timeline-events.json`; the import-neutral marker list is `handoff/markers.csv`. Events cover:

1. `00:00.000–00:13.640` — after-hours signal.
2. `00:13.640–00:26.370` — voicemail leak.
3. `00:26.370–00:34.200` — route construction and fixture attachment.
4. `00:34.200–00:39.880` — human judgment gate.
5. `00:39.880–00:47.680` — stop or book.
6. `00:47.680–00:56.050` — blueprint principle.
7. `00:56.050–00:61.411354` — one-week measurement.

## Conform checklist status

- [x] Timeline standard proposed.
- [x] Locked VO and animatic are hash-addressed.
- [x] Shot order and exact source seconds are recorded.
- [x] Whole-frame conform boundaries are listed.
- [x] Missing assets and unsupported capabilities are explicit.
- [ ] Resolve project settings established.
- [ ] Interchange imported.
- [ ] Media relinked by manifest ID.
- [ ] Frame offsets checked in Resolve.
- [ ] Alpha/blend behavior verified.
- [ ] Conform report and project archive exported.

Unchecked items are blocked, not implied by package existence.

## Sound, color, disclosure, and round trip

The animatic is VO-only. No music, ambience, SFX, stock, or generated media was added. Future sound must use the exact ticketed editorial jobs, protect narration, and avoid whooshes, risers, success chimes, or automation gloss.

The fixture CSV must always read `SYNTHETIC TEST FIXTURE — NOT EVIDENCE`. The WO-R01 card must always carry `SYNTHETIC WORK ORDER — NOT EVIDENCE`. Either object would block public delivery until replaced by an approved, provenance-complete asset.

Editorial, evidence, timing, or state changes in Resolve must return to the appropriate Blueprint Cinema artifact. Resolve finishing cannot approve a gate or silently change the operating model.

## Readiness decision

`PARTIAL.` An editor can inspect the reference, VO, events, markers, tracks, placeholders, sound/color intent, and missing capabilities without guessing. A validated interchange, actual Resolve conform, captions, separate plates, and approved assets do not exist and are not claimed.
