# R11 opening source audit

2026-09-09. Read-only wave-zero source audit; no creative approval, generation, provider contact, experiment modification, or canonical gate change.

## Decisive finding

**No existing selected Seedance presenter take speaking the cold-open first sentence was found in the inspected records.** The selected 404/407 pair covers the introduction at narration master **48.520–59.860**, not “A buyer is sitting across the table…”. Reusing its talking mouth over the opening words would be a mismatched speech substitution.

The search covered presenter001, Higgsfield001–003 and premium004 records. The other successful Seedance presenter test, Higgsfield001 P, speaks the later personal disclosure at master591.050–596.650; it failed fixed-VO timing. Presenter001 repair-r24 produced no Seedance video following a portrait-policy rejection. Absence here is a local-record finding, not an inventory assertion about every provider account.

## Selected avatar: proven properties and limits

Files under `blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/`:

- `404.mp4`: selected Seedance2.5 performance; SHA-256 `a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd`. Fresh probe:1920×1080,24fps,289 picture frames/12.041667s; generated audio12.05s. Prior independent QA established changed recording and a delayed initial onset. This is a performance reference, not exact-audio footage.
- `407-seedance-sync3.mp4`: existing Sync3 derivative of404; SHA-256 `1752e0356a3c0b86cbee70849e2b40df6de4ba483db103e9f2ef9904d606b965`. Fresh probe:1920×1080,24fps,273 picture frames/11.375s;48kHz mono audio11.34s. Prior independent QA measured0.99980151 recording correlation and zero lag in all22 active windows. It also found sampled head/blink continuity with404. Those earlier measurements were inspected, not rerun in this audit; they do not prove phoneme-perfect lip sync.
- Exact supplied passage: “This is The Operator Economy, where we show you how to use AI to build, own, and operate a sustainable business of one. Today we are building a sale readiness practice.” Source audio is Higgsfield002 `inputs/identity-11.34.wav`, SHA-256 `8d80cbb01c89533cb5f3338887818aaae00107835b1f9c166071502e077ab0f7`.

The existing edit uses407 at master48.52–59.50, cutting before the next sentence's audible onset. Its four-pixel bottom overscan at720p removes a source-edge noise strip; source timing stays unchanged. Preserve that safeguard in any reuse. The separate model-selection record does not confer final lip-sync or episode approval.

## Reusable workshop sources

Base: `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/`. All below were freshly hash-verified against premium004 staging records and probed as silent1916×1080/24fps video. These are historical selections, not a proposed R11 edit.

| Source relative to base | Available duration | Existing source select | Existing master placement |
|---|---:|---:|---:|
| `r6-character-first/public/media/shot-01.mp4` |15.041667s|0–14.77|0–14.77 in premium004|
| `r7-rapport-pause/public/media/shot-a.mp4` |11.041667s|0.320–4.153333|10.920–14.753333 in retained R8/R10 extract|
| `r8-context-coverage/public/media/shot-b.mp4` |8.041667s|0–6.233333|14.77–21.003333 in premium004|
| `r8-context-coverage/public/media/shot-c.mp4` |9.041667s|0–6.916667|21.003333–27.92|
| `r10-film-to-presenter/public/media/shot-d.mp4` |8.041667s|0.416667–7.576667|27.92–35.08 in premium004|

Premium004 removed an R6-to-R7 same-angle join at10.92 after QA found a pose jump. Do not restore that join without new continuity review. R8's earlier buyer select was6.25s; premium004's slightly shorter duration follows its14.77 start. Preserve frame-rate-specific selection distinctions when conforming.

## Applicable comparison learnings

1. HyperFrames assembled both earlier and later footage; it did not generate the acting. Higgsfield002/003 changed to Wan2.7, a new cast/office, blocking and coverage together. Those tests cannot isolate a platform or model-quality cause.
2. Higgsfield003 replaced the questioner's face with paperwork and the owner's close-up with a wider two-shot. That reduced visible enacted interaction. The earlier liked film already used close-ups; close-ups alone do not explain the later interrogation reading.
3. Premium004 controlled the workshop start image, written performance prompt and nine-second request across three models. Among those individual takes, Kling401 was closest to the intended stop; Seedance402 stopped early; CinemaStudio403 stopped several seconds early. This supports a choice among takes, not a universal ranking. The restored edit retained original Kling coverage.
4. Exact audio support is not proof of exact audio delivery. Seedance404 supplied the preferred motion but changed the recording;407 repaired speech against the locked WAV. Recording correlation and technical checks remain separate from normal-speed acting and mouth judgments.

## Checks and scope

All three work-order input hashes matched before and after inspection. Six staged source hashes and both selected presenter source hashes matched; media probes confirmed dimensions, cadence and available duration. No current full-decode, waveform rerun, visual playback, or new creative assessment was performed. Episode-level `README.md`, `episode.json`, and `input-lock.json` are absent from this isolated agent workspace; no canonical approval was inferred. The exact source selection and cold-open presenter deficit remain for the orchestrator to resolve.
