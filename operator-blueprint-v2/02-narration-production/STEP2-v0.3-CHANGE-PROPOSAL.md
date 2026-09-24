# V2 Step 2 v0.3 change proposal: Provider Selection

Status: proposed; documentation plus credential-free validation and request compilation

Proposal date: 2026-08-24

Prior proposal: Step 2 v0.2, retained unchanged as historical design and calibration evidence

External-action authorization: AUTH-01 issued and consumed; blocked on multiple samples. Corrective
AUTH-01B issued and consumed; complete three-sample metadata inventory recorded. No sample was
selected or downloaded. AUTH-01C was separately owner-approved, committed, and consumed. Its first
sample response failed the inventory-bound byte-count identity, so the batch stopped after one call;
samples two and three were not requested and Hume remains untouched.

## 2026-08-24 vendor-drift amendment: Hume leg stopped before upload

The proposal's frozen Hume candidate assumed one Manav clone running on Octave 1 so the same
provider request could use natural-language `description` acting instructions. Current official
Hume documentation makes that candidate internally incompatible:

- [`E0814`](https://dev.hume.ai/docs/resources/errors) requires Octave 2 for instant voice cloning;
- [`E0813`](https://dev.hume.ai/docs/resources/errors) and the
  [voice guide](https://dev.hume.ai/docs/text-to-speech-tts/voice) prevent an Octave 2-created clone
  from running on Octave 1;
- the [acting-instructions guide](https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions)
  keeps `description` on Octave 1 only; and
- cloned-voice access and commercial use require verified Creator-or-higher eligibility under the
  current [error reference](https://dev.hume.ai/docs/resources/errors),
  [FAQ](https://dev.hume.ai/docs/text-to-speech-tts/faq), and
  [Terms of Use](https://www.hume.ai/terms-of-use).

The existing Hume adapter, provider plan, compiled dry run, AUTH-02 draft, and AUTH-04 draft remain
frozen historical proposal artifacts. They are **not executable** and must not be silently changed
to fit the vendor. Before Hume can re-enter the comparison, the candidate must be redesigned,
checked for equal-treatment consequences, recompiled, and explicitly approved by the owner. A
Creator-or-higher account would clear only access/commercial eligibility, not the model mismatch.

There is no active AUTH-02. No Hume source upload, clone, TTS request, calibration, bakeoff
generation, long-form test, full capture, Step 3 action, account purchase, or tier change is
authorized. Step 1 remains locked; vendor drift is a Step 2 tool-fit failure, not an editorial
rewrite request.

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
2. Resolve one original owner recording under read-only ElevenLabs authority. When metadata cannot
   distinguish the complete named set, retrieve that exact bounded set for local owner listening,
   then prove one sample's provenance, consent, custody, and commercial-use basis before Hume.
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

Steps 3 through 9 above preserve the original proposal logic. Their Hume-dependent branch is now
non-executable under the dated vendor-drift amendment and cannot resume without the replacement
design and owner approval described there.

## Authority separation

The four initial authorizations are exactly:

1. `elevenlabs_sample_retrieval` — ElevenLabs read-only voice metadata and original-sample
   retrieval;
2. `hume_clone_creation` — Hume UI sample upload and one clone creation;
3. `elevenlabs_calibration` — ElevenLabs P1/P2 by E1/E2; and
4. `hume_calibration` — Hume P1/P2 by H1/H2.

The long-form/pickup test is a fifth later authorization. N4B full capture is a later, different
authorization available only after the selected method passes N4A. No v0.3 record grants Step 3.

AUTH-01's multiple-sample stop introduced one corrective least-privilege scope:
`elevenlabs_sample_metadata_inventory`. It is outside the four initial bakeoff actions and permits
one metadata request only, with zero selection, downloads, generation, spend, or Hume access. It
exists only to give the owner the sample IDs and safe metadata required for a later exact-sample
decision.

Because AUTH-01B's complete three-sample inventory still did not establish provenance, AUTH-01C
introduces a second corrective scope, `elevenlabs_named_sample_batch_retrieval`, with action kind
`read_only_named_sample_batch_retrieval`. It binds all three AUTH-01B filenames and sample IDs and
permits exactly three sample `GET` calls/downloads on success, no metadata or discovery request, a
20,000,000-byte aggregate ceiling, and `$0` spend. It is consumed before network access and permits
no retry, redirect, upload, TTS, or Hume action. Exact raw MP3s remain local and excluded from Git.
Technical QA cannot clear human provenance; Hume remains blocked until the owner listens and
approves one exact sample under a later decision.

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

The runtime's external-action surface is restricted to separately authorized, fail-closed
ElevenLabs reads: AUTH-01 metadata plus a single-sample attempt, AUTH-01B metadata-only inventory,
and AUTH-01C exact named-sample batch retrieval. Each executor consumes its authorization before
network access and enforces its own exact calls, bytes, destinations, and zero-dollar ceiling. None
can operate the Hume UI, create a clone, execute a provider bakeoff generation, blind-review
candidates, score performance, or select a method. The retained v0.2 ElevenLabs capture client is a
different contract and may not execute a v0.3 plan. These are authority and implementation
boundaries, not permissions to improvise. Offline validity does not authorize or consume an
external action.

## Acceptance before v0.3 can become authority

- The Hume challenger, if retained, is redesigned around one currently compatible model/control
  path, receives an equal-treatment review, is recompiled, and is explicitly owner-approved; the
  frozen Octave 1 clone-plus-description artifacts remain non-executable.
- Creator-or-higher account access and commercial eligibility are verified before any future Hume
  action; that verification does not waive the model-compatibility gate.
- Original-sample selector fails closed on zero or multiple samples without an exact new
  authorization.
- A multiple-sample review binds the complete AUTH-01B inventory, consumes AUTH-01C before network,
  makes exactly three bound downloads under 20,000,000 bytes and `$0`, and leaves provenance to the
  owner rather than technical QA.
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
