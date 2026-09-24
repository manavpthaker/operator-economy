# GEO agency Step 0 control fixture

This directory contains two synthetic dry runs of the same broad GEO-agency idea. Both are isolated from `01-candidates/`, `04-queue/`, and every episode stage. Neither is a production candidate, recommendation, episode, or owner approval.

## Step 0.1 baseline

The files in this directory root test the original exact-model-oriented rules using only frozen V1 intake material.

- Reviewer A: 20/100; Canvas fail; `continue research`.
- Reviewer B: 18/100; Canvas fail; `continue research`.
- Correct result for those inputs: the sparse lead did not contain enough usable evidence to advance.

These artifacts remain unchanged as the comparison baseline.

## Step 0.2 retest

The `step0.2-retest/` package applies the broader research model: direct facts about the problem plus bounded adjacent and component evidence for the new solution.

- Reviewer A: 82/100; all hard gates pass; `eligible`.
- Reviewer B: 76/100; all hard gates pass; `eligible`.
- Evidence class: `adjacent synthesis`.
- Production result: not promoted because fixtures cannot enter the active lifecycle.

The new review does not assume an existing GEO-agency precedent, exact search demand, buyer acceptance, service revenue, price, hours, outcome, or margin. It advances because the research now supplies valid parallels, a complete operating model, explicit assumptions, a causal narrative, independent audience signals, and a bounded validation plan.

Start with `step0.2-retest/README.md` for the comparison and artifact sequence.

## Control boundary

If this opportunity is later authorized as a real candidate, recreate it under the normal Step 0 paths with current research and an owner. Do not move, rename, promote, or queue either fixture package.
