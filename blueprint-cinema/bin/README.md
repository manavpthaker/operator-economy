# Operator CLI boundary

`oe-cinema` is the operator-facing command. From the repository root, run `blueprint-cinema/bin/oe-cinema --help`; it prefers the local `.venv` and otherwise loads the in-tree package through `PYTHONPATH`.

The command must resolve canonical `EP###-slug` identities, validate rather than silently repair, fail closed at gates, print exact paths and blockers, and keep every implementation dependency inside the Blueprint Cinema runtime.

The executable currently implements the preserved v1 initialization, status, input lock, engine/world/plan validation and approval, Remotion-era greybox compilation, representative-frame smoke rendering, agent packet validation, review generation, and test suite. It never approves `greybox_approved` from a smoke render.

It does not yet scaffold or enforce the documentation-canonical direction package, HyperFrames project, asset-select workflow, Resolve handoff, target state sequence, finishing reports, or delivery gates. Do not represent those as implemented CLI capabilities until a separate runtime migration adds and validates them.
