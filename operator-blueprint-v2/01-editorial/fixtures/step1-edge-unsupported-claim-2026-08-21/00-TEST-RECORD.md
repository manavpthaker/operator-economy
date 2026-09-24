# Step 1 Gate E5 edge test: unsupported script claims

Status: in test; fixture only; no production authority

Test ID: `step1-edge-unsupported-claim-2026-08-21`

Candidate ID: `candidate-test-2026-08-21-workflow-reliability-service`

Episode number: unassigned

Owner authorization: User authorized the E5 edge test on 2026-08-21.

## Purpose

Test whether plausible editorial language can introduce unsupported market size, buyer-demand, price, or typical-performance claims after the Canvas and narrative are coherent. Gate E5 must reject the exact additions, preserve the rest of the script, and choose either removal or a bounded Step 0 amendment request.

## Governing proposed v0.4 rules

These are the exact rules used before this test produced any amendments.

- `EDITORIAL-STANDARD.md` / `26cd90174248edc1f33b31b64c14736a1b0b9c743b63e1c471fe2af4df01fb8d`
- `STAGE-GATES.md` / `93f96501bb640fe267d211b18bb033b8027b41d4e0d10f1fd80479fda9c344cc`
- `TEAM-WORKFLOW.md` / `da8b647f2aeba397fa162f33d6be9467fbdfb6e79437ad94afdd187d3b9aeb15`
- `CLAIMS-MAP.template.md` / `d2f7ad8a226c76ce6715a89ed795373cf8739147f47e9215a53a88d503737ea0`
- `SCRIPT-STANDARD.md` / `a92c7d99f3cec19a46745137501e20ceb8158a635f23d25fe0bda8d2a9994731`
- `EDITORIAL-LOCK.template.md` / `88a66958862465cc825b643bb549e0ee0529af03111fd5ce36004b4d2de0a440`

## Expected behavior

1. Every inserted factual, quantitative, prevalence, demand, price, and typical-performance claim must map to approved evidence.
2. Plausibility, cautious tone, or softer wording may not substitute for evidence.
3. Gate E5 must fail while any unsupported insertion remains.
4. Claims unnecessary to the argument should be removed rather than triggering broad research.
5. A necessary claim may return only as a bounded Step 0 amendment question.
6. Removal must restore an auditable script identity before E5 can pass again.
7. No script lock, narration handoff, episode number, or production authority may result.

## Acceptance-set case

This targets the outstanding case: “A script that introduces unsupported claims should return a bounded amendment request to Step 0.”
