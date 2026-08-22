# Step 2: Narration Production

Status: proposed V2 Step 2 v0.1; ready for test, not yet authoritative.

Step 2 turns the exact, owner-approved Step 1 script into the final spoken spine of the episode. It controls performance direction, narrator and capture consistency, takes, pickups, dialogue editing, lexical conformity, the clean narration master, word-level timing, and the handoff to visual translation.

It does not rewrite the episode or start visual production.

## Entry condition

Step 2 may start only for a real numbered V2 episode with:

- a current Step 1 editorial lock;
- a current narration handoff;
- a current editorial-voice conformity report tied to the locked script;
- matching script and claims-map hashes;
- the locked spoken word count, plus a Step 2 comparison method that reproduces it;
- no unresolved editorial, evidence, legal, permission, or owner blocker; and
- documented authorization for the chosen human or synthetic narrator.

Fixtures may test the system without creating an episode. They are never production approvals.

## Production flow

```text
locked editorial handoff
→ handoff verification
→ performance direction
→ narrator and capture lock
→ calibration reads
→ full takes
→ selects and pickups
→ narration edit
→ lexical and technical conformity
→ word-level transcript
→ narration lock
→ Step 3 handoff
```

## Required outputs

A complete Step 2 package contains:

- verified editorial handoff checklist;
- performance-direction brief;
- approved narrator profile or an explicitly authorized episode-specific narrator identity;
- voice-and-capture lock;
- immutable raw-take register with file hashes;
- take reviews and select decisions;
- pickup log;
- narration edit decision list;
- clean narration master: PCM WAV, 48 kHz, 24-bit, mono;
- optional review MP3, clearly marked non-master;
- lexical-conformity report against the locked script;
- word-level transcript timed from the final narration master;
- technical measurements and independent-listener review;
- narration lock; and
- visual-translation handoff.

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
- Numbered subfolders contain reusable checklists and templates.

This documentation does not authorize an external voice-provider call, clone a voice, create an episode, or produce production audio. Step 2 remains proposed until its normal case, edge case, and failure behavior are tested and the owner explicitly locks it.
