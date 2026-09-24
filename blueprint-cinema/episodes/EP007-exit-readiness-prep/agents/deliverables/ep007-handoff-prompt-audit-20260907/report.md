# EP007 Step 2 → Step 3 intake and prompt audit

Date: 2026-09-07  
Work order: `ep007-handoff-prompt-audit-20260907`  
Disposition: **partial packet; audit complete, production-route acceptance unavailable**

## Bottom line

The assigned bytes have not drifted. The 13 files in the current Step 3 v0.4 input lock, all 13
artifacts named by the frozen E6 table, and all 8 artifacts named by the N7 table also match their
recorded hashes. That proves byte integrity only.

It does **not** establish a production-ready Step 2 → Step 3 handoff:

1. N7 requires an independent eyes-closed listen, but EP007 says no second-person listen occurred
   and then declares N7 passed.
2. The locked master is 48 kHz / 16-bit / mono while the current Step 2 contract requires 48 kHz /
   24-bit / mono. The current Step 2 validator also rejects EP007's legacy transcript shape.
3. EP007 has a timing handoff inside `narration-lock.md`, not the dedicated receiving record required
   by the shared Step 2 handoff template. Receiver, acceptance, editorial/performance context,
   visual-support constraints, origin/disclosure, and downstream audio boundaries are not assembled
   and accepted in one authoritative receipt.
4. Step 3 v0.4 remains proposed and unapproved. Its own episode manifest calls V1 a mechanically
   verified candidate awaiting process authority and says V2–V7 are not started.

The episode's business meaning is mostly present in the locked Step 1 sources. The dangerous gap is
the receiving route: a renderer can reach valid source bytes without receiving an explicit,
authority-resolved synthesis of what must be understood, withheld, qualified, and left unresolved.
No script or narration rewrite is indicated by this audit.

## 1. Hash and provenance audit

### Assigned work-order inputs

| Input | Expected SHA-256 | Recomputed result |
|---|---|---|
| `operator-blueprint-v2/02-narration-production/06-approval/VISUAL-TRANSLATION-HANDOFF.template.md` | `c2acbb52053d5a804cdb38adc299e460a9d7b23c0b8410bac51896d19d368b9c` | MATCH |
| `operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/narration-lock.md` | `61cfd940b9f8bfcb0e502e07f073a7a1457a671b9a4a35667e6ca08c2fafbbd5` | MATCH |
| `operator-blueprint-v2/episodes/EP007-exit-readiness-prep/03-visual-translation/input-lock.json` | `9adde76470b05da2d635521e8711e4d55ed76353a1479db50ba430449899a384` | MATCH |

The assigned paths and hashes appear at work-order lines 35–47. No assigned input drift was found.

### Current v0.4 freeze

All 13 entries in `input-lock.json` lines 9–65 resolve and match:

| ID | SHA-256 |
|---|---|
| `editorial_lock` | `7d3871804c82e7da09a59c01cd5ef4342ad0ad9141158869acc71d6d291a1319` |
| `operator_canvas` | `3376437f8eda00a4aec5b1ef6e0ff5379abb2f051e3512fc5d683ed2720b158f` |
| `episode_investment_thesis` | `868dc798eeb0513b083debb08ea376b333ae486e9a535be7facf5183e94726f4` |
| `narrative_spine` | `c053f4d95542ce9fc42e9a665d10576cc69e99577fc8849208970f9163efbe4f` |
| `episode_beat_sheet` | `eb953ffa1a0fc5bf4540842f8cd86db19838a1692c00e439c9fdfd538225f4fb` |
| `claims_map` | `0c4f715d71f816fb8190c5fc3777e61cfdabd3c2cc5f26a2aee7a89d0f5fe4e1` |
| `script` | `e56bbb80c1b3a21679a17459402130d820be285ee389fc2978ef8216d6487db0` |
| `canonical_w` | `333a45d7449f5cb4c3e394a9e262c3a3a60c3825e76563bc0149498f0b41860c` |
| `spoken_identity` | `d753a2ca34cc01e0282d10e83158d877c67614b50dbdb9f3ae17de4fc2e004fe` |
| `narration_lock` | `61cfd940b9f8bfcb0e502e07f073a7a1457a671b9a4a35667e6ca08c2fafbbd5` |
| `narration_master` | `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9` |
| `word_transcript` | `f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7` |
| `intentional_pause_map` | `0176614eb0902d945165956af8fa7ef890906d5f2e15692d14c9e0d9d8b8bdaa` |

The v0.4 process pointer and application pins in `input-lock.json` lines 5–90 also resolve and match.
The process hash is
`f1ea099a82b5f72f0032d27cbb570a2af1a5abbeb0aeb9a3731569d97f935c5f`.

### Nested lock tables

- E6: 13/13 frozen artifact rows at `01-editorial/editorial-lock.md:15-31` match.
- N7: 8/8 authoritative artifact rows at `02-narration-production/narration-lock.md:9-20`
  match.
- Across the V1 freeze and both tables, 23 unique editorial/narration source files were checked.
- The additional issued performance reference
  `01-editorial/narration-handoff.md` independently hashes to
  `090ec58c14849b65f8b20c773e0c5cb66c0fd8049028c320d9a8a2472f50e5bc`.
  It is not in the 13-entry V1 freeze or the E6/N7 reference tables.

### Mechanical checks and their limits

- Current v0.4 validator through V1: PASS, no V1 findings.
- OE skill-lock validator: PASS for 6 local files and 4 source records;
  `upstreamBytesVerified` remains false.
- Boundary Ledger validator: PASS, 55 paths and 0 errors. It retains warnings that the audio-first
  specimen has no encoded-media verification and a flattened illustration does not prove a
  motion-ready Working Model asset.
- Prompt-pack verifier: PASS for source bytes and coverage; it explicitly returns
  `creativeApproval: false` and `gateAdvance: false`.

These are integrity and structure checks. The v0.4 V1 validator enumerates the 13 required freeze
keys at `03-visual-translation-v0.4/fixtures/validate.py:46-78` and checks their paths/hashes plus a
positive duration at lines 249–268. It does not parse Step 2 gate truth, receiver acceptance, the
shared handoff's semantic fields, origin/disclosure, or the nested E6/N7 tables. The acceptance set
itself separates machine evidence from human meaning at
`03-visual-translation-v0.4/fixtures/ACCEPTANCE-SET.md:41-57`.

## 2. Proven Step 2 intake defects

### A. N7 says both "required" and "not done"

Current Step 2 gate authority says N7 passes only when the independent eyes-closed listen is
complete (`02-narration-production/STAGE-GATES.md:165-175`). EP007 records that no second person
performed it, describes the gap as "disclosed, not closed"
(`02-narration-production/narration-lock.md:38-44`), then declares N7 passed at line 79.

This is a gate contradiction, not an invitation to infer a waiver. Resolution requires an actual
listen or an explicit owner-approved change/exception in the governing authority. This audit does
neither.

### B. The locked master and transcript do not satisfy the current Step 2 contract

Step 2's required-output list specifies a clean 48 kHz / 24-bit / mono PCM WAV
(`02-narration-production/README.md:104-130`, specifically line 121). The shared handoff repeats that
format (`06-approval/VISUAL-TRANSLATION-HANDOFF.template.md:13-27`, specifically line 18). EP007's
lock and N6 technical record instead state 48 kHz / 16-bit / mono
(`narration-lock.md:24-26`; `technical-qc.md:9-18`). `ffprobe` confirms the actual master is
`pcm_s16le`, 48 kHz, mono, 16-bit, duration 1137.927479 seconds.

The current `oe-narration validate-transcript` contract expects a 24-bit working master and the
current nested transcript schema (`CLI-VALIDATION-CONTRACT.md:496-508`). Running it read-only against
the frozen EP007 transcript exits 2 with 15,936 findings. The root causes appear before the repeated
per-word errors: missing current `schema_version`, `spoken_identity`, and nested `master`; a 16-bit
master; and legacy word records using `W000000`/`token`/floating-second timing rather than the
current `w000000`/`canonical_token`/integer-millisecond/review-state shape.

Separate legacy-format checks establish that all 3,186 `token` values equal canonical W in order,
the top-level transcript and pause map point to the actual master hash, and all 276 pause records are
inside its recorded duration. That is useful content evidence, but it does not turn legacy bytes
into current-schema conformity. There is also a 1 ms rounded overlap between W000191 and W000192;
the current non-overlap contract would reject it.

No audio conversion or transcript migration is authorized here. Either would change frozen inputs
and require the corresponding invalidation/relock path.

### C. No complete Step 2 → Step 3 receiving record exists

Step 2 lists a visual-translation handoff as a required output
(`02-narration-production/README.md:104-130`). The shared template requires:

- episode identity, receiver, and dates (template lines 5–12);
- exact timeline authority and match confirmations (13–27);
- editorial and performance context with paths/hashes (29–40);
- visual-support qualifications, exact-screen treatment, deliberate-pause treatment, and Canvas
  coverage (41–50);
- origin, acquisition lineage, and synthetic disclosure (52–58);
- downstream audio boundaries (60–62); and
- path/hash/current-lock/blocker checks plus a receiving decision/signature (64–73).

EP007's `narration-lock.md:64-77` passes only master identity, duration, transcript, pause map, and
the prohibition on estimated timing/sample changes. There is no episode
`visual-translation-handoff.md`. The following receipt fields are therefore absent or unaccepted as
a complete handoff:

| Receipt field | Current evidence | Standing |
|---|---|---|
| Step 3 receiver/date and acceptance signature | none found | missing |
| Narration-lock revision/path/hash | reconstructable from V1 | not stated in a receiving record |
| Current transcript/master and pause/master conformity | legacy files are mutually hash-bound | current validator rejects transcript/format |
| N6/N7 conformity | lock asserts pass | contradicted by format and listen requirements |
| Editorial context inventory | parts are spread across V1 and E6 | not assembled/accepted |
| Performance direction | unique intent exists in issued `01-editorial/narration-handoff.md:28-49` | outside frozen V1/E6/N7 route |
| Pronunciation/caveat intent | exists at that file's lines 51–81 | outside frozen V1/E6/N7 route |
| Qualifications/risk needing picture support | Canvas/claims contain the source meaning | no accepted receiver synthesis |
| Exact names/numbers/evidence treatment | claims map supplies wording and prohibited inferences at `claims-map.md:15-42` | no accepted receiver synthesis |
| Deliberate pauses not to fill | pause map exists; performance handoff says the opening pause is the beat | treatment not accepted in one receipt |
| Narration/audio origin and synthetic disclosure | synthetic chain appears in `full-capture-review.md:1-20` and the take register | absent from the handoff surface and not frozen by V1 |
| Actual 16-bit/working-master and loudness/tail limits | disclosed in lock/QC | conflicts/limits not accepted by receiver |
| Content OS public-fact clearance | claims map says release still requires clearance at `claims-map.md:44-46` | no Step 3 receipt decision |

The fix is not to let a prompt reconstruct these silently. The receiver must record what is present,
absent, incompatible, not applicable, or interpretive, and authority must decide the unresolved
items.

## 3. Meaning present versus controls present

### Episode meaning already present

The frozen 13-source package is not empty of meaning:

- Canvas: roles, buyer, costly problem, offer, acceptance event, workflow, human/AI split,
  economics, unknowns, risks, and the visual-truth boundary
  (`operator-canvas.md:17-139`, `156-253`, `255-274`).
- Narrative spine: viewer movement, reveal order, causal chain, evidence placement, counterargument,
  mechanism callback, and ending (`narrative-spine.md:17-127`).
- Claims map: exact qualifications and prohibited inferences, including the excluded multiple-uplift,
  causal-sale, typical-fee, named-state, and host-experience claims (`claims-map.md:15-46`).
- Script, beat sheet, canonical W, transcript, and pause map: exact spoken content and legacy timing.

The unique performance handoff adds consequential direction that the 13-source route does not
explicitly carry: S00's pause is the beat, S01 is silent, the incumbent case must sound fair, the
economics is slow and each conclusion should sit, and the ending is a recommendation rather than a
flourish (`01-editorial/narration-handoff.md:28-49`).

### Step 3 controls already present

The v0.4 candidate already controls important failure modes:

- one substantive `unit_job` per unit;
- separate visual-world and picture/audio axes;
- narrator/language-carrier/visible-speech/mute expectations;
- exactly one business-operation or establishment binding;
- separate business-state and viewer-state domains;
- evidence-label preservation;
- exclusion of the returned v0.3 pilot and prior generation/edit choices; and
- no shot direction, physical performance, generator prompt, runtime choice, or episode approval in
  Step 3 (`PROCESS-MANIFEST.json:52-68`; `FILM-LAYER-AMENDMENT.md:117-130`).

Therefore the problem is not "add more cinematic rules." It is: make the locked meaning and
receiving limits explicit at the right gate, then test comprehension before downstream production.

### Proven contract gap: `camera_anchor`

The approved Step 3 scope says the persistent world defines camera anchors and every V4 unit records
one (`03-visual-translation/SCOPE-BOUNDARY.md:16-27`). The base standard and V4 gate repeat the
requirement (`VISUAL-TRANSLATION-STANDARD.md:116-137`;
`STAGE-GATES.md:104-124`). v0.4 says all v0.3 conditions remain unless explicitly superseded
(`FILM-LAYER-AMENDMENT.md:8-10`) and correctly leaves actual camera position, framing, lens, and
movement to Step 4 (`FILM-LAYER-AMENDMENT.md:117-127`).

But the v0.4 V4 table omits `camera_anchor` (`03-visual-translation-v0.4/04-VISUAL-PLAN.template.md:7-15`),
and its V4 validator does not check it (`fixtures/validate.py:355-399`). This is a
contract/template/validator mismatch, not permission for a prompt to invent a new field or for Step
4 to invent the semantic viewpoint. Candidate process authority must resolve it before V4.

## 4. Current authority and stale routing

The current Step 3 episode manifest is precise:

- process v0.4 is proposed, mechanically tested, and not approved;
- V1 is a mechanically verified candidate awaiting process authority;
- V2–V7 are not started; and
- Step 4 is not authorized.

Source: `03-visual-translation/EPISODE-REVIEW-MANIFEST.json:7-32`. The process manifest independently
says "not approved and not authority" at `03-visual-translation-v0.4/PROCESS-MANIFEST.json:1-7`.
Consequently, neither this audit nor a passing V1 hash check may claim `inputs_locked` as a current
production gate.

Three routing documents are stale relative to those newer records:

- EP007 root README says Step 1 is in progress, Step 2 not started, and no Step 3 process exists
  (`episodes/EP007-exit-readiness-prep/README.md:9-18`).
- shared Step 2 README says no V2 episode exists (`02-narration-production/README.md:12-15`).
- Step 3 scope says EP007 N5–N7 are open and no transcript exists
  (`03-visual-translation/SCOPE-BOUNDARY.md:95-101`).

They should not be used as current episode status. This audit did not rewrite them.

## 5. Proposed prompt-pack review

Reviewed snapshot:

- `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/prompt-handoff-review/PROMPTS.md`
- SHA-256: `9aa1faac090346bf65616dba3f776c5312080cbade6e46fd1bbcecda1d1c6a5a`

Verdict: **fit as an isolated proposed review aid; not production authority.** It now addresses the
material audit gaps without rewriting frozen manifests:

- protects meaning/reveal order and separates facts, authored representation, unknowns, viewer
  knowledge, and business state (`PROMPTS.md:18-48`);
- assigns episode meaning to Step 1 and visual semantics/mark-making to Boundary Ledger
  (`PROMPTS.md:50-54`);
- prohibits media generation, master changes, implementation, and gate advancement
  (`PROMPTS.md:61-64`);
- requires the 13-file, E6, and N7 hash inventories; separates current Step 2 validator
  compatibility from byte integrity; and identifies the additional performance reference as
  unfrozen (`PROMPTS.md:68-85`);
- explicitly inventories missing shared-handoff fields, independent-listen status, 16-bit/24-bit
  mismatch, legacy transcript incompatibility, and current authority (`PROMPTS.md:87-117`);
- requires explicit v0.4 approval plus a recorded V1 pass before V2 and retains V2/V3 stops
  (`PROMPTS.md:119-136`);
- stops on the camera-anchor discrepancy rather than silently omitting or inventing it
  (`PROMPTS.md:138-154`); and
- keeps V5/V6 direction separate from Step 4 shots/prompts/runtime and V7 as a future separately
  approved lock.

The accompanying `EP007-BEAT-INTENT.md` maps all 27 script sections and preserves opening,
mechanism, economics, ending, exact W spans, pause authority, and prohibited implications. Its
status line correctly calls it an authored review aid, not an approved engine, V4 plan, or shot
board. `verify-handoff.mjs` passes, but by its own output and `PROMPTS.md:8-10` it cannot judge
meaning or create approval.

No remaining prompt-language defect found in this frozen snapshot changes the conclusion. The pack
can expose the upstream gaps; it cannot resolve them, accept the handoff, approve v0.4, or pass V1.

## 6. Blueprint Cinema work-order routing failure

This issued work order is not valid under the current Blueprint Cinema runtime namespace:

- `blueprint-cinema/src/blueprint_cinema/paths.py:9-13` defines `BLUEPRINT_ROOT` as the
  `blueprint-cinema/` directory.
- `validation.py:1186-1204` requires owned output paths beginning
  `episodes/<folder>/agents/deliverables/<work-id>/` and resolves inputs under `BLUEPRINT_ROOT`.
- `validation.py:1220-1236` requires canonical episode/runtime/schema/renderer forbidden paths.

The issued order instead uses repository-root-prefixed input and output paths and omits the runtime's
canonical forbidden set (`work-order:7-12`, `35-50`). Direct semantic validation therefore reports:

- owned output escapes the isolated deliverable directory;
- all three inputs are missing under `BLUEPRINT_ROOT`; and
- the canonical forbidden paths are omitted.

The canonical Blueprint Cinema EP007 folder also has no `production-state.json`, so the production
CLI cannot establish the order's `required_gate: inputs_locked` precheck. No dispatcher was used.
No source copies, symlinks, schema edits, or fabricated production state were introduced to bypass
this. The report is delivered at the user-specified repository path, but the packet is marked
`partial` because current runtime acceptance is unavailable.

## 7. Required decisions before dependent visual production

1. Resolve Step 2 authority: independent-listen requirement, 16-bit versus 24-bit master contract,
   and legacy transcript compatibility. Do not silently waive, convert, or relabel.
2. Prepare and explicitly receive a complete Step 2 → Step 3 handoff. State every required field,
   including origin/disclosure, performance direction, qualifications, exact-screen constraints,
   audio limits, receiver, and acceptance. Decide whether/how the issued performance handoff enters
   the frozen route.
3. Approve or reject v0.4 as a process, then record a real V1 decision. Resolve the camera-anchor
   contract before V4.
4. Repair Blueprint Cinema work-order routing and establish canonical episode state separately;
   refresh stale status prose without rewriting frozen historical evidence.

Until those decisions exist, the defensible next artifact is the isolated prompt-review pack, not a
V2 engine, V4 plan, generation request, render, approval, or Step 4 handoff.

## Scope statement

This audit was read-only outside this deliverable directory. It made no network request, provider
call, synthetic generation, render, upload, external write, paid-service call, approval, canonical
state change, process-manifest edit, script edit, narration edit, or audio conversion.
