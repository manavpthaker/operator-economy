# Step 2: Narration Production

Status: proposed V2 Step 2 v0.2; ready for calibration tests, not yet authoritative.

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

## Production flow

```text
locked editorial handoff
→ handoff verification
→ performance direction
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

Synthetic capture additionally follows
[`02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md`](02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md).
Machine-checkable identities, validation states, and exit semantics follow
[`CLI-VALIDATION-CONTRACT.md`](CLI-VALIDATION-CONTRACT.md).

## Source-format policy

Request native PCM first. If the selected ElevenLabs account and model cannot return native PCM,
the only accepted fallback is `mp3_44100_192`. Preserve that provider output unchanged, record its
lossy origin, inspect it for audible codec artifacts, and decode/resample it exactly once into the
48 kHz, 24-bit, mono PCM working path. No later lossy intermediate is allowed. A WAV derived from
MP3 is a lossless working or delivery file with lossy origin; it is never native PCM acquisition.

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
- Numbered subfolders contain reusable checklists and templates.

This documentation, a completed template, a frozen configuration, or a passing local validation
does not authorize an external voice-provider call, spend provider credits, clone a voice, create
an episode, or produce production audio. Each external call requires separate explicit authority
for the named episode or fixture, voice, provider/model, and bounded calibration or full-capture
scope. Step 2 remains proposed until its normal case, edge case, and failure behavior are tested and
the owner explicitly locks it.
