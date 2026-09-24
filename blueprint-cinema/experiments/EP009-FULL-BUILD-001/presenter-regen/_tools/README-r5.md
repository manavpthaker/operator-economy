# EP009 r5 presenter adapter

Prepared, not globally active. `ACTIVE-PLAN.json` remains r4. Only the exact already-submitted P00 opening job may be processed independently. Root owns bulk clearance; flagged P01 pilots do not grant it.

Use this Python runtime:

```
/private/tmp/claude-501/-Users-brownmanbrain-GitHub-operator-economy/82de42ec-ae77-42eb-8a88-f56e54114dda/scratchpad/syncenv/bin/python
```

Script, from repository root:

```
blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-regen/_tools/regen_r5.py
```

`check` verifies all 22 parts offline: exact r3 PCM ranges, current artifacts, preserved prior executions, <=12-second generation limits and reserve arithmetic. `totals` reads the shared regeneration ledger. Neither activates work.

For the already submitted P00 job, run sequentially:

```
check
trim P00
fal-submit P00
fal-result P00
align P00
gate P00
nose P00
```

`fal-submit` is a paid operation, limited to the root-authorized single restoration. Existing submission intent blocks resubmission. Poll `fal-result` until completed. Do not rerun `native P00`: the original failed measurement is preserved and the explicit lexical selection is already bound.

After actual scoped review, write `P00/NOTES.json` with `review_status: complete`, boolean `flagged`, `reviewer`, `method`, `review_limitations`, and current `execution_sha256`, `restored_sha256`, `sync_gate_sha256`. Diagnostic flags remain flags; technical completion does not confer owner acceptance. Then:

```
take P00
conform-opening
verify-opening
index
```

Root currently requires unflagged P00 before r4 integration. The opening output is only `final-r5/opening-P00.mp4`, frames `[0,86)`. It never replaces whole seg001. Retain F01 `[86,135)` and all later r3 pictures. New full segments use `conform seg044` / `verify seg044` etc only after separate root bulk clearance. All outputs stay under `final-r5`; each part's new record is `TAKE-r5.json`. Existing videos, TAKE records and audio are preserved. Existing conformed media is never overwritten.

`final-r5/INDEX.json` binds `plan` and exact r3 `master`. It has 15 normal `segments` plus a separate `opening_insert`. Each entry preserves `output_frames`, `frames`, `parts_used`, `part_reviews`, `flagged_parts`, `technical_complete`, `owner_accepted:false`, and path/hash when present. Status is pending, pending-review, review-ready or review-ready-flagged; the last two are review eligibility, not acceptance.

P00 native timing selection is explicit: `P00/NATIVE-OFFSETS-SELECTION.json` binds the original failed record, separate `NATIVE-OFFSETS-lexically-anchored.json`, and immutable independent lexical audit/evidence. The selected record uses the same three windows within verified `[1.0,1.5]` seconds: offsets `1.19,1.09,1.27`, spread `.18`. The original wrong-phrase `.18`-second match remains preserved. The existing `.30`-second drift threshold and media checks still apply. Selection provenance is included in TRIM, SYNC-GATE and TAKE-r5. No selection defaults to the original failed measurement.

For eventual bulk work, `ACTIVE-PLAN` must bind the exact r5 plan and a `bulk_clearance` JSON with `status: cleared`, matching `selected_plan`, and nonempty hash-bound `pilot_review_evidence`. Missing/stale clearance blocks processing before provider transport. No clearance has been created here.

R5 maps 17 unchanged future parts to verified r3 PCM, replaces retired P08a/b/c with P08r3a/b, retains exact P01a/b prior executions and maps the standalone P00 generation. Retired part IDs are rejected. Copied preparation records retain their original source paths; the r5 plan explicitly binds their canonical copies. P13b's old guidance ends 24 zero samples before the true master end; final conform keeps the full r3 master and only zero-pads to the picture boundary.

Offline budget: 191 credits before P00 + 32.5 P00 committed + 1,526 remaining = 1,749.5 against 1,800; 50.5 headroom. This is accounting arithmetic, not a live price/balance preflight. Fal remains capped at $30 by the shared ledger.
