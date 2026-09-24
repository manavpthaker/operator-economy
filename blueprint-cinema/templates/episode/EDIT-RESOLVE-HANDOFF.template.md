# EP###: <episode title> — edit and Resolve handoff

## Control

- Handoff version:
- Episode:
- Picture stage:
- Input hashes:
- Directed-animatic reference:
- Asset-manifest hash:
- Edit-plan hash:
- Sound-plan hash:
- HyperFrames version:
- Resolve baseline:
- Owner:
- Status:

## Timeline standard

- Resolution:
- Frame rate / time base:
- Start timecode:
- Audio sample rate:
- Color-management strategy:
- Timeline color space / transfer:
- Output color space / transfer:
- SDR / HDR:
- Alpha interpretation:

## Package inventory

| Item | Path | Hash | Format | Duration / range | Status | Notes |
|---|---|---|---|---|---|---|
| Animatic reference | `<path>` | `<hash>` | `MP4` | `<duration>` | `<status>` | `<notes>` |
| OTIO | `<path>` | `<hash>` | `OTIO` | `<range>` | `<status>` | `<notes>` |
| FCPXML | `<path>` | `<hash>` | `FCPXML` | `<range>` | `<status>` | `<notes>` |
| Marker list | `<path>` | `<hash>` | `CSV` | `<range>` | `<status>` | `<notes>` |
| Opaque plate | `<path>` | `<hash>` | `<format>` | `<range>` | `<status>` | `<notes>` |
| Alpha plate | `<path>` | `<hash>` | `<format>` | `<range>` | `<status>` | `<notes>` |
| VO | `<path>` | `<hash>` | `<format>` | `<duration>` | `<status>` | `<notes>` |

## Track map

| Resolve track | Canonical role | Expected contents | Locked? | Notes |
|---|---|---|---|---|
| `V1` | `picture_primary` | `<contents>` | `<yes/no>` | `<notes>` |
| `V2` | `picture_broll` | `<contents>` | `<yes/no>` | `<notes>` |
| `V3` | `graphics_opaque` | `<contents>` | `<yes/no>` | `<notes>` |
| `V4` | `graphics_alpha` | `<contents>` | `<yes/no>` | `<notes>` |
| `V5` | `evidence` | `<contents>` | `<yes/no>` | `<notes>` |
| `V6` | `titles_identity` | `<contents>` | `<yes/no>` | `<notes>` |
| `V7` | `captions` | `<contents>` | `<yes/no>` | `<notes>` |
| `A1` | `vo` | `<contents>` | `<yes/no>` | `<notes>` |
| `A2` | `music` | `<contents>` | `<yes/no>` | `<notes>` |
| `A3` | `ambience` | `<contents>` | `<yes/no>` | `<notes>` |
| `A4` | `sfx` | `<contents>` | `<yes/no>` | `<notes>` |

## Timeline events

Copy for every event or generate from the canonical edit manifest.

### `<event-id>`

- Sequence / shot:
- Track role:
- Record in / out:
- Source asset / plate:
- Source in / out:
- Playback rate:
- Crop / scale / position:
- Opacity / blend / alpha:
- Transition:
- Narration word range:
- Graphics / evidence / title / caption overlays:
- Music / ambience / SFX cues:
- Continuity anchor:
- Approval dependency:

## Resolve conform checklist

- [ ] Project settings established before import.
- [ ] Locked VO and animatic reference imported.
- [ ] Interchange imported without unresolved errors.
- [ ] Approved assets relinked by manifest ID.
- [ ] Shot order matches reference.
- [ ] Event timing and transitions match reference.
- [ ] Alpha and blend behavior verified.
- [ ] Text and evidence timing verified.
- [ ] No media drift or frame offset.
- [ ] Missing and unsupported items reported.
- [ ] Conform report exported.

## Sound plan

- Sonic thesis:
- Music strategy:
- Reality ambience:
- System sound palette:
- Proof sound palette:
- Silence / breather plan:
- Narration treatment:
- Transition bridges:
- Prohibited clichés:

| Cue ID | Sequence / shot | Time / word cue | Asset | Job | Onset / tail | Perspective | Conflict check | Status |
|---|---|---|---|---|---|---|---|---|
| `<id>` | `<ids>` | `<cue>` | `<asset>` | `<job>` | `<range>` | `<perspective>` | `<result>` | `<status>` |

## Color and finishing plan

- Source color audit:
- Normalization:
- Shot matching:
- Reality-world target:
- System-world protection:
- Proof-world fidelity:
- Outcome target:
- AI / archival / stock integration:
- Fusion work:
- LUT / DCTL use:
- Review display and limits:

## Round-trip changes

| Change ID | Resolve change | Classification | Blueprint Cinema artifact affected | Returned? | Approval |
|---|---|---|---|---|---|
| `<id>` | `<change>` | `finish | trim | editorial | upstream` | `<artifact>` | `<yes/no>` | `<status>` |

## Delivery

- Picture-lock reference:
- Mezzanine master:
- Platform master:
- Captions:
- Mix and stems:
- Resolve project export / archive:
- QC report:
- Media-probe report:
- Rights / disclosure report:
- Checksums:

