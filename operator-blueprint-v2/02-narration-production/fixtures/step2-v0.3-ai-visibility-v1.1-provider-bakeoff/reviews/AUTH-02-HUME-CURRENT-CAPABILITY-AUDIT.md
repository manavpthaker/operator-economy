# AUTH-02 Hume Current-Capability Audit

Audited: 2026-08-24

Verdict: `BLOCKED BEFORE UPLOAD`

The provenance-bound Manav source is ready for a separately authorized clone action, but the
current Hume product no longer supports the exact challenger defined by this fixture.

## Current official constraints

- Hume error `E0814` says instant voice cloning is unavailable for Octave 1 and directs it to
  Octave 2.
- Hume error `E0813` says a voice created with Octave 2 cannot be used with Octave 1.
- Hume's acting-instructions guide says the separate `description` field is available only for
  Octave 1; Octave 2 support is still forthcoming.
- Hume error `E0810` says retrieving a cloned voice requires Creator or higher.
- Hume's TTS FAQ says Free and Starter are non-commercial; commercial use requires Creator or
  higher.

Sources:

- https://dev.hume.ai/docs/resources/errors
- https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions
- https://dev.hume.ai/docs/text-to-speech-tts/faq
- https://dev.hume.ai/docs/voice/voice-cloning
- https://www.hume.ai/pricing

## Why this changes the bakeoff

The frozen Hume candidate requires all three of these at once:

1. Manav identity from an uploaded voice clone;
2. Octave 1; and
3. a separate natural-language acting `description` for each passage.

Current Hume documentation makes that combination unavailable. Creating an Octave 2 clone now
would produce a voice that cannot run in the Octave 1 acting-instruction test. It would therefore
spend the one approved upload/clone action without creating the challenger the bakeoff was designed
to judge.

## Additional access gates

- The logged-in account tier and commercial eligibility are not yet verified from the account.
- Controlled Chrome access to `app.hume.ai` was blocked because its browser security check was
  unavailable. No attempt was made to bypass that control.
- The current runtime validates Hume clone authorization but has no independently reviewed UI
  action consumer.

## Authority boundary

No source was uploaded to Hume. No clone was created. No Hume generation occurred. The source
consent record remains valid, but AUTH-02 must stay draft until the owner chooses a revised Hume
test that is technically possible and the account and execution gates are cleared.
