# AI Visibility v1.1 Provider Bakeoff Fixture

Status: AUTH-01 stopped safely on multiple source samples; no sample download, audio, voice clone,
creative verdict, episode, or Step 3 authority

## Purpose

This fixture compares whether ElevenLabs v3 or Hume Octave can turn the same locked Operator
Economy words and performance intent into a voice that remains recognizably Manav while carrying
actor-level energy and beat control.

The bakeoff tests the acquisition path, not the script. It may add only approved nonlexical
direction. It may not rewrite, omit, add, replace, or reorder a spoken word.

## Frozen test material

| Passage | Function | W range | Tokens | Canonical W SHA-256 | Transport characters |
| --- | --- | ---: | ---: | --- | ---: |
| `P01-S00` | cold open, dry observation, promise, open question | `[0,139)` | 139 | `1e27c7c8793c6814935fcd74bbb41a87b2123ed0f19c53cd75b5835de9ec8454` | 792 |
| `P02-S11-S12` | construction, validation rules, verdict, final invitation | `[2627,3019)` | 392 | `54c3f3bc7c63a1f0ad8d23176d75b235290d153f19932d72f6413095e8bfd235` | 2,359 |

Both passages are exact slices of the approved 3,019-token `oe-spoken-text-v1` identity
`096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`.
Paragraph and thought boundaries are absolute half-open W ranges. The text files in `passages/`
are human-readable mirrors; the canonical W identity remains the machine authority.

## Bakeoff design

Each provider must return exactly two candidates for each passage:

| Provider | Candidate production | Calls if later authorized | Output target |
| --- | --- | ---: | --- |
| ElevenLabs v3 | two generations per passage using the same exact approved nonlexical tag anchors | 4 primary; 8 maximum with one conditional fallback per primary | native `pcm_48000`; only `mp3_44100_192` after a receipted PCM-capability rejection and a separately bound fallback request |
| Hume Octave 1 | one thought-partitioned request per passage with `num_generations: 2` | 2 primary; 4 maximum with one conditional fallback per primary | WAV first; only `mp3_44100_192` after a receipted lossless-capability rejection and a separately bound fallback request |

That yields eight blinded candidates: two providers × two passages × two candidates. Candidate
generation may vary; the locked words and approved passage-level direction may not. The
ElevenLabs identity is the existing owner-selected OE voice `yUXeTfC1IFOCSjGc96sQ`. The Hume
identity is deliberately unresolved until a separately authorized, UI-mediated Manav voice clone
produces a provenance receipt and immutable clone ID.

## Fail-closed state

- The ElevenLabs API key was read from the process environment for the authorized call and was not
  written to any repository artifact, receipt, path, or command result.
- One separately authorized ElevenLabs metadata call was made. It returned multiple attached
  source samples, so the one-use authorization was consumed and the runner stopped.
- No sample was selected or downloaded. The metadata failure receipt preserved the block reason but
  not the returned sample inventory; that receipt defect is recorded and is not a retry authority.
- No sample was uploaded and no voice was cloned.
- No TTS request was sent and no audio exists.
- AUTH-01 is consumed. AUTH-02 through AUTH-04 remain drafts with zero authority.
- The Hume request records contain a pending clone placeholder and are not execution-ready.
- Hume account tier and commercial-use eligibility are unverified. They must be checked before any
  Hume calibration approval; a logged-in session alone is not evidence.
- Modeled public rates are planning inputs, not account quotes or spend authority: ElevenLabs v3
  at `$0.10 / 1,000` text characters and Hume at a conservative Creator overage rate of
  `$0.15 / 1,000` text characters. Both must be refreshed before approval.

## Files

- `performance-envelope.json` is strictly provider-neutral. It freezes listener relationship,
  objectives, performance states, energy, required emphasis/pause/qualification/landing anchors,
  anti-targets, passage identities, and paragraph/thought boundaries.
- `adapters/elevenlabs-v3.json` binds the existing voice, model/settings, approved tag allowlist,
  absolute tag anchors, and double-LF paragraph transport.
- `adapters/hume-octave-1.json` binds the pending clone placeholder, the two exact owner-approved
  passage descriptions, deterministic subordinate thought directions, emitted-description hashes,
  and trailing silences.
- `provider-bakeoff-plan.json` declares the exact two-provider, two-passage, two-candidate test.
- `compiled/` contains the credential-free runtime's inspectable primary and conditional-fallback
  request bodies, hashes, counts, costs, destinations, and bound compilation record. A dry-run body
  is not a provider-call authorization.
- `authorizations/` contains four separate draft, unapproved action records.
- `reviews/BLIND-SCORING.template.md` separates listening evidence from provider identity.
- `reviews/LONG-FORM-CONFIRMATION.template.md` prevents a short-passage winner from being treated as
  a production narrator without a continuity test.
- `RESULTS.md` is the current human-readable state and eventual decision surface.

## Required sequence before any audio can exist

1. Validate the frozen W ranges, provider-neutral envelope, both provider adapters, plan,
   compilation hashes, primary and conditional-fallback call limits, destinations, and pricing
   model.
2. Repair and test the multiple-sample inventory receipt, then issue a new read-only metadata
   authorization if the owner wants to enumerate the exact sample IDs. Do not reuse AUTH-01.
3. After owner selection, separately authorize one exact sample download and complete provenance
   review. Only then may the UI-mediated Hume sample upload/clone be considered under its own
   authorization, with rights, consent, source
   sample hash, account tier, commercial-use eligibility, clone ID, and clone receipt.
4. Replace the Hume placeholder, regenerate its bodies, recompute every affected hash, and re-run
   the dry run.
5. Issue bounded, expiring calibration authorizations independently for ElevenLabs and Hume.
6. Acquire immutable raw outputs, blind them, verify exact words and technical provenance, and run
   the blind review.
7. Run the long-form confirmation before selecting a production path.

Passing JSON validation, a successful dry run, or a winning score cannot authorize provider
spend, full capture, production narration, or Step 3.
