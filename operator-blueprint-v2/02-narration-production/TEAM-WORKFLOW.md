# Step 2 Team Workflow

Status: proposed v0.1; test before approval.

One person or agent may perform several roles, but the decisions remain separate and independently reviewable.

## Accountable roles

### Owner

- approves the narrator identity and performance target;
- approves meaningful exceptions;
- performs the final creative decision; and
- signs the narration lock.

### Narration producer

- owns Step 2 state;
- verifies the Step 1 handoff;
- sequences work and consolidates reviews;
- protects raw files and provenance; and
- prepares the final handoff.

### Performance director

- translates the editorial argument into playable direction;
- directs calibration and full takes;
- identifies performance defects and pickups; and
- cannot change locked words.

### Narrator or voice custodian

- performs the script or operates the authorized synthetic voice;
- preserves the approved identity and capture configuration;
- records session or generation provenance; and
- flags wording that cannot be performed naturally rather than rewriting it.

### Dialogue editor

- assembles approved takes and pickups;
- performs conservative cleanup;
- maintains the edit decision list; and
- exports the clean narration master.

### Conformity editor

- compares the final spoken master to the locked script;
- investigates additions, omissions, substitutions, repeats, and truncations;
- records human dispositions; and
- does not approve a confirmed lexical change.

### Transcript editor

- aligns the final master at word level;
- validates timing invariants;
- records uncertain alignments; and
- binds the transcript to the master hash.

### Technical reviewer

- checks audio format, clipping, true peak, noise, edit continuity, and measurements;
- verifies that processing remains corrective rather than final-program mastering; and
- records pass, pickup, or block.

### Independent listener

- listens without visuals or production explanations;
- checks comprehension, pace, trust, fatigue, and credibility; and
- supplies a separate recommendation before owner approval.

## Parallel workflow

Parallel work begins only after its upstream gate is stable.

```text
N1 handoff accepted
        ↓
performance direction ───── pronunciation preparation
        ↓                            ↓
N3 voice/capture lock and calibration approval
        ↓
full takes by section
        ↓
performance review ─ conformity review ─ technical review
        └───────────────┬─────────────────┘
                        ↓
                 selects and pickups
                        ↓
                  narration edit
                        ↓
final conformity ─ transcript alignment ─ technical measurement
        └────────────────┬─────────────────────────────┘
                         ↓
               independent listen + owner lock
```

## Parallel-work rules

- Direction and pronunciation preparation may run in parallel after N1.
- Section-level take reviews may run in parallel after raw files are registered.
- Performance, lexical, and technical reviewers report independently before select consolidation.
- Final lexical conformity, transcript alignment, and technical measurement may run in parallel only against the same frozen master candidate.
- If that master changes, all three final checks rerun.
- Agents may propose decisions; only named humans approve owner, rights, and final creative gates.
- External provider calls require explicit episode authorization and credentials; documentation work alone does not grant it.

## Conflict rules

- The locked script wins over a more natural but different spoken phrase.
- A confirmed lexical mismatch wins over an automated “pass.”
- A performance concern wins over technical convenience when a same-word pickup can repair it.
- Authorization and consent blockers stop the work regardless of schedule.
- Step 1 owns word changes; Step 2 owns delivery; Step 3 owns visual interpretation; Resolve/Fairlight owns the final program mix.

## Required review record

Every gate decision records:

- episode and stage;
- input revision and hashes;
- reviewer and role;
- decision: `pass`, `revise`, `pickup`, `return_to_editorial`, or `blocked`;
- actionable findings;
- unresolved caveats; and
- date.

Silence, file existence, successful generation, or successful export is not approval.
