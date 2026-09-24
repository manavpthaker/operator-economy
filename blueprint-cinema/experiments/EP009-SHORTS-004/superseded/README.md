# Superseded — do not pick these up

The four r3 renders in `blueprint-cinema/experiments/EP009-SHORTS-003/` are **superseded by
this revision** and must not be used for upload, review, thumbnails, copy or any downstream
derivative.

| r3 render | Superseded by |
|---|---|
| `EP009-SHORTS-003/01-second-commission/review-r3.mp4` | `EP009-SHORTS-004/01-second-commission/review/01-second-commission-r4.mp4` |
| `EP009-SHORTS-003/02-cheap-tools/review/ep009-short02-avatar-r3-review-final.mp4` | `EP009-SHORTS-004/02-cheap-tools/review/02-cheap-tools-r4.mp4` |
| `EP009-SHORTS-003/03-guest-relationship/review/ep009-short03-avatar-forward-r3-review.mp4` | `EP009-SHORTS-004/03-guest-relationship/review/03-guest-relationship-r4.mp4` |
| `EP009-SHORTS-003/04-wrong-number/review-r3.mp4` | `EP009-SHORTS-004/04-wrong-number/review/04-wrong-number-r4.mp4` |

Also superseded:

- `EP009-SHORTS-003/REVIEW-PACKAGE.json` and the review page it points at,
  `assembly/qa/ep009-shorts-r3/index.html`. The current page is
  `assembly/qa/ep009-shorts-r4/index.html`.
- The `cliffhanger` block in every Short of `EP009-SHORTS-003/COPY-PACKAGE.json` and
  `COPY-PACKAGE.md`. `cliffhanger_line` is retired by `docs/content-rubric.md`. The titles,
  descriptions, pinned comments and on-screen cue specifications in that package are **not**
  superseded; they were applied here, with the deltas recorded in `../COPY-DELTA.md`.
- `EP009-SHORTS-003/PHONE-PLAYBACK-QA.json` and `VERIFICATION-EVENT.json`, which describe the
  r3 renders.
- `EP009-SHORTS-003/03-guest-relationship/source-contract.json`'s `next_word_excluded` record.
  That word, `W000584` "Nobody", is now inside the cut.

## Why nothing was deleted

The r3 renders, contracts and checks stay where they are. They are the evidence the
decision-log events for r3 hashed, and deleting them would break
`decision_log.py validate --evidence` for every earlier event. This file is the marker; the
bytes are the history.

## What is still live from r3

- `EP009-SHORTS-003/DIRECTION.md` — the avatar-forward direction. Still the governing look and
  identity. Short 01's presenter share of speech falls under it (0.665 to 0.516); that trade is
  flagged for the owner in `../STANDARD-JUDGMENT.md`.
- The accepted look-transfer natives under
  `EP009-FULL-BUILD-001/presenter-look-transfer/room-r1/`, which this revision re-read
  unchanged.
