# V2 Step 2 v0.2 change proposal: Narration Production

Status: proposed and under fixture test; not authority

Proposal date: 2026-08-23

Prior proposal: Step 2 v0.1

Production authorization: none

## Why v0.2 is required

V0.1 established the correct boundary: Step 1 owns the exact words and Step 2 owns their
performance, acquisition, edit, conformity, timing, and narration lock. It did not yet prove the
operating controls. V0.2 closes the gaps that could otherwise:

- accept an incomplete or stale Step 1 handoff;
- replace Step 1's ordered word identity with an episode-specific tokenizer or ASR guess;
- make a lossy source appear native by exporting it into a larger WAV container;
- mix configuration freeze, calibration approval, and full-capture authority;
- treat technical validity and creative approval as one decision;
- permit synthetic pickups without a tested continuity rule;
- bind a transcript to pre-edit audio rather than the final master; or
- lose synthetic origin, rights, and intentional-pause information downstream.

## Proposed operating doctrine

### 1. One immutable spoken-text identity

Step 2 deterministically reproduces Step 1 v1.5's whitespace-delimited ordered narration tokens.
The `W` count, exact sequence, and SHA-256 are lexical authority for all later work. Acoustic
`alignment_parts` may describe pronunciation but remain subordinate to their canonical `W` token.

### 2. Configuration precedes calibration

```text
N3 narrator rights and acquisition configuration frozen
→ separately authorized N4A four-part calibration
→ N4A technical review and owner creative approval
→ separately authorized N4B full capture
```

Calibration covers the cold open and promise, dense evidence, economics and uncertainty, and
difficult names, numbers, acronyms, and pronunciation.

### 3. Technical and creative decisions remain separate

`technical_pass` requires exact words, full provenance, truthful formats, a valid PCM delivery
master, valid timestamps, matching hashes, and technical audio QC.

`creative_approved` requires narrator fit, natural delivery, intelligibility, pace, trust,
continuity, and explicit owner approval after the full eyes-closed listen.

`workflow_status: locked` requires both against the same master hash. Neither implies the other.

### 4. Native source quality is not the delivery container

Native PCM is requested first. If unavailable from the selected ElevenLabs account/model, the only
fallback is `mp3_44100_192`. The provider output remains immutable and truthfully labeled lossy,
receives an audible artifact review, and is decoded/resampled once into 48 kHz, 24-bit, mono PCM.
No later lossy intermediate is allowed. The resulting WAV is not native PCM acquisition.

### 5. Synthetic narration uses an explicit continuity protocol

One full run may contain several provider requests when the model cannot accept the entire script.
Every request is bound to the same script identity, performance direction, narrator, settings,
pronunciation, batch, context, and source-format policy. Pickups receive new immutable job records
and may require a wider regenerated passage or full batch when continuity cannot be proven.

V2 must not invoke or import legacy `studio/scripts/originate/generate_vo.py` because that path may
rewrite lexical content and does not enforce these contracts.

### 6. The final master creates downstream time

Interim ASR is diagnostic. The authoritative word transcript and intentional-pause map are produced
from the lexically clean final narration master and bound to that exact hash and duration. Any
sample-level master change invalidates them and every later state.

## Fixture acceptance set

### Authorized positive control

AI Visibility v1.1 is the only current positive Step 2 fixture. It is frozen under Step 1 v1.5 with:

- script SHA-256 `74048b55ed15ed6ed679abb5a6c892def8a8a40e75e7cebeafdfde319dd67efa`;
- clean read-through SHA-256 `544deaeb4324c116fcb5bb7b89e636908d460d63de2bbfd9121155e324979aa6`;
- 3,019 ordered whitespace-delimited `W` tokens; and
- ordered narration-token SHA-256
  `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`.

It is a fixture only. It is not promoted, numbered, cleared for public facts, or authorized for
visual production or release.

### Historical negative control

Workflow Operations is retained unchanged as historical evidence. It is expected to fail N1
because it lacks the current Step 1 v1.5 lock and ready narration handoff. Step 2 must not upgrade or
repair it.

### Adversarial controls

1. Remove `not` while preserving technically clean audio. Lexical conformity must block.
2. Change narrator, provider model, material settings, human room/microphone, or native source
   format during a pickup. Return to N3 and recalibrate.
3. Change one sample after alignment. Transcript, pause map, technical pass, creative approval,
   narration lock, and Step 3 handoff must become stale immediately.
4. Rename an MP3 as WAV. Codec inspection must expose the real lossy source.
5. Attempt to set `creative_approved` through automation. State validation must reject it.

## Required evidence before approval

- All v0.2 authority and template files pass link, table, whitespace, and identity checks.
- AI Visibility reproduces its frozen script and `W` identities exactly.
- Workflow Operations reaches the expected N1 failure without mutation.
- Every adversarial fixture reaches its expected blocked or return state.
- The OE narrator has a documented rights basis and owner-selected reference.
- Native provider output capability is tested truthfully; fallback handling is proven if needed.
- Calibration audio passes technical review and explicit owner creative review.
- One complete-script control proves continuity, final-master conformity, transcript and pause-map
  binding, invalidation, and narration lock.

## Current boundary

The documentation and local fixture setup may prepare text, direction, identities, expected
decisions, and validation contracts. It does not itself call a provider, spend credits, record a
human, create an episode, grant either approval state, authorize Step 3, or release anything.
