# Step 2 Team Workflow

Status: proposed v0.3 provider-selection revision; test before approval.

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

For a provider bakeoff, the narration producer also verifies that the four initial authorizations
remain separate, that the later long-form test has its own fifth authorization, and that no record
is mislabeled as N4B full-capture authority.

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

### Original-sample custodian

- resolves exactly one authorized original human recording;
- verifies owner consent, provenance, commercial-use basis, hash, and custody;
- stops when the account exposes zero samples or more than one sample without a new exact-sample
  authorization;
- preserves sensitive audio outside Git; and
- does not substitute generated, remixed, ripped, mixed-program, or unknown-source audio.

### External-action operator

- performs only the exact provider/account/UI action named in the active authorization;
- treats login state and credentials as access, never approval;
- consumes the authorization before mutation, generation, or retrieval begins;
- records immutable provider or UI receipts and uncertain external state; and
- stops before retry, clone replacement, extra generation, long-form work, or full capture.

The Hume clone action may be UI-mediated. The operator records the provenance-bound source hash and
resulting clone identity. The public Create Voice API must not be represented as a human-audio
upload-clone endpoint.

### Blind-review curator

- verifies hard gates before creative scoring;
- creates lossless review copies under one disclosed gain-only policy;
- randomizes candidate and passage codes without revealing provider or settings;
- seals the code map and raw hashes until all signed scorecards are frozen; and
- does not score the candidates;
- leaves every scorer sheet blind and immutable after signature; and
- creates a separate consolidation that binds both scorecard hashes and the sealed-map hash before
  unsealing and calculating passage selects.

### Independent listener

- listens without visuals or production explanations;
- checks comprehension, pace, trust, fatigue, and credibility; and
- supplies a separate recommendation before owner approval.

## Parallel workflow

Parallel work begins only after its upstream gate is stable.

```text
N1 handoff accepted
        ↓
performance direction + provider-agnostic envelope ─ pronunciation preparation
        ↓                            ↓
when method unresolved: sample provenance gate
        ↓
four separately authorized external actions
        ↓
blind short scoring
        ↓
separately authorized long-form/pickup test for eligible methods
        ↓
owner method selection
        ↓
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
- Original-sample provenance review may prepare metadata after N2, but retrieval, Hume upload,
  clone creation, and narration synthesis each wait for their exact authorization.
- Eleven E1/E2 use the same text, tags, model, voice, and settings and differ only by
  seed/generation. Within each passage, Hume H1/H2 are two generations from one identical
  `POST /v0/tts` JSON request and description with `num_generations: 2`.
- The short review remains blind until owner and independent-listener scorecards are signed.
- Consolidation and unblinding occur only in the curator record, never by appending to a signed
  scorer sheet.
- Score all eight clips. For each provider, the highest hard-gate-passing P1 generation and highest
  hard-gate-passing P2 generation become its passage selects; their arithmetic mean is the provider
  score. Unselected failures and variance remain operational metrics, not score penalties.
- Every provider must have two passing passage selects and score at least 80. The short-round leader
  advances; a runner-up advances only within 5.0 points.
- The long-form test uses 3.5 to 4.5 minutes plus one same-word pickup several hours later under its
  own authorization. It is not N4B full capture.
- Long-form/pickup is pass/fail, not a rescore. Use frozen short provider scores: retain ElevenLabs
  when it passes confirmation and is within 5.0 points of Hume or leads; adopt Hume only when its
  short score is at least 80, leads by more than 5.0 points, and it passes continuity and pickup.
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
- The initial provider-selection round requires exactly four separate authorizations: ElevenLabs
  read-only voice metadata/sample retrieval; Hume UI upload plus one clone; ElevenLabs two-passage,
  two-generation short calibration; and Hume two-passage, two-generation short calibration.
- The exact machine scopes are `elevenlabs_sample_retrieval`, `hume_clone_creation`,
  `elevenlabs_calibration`, and `hume_calibration`.
- The later long-form continuity/pickup test is a fifth authorization. N4B full capture requires a
  new authorization after N4A passes.
- V2 agents and tooling must not invoke or import V1
  `studio/scripts/originate/generate_vo.py`.

## Conflict rules

- The locked script wins over a more natural but different spoken phrase.
- A confirmed lexical mismatch wins over an automated “pass.”
- The Step 1 `W` identity wins over ASR wording or acoustic segmentation.
- Source inspection wins over a filename or requested provider format.
- A performance concern wins over technical convenience when a same-word pickup can repair it.
- A performance-only creative revision stays in Step 2. Step 1 reopens only for an actual requested
  word change or editorial defect.
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
