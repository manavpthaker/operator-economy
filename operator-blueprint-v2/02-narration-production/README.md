# Step 2: Narration Production

Status: proposed V2 Step 2 v0.3 provider-selection revision; not yet authoritative. The v0.2
calibration record remains frozen history.

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

The retained AI Visibility v1.1 N4A batch is a **technical PASS** and an owner **creative REVISE**.
The audio and receipts remain valid technical evidence, but N4A did not pass. The approved Step 1
words remain locked: this is a performance/provider problem, not an editorial rewrite request.

V0.3 therefore adds a provider-agnostic performance envelope and a bounded ElevenLabs-versus-Hume
bakeoff before another N4A decision. The bakeoff grants no N4B full capture or Step 3 authority.
See [`TOOL-AUDIT-AND-BAKEOFF.md`](TOOL-AUDIT-AND-BAKEOFF.md).

## Production flow

```text
locked editorial handoff
→ handoff verification
→ performance direction and provider-agnostic performance envelope
→ when the current method is unapproved: original-sample provenance gate
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

Synthetic capture additionally follows
[`02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md`](02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md).
Machine-checkable identities, validation states, and exit semantics follow
[`CLI-VALIDATION-CONTRACT.md`](CLI-VALIDATION-CONTRACT.md).

The v0.3 CLI can validate the envelope, provider adapters, bakeoff plan, and four initial action-
authorization shapes, then compile credential-free ElevenLabs and Hume dry runs. Its one narrow
external-action client can consume a separately approved `AUTH-01`, read the exact ElevenLabs voice
metadata, and retrieve the single selected source sample into ignored local custody. It cannot
operate the Hume UI, create a clone, execute a bakeoff generation request, score a performance,
select a provider, or grant any downstream authority. A retrieved sample remains blocked from Hume
until an owner provenance listen and a separate `AUTH-02`.

When AUTH-01 stops because the voice has multiple attached samples, the corrective scope
`elevenlabs_sample_metadata_inventory` may be separately authorized. It permits one metadata call
that records a safe sample inventory for owner review, with zero selection, downloads, generation,
spend, or Hume access. It is not one of the four initial bakeoff actions and cannot replace them.

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
