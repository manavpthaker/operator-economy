# Existing-performance conform helper

`presenter-look-transfer/_tools/conform_existing.py` writes only into this `final-r1` directory. It never generates provider media, renders a full episode, changes an active selection, or processes P00/P08.

Use the syncenv Python, which includes numpy:

```sh
PY=/private/tmp/claude-501/-Users-brownmanbrain-GitHub-operator-economy/82de42ec-ae77-42eb-8a88-f56e54114dda/scratchpad/syncenv/bin/python
TOOL=blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/_tools/conform_existing.py
"$PY" "$TOOL" check --manifest /absolute/path/to/room-selections.json --segment seg074
"$PY" "$TOOL" render --manifest /absolute/path/to/room-selections.json --segment seg074
```

Omit `--segment` to check/conform all entries supplied in the manifest. It can contain a completed subset of the14 existing segments. Existing output files are never overwritten; a failure leaves its intent, log and partial output for diagnosis. `EXAMPLE-seg074-pending.json` demonstrates the schema with the completed room pilot and deliberately no review verdict; it was checked only, not rendered.

Manifest fields: `record_type: ep009_existing_performance_room_selections`; exact hash bindings `base_build`, `source_audit`, `master`, `look_reference`; `selections` list. Every selection has `segment`, `pieces`, and optional `scoped_review`. Each piece has `id`, `source:{path,sha256}` for the selected room-native MP4, `source_frames:[inclusive,exclusive]`, and `original_frames:[inclusive,exclusive]` in the original segment's local frame coordinates. JSON paths are repository relative.

For ordinary segments the only piece is the segment ID, with both ranges `[0,original_frame_count)`. Long segments must bind `long_delivery` to `long-source-slices/guarded-r1/DELIVERY.json` and use these exact pieces:

|Segment/piece|Room-native source frames|Original local frames|
|---|---|---|
|seg019a|[0,333)|[0,333)|
|seg019b|[45,106)|[333,394)|
|seg071a|[0,97)|[0,97)|
|seg071b|[0,352)|[97,449)|
|seg071c|[31,96)|[449,514)|

All original local frames must appear once, consecutively. Original joins remain at333 and97/449; overlap context and end guards are excluded. Inputs must already have exact consecutive24fps timestamps and cover every selected frame. The helper rejects missing frames, alternate cuts, frame retiming and the old original video being supplied as a replacement. It scales1920×1080 to1280×720 without another crop. Existing1280×720 room outputs are accepted at their existing scale.

Audio comes exclusively from the hash-bound r3 master, exactly2000 mono48kHz PCM16 samples per frame. Only seg075's existing1080-sample program tail can require zeros. A WAV sidecar preserves exact PCM; the MP4 uses stereo AAC. The helper checks encoded audio against the sidecar, counts all output frames, and hashes every decoded original and replacement frame.

Per segment it writes MP4, PCM sidecar, full source-frame map, original/replacement frame hashes, encode intent/log, conform record, verification and `*-SELECTION.json`. The selection plus verification contain the exact fields consumed by `build_review.py`. Combine selection objects under the existing review builder's `replacements` key; P08 must be provided independently.

`scoped_review` is copied from explicit supplied review evidence; the helper never derives appearance or motion approval from successful rendering. Omitted review becomes `pending, flagged:true`. A claimed complete review must name its reviewer, method, limits and bound evidence. The full-review builder still independently rejects missing, incomplete or flagged performance/appearance reviews. Owner acceptance remains false in all conform outputs.
