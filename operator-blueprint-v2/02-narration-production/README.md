# Step 2: Narration Production

Status: **approved production authority**, locked 2026-09-01. Amended 2026-09-02 with the N4B and
N6 completeness contract, after an owner listen on EP007 found nine of twenty-four chunks ending
mid-word while every automated conformity check reported clean. The narration method is the two-stage
acted-guide chain frozen as `n3-two-stage-acted-guide-v2`: Google `gemini-2.5-pro-tts` (voice
`Algieba`) performs the locked words under the candidate-C4 method-level register, and ElevenLabs
Voice Changer `eleven_multilingual_sts_v2` transfers that performance onto Original C
`scMbPZwQjr40V1MzL3Nj`. N3 and N4A both passed on the AI Visibility v1.1 fixture. The v0.2 through
v0.4 records remain frozen history.

N4B full capture is **not** authorized by this lock. It requires a current Step 1 editorial lock for
a real episode plus its own separate bounded authorization. No V2 episode exists yet.

Step 2 turns the exact, owner-approved Step 1 script into the final spoken spine of the episode. It controls performance direction, narrator and capture consistency, takes, pickups, dialogue editing, lexical conformity, the clean narration master, word-level timing, and the handoff to visual translation.

It does not rewrite the episode or start visual production.

## Entry condition

Step 2 may start only for a real numbered V2 episode with:

- a current Step 1 editorial lock;
- a current narration handoff;
- a current editorial-voice conformity report tied to the locked script;
- matching locked package and live-authority hashes;
- the Step 1 v1.5 ordered, whitespace-delimited spoken-token identity reproduced under
  `oe-spoken-text-v1`;
- no unresolved editorial, evidence, legal, permission, or owner blocker; and
- documented authorization for the chosen human or synthetic narrator.

The current upstream authority is
[`../01-editorial/STEP1-v1.5-APPROVAL.md`](../01-editorial/STEP1-v1.5-APPROVAL.md). The approved AI
Visibility v1.1 package may enter N1 as a narration-system fixture only. It has no episode number,
public-fact clearance, visual authorization, or release authority. Workflow Operations is retained
as historical evidence and is expected to fail N1 because it does not have a current Step 1 v1.5
lock and ready narration handoff.

Fixtures may test the system without creating an episode. They are never production approvals.

## Current fixture decision

The retained AI Visibility v1.1 N4A batch remains a **technical PASS** and owner **creative
REVISE**. V0.3's Hume clone-plus-description challenger was stopped before upload by its model and
clone incompatibility. V0.4 then preserved the owner-selected Original C identity and technically
captured two direct Eleven v3 P01 candidates. The owner rejected both as flat, with no inflection or
emotion. No candidate is selected and no prior authorization can be replayed.

V0.5 tests a materially different acting layer without changing the locked script or Original C:
first generate two directed Gemini guide performances for exact `W[30,110)`, then, only after guide
QA and an explicit owner selection, consider one separately authorized ElevenLabs Voice Changer
transfer into Original C. The Google and Eleven actions are independent authority gates. The
Eleven action remains blocked until an exact selected guide, rights, data-use protection, and a new
authorization exist. See
[`STEP2-v0.5-CHANGE-PROPOSAL.md`](STEP2-v0.5-CHANGE-PROPOSAL.md) and the
[`v0.5 fixture`](fixtures/step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest/).

Both G1 and recovery G1R1 are now consumed after one candidate-A HTTP `403` each; neither produced
audio or called candidate B. G1R1 verified the exact temporary role before the request and its
removal afterward. The actual Google rejection cause remains unknown, and V1 stays blocked.

This is a method microtest, not another N4A. A passing short transfer would authorize nothing by
itself; it could only support a later owner decision about a separately authorized long-form and
pickup test.

## Production flow

```text
locked editorial handoff
→ handoff verification
→ performance direction and provider-agnostic performance envelope
→ when the current method is unapproved: original-sample provenance gate
→ when one source cannot be selected from metadata: exact named-sample local review
→ four separately authorized short-bakeoff actions
→ blind short scoring
→ separately authorized long-form continuity and pickup test for eligible methods
→ owner provider-method selection
→ N3 narrator identity and acquisition configuration freeze
→ separately authorized N4A calibration, diagnostics, and owner approval
→ separately authorized N4B full capture and interim diagnostics
→ selects and pickups
→ narration edit
→ freeze one narration-master candidate
→ final-master alignment, lexical conformity, word transcript, pause map, and technical QC
→ technical_pass
→ independent eyes-closed listen and owner creative decision
→ creative_approved
→ narration lock
→ Step 3 handoff
```

This remains the target flow. The frozen v0.3 Hume branch stays suspended by its recorded
vendor-drift stop; it may not advance merely because the remaining generic flow is documented.

The isolated v0.5 method subloop is stricter: exact plan and dry run, separate `AUTH-G1`, guide
capture and QA, explicit owner selection, then a newly compiled exact-guide transfer, verified
Eleven no-training or ZRM state, and separate `AUTH-V1`. A failed guide stops before Eleven. A
failed transfer stops before any settings iteration or long-form work.

Interim ASR may flag likely mistakes in calibration, takes, chunks, and pickups. It is diagnostic
only. The authoritative transcript and pause map are derived from the exact final master candidate.
Any sample-level master change invalidates those artifacts and every later decision.

## Required outputs

A complete Step 2 package contains:

- verified editorial handoff checklist;
- performance-direction brief;
- provider-agnostic performance envelope;
- approved narrator profile or an explicitly authorized episode-specific narrator identity;
- voice-and-capture lock;
- machine-validatable calibration and full-capture plans;
- separate provider-call authorization for calibration and full capture, when applicable;
- calibration and full-capture reviews;
- documented native acquisition format and separate delivery-master format;
- immutable raw-take register with file hashes;
- take reviews and select decisions;
- pickup log;
- narration edit decision list;
- clean narration master: PCM WAV, 48 kHz, 24-bit, mono;
- optional review MP3, clearly marked non-master;
- source-format conversion record when acquisition is not already the delivery format;
- lexical-conformity report against the locked script;
- word-level transcript timed from the final narration master;
- intentional-pause map bound to the same final narration master;
- technical measurements and independent-listener review;
- narration-state record showing separate technical and creative decisions;
- narration lock; and
- visual-translation handoff.

When provider selection is unresolved, the package additionally requires the sample-provenance,
authorization, blind-score, long-form/pickup, and method-selection records in
[`TOOL-AUDIT-AND-BAKEOFF.md`](TOOL-AUDIT-AND-BAKEOFF.md). A provider-method selection is an N3 input,
not an N4A creative pass or narration lock.

The proposed v0.3 record set is:

- [`02-direction/PERFORMANCE-ENVELOPE.template.md`](02-direction/PERFORMANCE-ENVELOPE.template.md);
- [`02-direction/ORIGINAL-SAMPLE-PROVENANCE.template.md`](02-direction/ORIGINAL-SAMPLE-PROVENANCE.template.md);
- [`02-direction/PROVIDER-BAKEOFF-PLAN.template.md`](02-direction/PROVIDER-BAKEOFF-PLAN.template.md);
- [`02-direction/PROVIDER-BAKEOFF-AUTHORIZATION-REGISTER.template.md`](02-direction/PROVIDER-BAKEOFF-AUTHORIZATION-REGISTER.template.md);
- one separately approved record per initial scope from
  [`02-direction/PROVIDER-EXTERNAL-ACTION-AUTHORIZATION.template.md`](02-direction/PROVIDER-EXTERNAL-ACTION-AUTHORIZATION.template.md);
- one later eligible-method authorization from
  [`02-direction/LONG-FORM-AUTHORIZATION.template.md`](02-direction/LONG-FORM-AUTHORIZATION.template.md);
- one immutable blind sheet per scorer from
  [`03-takes/PROVIDER-BAKEOFF-SCORECARD.template.md`](03-takes/PROVIDER-BAKEOFF-SCORECARD.template.md);
- one separate unblinding and arithmetic record from
  [`03-takes/PROVIDER-BAKEOFF-CONSOLIDATION.template.md`](03-takes/PROVIDER-BAKEOFF-CONSOLIDATION.template.md);
- one signed long-form confirmation review per listener and advanced provider from
  [`03-takes/LONG-FORM-CONTINUITY-REVIEW.template.md`](03-takes/LONG-FORM-CONTINUITY-REVIEW.template.md); and
- the final N3 method decision in
  [`06-approval/PROVIDER-METHOD-SELECTION.template.md`](06-approval/PROVIDER-METHOD-SELECTION.template.md).

The isolated v0.5 record set adds:

- one `oe-performance-transfer-plan-v1` binding exact locked words, guide request, media policy,
  blocked transfer contract, and zero downstream authority;
- one `oe-synthetic-guide-authorization-v1` for Gemini guide generation only;
- one later `oe-voice-transfer-authorization-v1` for one exact selected guide only;
- for an exact active G1 only, immutable
  `authorizations/consumed/<authorization_id>.consumed.json` and exactly one
  `receipts/google/<authorization_id>.run.json` or
  `receipts/google/<authorization_id>.failure.json`, plus the two bound raw guide destinations;
- transfer raw-media receipts outside Git plus credential-free committed summaries;
- separate guide lexical/technical QA, guide performance review, owner guide selection, transfer
  lexical/identity/technical QA, and owner creative disposition; and
- a long-form/pickup authorization only if the short microtest passes and the owner separately
  chooses to continue.

Synthetic capture additionally follows
[`02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md`](02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md).
Machine-checkable identities, validation states, and exit semantics follow
[`CLI-VALIDATION-CONTRACT.md`](CLI-VALIDATION-CONTRACT.md).

The v0.3 CLI can validate the envelope, provider adapters, bakeoff plan, and action-authorization
shapes, then compile credential-free ElevenLabs and Hume dry runs. Its narrow read-only clients may
act only under a separately approved authorization: AUTH-01 for one exact metadata-and-single-
sample attempt, AUTH-01B for one metadata-only inventory, or AUTH-01C for the exact three-sample
local-review batch described below. It cannot operate the Hume UI, create a clone, execute a
bakeoff generation request, score a performance, select a provider, or grant downstream authority.
Downloaded bytes remain blocked from Hume until an owner provenance listen and a separate AUTH-02.

The v0.5 CLI extension separately validates and compiles the performance-transfer plan, Gemini
guide requests, bound provider adapters, and the blocked exact-guide Voice Changer request. Dry
runs access no credentials, network, account, or audio. V0.5 now includes an independently replayed,
consume-before-network G1 executor for exactly two Google guide requests; the committed G1 draft
has zero caps and cannot enter it. Separate exact G1 and recovery G1R1 authorizations are consumed;
each candidate-A request returned HTTP `403`, no audio was produced, and no retry occurred. G1R1's
bounded wrapper verified temporary-role cleanup. Voice Changer still has no executor and rejects
`--execute`.
Neither installed code nor a successful guide run can infer guide selection, effective
data-protection state, cross-provider disclosure, full capture, or downstream authority.

When AUTH-01 stops because the voice has multiple attached samples, the corrective scope
`elevenlabs_sample_metadata_inventory` may be separately authorized. It permits one metadata call
that records a safe sample inventory for owner review, with zero selection, downloads, generation,
spend, or Hume access. It is not one of the four initial bakeoff actions and cannot replace them.

When that complete inventory still cannot support a safe metadata-only choice, the separate scope
`elevenlabs_named_sample_batch_retrieval` with action kind
`read_only_named_sample_batch_retrieval` may authorize local review of the whole named set. For
AUTH-01C that means exactly the three AUTH-01B samples, exactly three sample `GET` calls and three
downloads on success, a 20,000,000-byte aggregate ceiling, and `$0` spend. The authorization is
consumed before network access and permits no metadata/discovery call, retry, redirect, upload,
TTS, or Hume action. Exact raw MP3 responses stay immutable and excluded from Git under local
custody. Technical inspection cannot establish identity or provenance; the owner must listen and
approve one usable original human sample before Hume can be considered.

## Source-format policy

Request provider-native PCM or PCM WAV first. If the separately authorized provider/account/model
cannot return either, the only accepted lossy fallback remains `mp3_44100_192`, and only after a
documented capability-unavailable response covered by the authorization. Preserve the provider
output unchanged, record its lossy origin, inspect it for audible codec artifacts, and
decode/resample it exactly once into the 48 kHz, 24-bit, mono PCM working path. Authentication,
timeout, rate-limit, transport, and server failures do not authorize fallback. No later lossy
intermediate is allowed. A WAV derived from MP3 is a lossless working or delivery file with lossy
origin; it is never native PCM acquisition.

## Decision vocabulary

- `technical_pass` means one exact master hash passes provenance, source-format disclosure,
  lexical conformity, transcript and pause-map identity, timing invariants, and technical QC. It
  is not creative approval.
- `creative_approved` means the named owner approves the complete performance after the independent
  eyes-closed listen. It requires a current `technical_pass`.
- `workflow_status: locked` requires both states against the same master hash. Provider success, ASR,
  export, or local validation cannot set `creative_approved`.

## Hard boundary

Step 2 owns the spoken performance and narration asset. It does not own:

- research, claims, positioning, structure, or script changes;
- footage, scenes, storyboards, motion design, or AI video generation;
- music, sound effects, ambience, or the final program mix;
- final-program loudness, Resolve color, finishing, or delivery; or
- publishing and distribution.

If the words must change, Step 2 stops and sends a script-change request to Step 1. Step 1 issues a new editorial lock before affected narration work resumes.

## Authority in this folder

- `NARRATION-STANDARD.md` defines the creative and technical contract.
- `STAGE-GATES.md` defines the required decisions and invalidation rules.
- `TEAM-WORKFLOW.md` defines roles, parallel work, and handoffs.
- `REFERENCE-MAP.md` separates live authority from retained V1 lessons.
- `PORTING-MANIFEST.md` records provenance and frozen reference hashes.
- `CLI-VALIDATION-CONTRACT.md` defines machine state, validation, and invalidation.
- `TOOL-AUDIT-AND-BAKEOFF.md` defines the proposed v0.3 provider-selection controls and the exact
  ElevenLabs/Hume external-action boundaries.
- `STEP2-v0.5-CHANGE-PROPOSAL.md` defines the isolated sequential Gemini-guide and Saved-C transfer
  microtest without altering the canonical stage gates.
- `STEP2-v0.3-CHANGE-PROPOSAL.md` records the proposed semantic delta while
  `STEP2-v0.2-CHANGE-PROPOSAL.md` remains the frozen prior proposal.
- Numbered subfolders contain reusable checklists and templates.

This documentation, a completed template, a frozen configuration, or a passing local validation
does not authorize an external voice-provider call, read an account, retrieve a voice sample,
upload a sample, create a clone, spend provider credits, create an episode, or produce production
audio. Login state is never authorization. The initial v0.3 bakeoff requires four independent
authorizations: ElevenLabs read-only metadata/sample retrieval, Hume UI upload plus one clone,
ElevenLabs two-passage/two-generation short calibration, and Hume two-passage/two-generation short
calibration. Their machine scopes are `elevenlabs_sample_retrieval`, `hume_clone_creation`,
`elevenlabs_calibration`, and `hume_calibration`. A later long-form continuity/pickup test requires
a fifth human authorization and is not an initial machine scope. None grants
N4B full capture or Step 3. Step 2 remains proposed until its normal case, edge case, and failure
behavior are tested and the owner explicitly locks it.

The separately authorized corrective inventory scope
`elevenlabs_sample_metadata_inventory` is outside that four-action bakeoff sequence. It exists only
to enumerate safe metadata after a multiple-sample stop and grants no selection or download.

The separately authorized AUTH-01C scope `elevenlabs_named_sample_batch_retrieval` is also outside
the four-action sequence. It grants only the exact three inventory-bound local-review downloads and
cannot approve provenance, select production audio, disclose anything to Hume, or authorize AUTH-02.

The proposed v0.5 `AUTH-G1` and `AUTH-V1` scopes are also outside the frozen v0.3 bakeoff sequence.
Neither is active. They may not be combined: guide-generation authority does not permit disclosure
to ElevenLabs, and a transfer draft cannot become executable until it binds one owner-selected,
passing guide and verified current data-use protection.
