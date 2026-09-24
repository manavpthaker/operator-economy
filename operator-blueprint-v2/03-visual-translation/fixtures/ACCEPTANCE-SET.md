# Step 3 acceptance set

Status: **proposed v0.3**. Frozen when Step 3 is approved.

Standard under test: `VISUAL-TRANSLATION-STANDARD.md` · Gates: `STAGE-GATES.md`

Validator: `validate.py` — SHA-256 `fc1721583c49975991a4c69f09a572ffbee83d0107a16c1d794a3d6d02396470`

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
executable through an explicit legacy mode. A separate v0.3 baseline and its patch controls test
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
verb fields are not valid v0.3 production fields; preserving them prevents a rule change from
rewriting prior acceptance evidence.

### Boundary Ledger v0.3 controls

| Control | Injected defect | Must fail | Result |
|---|---|---|---|
| `positive/boundary-ledger-derived` | none; business operation derives from upstream state and selects a permitted pinned operation | nothing | **PASS** |
| `adversarial/a10-derived-operation-diverges` | `business_operation` widens the locked upstream state | **V2** | **PASS** |
| `adversarial/a11-boundary-ledger-hash-drift` | semantic-core hash no longer matches the pinned file | **V1** | **PASS** |
| `adversarial/a12-unknown-boundary-operation` | Rev D-style `activate` is used as an operation ID but does not exist in the pinned core | **V2** | **PASS** |
| `adversarial/a13-local-motion-vocabulary` | Step 3 adds an episode-local motion vocabulary | **V2** | **PASS** |
| `adversarial/a14-implementation-primitive` | Step 3 authors scene/animation implementation primitives | **V2** | **PASS** |
| `adversarial/a15-role-operation-disallowed` | valid core operation is paired with a semantic role the pinned motion binding does not permit | **V2** | **PASS** |
| `adversarial/a16-contract-version-missing` | current artifact omits the current contract version | **V1** | **PASS** |
| `adversarial/a17-plan-state-diverges` | plan after-state widens the selected engine operation | **V4** | **PASS** |
| `adversarial/a18-operation-provenance-missing` | derived operation omits its exact upstream locator | **V2** | **PASS** |
| `adversarial/a19-nested-motion-vocabulary` | a nested episode-model note authors an animation lexicon | **V2** | **PASS** |
| `adversarial/a20-visual-model-missing` | Step 3 omits its authored episode-specific visual model | **V2** | **PASS** |
| `adversarial/a21-forked-boundary-ledger` | a self-hashed fork claims the Boundary Ledger name and version | **V1** | **PASS** |
| `adversarial/a22-non-engine-vocabulary` | a scene-primitive vocabulary is hidden in the visual plan | **V2** | **PASS** |

## Markdown section-locator provenance (v0.3)

Real Step 1 artifacts are Markdown, not JSON. For a Markdown source the provenance chain is
**path -> hash -> section -> verbatim quote**. The validator proves the cited quote is real and
comes from the cited section; whether the derived `state_before` and `state_after` faithfully
represent that quote is the named human approval V2 already requires. A machine can verify
provenance, not the fidelity of a paraphrase, and this contract does not pretend otherwise.

| Control | What it proves | Gate | Result |
|---|---|---|---|
| `positive/markdown-provenance` | a nested heading locator resolves and its verbatim quote verifies | — | **PASS** |
| `adversarial/a23-markdown-locator-unresolved` | a locator naming a non-existent heading fails closed | **V2** | **PASS** |
| `adversarial/a24-markdown-quote-outside-section` | a quote present in the document but outside the cited section fails | **V2** | **PASS** |
| `adversarial/a25-markdown-quote-missing` | citing a Markdown section with no verbatim quote fails | **V2** | **PASS** |
| `adversarial/a26-markdown-source-hash-drift` | a drifted Markdown source hash fails | **V2** | **PASS** |

`a24` is the load-bearing control: it fails a quote that appears elsewhere in the same file, which
is what distinguishes section-scoped resolution from document-wide containment.

Run the full suite. Ten legacy controls preserve the superseded v0.1 contract and are never edited
to conform to a later rule; forty-four exercise v0.3.

```bash
# legacy v0.1 contract -- 10 controls
python3 validate.py --legacy positive/clean-baseline
for d in adversarial/a[1-9]-*; do python3 validate.py --legacy "$d"; done

# v0.3 contract -- 44 controls
for d in positive/boundary-ledger-derived positive/markdown-provenance positive/establishment-class; do
  python3 validate.py "$d"
done
for d in adversarial/a1[0-9]-* adversarial/a2[0-9]-* adversarial/a3[0-9]-* adversarial/a4[0-3]-*; do
  python3 validate.py "$d"
done

# stage-scoped, for an episode mid-flight
python3 validate.py --through V2 <episode-dir>
```

The frozen result of the last full run is `ACCEPTANCE-EVIDENCE.md` — every control listed with its
actual outcome, not a summary.


## Establishment class and v0.3 bindings

`establish` changes what the viewer can identify, not the state of the business. Recording it as a
derived business operation would require a `state_before` no upstream artifact contains. v0.3 holds
it in a separate `AUTHORED` establishment class so the derivation invariant needs no exception.

| Control | What it proves | Gate | Result |
|---|---|---|---|
| `positive/establishment-class` | a valid establishment row with upstream-cited actors passes | — | **PASS** |
| `adversarial/a27-authored-in-business-operations` | the same viewer-state operation inside `business_operations` fails | **V2** | **PASS** |
| `adversarial/a28-establishment-carries-business-state` | an establishment row carrying business-state fields fails | **V2** | **PASS** |
| `adversarial/a29-establishment-acts-on` | an establishment row using `acts_on` rather than `reveals` fails | **V2** | **PASS** |
| `adversarial/a30-establishment-provenance-missing` | an establishment row with no verbatim upstream quote fails | **V2** | **PASS** |
| `adversarial/a31-establishment-role-op-disallowed` | an establishment role-operation pair the binding forbids fails | **V2** | **PASS** |
| `adversarial/a32-object-class-no-instances` | an operation acting on a class with no instances fails | **V3** | **PASS** |
| `adversarial/a33-class-instance-absent` | a class declaring an instance absent from the world fails | **V3** | **PASS** |
| `adversarial/a34-changed-by-unknown-operation` | `changed_by` naming an unknown operation fails | **V3** | **PASS** |
| `adversarial/a35-revealed-by-unknown-establishment` | `revealed_by` naming an unknown establishment row fails | **V3** | **PASS** |

`a27` paired with `positive/establishment-class` is the load-bearing test: the identical operation
must fail inside `business_operations` and pass inside the establishment class.

v0.3 also splits `operation_bindings` into `changed_by`, `carried_by` and `revealed_by`, because an
object an operation changes, one it merely carries, and one an establishment row reveals are three
different relationships that the single field was conflating.

## V1 freeze and V3 world integrity (v0.3, second pass)

Added after an owner review returned both Step 3 authority and EP007's activation. Each closes a
condition that was being asserted in prose rather than checked.

| Control | What it proves | Gate | Result |
|---|---|---|---|
| `adversarial/a36-input-lock-incomplete` | a V1 freeze omitting an upstream artifact fails | **V1** | **PASS** |
| `adversarial/a37-input-lock-hash-drift` | a frozen artifact changing after the lock fails | **V1** | **PASS** |
| `adversarial/a38-motion-status-unrecorded` | not acknowledging the motion binding's provisional status fails | **V1** | **PASS** |
| `adversarial/a39-legacy-transition-form` | a transition asserting neither trigger nor reversibility fails | **V3** | **PASS** |
| `adversarial/a40-transition-without-trigger` | a transition not naming what causes it fails | **V3** | **PASS** |
| `adversarial/a41-world-declares-no-paths` | a world with no traceable routes fails | **V3** | **PASS** |
| `adversarial/a42-anchor-without-qualification` | an evidence anchor stating no limit on what it may imply fails | **V3** | **PASS** |
| `adversarial/a43-binding-disagreement` | engine `acts_on` and world `changed_by` disagreeing fails | **V3** | **PASS** |

`a36`, `a38` and `a40` are full fixture directories rather than merge patches: **deleting a key
cannot be expressed as a patch**, because the merge restores it from the base. A case that appears
to test an omission while silently inheriting the value proves nothing.

## Complete-contract checks (v0.3, third pass)

Added after a second owner return. Each replaces a condition that a shallower check had let pass.

| Control | What it proves | Gate | Result |
|---|---|---|---|
| `adversarial/a44-transition-trigger-not-a-changer` | a transition triggered by an operation that does not change the object fails | **V3** | **PASS** |
| `adversarial/a45-static-object-with-transitions` | an object both static and transitioning fails | **V3** | **PASS** |
| `adversarial/a46-nonstatic-with-no-changer` | an object neither static nor changed by anything fails | **V3** | **PASS** |
| `adversarial/a47-path-without-edges` | a path that is a state list rather than a route fails | **V3** | **PASS** |
| `adversarial/a48-path-edge-without-condition` | a path edge stating no condition fails | **V3** | **PASS** |
| `adversarial/a49-path-without-traveler` | a path not naming what travels it fails | **V3** | **PASS** |
| `adversarial/a50-anchor-without-must-not-imply` | an anchor dropping its upstream must-not-imply limit fails | **V3** | **PASS** |

`a45` and `a46` are full fixture directories mutating one object in place. As merge patches they
replaced the whole objects array, which cascaded into V4 and stopped the control isolating its own
condition.

V1's freeze now covers the **complete governing input set** — thirteen artifacts including both
locks, the thesis, spine, outline, script and spoken identity — not a convenience subset.

## Required behaviours

Step 3 must continue to satisfy all of the following:

1. A derived engine field that diverges from the locked Canvas fails. Step 3 cannot produce a second description of the business.
2. Preserved v0.1 controls continue to reject unsupported compounding and broken verb reachability.
3. Current validation requires `contract_version: 0.2`; only `--legacy` can execute preserved v0.1 evidence.
4. Every v0.3 `business_operation` matches its exact locked upstream before/after state.
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
  sources are Markdown; the v0.3 section-locator adapter closes that gap for business-operation
  provenance and is exercised against EP007's real locked artifacts. It verifies provenance only,
  never that a derived state faithfully paraphrases its quote.
- Direction-bible and rhythm-map prose remain human-audited for disguised local vocabulary. The
  recursive primitive scan covers the five locked JSON artifacts represented in this fixture set.
- Semantic euphemisms for a local implementation vocabulary still require human review. The
  validator rejects known vocabulary and primitive field families recursively; it cannot infer the
  intent of every arbitrary field name.

**These gaps are recorded rather than hidden.** A clean run across fifty-four controls proves the
mechanical conditions bite. It does not prove Step 3 is complete.

## Scope boundary

Passing this set would approve Step 3 behaviour only. It does not approve an episode's visuals,
approve Boundary Ledger's provisional motion implementation, populate any workspace, choose a
runtime, or make Steps 4 through 8 authoritative.
