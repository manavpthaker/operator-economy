# AUTH-02 Source Provenance Disposition

Recorded: 2026-08-24T23:37:34Z

Status: `CONDITIONAL PASS`

This disposition applies only to the exact local byte object below. It does not make AUTH-01C a
successful retrieval and does not authorize a Hume action by itself.

## Exact source

- Local excluded-media path:
  `local-media/elevenlabs/AUTH-01C-20260824T214346Z/ivc_1.mp3`
- SHA-256: `dd3f0887acb5bc4c623476eb053136d3f0ce7d6828168874911f8b0dcecd64f9`
- Actual bytes: `8,641,768`
- Actual media: MP3, 44.1 kHz, mono, 192 kbps, `360.000023` seconds
- Full decode: pass
- Git custody: excluded; the full source must never be committed or published

## Owner findings

Manav Thaker confirmed in the active Codex task that:

- the source is his original human recording;
- it is not AI-generated or voice-converted;
- the complete six-minute recording contains only Manav; and
- this exact source SHA may be disclosed once to Hume for one upload and one clone creation.

The machine-readable consent record is
`receipts/hume/AUTH-02-20260824T233734Z-source-provenance-and-consent.json`.

## Metadata discrepancy disposition

AUTH-01B listed `5,760,813` bytes, while the official sample endpoint returned `8,641,768` bytes,
a difference of `2,880,955` bytes or `50.0095%`. That discrepancy remains preserved. Hume may bind
only the actual local bytes and SHA above. The provider's opaque inventory hash has no documented
algorithm and is not treated as a checksum or corruption result.

Owner listening resolves human identity, single-speaker provenance, and synthetic-source exclusion
for the exact local object. It does not retroactively change AUTH-01C's failed-closed outcome.

## Remaining gates

- Confirm no third-party music or other rights-bearing material is present.
- Verify the logged-in Hume tier and commercial-use eligibility from current account evidence.
- Create, validate, commit, and consume a separate active AUTH-02 before the upload.
- Use the documented Hume Platform UI for exactly one upload and exactly one clone.

No TTS generation, calibration, bakeoff generation, retry, replacement upload, second clone,
account purchase, full capture, Step 2 lock, Step 3, or publication is authorized.

This provenance record does not itself authorize Hume upload or clone creation.
