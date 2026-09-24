# Runtime source boundary

The preserved v1 deterministic Python orchestration lives here under the `blueprint_cinema` package.

Responsibilities include path and identity resolution, hashes, input locking, schema and semantic validation, production state, agent-packet validation, render-data compilation, and human-readable review generation.

Runtime code does not contain episode-specific visual compositions or infer visual decisions from narration strings. EP006's explicit authored action-to-word mapping remains root-owned inside its episode workspace.

This package does not yet implement the canonical HyperFrames-to-Resolve production contract, target state sequence, direction, asset-selection, edit-manifest, finishing, or delivery layers. See `../TOOLCHAIN.md` and `../WORKFLOW.md` for the documentation-canonical target.
