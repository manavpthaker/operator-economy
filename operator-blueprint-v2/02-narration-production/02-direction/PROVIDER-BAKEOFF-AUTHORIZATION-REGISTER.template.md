# Provider Bakeoff Authorization Register

Template version: proposed Step 2 v0.3.

This is an index, not a combined authorization. Every row points to its own separately signed and
consumed record created from `PROVIDER-EXTERNAL-ACTION-AUTHORIZATION.template.md`.

| ID | Exact scope | Friendly action | Authorization path/SHA-256 | Status | Consumption/outcome receipt path/SHA-256 | Grants next scope |
| --- | --- | --- | --- | --- | --- | --- |
| AUTH-01 | `elevenlabs_sample_retrieval` | ElevenLabs read-only voice metadata and exactly one original-sample retrieval | | draft | | no |
| AUTH-02 | `hume_clone_creation` | Hume UI upload of one provenance-bound sample and exactly one clone creation | | draft | | no |
| AUTH-03 | `elevenlabs_calibration` | ElevenLabs short calibration: P1/P2 × E1/E2 | | draft | | no |
| AUTH-04 | `hume_calibration` | Hume short calibration: P1/P2 × H1/H2 | | draft | | no |
| AUTH-05 | `long_form_continuity_and_later_pickup` (human scope; not initial machine enum) | Later 3.5-to-4.5-minute continuity test plus several-hours-later same-word pickup for eligible providers | | not_created | | no |

## Separation checks

- Four initial authorizations exist as four files: yes / no
- No authorization was inferred from credentials, login, earlier N4A, or another row: yes / no
- AUTH-05 was absent until blind short scoring was signed and unsealed: yes / no
- No row uses capture phase `full`: yes / no
- No row grants N4B or Step 3: yes / no
- Reviewer/date:
