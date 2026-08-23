# Step 2 Team Workflow

Status: proposed v0.2; test before approval.

One person or agent may perform several roles, but the decisions remain separate and independently reviewable.

## Accountable roles

### Owner

- approves the narrator identity and performance target;
- approves meaningful exceptions;
- performs the calibration and final creative decisions;
- is the only role that may set `creative_approved`; and
- signs the narration lock.

### Narration producer

- owns Step 2 state;
- verifies the Step 1 handoff;
- sequences work and consolidates reviews;
- protects raw files and provenance;
- keeps native acquisition identity separate from delivery-master identity;
- records separate calibration and full-capture authorizations; and
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

For synthetic narration, the voice custodian also owns the frozen request envelope, chunk map,
provider job-ID capture, raw outputs, source-format inspection, and pickup-continuity evidence
required by `02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md`.

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
- verifies native acquisition and delivery formats separately;
- confirms a fallback MP3 was inspected, converted once, and never described as native PCM;
- verifies that processing remains corrective rather than final-program mastering; and
- may recommend or record `technical_pass` when every N6 requirement passes, but cannot grant
  creative approval.

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
N3 identity/acquisition freeze
        ↓
separately authorized N4A calibration
        ↓
technical review ───── owner calibration approval
        ↓
separately authorized N4B full capture
        ↓
performance review ─ conformity review ─ technical review
        └───────────────┬─────────────────┘
                        ↓
                 selects and pickups
                        ↓
                  narration edit
                        ↓
final conformity ─ transcript/pause alignment ─ technical measurement
        └────────────────┬─────────────────────────────┘
                         ↓
                  technical_pass
                         ↓
               independent listen + owner creative_approved
                         ↓
                    narration lock
```

## Parallel-work rules

- Direction and pronunciation preparation may run in parallel after N1.
- Calibration may begin only after N3 and a bounded calibration authorization.
- Full capture may begin only after current N4A owner approval and a separate full-capture authorization.
- Section-level take reviews may run in parallel after raw files are registered.
- Performance, lexical, and technical reviewers report independently before select consolidation.
- Final lexical conformity, transcript alignment, and technical measurement may run in parallel only against the same frozen master candidate.
- If that master changes, all three final checks rerun.
- Agents may propose decisions; only named humans approve owner, rights, calibration creative, and
  final creative gates.
- External provider calls require explicit fixture-or-episode authorization and credentials for
  each bounded phase; documentation work alone does not grant it.
- V2 agents and tooling must not invoke or import V1
  `studio/scripts/originate/generate_vo.py`.

## Conflict rules

- The locked script wins over a more natural but different spoken phrase.
- A confirmed lexical mismatch wins over an automated “pass.”
- The Step 1 `W` identity wins over ASR wording or acoustic segmentation.
- Source inspection wins over a filename or requested provider format.
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
