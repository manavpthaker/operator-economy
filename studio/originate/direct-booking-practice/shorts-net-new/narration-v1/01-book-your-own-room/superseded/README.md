# Superseded local ASR attempt, guide 01

The first exact-copy run reported `accepted: false` at token 43. The divergences were
`twenty` / `20`, `forty` / `40` and `ten` / `10`: Whisper wrote digits for number words the
narrator spoke correctly. The gate's normalizer compared surface strings, so an orthographic
difference failed a guide that is in fact exact.

This is kept as evidence of a tooling false negative, not a narration defect. The normalizer now
compares numeric values, so `twenty` and `20` reconcile while `thirty` and `twenty` still fail.
No provider call was made for this attempt; ASR is local and free. The guide WAV, the Google
receipt, the raw response and the submission intent were never touched.
