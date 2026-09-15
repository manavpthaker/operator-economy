# Preserved v1 validation and test boundary

The suite tests identity, schemas, input hashes, media timing, state transitions, downstream invalidation, clean-room exclusions, persistent-world references, consent and human-review paths, complete timeline coverage, outbound gate ordering, configured failures, agent isolation, renderer-data determinism, distinct overview/focus Remotion frames, authored camera routing, and distinct deck-prototype slides that reuse stable object IDs without rendering the complete network map.

Tests must use temporary fixtures and must not mutate the real EP006 state to exercise failure behavior.

Passing this suite proves the v1 contracts only. It does not prove the documentation-canonical direction artifacts, HyperFrames runtime, asset selection, Resolve conform, picture lock, color, sound, captions, or delivery workflow. The future migration must add explicit tests rather than reinterpreting these results.

Run `blueprint-cinema/bin/oe-cinema test` or `blueprint-cinema/.venv/bin/python -m pytest blueprint-cinema/tests -q` from the repository root.
