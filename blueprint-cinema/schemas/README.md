# Schema contracts

Strict JSON Schemas are implemented here for:

- episode project identity;
- input locks;
- production state and approvals;
- episode engines;
- persistent worlds;
- visual plans;
- shot-level scene directions;
- asset tickets and provenance;
- agent work orders;
- agent deliverables;
- deterministic renderer data where appropriate.

Schemas must reject unknown fields, require substantive authored values, support editor `$schema` fields, and be paired with semantic validation where JSON shape alone is insufficient.

The schemas reject unknown fields and are paired with Python semantic validation for identity agreement, input hashes and timing, state order and invalidation, world topology, timeline continuity, picture/audio coherence, mode-bound delivery face functions, narrator-led mute tests, required adjacent direction facts, setup-reference integrity, typed continuity-anchor structure, reference resolution for `world_object`, `asset_ticket`, and `shot_layer` anchors, shot geometry, exact word cues, text emphasis, evidence choreography, outbound gate order, clean-room exclusions, renderer pins, and worker isolation.

Direction-facts validation proves required presence, allowed structure, and reference integrity. It does not prove that an authored description is a truthful or effective directorial choice; that remains a review judgment.
