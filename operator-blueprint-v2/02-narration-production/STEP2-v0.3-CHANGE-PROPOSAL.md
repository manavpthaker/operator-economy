# V2 Step 2 v0.3 change proposal: Provider Selection

Status: proposed; documentation plus credential-free validation and request compilation

Proposal date: 2026-08-24

Prior proposal: Step 2 v0.2, retained unchanged as historical design and calibration evidence

External-action authorization: none

## Why v0.3 is required

V0.2 proved the AI Visibility narration path could preserve locked words, enforce a bounded
authorization, acquire native PCM, retain immutable provenance, and separate technical evidence
from human creative approval. Its retained N4A result is:

- technical acquisition and preflight: **PASS**;
- owner creative performance decision: **REVISE**;
- N4A gate: **not passed**;
- full capture and Step 3: **not authorized**.

That is a measurement of narration performance, not a failure of the Step 1 script. V0.3 keeps the
3,019-token `W` identity locked and tests whether a different provider method can perform the same
episode more effectively.

## Proposed delta

1. Freeze one provider-agnostic performance envelope and translate it through separately hashed
   ElevenLabs and Hume adapters.
2. Retrieve exactly one original owner recording under read-only ElevenLabs authority and prove its
   provenance, consent, custody, and commercial-use basis.
3. Upload that hash-bound sample through Hume's documented UI-mediated clone flow and create exactly
   one clone under a separate authorization.
4. Generate a fair short comparison: two exact passages and two generations per provider.
5. Reject candidates before scoring for rights, words, format, artifact, comprehension, or blind
   integrity failures.
6. Score all eight clips blind on separate immutable owner and independent-listener scorecards.
7. In a separate curator consolidation bound to both scorecard hashes and the sealed-map hash,
   unseal providers, select each provider's best passing P1 and P2 generations, and average those
   passage scores into the provider short score.
8. Advance the eligible leader and only a runner-up within 5.0 points to a later, separately
   authorized 3.5-to-4.5-minute continuity and pickup test.
9. Treat long-form/pickup as pass/fail confirmation, not a rescore. Apply the final comparison to
   frozen short provider scores: retain ElevenLabs when it passes confirmation and is within 5.0
   points of Hume or leads; adopt Hume only when Hume reaches 80, leads by more than 5.0 points, and
   passes confirmation.

The complete doctrine is in
[`TOOL-AUDIT-AND-BAKEOFF.md`](TOOL-AUDIT-AND-BAKEOFF.md).

## Authority separation

The four initial authorizations are exactly:

1. `elevenlabs_sample_retrieval` — ElevenLabs read-only voice metadata and original-sample
   retrieval;
2. `hume_clone_creation` — Hume UI sample upload and one clone creation;
3. `elevenlabs_calibration` — ElevenLabs P1/P2 by E1/E2; and
4. `hume_calibration` — Hume P1/P2 by H1/H2.

The long-form/pickup test is a fifth later authorization. N4B full capture is a later, different
authorization available only after the selected method passes N4A. No v0.3 record grants Step 3.

## Frozen history

- `STEP2-v0.2-CHANGE-PROPOSAL.md` remains the v0.2 design record.
- The existing fixture audio, raw hashes, receipts, and technical review remain valid evidence.
- The consumed v0.2 provider authorization cannot be replayed.
- Workflow Operations remains the historical N1 failure control.
- Step 1 v1.5 and AI Visibility's script/`W` identities remain unchanged.

## Runtime truth

The runtime now validates the provider-neutral performance envelope, provider adapters, provider-
bakeoff plan, and all four initial action-authorization shapes, and it compiles credential-free
ElevenLabs and Hume dry-run requests. It verifies exact `W` ranges, Eleven tag stripping and
double-LF transport, Hume `POST /v0/tts` description expansion with `num_generations: 2`, output
policy, and bounded call/character accounting.

It does not retrieve Eleven samples, operate the Hume UI, create a Hume clone, execute either
provider's bakeoff request, blind-review candidates, score performance, or select a method. The
retained v0.2 ElevenLabs capture client is a different contract and may not execute a v0.3 plan.
These are authority and implementation boundaries, not permissions to improvise. Offline validity
does not authorize or consume an external action.

## Acceptance before v0.3 can become authority

- Original-sample selector fails closed on zero or multiple samples without an exact new
  authorization.
- Hume UI clone receipt ties one clone ID to the one authorized source hash.
- All four initial authorizations are separate, bounded, consumed, and independently reviewable.
- E1/E2 are identical Eleven requests except seed/generation; H1/H2 are two generations from one
  identical Hume request and description.
- P1 and P2 are exact equal `W` ranges across providers.
- Every raw output is immutable and passes PCM/WAV-first source inspection or the exact
  `mp3_44100_192` exception.
- All eight clips receive hard-gate disposition and blind scoring.
- Signed scorer sheets remain blind and immutable; unblinding and arithmetic occur only in a
  separately hashed curator consolidation.
- Provider select and within-5 calculations reproduce from frozen scorecards.
- AUTH-05 is absent until the short scores identify eligible providers.
- Long-form candidates cover 3.5 to 4.5 minutes, the required argument modes, an eyes-closed fatigue
  listen, and a several-hours-later pickup behind a blind seam.
- The asymmetric final selection rule is applied exactly.
- No action sets N4A, `creative_approved`, N4B, narration lock, or Step 3 by inference.

Until these are proven and the owner approves the system change, Step 2 remains proposed v0.3.
