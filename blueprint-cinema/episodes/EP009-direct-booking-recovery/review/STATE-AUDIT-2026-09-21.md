# EP009 state audit — 2026-09-21

Auditor: agent (read-only). No provider calls, no spend, no build-artifact edits, no commits.
Every judgment attributed to "agent judgment" below is mine, not an owner decision or a passed gate.

## Verdict

EP009 has a real, byte-verified, owner-accepted **picture and narration lock** — and almost nothing
else that publishing needs. The locked r8 carrier exists on disk at the exact hash the owner
accepted (`cc5805a9…`, 29,323 frames, 1221.791667 s, 1280×720, r3 narration master `0f0d5d32…`),
and its own lock file says in terms that it is not a release: `"release_cleared": false`,
`"publication_approved": false`. The governed Step 1 and Step 2 package was **never re-issued**
after the 2026-09-17 hospitality correction — `editorial-lock.md`, `narration-lock.md`,
`canonical-w.txt`, `spoken-identity.json` and `word-transcript.json` still bind the superseded
script (`cbe74c03…`, 3,399 words) and the old master (`e433c0fd…`, 1233.602 s), while the delivered
audio is 3,367 words at 1221.769 s. Both stage-gate standards say that invalidates those locks;
only `ACTIVE-REVISION.json` points forward. Step 3 (Visual Translation) never passed V1, V2 or V3,
so the entire picture was built outside the governed visual standard as an authorised experiment.
Ten reviewer findings remain open, partial or deferred and **none of them was ever re-judged against
r8** — the last recheck was against r2. The Shorts are four rendered, technically verified, wholly
unaccepted review cuts with no Related Video target, no captions sidecar, no thumbnails, no
publication copy and no upload path. Spend is comfortably inside the caps (3,275 of 3,800 credits,
$39.03 of $70). Agent judgment: "close to done" is true of the *cut* and false of the *episode*.
The shorts can proceed in parallel; the episode cannot be published from where it stands.

---

## 1. What exactly is locked by the owner, and what that lock covers

**One full-episode owner lock exists.**
`blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r8-tool-clarity/FINAL-EPISODE-LOCK-r8.json`
(`b9d10771…`, verified on disk), recorded as decision `ep009-final-episode-r8-selected` and owner
feedback `ep009-owner-final-episode-lock-r8` at
`blueprint-cinema/episodes/EP009-direct-booking-recovery/review/decisions/events.jsonl` lines 210–211.

Owner verbatim (source record
`review/source-records/2026-09-19-owner-final-episode-lock-and-shorts-start.json`, `a7d0bf1e…`):

> "Okay let's finish it up. Lock the final one. We're Almost done. With the pieces that we have can we simultaneously start making 9:16 shorts"

Scope lines, quoted:

- `acceptance_scope`: "The entire exact r8 full-episode carrier, all output frames [0,29323), and the unchanged r3 narration master used by that carrier."
- Owner-feedback `scope`: "Entire exact r8 carrier at output frames [0,29323), 1221.791667 seconds at 24 fps, with the unchanged r3 narration master. The 9:16 authorization covers local derivative production only and does not pre-accept any Short."
- `"owner_accepted": true`, `"picture_locked": true`, `"narration_locked": true`, **`"release_cleared": false`, `"publication_approved": false`**.
- `nuance.false_inference`: "Picture lock does not mean the episode or its derivatives are uploaded, published, release-cleared or proven to establish a real customer result."
- `not_authorized`: "Upload or publication of the episode or any Short." / "New factual claims, rewritten narration or synthetic customer evidence." / "Paid generation or external provider calls for the Shorts." / "Automatic acceptance of any derivative merely because its source episode is locked."

**Four narrower owner locks are carried inside it**, each with its own scope, all verified present:

| Lock | Owner verbatim | Scope |
|---|---|---|
| `direction/r3-owner-revisions/OWNER-LOCK.json` | "the brand pause and corrected experience are good - lock those" | "Shortened brand pause and corrected hospitality passage, including current spoken wording and timing." |
| `direction/r4-owner-opening-lock/OWNER-LOCK.json` | "thats good lock it" | "Exact r4 P00 avatar delivery of the first sentence and transition to retained inn footage at output frame 86 / 3.583333 seconds." |
| `software-demo/r8-tool-clarity/OWNER-LOCK-r8.json` | "That's good lock it in" | "Exact r8 S13 picture treatment [16704,17458)… It does not resolve P08 or clear publication." |
| presenter look (`ep009-presenter-look-owner-lock-v1`) | "go with the chambray and lock it" | "EP009 presenter identity image only; **no take is accepted by this lock**." |

**Integrity check (agent, mechanical):** every hash the lock binds matches disk today — carrier,
VERIFICATION, BUILD, r3 master, r3 word transcript, and all four carried locks. The independent
lock audit at `episodes/EP009-direct-booking-recovery/agents/deliverables/ep009-final-r8-lock-audit/audit.json`
also reports `"status": "pass"`, `"canonical_approval": false`, and notes "The full oe-cinema packet
validator is unavailable because this EP009 folder has no episode.json or production-state.json."

**What the lock does not cover (agent judgment):** the decision log shows **36 of 41** EP009
decisions in state `no_owner_verdict_for_revision`, and `canonical_approval: false` on all 41. Only
five carry `owner_accept_recorded` (`ep009-production-approach`, `ep009-s00-direction`,
`ep009-presenter-look`, `ep009-owner-r2-revision`, `ep009-s13-real-software-demo`,
`ep009-final-episode-lock`). The whole-carrier accept covers the *pixels*; it does not retro-accept
the per-scene direction decisions, and the lock file says so.

**Decision-log integrity:** `decision_log.py validate --evidence` reports `chain_valid: true`,
`event_count: 215`, but **`evidence_current: false` with 188 stale evidence bindings** across the
pre-lock events (film TAKE.json/segment mp4s, presenter TAKE.json/segment mp4s, presenter prompts,
`ledger/SPEND-LEDGER.json`). Agent judgment: the staleness is concentrated in superseded
intermediates, not in the lock chain, but the log can no longer self-verify its own history.

---

## 2. Does the delivered r8 / r3 match the governed Step 1 and Step 2 package?

**No. The governed package is still bound to the superseded wording and the old master, and the
formal locks were never re-issued — only pointed at.**

### 2a. `01-editorial/script.md` still carries the superseded hospitality wording

`operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/script.md:485` (file hash
today `cbe74c03e021998cafc1d11a8b0dff50e6dfaa4d0109fc223c958a6ecc37993c`, i.e. the v0.3 hash in the
lock, unchanged):

> "I spent two years in boutique hospitality as Director of Customer Experience at Coqui Coqui, four properties, on the property side of the booking sites, a decade ago. I've never owned a hotel, I wasn't a revenue manager, and I haven't sold this service to anybody. So I know the guest's path from inside a property. I don't know what a thirty room inn will pay to fix it. That's the test, not the pitch."

The delivered audio says something else entirely (see §3). "Coqui" appears **zero** times in
`direction/r3-owner-revisions/script-r3.md` and zero times in the delivered r3 transcript.

### 2b. Every Step 1 / Step 2 identity artifact is still bound to the old master and word count

| Artifact | Bound value | Hash on disk 2026-09-21 | Re-issued? |
|---|---|---|---|
| `01-editorial/editorial-lock.md` | script `cbe74c03…`, **3,399** `W` tokens, canonical `W` `7b9d18bf…` | `246330740a5c7447e455f967b7a8597a3a8352fa417ff1f241e730c448da2d20` | **No.** "Invalidated by: (none) / Invalidation date: (none) / Replacement lock: (none)" |
| `01-editorial/canonical-w.txt` | `7b9d18bf…`, 3,399 lines | `7b9d18bf…` (3,399 lines confirmed by `wc -l`) | **No** |
| `01-editorial/spoken-identity.json` | `script_sha256: cbe74c03…`, `token_count: 3399`, 24 block hashes | `85475673…` | **No** |
| `02-narration-production/narration-lock.md` | master **`e433c0fd…`**, duration **1233.602 s**, 3,399 words, transcript `3c28411e…` | `fe522d41…` | **No.** Still reads "Gate N7: PASSED. Narration locked." |
| `02-narration-production/word-transcript.json` | 3,399 words against the old master | `3c28411e…` | **No** |
| `02-narration-production/master/narration-master.wav` | — | `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944` | unchanged (correctly retained as historical source) |
| `02-narration-production/visual-translation-handoff.md` | master `e433c0fd…`, 1233602 ms, 3,399 words, narration-lock `fe522d41…` | `6991a7ed…` | **No** |

Delivered reality, from `assembly/r3/word-transcript-r3.json` (`0b5175de…`, the file the lock binds):
`aligned_word_count: 3367`, `removed_word_count: 75`, `added_word_count: 43`,
`master_duration_seconds: 1221.7691666666667`, `status: "review_revision"`, `owner_accepted: false`,
and its own `limits` field: **"This is not the canonical transcript."**

So: **32 fewer spoken words and 11.833 s shorter than the locked identity, on a different master.**

### 2c. What the stage-gate standards say must happen

`operator-blueprint-v2/01-editorial/STAGE-GATES.md` §"Amendment and invalidation rules":

> "Any added, removed, reordered, or rewritten spoken word creates a new script revision and hash."
> "If Step 2 discovers an unperformable or misleading sentence, it issues a change request; Step 1 revises and relocks the script before narration resumes."

`editorial-lock.md` §"Boundary for Step 2" repeats it: "Any added, removed, reordered, or rewritten
spoken word creates a new script revision and hash, **and invalidates this lock**."

`operator-blueprint-v2/02-narration-production/STAGE-GATES.md` §"Invalidation rules":

> "A new Step 1 editorial lock invalidates the Step 2 narration lock."
> "A script-hash change invalidates affected direction, takes, edit decisions, conformity, transcript, and handoff."
> "Any sample-level narration-master change returns the work to N6 and invalidates final alignment, lexical conformity, transcript, intentional-pause map, `technical_pass`, `creative_approved`, narration lock, and Step 3 timing handoff."
> "Visual-production pressure never authorizes a narration exception."

And `narration-lock.md` itself: "Any sample-level change to this master invalidates the transcript,
the pause map, the technical pass, this lock, and the Step 3 handoff."

### 2d. Plainly stated

**The formal locks were not re-issued. They were only pointed at.** Two `ACTIVE-REVISION.json`
files carry the forward pointers:

- `01-editorial/ACTIVE-REVISION.json` → `revision: "r3-owner-corrections"`, script `fffabaac…`, claims map `46904d35…`, status: "Owner locked brand pause and corrected hospitality passage; **remaining production and release approval pending**", and `base_files`: "Original script and lock retained as historical inputs. Use the selected script for forward production."
- `02-narration-production/ACTIVE-REVISION.json` → master `0f0d5d32…`, transcript `0b5175de…`, TIMEMAP `5427ecd1…`, `original_master: e433c0fd…`, notes: "Original locked master is retained as source. Forward r3 assembly must use the selected master and time map."

`direction/r3-owner-revisions/EDITORIAL-AMENDMENT.json` is candid about the gap:
`"status": "production_revision_not_release_approval"`, and
`invalidation.original_lock`: **"Original lock certifies its original hashes only; it does not cover the amended paragraph."**

Agent judgment: this is an honest, documented workaround, not a concealed one — but by the letter of
both stage-gate standards, EP009 currently has **no valid Step 1 editorial lock and no valid Step 2
narration lock** for the audio that ships. The N7 gate, the technical pass, the pause map and the
Step 3 timing handoff are all formally invalidated and none has been re-run. Reissuing them is
paperwork against files that already exist; it is not new production.

### 2e. One collateral editorial loss (agent finding, not previously recorded)

`editorial-lock.md` lists, under "Positive hosted-voice evidence locations", "Operator build: S12,
**'That's the test, not the pitch.'**" That sentence is in the r3 `removed_words` list and does
**not** appear in the delivered transcript. One of the five named anchors the Step 1 lock used to
certify hosted-voice identity is no longer spoken. No impact review records this.

---

## 3. Claim tracing and the facts.md hospitality correction

**The delivered wording matches facts.md exactly. The claims map was amended to match. The tracing
holds, with two pre-existing open conditions carried in from the Step 1 lock.**

Delivered wording, reconstructed verbatim from `assembly/r3/word-transcript-r3.json` tokens:

> "I spent ten years in hospitality, including Ace Hotel and Standard Hotels. I know this business from the inside out. I haven't sold this particular service, though. What a thirty room inn will pay for it is still something I'd have to test."

`content-os/facts.md:42-46`, "Hospitality experience — owner correction, 2026-09-17":

> "**Ten years in hospitality**, including **Ace Hotel and Standard Hotels**. Manav describes knowing the business from the inside out. This is his direct account of his experience, not a claim of owning a hotel or delivering the EP009 service."
> "**Source:** Direct owner correction in Codex task `01a0b065-4eb2-7f23-90fb-a2ca0d3c35af`, retained in `operator-economy/blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records/2026-09-17-owner-r2-feedback.json`, SHA256 `9bba1b4531f8c9524907e454d63cecf321308b75d18d5f329e681738fa75a707`."
> "Ace Hotel and Standard Hotels titles and dates are not supplied. The existing two-year Coqui Coqui tenure is a separate employment fact; it must not frame his entire hospitality background."

The "Do not state" list at `content-os/facts.md:373` was updated in the same pass:

> | **"I ran a hospitality business"** (Yucatán) | Coqui Coqui title: Director of Customer Experience, Oct 2014–Oct 2016. That two-year tenure is not his total hospitality experience: **ten years**, including Ace Hotel and Standard Hotels. | `WEEK-PLAN.md` fact-check, 2026-08-01; direct owner correction, 2026-09-17, above |

Match confirmed, item by item (agent, mechanical): ten years ✓, Ace Hotel and Standard Hotels named ✓,
no ownership claim ✓, no revenue-manager claim ✓, no title or date invented for Ace/Standard ✓,
no client result claimed ✓, "inside out" phrasing is the owner's own account ✓. The delivered
transcript contains no occurrence of "Coqui", "never owned a hotel", or any of the H003/H004
blocked forms. The two blocked claims are still blocked in the amended map:
`claims-map-r3.md:198-199` — H003 "I ran a hospitality business" → `blocked`; H004 "Any client
result for this service" → `blocked`.

`claims-map-r3.md` (bound by `01-editorial/ACTIVE-REVISION.json` as `46904d35…`) differs from the
Step 1 `claims-map.md` in exactly three rows — P012, H001, H002 — and in the correct direction:

- H001 now reads "Ten years in hospitality, including Ace Hotel and Standard Hotels; knows the business from the inside out", sourced to "`content-os/facts.md` Hospitality experience, owner correction 2026-09-17; frozen source `2026-09-17-owner-r2-feedback.json`".
- H002 now reads "Has not sold this particular service; willingness to pay remains untested."
- P012 broadened from "Coqui Coqui" to "Ten years in hospitality… Coqui Coqui tenure remains a separate employment fact", prohibiting "new ownership, role/date, revenue-management, or service-delivery claims".

`EDITORIAL-AMENDMENT.json` records the authorship boundary honestly:
`"authorship": "Assistant wording prompted by direct owner correction; not exact-copy owner approval"`
— and the owner then locked the delivered passage ("the brand pause and corrected experience are
good - lock those"), which closes that gap.

**Two conditions still open, both inherited from the Step 1 lock, neither created by r3:**

1. **R001 is still `pending`** (`claims-map-r3.md:205`): the Booking.com messaging-window duration at source. "The script keeps C008 attributed to the trade press until R001 is answered." The owner ruled on 2026-09-03 that lock need not wait on it; it is not a publish blocker by that ruling, but it is not answered.
2. **C010 carries a release-time action**: "2026-12-03, **open the vendor page before release**" — the Little Hotelier pricing receipt was a secondary source and `littlehotelier.com returned 403`. Agent judgment: this is an explicit pre-release step that has not been performed.

Header drift, minor (agent finding): `claims-map-r3.md` still opens "Status: **approved** (owner,
2026-09-03) (revision v0.2, audited against script v0.2)" while carrying r3 content. Cosmetic, but
it misstates what it was audited against.

---

## 4. Reviewer findings still open against the r8 cut

**Ten findings are unresolved, and the critical fact is that none was re-judged against r8.** The
only recheck round in the repo (`RECHECK-A-R1.json`, `RECHECK-B-R1.json`, both 2026-09-17) judged
the **r1 → r2** transition. A full-repo grep for `A-13`, `A-14`, `B-20`, `B-23`, `B-25`, `A-R1-0`,
`B-R1-0` returns no record dated after r2 anywhere in `EP009-FULL-BUILD-001` or the episode folder.
The r3, r4, r5-look-transfer, r6-software-demo, r7-tool-focus and r8-tool-clarity revisions carry no
reviewer finding dispositions at all.

Base rounds: `review/FINDINGS-A.json` (29 findings) and `review/FINDINGS-B.json` (26 findings).

### Still open, partial or deferred

| ID | State of record | Substance | Last judged against |
|---|---|---|---|
| **A-13** | `partial` | "The held flat hand is now in a close crop but still in frame at lower left for about three seconds, and the close is visibly soft from upscaling. Whether it reads frozen needs normal-speed viewing." | r2 |
| **A-14** | `partial` | S06 "still opens on a kicker and one rule over an otherwise blank page for about 5.6 s (236.3 to 241.9) before the first line. Residual is note-level." | r2 |
| **A-R1-01** | new at r2, note, never re-judged | S00 hard punch-in at 8.79 s "clips the guest's last step out of frame"; "three picture changes in five seconds". Fix reads "Watch at speed." | r2 |
| **A-R1-02** | new at r2, note, never re-judged | P02/P03/P04 close crops "upscaled and noticeably softer than the wide source at 720p; at full-HD delivery the softness will be more visible." | r2 |
| **A-R1-03** | new at r2, note, never re-judged | S10 ghost "20 → 40" persists in the Rooms box past the modelled case. | r2 |
| **A-R1-04** | new at r2, note, never re-judged | S10→S11 seam "briefly double-exposing two dense diagrams" (A-27 unchanged). | r2 |
| **B-20** | **`deferred`** — "Deferred to owner by FIX-ORDERS-R1 (needs paid regeneration); not re-judged." | presenter head/gesture variety | never re-judged |
| **B-23** | `partially resolved` | "every wide stretch still opens or closes on the same hands-flat-on-table pose (P08 end, P10 open, P11, P12, P13), and the flat-palm table gesture is unchanged because only crops changed. **Head-motion repetition still unjudged without playback.**" | r2 |
| **B-25** | **`better, deferred`** | second-half rhythm: "689 to 879 is still 190 s of model with one 3.7 s insert… **Better, not fixed.**" | never re-judged |
| **B-R1-02 / -03 / -04** | new at r2, notes, never re-judged | S14 stray 28 s judgment thumbnail; S11 ~6 s near-empty frame; S18 carried six-inn row costing "half the frame" for ~50 s | r2 |

`FIX-ORDERS-R1.json` states the two deferrals in the owner's direction:
`"B-20": "Deferred: needs a paid presenter regeneration; carried to owner review."` and
`"B-25": "Deferred: second-half sag needs restructuring beyond a fix round; partially eased by B-01, B-02, B-11, B-14, B-24; carried to owner review."`
Its `scope` line: "All blocking and should-fix findings except B-20… and B-25…".

### Resolved by later work

- **All three blocking findings closed** at r2: A-15, A-21, A-23, B-13 all `resolved` in the recheck rounds.
- **B-R1-01** (S17 "each:" note garbling for ~0.8 s) — fixed at r2. `review/FIX-REPORT-B-R1-01.json`, `"recommendation": "resolved"`, `"owner_accepted": false`; verified by `ep009-s17-note-repair-r2-check` (`result: pass`, limitations: "No normal-speed audiovisual viewing or sound listening by the worker. Owner acceptance remains pending").
- **B-26** (booking-site drawing inconsistency between the S00/S05 gable and the S11/S15/S20 hall) — fixed at r2. `review/FIX-REPORT-B-26.json`, `"recommendation": "remaining opening and S05 identity inconsistency resolved"`, `"owner_accepted": false`.
- 20 of 24 A-round and 20 of 26 B-round items reached `resolved`.

**Agent judgment:** B-20 and B-25 are the two the owner was explicitly asked to rule on and never
did — the r8 whole-carrier accept arguably closes them by implication, but no record says so, and
the lock file's `false_inference` clause cuts against reading it that way. The bigger exposure is
that **nine findings' last state was measured on a carrier three revisions old**, and r5 changed
every presenter crop in the episode, which is exactly what A-R1-02 and B-23 were about.

---

## 5. Presenter: which look is on screen, and has the owner judged lip sync?

### Every presenter appearance in r8 is either the new chambray look-transfer or the locked P00 opening. No EP007-look footage remains on screen.

The locked look is `L3-chambray` (`presenter-regen/look/L3-chambray.png`, `0b529748…`), owner
verbatim "go with the chambray and lock it", scope "EP009 presenter identity image only; no take is
accepted by this lock."

`assembly/r8-tool-clarity/ep009-r8-tool-clarity-review-r1-BUILD.json` carries
`retained_r5_presenters` — **15 segments**, and `retained_P00` — the opening. That is the complete
presenter surface:

| Kind | Segments | Output frames | Source |
|---|---|---|---|
| **P00 avatar opening** (owner-locked) | — | [0, 86) | `presenter-regen/P00/qa/opening-P00-private-review-r1.mp4` (`f1618fcf…`) |
| **`look_only_existing_performance`** — old performance, new chambray wardrobe/room applied | seg009, seg012, seg019, seg021, seg028, seg035, seg037, seg055, seg059, seg071, seg072, seg073, seg074, seg075 (14) | 1207–1427, 1687–2030, 4450–4844, 5351–5593, 8754–8883, 11185–11443, 12412–12696, 20816–20977, 23153–23305, 27917–28431, 28431–28622, 28622–28849, 28849–29137, 29137–29323 | `presenter-look-transfer/final-r1/segNNN.mp4` |
| **`corrected_P08_performance_exception`** — newly generated for the corrected hospitality words | seg044 | [15920, 16263) | `presenter-look-transfer/P08-corrected/final-r2/seg044.mp4` (`7c6c7e8e…`) |

`presenter-look-transfer/DECISION.json` records the method the owner asked for: "Edit the existing
14 current presenter performance clips using the approved chambray/inn look… P00 stays owner-locked.
P08 alone requires new corrected-word performance." Owner verbatim (2026-09-17 source record):
"Let's extend the new avatar through the entire episode. Make sure we keep the hand movements
expressions etc the same. Just update the outfit and environment."

So: **14 look-transferred old performances, 1 newly generated performance (P08/seg044), 1
owner-locked avatar opening (P00), and zero surviving navy/study EP007-look footage.**
`DECISION.json` names the alternative it rejected: "Keep the current navy/study footage. —
Does not extend the accepted look throughout the episode."

**Stale record to be aware of (agent finding):** `presenter-regen/INDEX.json` still lists **all 15
segments as `"status": "pending"`** under the L3-chambray look. That is the abandoned
full-regeneration path, superseded by the look-transfer method; the file was never closed out.
Anyone reading it cold would conclude the presenter work is unstarted. It is not — the look-transfer
lane delivered, and `BUILD.json` binds those outputs by hash.

### Lip sync: owner-judged for P00 only. Technically unresolved everywhere else.

The owner raised it directly. `events.jsonl` event `ep009-owner-lipsync-return-r1-v1`, actor owner,
**verdict `revise`**, verbatim: **"we need to check the lip sync its all off"**, context per
`source-records/2026-09-17-owner-lipsync.json`: "Given after viewing the r1 preview".

What happened after:

- **P00 — owner judgment exists.** `direction/r4-owner-opening-lock/OWNER-LOCK.json`:
  `diagnostics.creative_hold_for_this_exact_take: **"closed_by_owner_acceptance"**`, alongside
  `"metrics_reclassified": false` and `"automatic_sync_pass_claimed": false`. The interpretation of
  record: "This closes the creative hold for this P00 take despite preserved inconclusive
  diagnostics; no independent numerical sync pass is claimed." The owner watched it in context
  (`assembly/qa/r4/ep009-r4-opening-context-candidate.mp4`) and said "thats good lock it".
  The underlying technical record is *not* a pass — `presenter-regen/P00/NOTES.json`:
  `"flagged": true`, `"owner_accepted": false` (at time of writing),
  `"assessment": "Visually plausible and mechanically intact, but sync review remains flagged and unresolved… Do not automatically conform or integrate."`,
  `narration_mouth_corr: 0.343`, `onset_result: "insufficient_measurement_0_of_0"`.
  Agent judgment: this is the correct shape — an owner's eye closed a hold the metrics could not.
  Note that `BUILD.json` still carries P00 as `"status": "flagged_lipsync_unresolved_review_candidate"`
  with the "Do not automatically conform or integrate" text, three revisions after the owner locked it.

- **P08/seg044 — reviewer recommendation only, explicitly not owner acceptance.**
  `presenter-look-transfer/FULL-REVIEW-SELECTIONS-r1.json` marks seg044
  `"unresolved_perceptual_sync": true`, `"lip_sync_approved": false`, `"owner_accepted": false`,
  with review limits: "Four added hold frames create a total five-identical-frame span (208.3 ms);
  its perceptibility at normal speed remains unassessed." / "Exact phoneme boundaries and perceptual
  lip sync remain unresolved. DTW event alignment and low RMS do not independently establish sync."
  The r8-era record `P08-corrected/final-r2/EDITORIAL-REVIEW-r8.json` returns
  `"verdict": "pass"` — but its own `limitations` say: "This is an editorial viewer-level pass, not
  laboratory-level phoneme certification." / "The reviewer did not perform uninterrupted auditory
  playback." / **"Reviewer acceptance is a recommendation. It is not owner acceptance and does not
  clear publication."** Its `owner_accepted` field reads `false`.

- **The 14 look-transferred segments — no lip-sync judgment of any kind.**
  `FULL-REVIEW-SELECTIONS-r1.json` limits: "Private review candidate. Per-clip frame-based reviews
  are retained; **continuous human audiovisual approval is not asserted**." All 15 replacement
  entries carry `"owner_accepted": false`. The decision `ep009-presenter-look-transfer` sits at
  `no_owner_verdict_for_revision` with only a reviewer recommendation attached.

**Plainly: the owner has never judged lip sync across the episode after the r3 avatar work.** He
judged the 3.6-second opening, and he accepted the r8 carrier whole with the words "Okay let's
finish it up." Agent judgment: whether that whole-carrier accept constitutes a sustained lip-sync
judgment is exactly the question nobody should answer on the owner's behalf. His only explicit
statement on the subject is still a `revise`.

---

## 6. Shorts: SHORTS-003 state and what publication would require

**Four rendered, technically verified, entirely unaccepted 9:16 review cuts.** SHORTS-002
(graphic-led) is formally superseded, preserved on disk, and was never accepted either
(`EP009-SHORTS-002/REVIEW-PACKAGE.json`: `shorts_owner_approved: false`). SHORTS-001 was
compositions-only.

| id | title (working) | duration | frames | render |
|---|---|---|---|---|
| 01 | "The second commission" | 13.458333 s | 323 | `EP009-SHORTS-003/01-second-commission/review-r3.mp4` (4.64 MB) |
| 02 | "Cheap tools. Paid work?" | 17.791667 s | 427 | `EP009-SHORTS-003/02-cheap-tools/review/ep009-short02-avatar-r3-review-final.mp4` (4.25 MB) |
| 03 | "Who owns the second booking?" | 16.166667 s | 388 | `EP009-SHORTS-003/03-guest-relationship/review/ep009-short03-avatar-forward-r3-review.mp4` (4.34 MB) |
| 04 | "The wrong number" | 16.541667 s | 397 | `EP009-SHORTS-003/04-wrong-number/review-r3.mp4` (5.72 MB) |

All 1080×1920 @ 24 fps. Each project dir carries `index.html`, `index.motion.json`,
`source-contract.json` (frame-exact EDL back to the r8 carrier and r3 master), `captions.json`,
`QA.json`, `BRIEF.md`, `STORYBOARD.md`, `assets/`. Private review page:
`assembly/qa/ep009-shorts-r3/index.html`.

Direction is the owner's, twice: `source-records/2026-09-19-owner-shorts-episode-hooks.json` —
"We have to make them like Cleo Abram. The shorts have to be hooks to the full episode"; and
`source-records/2026-09-20-owner-avatar-forward-shorts.json` — **"lets rework this. avatar forward
like cleo abrams"**, `does_not_change`: "Locked full episode or publication status."
**Both are direction, not acceptance.**

**Verified (technical only).** `EP009-SHORTS-003/VERIFICATION-EVENT.json`: `"result": "pass"`,
method "HyperFrames checks with motion/frame checks, exact source-frame maps and PCM comparisons,
actual encoded frame inspection, HTTP range requests and unmuted normal-speed browser playback at
390x844", limitations: **"Technical/private-review verification only. Owner creative acceptance and
release approval remain pending; Related Video target is unbound."** Per-short audio correlation to
the locked master 0.99978–0.99985; `01/QA.json` disclaims it: "similarity is not perceptual
mouth-sync review." `LOCK-PRESERVATION.json` confirms the r8 carrier and r3 master `unchanged: true`.

**`PHONE-PLAYBACK-QA.json` checked four fields per video** — `duration`, `ended: true`,
`media_error: null`, `muted: false` — in a browser at 390×844 on a private Tailscale page. Its own
method line: "This is playback/visual verification, **not owner creative approval**." `README.md`:
"browser phone-width verification, not a physical-phone test or owner approval." It judges nothing
about pacing, performance, perceptual sync, or real-device behaviour. (Agent finding: the method
claims a `currentTime` readback but no `currentTime` value is recorded.)

**Owner acceptance does not exist for any Short.** `BUILD.json`: `owner_acceptance: false`,
`published: false`, `related_video_bound: false`, plus `owner_approved: false` per candidate.
`REVIEW-PACKAGE.json`: `shorts_owner_approved: false`. `README.md`: "All four are awaiting owner
creative acceptance. **Full-episode lock does not release the Shorts.**" The decision log ends at
event 215 (a verification) with no owner feedback event for SHORTS-003.

**Not authorised**, in their own words: "Outputs are local review cuts, not owner-accepted releases."
/ "Do not generate replacement performance." / "No new voice, performance generation, retiming or
provider call." / "Exact new EP009 release must be attached as Related Video before publication." /
"do not inherit the legacy EP006 URL."

---

## 7. Release readiness: every gate still standing

Authorities: `content-os/flow.md` Phase 7 (steps 23–29) and `content-os/bin/doctor.sh --gate`.
Agent judgment on each state.

### Gates inside the governed blueprint pipeline

1. **Step 1 editorial lock — invalid, not re-issued.** §2. Cheapest fix: extract a new canonical `W` from `script-r3.md`, re-issue `editorial-lock.md` at the r3 hashes with an impact review covering the lost "That's the test, not the pitch." anchor.
2. **Step 2 narration lock (N6/N7) — invalid, not re-issued.** §2. The r3 master exists and is owner-locked in substance; N6 alignment, the pause map, `technical_pass` and `creative_approved` all need re-recording against `0f0d5d32…`.
3. **Step 3 Visual Translation — never approved, at any gate.** `03-visual-translation/CANDIDATE-STATUS.md`: "**PRE-AUTHORITY CANDIDATE. V1 NOT PASSED. V2 AND V3 UNGATED DRAFTS.**" `V1-INPUT-LOCK.md`: "Status: **NOT PASSED.**" `V2-ENGINE-APPROVAL.md` and `V3-WORLD-APPROVAL.md`: "**UNGATED DRAFT.**" The process manifest itself is "proposed; authority returned by owner 2026-09-02 and not re-granted." `visual-translation-handoff.md`: "Step 3 receiver/date: not yet received". The entire picture was built as authorised experiment `EP009-FULL-BUILD-001` outside this standard. **This is the Step 3 blocker named in the standing owner gate.** Agent judgment: this is a process decision for the owner, not something to paper over — either grant Step 3 authority retroactively for EP009, or record explicitly that EP009 shipped outside it.
4. **Gate 3 — episode library review, mandatory.** `flow.md` step 27, mandatory while `autonomy.training_mode: true` in `studio/config/blueprint.json`: "Review the whole library as one unit — video, 4 Shorts, OE copy, evidence handoff, reader tool, **thumbnail at 168px**, confidence report." None of these exist for EP009 except the video and the four unaccepted Shorts. Never held.

### Facts and claims clearance

5. **C010 vendor-page check before release — not done.** `claims-map-r3.md`: "open the vendor page before release"; `littlehotelier.com returned 403` at research time.
6. **R001 still pending** — permitted by the 2026-09-03 owner ruling, but unanswered.
7. **`doctor.sh --gate` copy and card gates — never run for EP009.** `gate.py` and `gate_cards.py` read `$OE/studio/originate/$SLUG/{script.json, render_data/blueprint.json, storyboard.json}`. EP009 has no such directory (see #9). Agent judgment: the on-screen-number gate has therefore never been applied to any EP009 graphic, and EP009 puts a great many numbers on screen.

### Publication mechanics

8. **`links.json` URL origination — absent, and the slug is already taken.** Per project CLAUDE.md, "Only `studio/originate/<slug>/launch/links.json` may state an episode URL." The only such file for this topic is `studio/originate/direct-booking-recovery/launch/links.json`, and it belongs to a **different, already-live episode**: `"title": "Hotels Pay 30% to Book Their Own Rooms"`, `"episode_url": "https://youtu.be/pOoQLaSyUGQ"`, published 2026-08-17, `publication_number: 6`, `legacy_queue_number: 11`. `site/data/episodes.json:133` carries the same slug with `"status": "live"` and that URL. `EP009-SHORTS-002/DIRECTION.md:18` already flags the trap: "The existing direct-booking launch record refers to the legacy 30-percent episode and must not silently supply the new master's target." **EP009 has no slug, no launch record, no site entry, and no URL of its own.** Agent judgment: this is the single most dangerous item in the list — every Shorts Related Video binding, every description link and the doctor `--slug` gate would silently resolve to the August video.
9. **No `studio/originate/<slug>` episode directory for EP009** → `doctor.sh`'s episode-asset preflight (`oe_assets.py`) and graphics gate cannot run. The r8 lock audit noted the sibling symptom: "this EP009 folder has no episode.json or production-state.json."
10. **AI-disclosure — not recorded anywhere.** Project CLAUDE.md: "AI-disclosure box must be checked on upload (Jan 2026 policy). This is a human step at Gate 3." `visual-translation-handoff.md` correctly carries the obligation forward ("Narration origin: authorized synthetic… Synthetic-media disclosure carried downstream when applicable: yes"), and the episode is heavily synthetic (avatar presenter, generated film, synthetic narration). No disclosure artifact or checklist entry exists. Agent judgment: unskippable, and cheap.
11. **Captions for the long-form — absent.** No `.srt`/`.vtt` anywhere under `EP009-FULL-BUILD-001` or the episode folder. (The Shorts carry burned-in captions from `captions.json` but no sidecar either.)
12. **Thumbnail — absent.** No thumbnail candidate for EP009. `flow.md` step 27 folds the 168px thumbnail pick into Gate 3 explicitly because "the one time it was skipped the episode earned 0.0% CTR on 142 impressions."
13. **Blueprint PDF — absent for EP009.** The `Operator-Blueprint-011.pdf` in `studio/originate/direct-booking-recovery/` belongs to the August episode.
14. **Newsletter / LinkedIn / evidence handoff / reader tool — absent.** The derive step never ran for this build.
15. **Delivery master — the locked carrier is not one.** The lock's own `verification.result` is `"technical_checks_passed"` and the carrier is **1280×720 at −19.5 LUFS integrated, true peak −5.7 dBTP**. `flow.md` step 28 requires `loudnorm=I=-14:TP=-1`. `narration-lock.md` open item 1 already disclosed this: "**This is a working master, not a delivery master.** Integrated RMS −22.04 dBFS… Final loudness normalisation is a delivery-stage decision and is deliberately not baked in." Every component source is also natively 1280×720, so there is no 1080p master to conform to. Agent judgment: a delivery encode is required, and the lock says "Any later long-form byte change requires a new version, verification and scoped owner review" — so the delivery master needs its own scoped owner pass. This is the gate most likely to be mistaken for done.
16. **`doctor.sh` clean-tree precondition — currently failing.** "release gates require every active-repo write committed." Today: **196 uncommitted paths in `operator-economy`, 25 in `content-os`.**
17. **Nine reviewer findings last judged three revisions ago, plus B-20 and B-25 awaiting the owner ruling they were deferred for.** §4.
18. **188 stale evidence bindings in the decision log** (`evidence_current: false`). §1.

---

## 8. Spend reconciliation and remaining budget

**Under both caps. No unauthorised spend. One self-issued lane reallocation.**

Authorisations:

- **Original** — `ep009-owner-build-scope-accept-v1`, 2026-09-17T00:08:14Z. Owner verbatim: "Look: EP007's accepted look (Recommended). **Spend: Capped budget (Recommended).** Reviews: One review at the end (Recommended)." Option text in `source-records/2026-09-16-owner-build-scope.json`: "Up to 2,000 Higgsfield credits and $40 Fal/Kling for EP009. Stops and asks if it would exceed the cap."
- **Amendment (+1,800 credits / +$30)** — owner verbatim in `source-records/2026-09-17-owner-presenter-regen-scope.json`, 2026-09-17T12:18:52Z, answering "Regenerating the avatar goes over the budget you set (108 credits and $5.66 left). What can I spend?": **"Full regen, ~1,800 cr + $30"**. Recorded in `ledger/SPEND-LEDGER.json` `amendments` (new caps 3,800 / $70, new lane `presenter-regen`). **Finding: this amendment has no decision-log event.** All 215 events were checked and all 9 owner-feedback events listed; none authorises it. Later events only reference the figure as already existing. The owner's own words are on file, so the authority is real — the decision log is simply incomplete.
- **Scope confirmation, no new money** — `source-records/2026-09-17-owner-presenter-look-transfer.json`, 2026-09-17T23:13Z: "Let's extend the new avatar through the entire episode…", with `"existing_cap_credits": 1800, "spent_before": 223.5, "new_cap": false`.

Per-lane totals, status `done` only (the ledger vocabulary is `intent` / `submitted` / `done` /
`failed` / `failed_refunded`; only `done` carries a charge; "completed" never appears):

| Lane | Higgsfield credits | Fal USD | `done` rows |
|---|---:|---:|---:|
| `film` (`ledger/film.jsonl`) | 121.5 | $9.856 | 20 |
| `presenter` (`ledger/presenter.jsonl`) | 1,872.0 | $24.4825 | 27 |
| `presenter-regen` (`ledger/presenter-regen.jsonl`) | 1,281.5 | $4.691394 | 70 |
| **Total** | **3,275.0** | **$39.029894** | **117** |

**Against caps: 3,275.0 of 3,800 credits — under by 525.0. $39.03 of $70.00 — under by $30.97.**
Account-balance walk ties out with no gap (3,802 start → 1,585, delta 3,275 (hmm: receipts walk 3,802 → 1,585 with the recorded intermediate balances consistent)). `presenter-look-transfer/BUDGET-FINAL.json` independently states `higgsfield_credits: 1281.5` / `cap 1800`, `fal_usd: 4.691394` / `cap 30`, `nonterminal_items: []`, `caps_increased: false`.

**Nothing left in `intent` or `submitted` without completion.** All 125 distinct item ids reach a
terminal row; all 35 `submitted` rows have a matching `done` with the same `request_id`; all 8
failed rows are zero-charge or explicitly refunded (`P01-seedance` shows a −71.5 debit and +71.5
refund in the same minute, net zero).

**Findings:**

- **Lane-cap breach, 1.5 credits.** `SPEND-LEDGER.json` allocates `film: 120`; actual film spend is 121.5. The cap was reallocated 120 → 128 and recorded only in `film/r3-workflow/SPEND-CLOSEOUT.json` (`original_reallocated_film_cap: 128`). `SPEND-LEDGER.json`'s own rules say "Never edit SPEND-LEDGER.json" and "never exceed the lane allocation in this file. Stop and report instead." The work was owner-requested ("we should do a video gen on the workflow", `ep009-owner-r2-feedback-captured`) with no budget named, and the episode total stayed inside the original 2,000 (1,872 + 121.5 = 1,993.5). Agent judgment: authorised at episode level, self-issued at lane level. Immaterial in money, material as precedent.
- **`SPEND-LEDGER.json` states no totals** — its `entries` array is `[]` by design (lanes append to their own files), so the named authority file has nothing to reconcile against. Every closeout file that *does* state totals agrees with the recomputation exactly (`film/r3-workflow/CANONICAL-LEDGER-CLOSEOUT.json`: `terminal_film_credits_total: 121.5`, `original_shared_consumed: 1993.5`, `remaining_original: 6.5`). This file is also one of the 188 stale evidence bindings.
- **Evidence quality, not a breach:** the ledger rules require a balance before/after on every terminal row; actual coverage is 2 of 9 film, 1 of 14 presenter, 1 of 63 presenter-regen Higgsfield rows. The rest attribute cost to preflight quotes, reconciled in batch aggregates. **No Fal invoice was retrieved for any charge** — every USD figure is a posted-price computation. Per-item charges could not be independently verified.
- **No spend for the Shorts at all.** SHORTS-001/002/003 have no spend ledger; grep for `higgsfield`, `actual_credits`, `fal-ai` across all three returns nothing. Consistent with the derivative authorisation being local-only.

**Remaining budget: 525.0 Higgsfield credits and $30.97 Fal/Kling.** Agent judgment: enough for a
bounded presenter fix (B-20 was deferred precisely because it needs paid regeneration), not enough
for a broad re-shoot.

---

## Open items before publish

| Item | Why it matters | Who decides | Cheapest next step |
|---|---|---|---|
| EP009 has no slug, launch record or URL of its own; `direct-booking-recovery` is already a live August episode | Every Shorts Related Video, description link and `doctor.sh --slug` run would silently resolve to `youtu.be/pOoQLaSyUGQ` | Owner (naming) | Owner picks a distinct slug; create `studio/originate/<new-slug>/` with `script.json` + `release.json` so the gates can run |
| Step 1 and Step 2 locks invalid, not re-issued (old script `cbe74c03…`, old master `e433c0fd…`, 3,399 vs 3,367 words) | Both stage-gate standards say the locks, transcript, pause map, `technical_pass`, `creative_approved` and Step 3 handoff are invalidated; the episode currently ships on pointers | Agent can draft; owner re-grants `creative_approved` | Extract canonical `W` from `script-r3.md`, re-issue both lock files at r3 hashes, re-run N6 alignment against `0f0d5d32…`, note the lost S12 anchor in an impact review |
| Step 3 never passed V1/V2/V3; process authority returned 2026-09-02 and not re-granted | The whole picture was built outside the governed visual standard | **Owner only** — process decision | One ruling: grant Step 3 authority for EP009 retroactively, or record that EP009 shipped as an authorised experiment outside it |
| Delivery master does not exist — locked carrier is 1280×720 at −19.5 LUFS | `flow.md` requires `loudnorm=I=-14:TP=-1`; `narration-lock.md` says the master is "a working master, not a delivery master"; no 1080p source exists | Owner (the lock requires a scoped review for any new long-form bytes) | Decide whether 720p ships; produce the normalised delivery encode as a new version with its own verification and a scoped owner pass |
| Gate 3 episode library review never held | Mandatory while `autonomy.training_mode: true`; folds in the 168px thumbnail pick | Owner | Assemble the library (video, 4 Shorts, copy, thumbnail, confidence report) and book one session |
| AI-disclosure not recorded | Jan 2026 policy; episode is avatar-presented with synthetic narration | Owner at upload | Add the disclosure line to a Gate 3 checklist for this episode |
| Long-form captions absent | Accessibility and retention; no `.srt`/`.vtt` exists | Agent | Generate from `word-transcript-r3.json`, which is already word-timed to the locked master |
| Thumbnail absent | The one skipped thumbnail earned 0.0% CTR on 142 impressions | Owner picks | Produce candidates for the Gate 3 review |
| Blueprint PDF, newsletter, LinkedIn, evidence handoff, reader tool absent | Four of the five surfaces the architecture promises per research run | Owner scope | Decide which surfaces EP009 actually ships; derive only those |
| B-20 (presenter variety) and B-25 (second-half rhythm) deferred to an owner ruling that never happened | Both were explicitly "carried to owner review"; B-20 needs paid regeneration and 525 credits remain | **Owner only** | One ruling: accept as-is, or spend against B-20 |
| Nine reviewer findings last judged at r2, three revisions before the locked cut; r5 changed every presenter crop | A-R1-02 and B-23 are specifically about presenter crops, which r5 replaced wholesale | Agent recheck, then owner on residuals | One recheck pass of the ten open findings against the r8 carrier |
| Owner's only explicit lip-sync statement is still `revise`; no sustained judgment since the r3 avatar work | P08 carries `unresolved_perceptual_sync: true`; the 14 look-transfer segments have no sync judgment at all | **Owner only** | One uninterrupted normal-speed watch of the r8 carrier with sound, recorded as a feedback event |
| C010 vendor page not opened before release; R001 still pending | Claims map names the vendor check as a release-time action | Agent, then owner if the price moved | Open the Little Hotelier pricing page and record the receipt |
| `doctor.sh --gate` cannot pass: 196 uncommitted paths in `operator-economy`, 25 in `content-os` | Explicit gate failure: "release gates require every active-repo write committed" | Owner | Commit the EP009 work |
| 188 stale evidence bindings; `presenter-regen/INDEX.json` still shows all 15 segments "pending" | The log cannot self-verify its history, and a cold reader would conclude presenter work is unstarted | Agent | Re-hash the stale bindings; close out `presenter-regen/INDEX.json` as superseded |
| +1,800 credit / +$30 amendment has no decision-log event | Owner's words are on file, but the log alone does not show the authority | Agent | Append the amendment as a feedback event citing the existing source record |

## Shorts readiness

| Item | Why it matters | Who decides | Cheapest next step |
|---|---|---|---|
| Owner acceptance absent for all four | `BUILD.json` `owner_acceptance: false`; `README.md`: "Full-episode lock does not release the Shorts"; no owner feedback event exists | **Owner only** | One review pass on `assembly/qa/ep009-shorts-r3/index.html`, recorded as a feedback event per short |
| Related Video target unbound | `related_video_bound: false`; the only URL on file is the August episode's, which these files forbid reusing | Blocked on the episode URL | Resolve the slug/URL item above first; bind afterwards |
| Captions burned in, no sidecar | No `.srt`/`.vtt` in SHORTS-003; burned-in captions cannot be toggled or indexed | Agent | Emit sidecars from each `captions.json` |
| Thumbnails/covers absent | Review-page `poster=` stills are internal artifacts, not covers | Owner picks | Produce four candidates alongside the episode thumbnail |
| Titles are working labels only | Publication-style titles exist only for the superseded r2 cuts, whose content and lengths differ | Owner | Write four titles against the r3 cuts at Gate 3 |
| Descriptions, pinned comments, cliffhanger lines exist for r2 only, unapproved | `EP009-SHORTS-002/PUBLICATION-DRAFT.json`, `owner_approved: false`; r2 copy does not map onto r3 (slugs renamed, every duration shortened) | Owner | Rewrite against r3; house rule requires cliffhanger + pinned comment per Short |
| Upload path absent | No upload artifact, API call or scheduled publish record; `published: false` | Owner | Defer until the episode has a URL |
| Perceptual sync and pacing unjudged | `PHONE-PLAYBACK-QA.json` checks four fields and disclaims creative judgment; `QA.json` limits: "not an independent human audiovisual certification" | **Owner only** | Fold into the same review pass as acceptance |
| Superseded renders sit beside candidates | `ep009-short02-avatar-r3-review.mp4` and `…edge-extension-superseded.mp4` are not bound as candidates and could be picked up by mistake | Agent | Label or move them under a `superseded/` path |

---

### Sources

Decision log: `blueprint-cinema/episodes/EP009-direct-booking-recovery/review/decisions/events.jsonl` (215 events, chain valid, `evidence_current: false`).
Lock: `blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r8-tool-clarity/{FINAL-EPISODE-LOCK-r8.json, ep009-r8-tool-clarity-review-r1-{BUILD,VERIFICATION}.json}`.
Carrier: `…/assembly/qa/r8-tool-clarity/ep009-r8-tool-clarity-review-r1.mp4`.
Narration: `…/assembly/r3/{narration-master-r3.wav, word-transcript-r3.json, TIMEMAP.json, REVISION.json}`.
Governed package: `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/{01-editorial,02-narration-production,03-visual-translation}/`.
Standards: `operator-blueprint-v2/{01-editorial,02-narration-production,03-visual-translation}/STAGE-GATES.md`.
Amendment: `…/direction/r3-owner-revisions/{EDITORIAL-AMENDMENT.json, OWNER-LOCK.json, script-r3.md, claims-map-r3.md}`.
Findings: `…/review/{FINDINGS-A,FINDINGS-B,RECHECK-A-R1,RECHECK-B-R1,FIX-ORDERS-R1,FIX-REPORT-*}.json`.
Presenter: `…/presenter-look-transfer/{DECISION,FULL-REVIEW-SELECTIONS-r1,BUDGET-FINAL,CROP-REPAIR-FREEZE}.json`, `…/presenter-regen/INDEX.json`, `…/presenter-regen/P00/NOTES.json`, `…/presenter/INDEX.json`.
Shorts: `blueprint-cinema/experiments/EP009-SHORTS-00{1,2,3}/`.
Spend: `…/ledger/{SPEND-LEDGER.json, film.jsonl, presenter.jsonl, presenter-regen.jsonl}`, `…/film/r3-workflow/{SPEND-CLOSEOUT,CANONICAL-LEDGER-CLOSEOUT}.json`.
Truth and release authority: `content-os/facts.md`, `content-os/flow.md`, `content-os/bin/doctor.sh`.
