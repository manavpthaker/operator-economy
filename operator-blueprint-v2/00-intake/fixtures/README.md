# Step 0 test fixtures

Status: frozen Step 0.2 acceptance evidence; locked 2026-08-21.

Fixtures test the decision system without entering the active candidate lifecycle. They are never production research, queue entries, owner overrides, episodes, or public claims.

A full Step 0.2 eligibility fixture keeps its seven required artifacts together so reviewers can inspect the complete decision package. Early-exit and multi-candidate fixtures may stop sooner when they are specifically testing disposition behavior. Fixtures may also include clearly labeled shadow reviews or test notes. Fixture evidence may deliberately be missing, stale, weak, parallel, modeled, or hypothetical to test both valid transfer and fail-closed behavior.

`step0.2-proof-suite/` is a multi-candidate discrimination test. It uses a full positive package plus bounded borderline and negative controls to verify pass, continue-research, and archive behavior without entering the production lifecycle.

`legacy-episode-calibration-2026-08-21/` retrospectively screens published EP001-EP005 premises, then gives the borderline EP003 workflow-automation premise a fresh full review. It tests whether prior publication receives no automatic credit, weak historical economics are discarded, a stronger operating offer can be recovered from valid evidence, and two review passes remain on the same side of the promotion threshold.

`ACCEPTANCE-SET.md` records the locked expected behaviors and decision-artifact hashes. Preserve dated fixture inputs and results. When evidence needs a current refresh, add a new dated fixture instead of rewriting the historical control.
