# Private review execution

Run from this HyperFrames directory with CLI 0.8.31. The user's current full-edit request authorizes the local review render. Keep the original locked WAV as the only audio track; every selected scene video is muted and starts at source zero. Avatar 205 is selected for review, not owner-approved.

1. Final check: `HYPERFRAMES_RUN_ID=ep007-revision-003-final-001 npx --yes hyperframes@0.8.31 check --snapshots --at 0,7,14.766667,14.8,18,21.266667,21.3,28,35.066667,35.1,41,48.5,48.533333,54,59.833333 --json`.
2. Animation map: run the repository's `.agents/skills/hyperframes-animation/scripts/animation-map.mjs` against this directory with `--frames 4 --width 1280 --height 720 --fps 30 --out .hyperframes/anim-map`. The machine report is `.hyperframes/anim-map/animation-map.json`; interpret flags against the authored source and actual snapshots.
3. Studio: `npx --yes hyperframes@0.8.31 preview --background`. Verify the returned project URL and `preview --status`; preserve the server for the lead's independent review.
4. Local render: `HYPERFRAMES_RUN_ID=ep007-revision-003-final-001 npx --yes hyperframes@0.8.31 render --fps 30 --quality high --output ../review-media/ep007-revised-higgsfield-hyperframes-test.mp4`.
5. Verify 1,796 video frames at 30 fps, the exact first and last visible frames, all cut boundaries, and the encoded audio against `../inputs/opening-59.86.wav`. Bind the actual output hash and probe to the run ledger.

The lead owns independent performance/audio review and the episode ledger. No publication, external feedback, public issue or canonical gate change is authorized by this private test.
