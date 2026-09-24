# G1 owner authorization and readiness record

Status: **ACTIVE AUTHORIZATION MATERIALIZED; UNCONSUMED; NOT EXECUTED**

Recorded at: `2026-08-25T23:37:57Z`

Authorized by: Manav Thaker

Authorization window: `2026-08-25T23:37:57Z` through, but not including,
`2026-08-26T23:37:57Z`. The authorization expires after exactly 24 hours or is permanently consumed
before the first credential refresh or provider request, whichever occurs first.

## Owner decision

The owner approved the exact bounded G1 synthetic-guide microtest represented by the frozen plan,
compiled two-request set, active authorization, limits, and exclusions below. This record documents
that decision; it does not broaden it or authorize Voice Changer, guide selection, full capture,
Step 3, sharing, or publication.

## Immutable authorization bindings

| Artifact or identity | Path or SHA-256 |
| --- | --- |
| Preserved zero-authority draft | `authorizations/01-google-synthetic-guide.DRAFT.json` |
| Preserved draft SHA-256 | `eae5bcca9df42835b5d9f447db64d389c8c109ad9eeb00716d191326fe0540e5` |
| Active authorization | `authorizations/01-google-synthetic-guide.ACTIVE.20260825T233757Z.json` |
| Active authorization SHA-256 | `6d5ae0e6719bae8100cd437b8faa875cbd3f9b3969e09749544d5e5ab06366ea` |
| Performance-transfer plan SHA-256 | `f73f42e1221753d394ba5de31550094a9aa98e950987e415cb4b0f0c85365f53` |
| Canonical W SHA-256 | `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a` |
| Exact `W[30,110)` token-slice SHA-256 | `790a8176c5085968bd24c8572dacc5539b4e686f6b9b269cba2fd330c08d4a4a` |
| Exact spoken transport SHA-256 | `db3ccbb400f6bde4099f08b79b4402c374577cae4e622b0087649482e4f7d1cb` |
| Acting-prompt SHA-256 | `8cfe0391324bce56cb6bf6d83ef0e781479de14c08a7861716e9716f9017b416` |
| Canonical 1,440-byte request-body SHA-256 | `4acd99a738125e942fc1a6c2e4ef8df9c819397c9a2627fb494e73d63d004c53` |
| Two-request set SHA-256 | `ed1aa73a04db602b8ed2611731346e3f0bfae9d48d55a4f94bb5110da85c0cba` |
| Private quota-project binding SHA-256 | `68a5cdeb9918bf84d3f59c3f428e8e12a40b33f1ab0d0eaee19276be6761c0f2` |

The raw quota-project identifier is deliberately absent from Git.

## Readiness evidence and evidence limit

Immediately before authorization materialization, the operator reported that:

- local Google ADC authentication was complete;
- billing was enabled for the hash-bound project; and
- `texttospeech.googleapis.com`, initially disabled, had been enabled successfully.

This is operator-reported live-state evidence, not a credential or cloud-response capture. This
authorization patch did not open ADC, read a token, query Google, store an account or project
identifier, or make a provider request. Execution must still hash-match the private
`GOOGLE_CLOUD_QUOTA_PROJECT` value and pass the runtime's symlink-free ADC preflight.

## Exact authorized action and ceilings

- Exactly two independent, identical, unseeded `POST` requests to
  `https://us-texttospeech.googleapis.com/v1/text:synthesize`.
- Model `gemini-2.5-pro-tts`, voice `Achird`, language `en-US`.
- Exact locked dialogue in `input.text`; exact nonlexical acting prompt in `input.prompt`.
- `LINEAR16`, 24 kHz, mono WAV; at most two outputs.
- At most 1,440 request-body bytes per call and 2,880 total request-body bytes.
- At most 4,000,000 provider-response bytes per call.
- At most 50 seconds and 2,500,000 WAV bytes per output; at most 5,000,000 total audio bytes.
- Modeled authorization ceiling `$0.66`, accrued as `$0.33` per attempted call; this is not an
  observed provider invoice or provider-enforced spend cap.
- No redirect, retry, fallback, alternate model, alternate voice, alternate request, or resume.
- After immutable authorization consumption, token refresh uses exact argv
  `gcloud auth application-default print-access-token --quiet`, with no `--scopes` override.

## Deterministic one-shot evidence paths

- Consumption:
  `authorizations/consumed/AUTH-G1-ai-visibility-v1.1-p01-synthetic-guide-20260825T233757Z.consumed.json`
- Complete success:
  `receipts/google/AUTH-G1-ai-visibility-v1.1-p01-synthetic-guide-20260825T233757Z.run.json`
- Post-consumption failure:
  `receipts/google/AUTH-G1-ai-visibility-v1.1-p01-synthetic-guide-20260825T233757Z.failure.json`
- Candidate A: `outputs/raw/google/P01-W0030-W0110/candidate-A.wav`
- Candidate B: `outputs/raw/google/P01-W0030-W0110/candidate-B.wav`

At materialization time, none of those consumption, run, failure, or audio artifacts existed. A
later execution may create the consumption record and then exactly one run-or-failure receipt. If
the first output passes and the second call fails, the first immutable WAV remains a receipt-bound
partial output and this authorization stays consumed.
