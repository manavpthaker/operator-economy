# V2 episode workspaces

Status: naming and Step 1 workspace rules are canonical under V2 Step 1 v1.0. The Step 2 workspace layout is proposed for narration-production testing. No V2 episode exists.

Future episode folders use:

```text
EP###-kebab-case-slug
```

Examples are illustrative only:

```text
EP007-example-opportunity
EP008-another-example
```

Do not create either example.

## Number assignment

- Step 0 candidates do not receive episode numbers.
- `eligible` candidates do not receive episode numbers.
- Step 1 assigns the next number only after a current promotion record passes Gate E1.
- The assigned number is three digits and becomes part of the folder name and episode identity.
- An assigned number is never reused. A cancelled episode keeps its number and receives a cancellation record.
- A slug may be clarified with a rename record, but the episode number never changes.

## Proposed episode layout

```text
episodes/EP###-slug/
├── README.md
├── 00-intake/
│   └── promotion-package/
├── 01-editorial/
│   ├── handoff.md
│   ├── editorial-contract.md
│   ├── operator-canvas.md
│   ├── narrative-spine.md
│   ├── episode-outline.md
│   ├── voice-and-comedy-map.md
│   ├── claims-map.md
│   ├── script.md
│   ├── performance-readthrough.md
│   ├── editorial-voice-conformity.md
│   ├── review-disposition.md
│   ├── editorial-lock.md
│   └── narration-handoff.md
├── 02-narration-production/
│   ├── editorial-handoff-checklist.md
│   ├── performance-direction.md
│   ├── voice-and-capture-lock.md
│   ├── raw/
│   ├── take-register.md
│   ├── take-reviews/
│   ├── selects/
│   ├── pickups/
│   ├── pickup-log.md
│   ├── narration-edit-decision-list.md
│   ├── master/
│   │   ├── narration-master.wav
│   │   └── narration-review.mp3
│   ├── lexical-conformity.md
│   ├── word-transcript.json
│   ├── technical-qc.md
│   ├── independent-listen.md
│   ├── narration-lock.md
│   ├── visual-translation-handoff.md
│   └── change-requests/
├── 03-visual-translation/
├── 04-preproduction/
├── 05-production/
├── 06-resolve-finish/
├── 07-publishing/
└── 08-distribution/
```

The top-level numbered directories define process standards. The numbered directories inside an episode workspace hold that episode's artifacts. Files do not move between top-level stage folders as the episode advances.

The Step 2 `raw/`, `selects/`, `pickups/`, and `master/` directories are episode-workspace locations, not permissions to record, generate, or commit audio. Provider calls and narrator usage still require explicit authorization. Large or private media follows the repository's approved storage policy rather than being committed by default.

## Current state

This directory contains only this rule document. It does not contain an episode workspace, assign an episode number, or imply that a candidate has been promoted.
