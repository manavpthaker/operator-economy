# Missing implementation boundary

The shared Blueprint Cinema v1 runtime does not implement the documentation-canonical v2 direction, HyperFrames build-packet, rendered-review, or Resolve-handoff gates. This experiment proves those contracts manually and with an isolated validator; it does not add them to shared production code.

## Implemented and validated

- Locked local narration, VO, word timings, and hashes.
- Experiment-local engine, world, full-timeline plan, direction, agent packets, and asset tickets.
- HyperFrames root and seven bounded shot compositions.
- HyperFrames lint, check, Studio preview, required snapshots, full MP4 render, contact sheets, and media probe.
- Hash-addressed output manifest and synthetic placeholder manifest.

## Manually assembled and structurally checked

- Resolve timeline event list.
- Whole-frame boundary conform and marker CSV.
- Handoff inventory and capability classification.
- Agent packet serial merge and final cross-boundary review.

## Documentation-only

- Resolve track map.
- Sound and color-management proposals.
- Round-trip governance.
- Expected alpha/plate treatment.

## Blocked

- OTIO or FCPXML: no current shared exporter/validator was found, so no interchange file is fabricated.
- Resolve import, relink, conform, marker verification, and project archive: Resolve launch/modification is prohibited in this test.
- Captions: the word table exists, but no approved caption artifact or importer was implemented in this bounded rehearsal.
- Opaque/alpha production plates: only a complete review MP4 was rendered.
- Reality, operator, dispatch, outcome, ambience, and SFX selects: exact tickets exist; no sourcing or generation was authorized.
- Public delivery: the fixture CSV and WO-R01 are synthetic rehearsal material and explicitly block public use.

## Known technical issues

1. Source word times and shot boundaries are subframe values. The handoff preserves those exact seconds and separately lists nearest 30-fps boundaries; this conversion is manual.
2. HyperFrames `0.8.4` rendered a container tag of `hyperframes_version=0.0.0-dev`. CLI invocation and the explicit pin remain authority.
3. The shared state machine cannot represent or enforce this rehearsal's v2 direction and handoff gates.
