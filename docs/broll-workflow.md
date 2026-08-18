# OE Footage Workflow

## Current state

The Shorts pipeline has an operational B-roll path: clip selection proposes timestamped queries, `fetch_broll.py` searches Pexels, `broll.json` supports approve/reject/swap review, `prepare_render.py` remaps timings, and `BRollOverlay.tsx` inserts muted full-frame footage.

Long-form now resolves approved `footage_manifest.json` entries, stages their media in Remotion public assets, and renders frame-accurate in/out points through `BRollScene.tsx`. Missing media is a conspicuous render blocker and `prepare_longform.py` stops before render when a requested manifest entry is absent or invalid. Pexels is currently the only automated contextual-footage provider, and `PEXELS_API_KEY` is not currently available in the loaded repository environment.

## Target flow

`script beat -> footage role -> source route -> candidates -> rights gate -> selection -> footage manifest -> storyboard timecode -> Remotion -> preview gate`

### 1. Assign a story role

Every footage beat must be one of:

- `human_context`: a person performing the work in the actual environment.
- `market_force`: the platform, intermediary, institution, or branded surface shaping the outcome.
- `proof`: receipt, source document, dashboard, number, or observable result.
- `process`: the mechanism operating step by step.
- `outcome`: the human or business state after the mechanism works.

### 2. Route sourcing by role

Use sources in this order:

1. Original capture or screen recording for `proof` and `process`.
2. Licensed archival, company press assets, or permissioned product footage for `market_force`.
3. Specific licensed footage from Pexels or Pixabay for `human_context` and `outcome`.
4. Generated plates only when reality cannot reasonably be captured; label them internally as generated.

Never use footage merely to fill the screen. Generic typing, empty offices, abstract technology, decorative drone shots, and semantically adjacent stock fail review.

### 3. Search and review

Generate three concrete queries per beat, including subject, action, setting, framing, and exclusions. Download proxies, not final assets, and produce a contact sheet or proxy reel. A human selects the semantic match; the first search result is never auto-approved.

```bash
# Created automatically after plan_assets when the final storyboard uses B-roll
python scripts/originate/footage_manifest.py init originate/<slug>/script.json

# Searches Pexels only for human_context/outcome; writes JSON + an HTML proxy review
python scripts/originate/source_footage.py search originate/<slug>/script.json

# Explicitly promote one reviewed candidate
python scripts/originate/source_footage.py approve originate/<slug>/script.json \
  <manifest-id> <candidate-id> --faces-review cleared \
  --source-in 1.2 --source-out 6.8

# Hard rights/file/timecode/hash gate
python scripts/originate/footage_manifest.py validate originate/<slug>/script.json
```

### 4. Record provenance

The canonical `footage_manifest.json` entry must include:

```json
{
  "id": "hotel-checkin-01",
  "role": "human_context",
  "narration_anchor": "the hotel did the work",
  "preview_eligible": true,
  "provider": "pexels",
  "asset_id": "...",
  "page_url": "...",
  "creator": "...",
  "license": "...",
  "license_checked_at": "YYYY-MM-DD",
  "downloaded_at": "...",
  "sha256": "...",
  "faces_review": "cleared",
  "source_in": 2.4,
  "source_out": 7.8,
  "crop": "16:9 center-right"
}
```

### 5. Insert and gate

Storyboards reference manifest IDs rather than raw URLs. Preparation validates the selected file, duration, rights fields, crop, and timeline bounds before copying it into Remotion. The first 30 seconds must contain at least one human beat, one market-force or proof beat, and one process or outcome beat. No unresolved footage ticket may reach render approval.

## Implementation status

Implemented:

1. Long-form `BRollScene` renders `source_video`, source in/out points, crop, and focal position.
2. `footage_manifest.json` records role, rights, hash, face review, timecodes, and crop.
3. Role-aware sourcing sends Pexels only `human_context` and `outcome`; other roles become capture/artifact tasks.
4. File existence, checksum, `ffprobe`, source bounds, unresolved media, and first-30-second role coverage are hard checks.
5. Candidate search emits `footage_candidates.json` and a playable `footage_candidates.html` review.

Remaining:

1. Adapt the Shorts `broll.json` path to consume the same manifest schema.
2. Add Pixabay or a paid archival provider only if Pexels coverage proves insufficient.
3. Add recorded provider fixtures and a one-frame episode B-roll render fixture to CI.
