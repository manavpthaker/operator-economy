# EP009 r4 presenter integration — prepared, not rendered

The new builder reads the frozen, technically verified full r3 BUILD. It uses that source table and its exact master, transcript, time map, scoped owner lock and six film inserts. Only eligible presenter picture selections may change; total duration stays 29,323 frames. It never replaces or rewrites r3 files.

`../_tools/build_r4.py` expects `presenter-regen/final-r5/INDEX.json` with bound `plan` and `master`, fifteen `segments` entries, and one separate `opening_insert`. Every eligible entry must be `review-ready`, technically complete, explicitly unaccepted, hash-current, 1280×720 at 24 fps, and exactly match its revised output interval. Flagged entries are held, with their evidence retained in readiness reporting. Obsolete P08 parts are rejected.

- P00 replaces only frames `[0,86)`. F01 remains at its original source `[86,135)`; F02 begins at frame 135 without a timing or source shift.
- Corrected P08 covers `[15920,16263)` with `P08r3a` and `P08r3b`. Its locked audio remains the r3 master; no older speaking P08 source is eligible.
- All other revised presenter slots follow the 75 frozen r3 row ranges.

Readiness is read-only by default:

```sh
python3 blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/_tools/build_r4.py
```

After the required selections exist, prepare a new BUILD and filter graph without encoding:

```sh
python3 blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/_tools/build_r4.py --write-plan --name ep009-r4-preflight
```

When root authorizes full rendering, use a different fresh name with `--render`. Files go to `assembly/r4/` and `assembly/qa/r4/`; pre-existing names are refused. Default `full-review` refuses any missing or flagged selection. A partial draft must name each intended replacement, for example:

```sh
python3 blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/_tools/build_r4.py --mode partial-review --select P00
```

That command changes only the first 86 picture frames once P00 is eligible. The other fourteen r1 presenter segments and corrected P08 still remain as r3, even if other files happen to exist. Add `--write-plan` to retain the plan, or `--render` only after root authorizes that render. A requested missing or flagged selection blocks the render; it cannot silently fall back. No flag override exists in this builder.

After encoding, run `../_tools/verify_r4.py <new BUILD>` using the local syncenv runtime. This verifies the complete decode and every audio sample against the unchanged r3 master, including unity stereo level and silent final padding. Normal-speed audiovisual inspection and changed-seam inspection remain separate tasks. No tool here marks a new take owner-accepted or advances release.

Preparation validation: Python syntax parsed; in-memory whole-timeline replacement tests confirmed that only `[0,86)` and `[15920,16263)` changed, with the remaining 28,894 source-frame identities unchanged. A deliberately invalid 87-frame opening was rejected. Read-only readiness correctly held all sixteen required selections while the r5 index was absent. No provider calls, active-plan edits, or full render were performed during builder preparation.
