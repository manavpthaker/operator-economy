# EP007 Shorts 02–04 Original C transfer

`transfer_shorts_02_04.py` is a separate one-attempt-per-short ElevenLabs Voice Changer runner. It does not resume the stopped narration-v3 batch. No automatic retry is implemented. `check` makes **no network request**; `preflight` reads the ElevenLabs account and voice without generation; only `transfer` posts paid audio. The accepted output is still pending final Original C exact-copy ASR and owner review of the finished private video. This runner does not release or upload anything.

The runner is currently held by guide QC, not provider balance:

- Short 02: preserved guide has a documented opening exact-copy failure. Do not transfer this take. A new guide attempt needs separate owner direction; a local ASR discrepancy can only be overturned by an owner listening source and independent exact-copy evidence.
- Shorts 03–04: preserved guides have tail-silence holds. A derived copy may append at most 500 ms of zero PCM samples without changing any source sample. Re-probe and re-transcribe that derived file; preserve the original guide.

Each Short needs these local files before `check` passes:

1. `GUIDE-ASR.json`, following the Short 01 `GUIDE-ASR.json` schema: `accepted_for_transfer_preflight: true`, `status` beginning `pass_exact_normalized_locked_words_and_timing`, and hashed `media`, `script`, and `transcript` references. The runner independently recomputes token equality and word-timing bounds from the transcript.
2. If a derived tail exists, `DERIVED-GUIDE-REPAIR.json` following Short 01's record. The runner independently checks the original PCM is a byte-exact prefix and the appended frames are all zero, no more than 500 ms.
3. If `HOLD.json` or a held `GUIDE-QC-V1.json` exists, `GUIDE-HOLD-RESOLUTION.json` with `record_type: ep007_guide_hold_resolution_v1`, `status: pass_resolved_with_preserved_evidence`, `short_id`, `resolution_kind`, `guide_asr: {sha256}`, and `prior_holds: [{path, sha256}]` for every held record. A tail hold requires `resolution_kind: lossless_silence_tail_repair`. An opening exact-copy hold requires `resolution_kind: owner_listened_and_alternate_asr_proved_exact_copy` plus `owner_listening_source: {path, sha256, verbatim}` pointing into the owner decisions folder.
4. `GUIDE-TRANSFER-SELECTION.json` with `record_type: ep007_guide_transfer_selection_v1`, `status: pass_selected_for_original_c`, `short_id`, and `{path, sha256}` references named `selected_guide`, `source_guide`, `google_receipt`, `guide_asr`, `derived_repair` (derived only), and `hold_resolution` (when applicable). This immutable selection is hash-bound into preflight and the submission intent.

Run one short at a time, after its QC records are genuinely complete:

```bash
python3 studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/transfer_shorts_02_04.py check short-03-how-you-charge
python3 studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/transfer_shorts_02_04.py preflight short-03-how-you-charge
python3 studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/transfer_shorts_02_04.py transfer short-03-how-you-charge
```

The runner pins the locked scripts, broad owner source/event, Original C voice ID and settings, and provider helper. It requires a live unshared generated Original C voice, estimates at 1,000 credits/minute, and refuses a transfer when prior Shorts 02–04 actual usage plus the next forecast would exceed the aggregate 3,200-credit operational ceiling. A written submission intent is terminal for that Short even after a timeout or other uncertain result. The provider may charge differently than the forecast; exact cost must be present in the response header before a later Short can proceed.
