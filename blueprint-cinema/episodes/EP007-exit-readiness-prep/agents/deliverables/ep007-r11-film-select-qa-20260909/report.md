# R11 film-select source QA

Date: 2026-09-09. Role: independent QA reviewer. Scope: read-only source/frame inspection for the isolated R11 proposal; no composition edits, provider work, production approval or state change. Status: partial, finalized at orchestrator request after a separate provider failure.

## Verified inputs

- EDIT-PLAN.md: `e9609c62b9c0f10e0948d6c46dfb6eeb84251892227c52cc50a99c828330cf6d`, matches work order.
- R6 shot-01.mp4: `e0b4067004d83f4ba00be589d72ffc43d8305319a63be2217f19d594d6d2521c`, matches work order.
- R10 shot-e.mp4, additionally inspected as acceptance-check source: `36ddf54067fb28c2223a81ce8dcac31298112cdd5c6b862eeb6e772ae10598a2`. This third source was not hash-pinned in the issued order; the observed hash matches the source history supplied to the reviewer. Orchestrator should pin it before integration.

R6 and E are H.264, 1916×1080, 24 fps. R6 is 361 frames / 15.041667 seconds; E is 241 frames / 10.041667 seconds. Both have no reported audio stream. The proposed source ranges are in bounds.

## R6 continuous-source reframes

Keep source time equal to master time for all three pieces. This retains motion continuity and avoids the R6-to-R7 same-angle pose discontinuity. Recommendations below are source-pixel rectangles `(x, y, width, height)`, displayed at 1280×720. No zoom animation is proposed.

| Master/source range | Framing | Proposed source rectangle | Evidence and limits |
|---|---|---|---|
|4.041667–7.708333|Wide establishment|Full 1916×1080 source, cover-fit to 1280×720|1 fps samples across the specified early-to-late source establish both people, table and shared paper. Cover-fit trims approximately 1.125 source pixels top and bottom; no blank edge.|
|7.708333–11.25|Owner-focused close-up|`(40, 0, 1024, 576)`|A nearby `(40, 20, 1024, 576)` crop was actually inspected at source9.0. Face and upper torso remain readable; buyer is excluded without a bisected face. Recommended y=0 adds headroom. That exact y=0 crop and both edit boundaries remain tentative until integration review.|
|11.25–14.75|Buyer-focused close-up|`(892, 0, 1024, 576)`|A nearby `(892, 20, 1024, 576)` crop was actually inspected at source13.0. Face and upper torso remain readable; owner is excluded. Recommended y=0 avoids tight hair clearance. Exact y=0 and both edit boundaries remain tentative until integration review.|

Each close-up rectangle is fully inside the 1916×1080 source and upscales 1.25× to the requested review resolution. This is an approximately 1.87× digital punch-in relative to the wide, not a new camera angle. Mild image softness is the trade-off. Both people look down toward the established paper; owner remains directed down/right and buyer down/left. These crops preserve geography but cannot create eye contact or rapport absent in this R6 source. Use them for the numbers/setup beats, not as proof of an interpersonal exchange.

Observation: buyer's mouth is visibly open in some later R6 samples, including source13.0. This is not synchronized dialogue; keep the scene explicitly illustrative narrated dramatization. Actual speed/mouth cadence and the cut into retained buyer-question coverage still need audiovisual review.

## E aftermath select

Proposed source4.75–9.75 is a valid five-second range with approximately0.292 seconds of post-handle. In the 2 fps contact strip covering that range, the owner's lips appear closed, her attention stays down, and the buyer holds his gaze toward her. Hands remain settled at the table with small natural repositioning. No obvious hand duplication, prop teleport, screen-direction reversal or background reset appears in these samples. Wardrobe, green binder, shared paper, pencil and keys preserve the workshop geography.

Interpretation: the range can carry quiet human consequence after the arithmetic graphic. It does not demonstrate a numerical loss or a completed deal. The buyer's attentive gaze makes the two-shot more relational than the early R6 setup.

Limit: this is sampled visual evidence, not a continuous at-speed lip/hand stability verdict. Tiny transient artifacts may fall between samples. The complete edited five-second hold should be watched with the original narration before acceptance. The reaction may read as subdued reflection more than acute stress; do not describe stress as an objectively verified performance result.

## Inspection evidence and checks

- Exact input SHA-256 checks: pass.
- ffprobe codec, dimensions, timebase, duration and frame count: pass.
- Source-range and crop geometry bounds: pass.
- Locally viewed R6 wide contact sheet at 1 fps, E contact sheet at 2 fps, plus source9.0 owner crop and source13.0 buyer crop.
- Contact sheets and crop diagnostics are under this packet's ignored `diagnostics/` folder; `git check-ignore` confirms the rule.
- No normal-speed assembled cut, adjacent B/C/D boundary review, full-frame temporal artifact test or HyperFrames runtime review was completed by this worker.

The episode-level README, episode.json and input-lock were not present at the requested episode root in the file inventory. This is a wave-zero source audit bound to the experiment work order, not a canonical episode review. Do not infer an approved input gate.

## Handoff

Use the bounded geometry as a draft recommendation only. Before locking, review the actual 7.708333 and11.25 crop changes and14.75 handoff at normal speed, then review E with the consequence narration. Preserve the original source files and use composition crops, not destructive transcodes. No new generation is needed for these film selections.
