# Calibration media ledger

The calibration receipts and hashes are versioned. The provider-raw PCM and review WAV files stay
local because this repository does not have Git LFS and its existing policy keeps large generated
media out of Git.

Current local batch: `20260823T200928Z`

- Media size: approximately 142 MB
- Provider raw: five immutable native-PCM files
- Working review media: five 48 kHz, 24-bit, mono PCM WAV files
- Capture receipt: `20260823T200928Z/provider-raw/capture-run-receipt.json`
- Conversion receipts: `20260823T200928Z/working/*.conversion.json`
- Human-readable hashes and technical findings: `../N4A-CALIBRATION-TECHNICAL-REVIEW.md`

Do not delete or regenerate this media while the N4A owner decision is pending. A regeneration
requires a new bounded provider authorization. Before this fixture becomes a production episode,
choose a durable media store that preserves immutable raw bytes and recorded SHA-256 values.
