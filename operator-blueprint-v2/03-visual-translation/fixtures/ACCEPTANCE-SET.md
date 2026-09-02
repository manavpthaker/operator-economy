# Step 3 acceptance set

Status: **proposed v0.2**. Frozen when Step 3 is approved.

Standard under test: `VISUAL-TRANSLATION-STANDARD.md` · Gates: `STAGE-GATES.md`

Validator: `validate.py` — SHA-256 `5105ac6b12d9104928f2311b5d029a70695fcec29c10b331bee68c5e130a3adf`

Fixtures are test-only. They cannot create an episode workspace, approve any episode's visuals, or authorize Step 4.

## What the validator does and does not establish

It implements only the gate conditions that are **mechanically decidable**. It clears **hygiene**.

It cannot establish whether the direction is any good. Whether a selected Boundary Ledger operation
is the clearest expression of the business state, whether the world is coherent, or whether a style
frame is worth looking at are creative decisions each gate records separately. A clean validator run
is readiness for that judgement, never a substitute for it.

This mirrors the distinction Step 2's E5V draws between mechanical support and positive identity, and it exists for the same reason: a passing structural check is exactly the evidence that misled the EP006 coverage review at 21 out of 23.

## Controls

Twenty-four controls. The original v0.1 baseline and nine adversarial controls remain unchanged and
executable through an explicit legacy mode. A separate v0.2 baseline and thirteen patch controls test
the Boundary Ledger derivation contract. Every adversarial control must fail **exactly** its target
gate, not merely fail.

### Preserved v0.1 controls

| Control | Injected defect | Must fail | Result |
|---|---|---|---|
| `positive/clean-baseline` | none | nothing | **PASS** |
| `adversarial/a1-engine-diverges` | engine restates the customer differently from the Canvas | **V2** | **PASS** |
| `adversarial/a2-inert-unit` | plan unit with no state change and no evidence, unjustified | **V4** | **PASS** |
| `adversarial/a3-look-final` | look recorded as final rather than provisional | **V6** | **PASS** |
| `adversarial/a4-runtime-named` | a runtime named inside a locked artifact | **V7** | **PASS** |
| `adversarial/a5-estimated-timing` | unit timing estimated rather than transcript-bound | **V4** | **PASS** |
| `adversarial/a6-orphan-claim` | evidence anchor bound to a claim ID that does not exist | **V3** | **PASS** |
| `adversarial/a7-label-upgrade` | a visual upgrades an evidence label from MODELED to OBSERVED | **V4** | **PASS** |
| `adversarial/a8-unreachable-object` | world object neither verb-reachable nor marked static | **V3** | **PASS** |
| `adversarial/a9-compounding-metaphor` | mechanic named a compounding flywheel with no compounding evidence | **V2** | **PASS** |

These controls preserve the history of the superseded local-mechanic contract. Their mechanic and
verb fields are not valid v0.2 production fields; preserving them prevents a rule change from
rewriting prior acceptance evidence.

### Boundary Ledger v0.2 controls

| Control | Injected defect | Must fail | Result |
|---|---|---|---|
| `positive/boundary-ledger-derived` | none; business operation derives from upstream state and selects a permitted pinned operation | nothing | **PASS** |
| `adversarial/a10-derived-operation-diverges` | `business_operation` widens the locked upstream state | **V2** | **PASS** |
| `adversarial/a11-boundary-ledger-hash-drift` | semantic-core hash no longer matches the pinned file | **V1** | **PASS** |
| `adversarial/a12-unknown-boundary-operation` | Rev D-style `activate` is used as an operation ID but does not exist in the pinned core | **V2** | **PASS** |
| `adversarial/a13-local-motion-vocabulary` | Step 3 adds an episode-local motion vocabulary | **V2** | **PASS** |
| `adversarial/a14-implementation-primitive` | Step 3 authors scene/animation implementation primitives | **V2** | **PASS** |
| `adversarial/a15-role-operation-disallowed` | valid core operation is paired with a semantic role the pinned motion binding does not permit | **V2** | **PASS** |
| `adversarial/a16-contract-version-missing` | current artifact omits the v0.2 contract version | **V1** | **PASS** |
| `adversarial/a17-plan-state-diverges` | plan after-state widens the selected engine operation | **V4** | **PASS** |
| `adversarial/a18-operation-provenance-missing` | derived operation omits its exact upstream locator | **V2** | **PASS** |
| `adversarial/a19-nested-motion-vocabulary` | a nested episode-model note authors an animation lexicon | **V2** | **PASS** |
| `adversarial/a20-visual-model-missing` | Step 3 omits its authored episode-specific visual model | **V2** | **PASS** |
| `adversarial/a21-forked-boundary-ledger` | a self-hashed fork claims the Boundary Ledger name and version | **V1** | **PASS** |
| `adversarial/a22-non-engine-vocabulary` | a scene-primitive vocabulary is hidden in the visual plan | **V2** | **PASS** |

Run the two contracts explicitly:

```bash
python3 validate.py --legacy positive/clean-baseline
for d in adversarial/a[1-9]-*; do python3 validate.py --legacy "$d"; done

python3 validate.py positive/boundary-ledger-derived
for d in adversarial/a1[0-9]-* adversarial/a2[0-2]-*; do python3 validate.py "$d"; done
```

## Required behaviours

Step 3 must continue to satisfy all of the following:

1. A derived engine field that diverges from the locked Canvas fails. Step 3 cannot produce a second description of the business.
2. Preserved v0.1 controls continue to reject unsupported compounding and broken verb reachability.
3. Current validation requires `contract_version: 0.2`; only `--legacy` can execute preserved v0.1 evidence.
4. Every v0.2 `business_operation` matches its exact locked upstream before/after state.
5. Every operation carries a source artifact path, live SHA-256, exact locator, and substantive mapping rationale.
6. Boundary Ledger core and motion binding must resolve to the canonical repository paths and be
   versioned and hash-pinned; drift or a self-hashed fork fails V1.
7. Every selected role and operation exists, and the pinned binding permits the pair.
8. Step 3 authors an episode-specific visual model that covers every derived operation.
9. Step 3 authors neither a local brand motion vocabulary nor an implementation primitive; named
   aliases are rejected recursively across engine, world, visual plan, look, and lock artifacts.
10. Every object an operation acts on exists, and every world object is operation-reachable or explicitly static.
11. An evidence anchor bound to a nonexistent claim fails.
12. Plan timing that is estimated rather than transcript-bound fails.
13. Plan before/after state must equal the selected engine operation's before/after state.
14. A plan unit with no state change and no evidence fails unless justified in writing.
15. A visual that upgrades an evidence label fails.
16. A look recorded as anything but provisional fails.
17. A runtime named in any locked artifact fails.
18. A broken audio-only element fails.
19. A structural pass never implies creative approval.

## Change control

- A semantic change to any gate condition, the derived-selected-authored split, the Boundary Ledger
  pin, the act-approval rule, the provisional-look rule, or the runtime exclusion requires a new Step 3 version.
- Rerun the full acceptance set before approving that version.
- Preserve these controls. **Do not edit a control to conform to a new rule.** If a control's expected outcome changes, add a dated fixture and state whether it changed because the rule changed or because the input changed.

## Known gaps

The validator does not yet cover:

- V1 Step 1 and Step 2 artifact-hash verification, which needs a real episode with both locks.
  Boundary Ledger file-hash drift is covered by `a11`.
- V5a and V5b entirely. Rhythm and direction are judgement gates with no mechanical surface, and no fixture here tests them.
- Continuous act coverage and gap detection in V4, which needs a real transcript.
- Object permanence in V3, which is a visual judgement rather than a data property.
- The provenance control currently exercises JSON artifacts with dot-key locators. Canonical Step 1
  sources are Markdown, so a production gate still needs a hash-locked section-locator adapter; this
  fixture validator must not be represented as that adapter.
- Direction-bible and rhythm-map prose remain human-audited for disguised local vocabulary. The
  recursive primitive scan covers the five locked JSON artifacts represented in this fixture set.
- Semantic euphemisms for a local implementation vocabulary still require human review. The
  validator rejects known vocabulary and primitive field families recursively; it cannot infer the
  intent of every arbitrary field name.

**These gaps are recorded rather than hidden.** A clean run across twenty-four controls proves the
mechanical conditions bite. It does not prove Step 3 is complete.

## Scope boundary

Passing this set would approve Step 3 behaviour only. It does not approve an episode's visuals,
approve Boundary Ledger's provisional motion implementation, populate any workspace, choose a
runtime, or make Steps 4 through 8 authoritative.
