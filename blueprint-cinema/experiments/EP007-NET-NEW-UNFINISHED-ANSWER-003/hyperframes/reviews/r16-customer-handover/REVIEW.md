# R16 customer relationship test

Status: isolated browser review candidate. Creative acceptance and encoded delivery remain unverified.

## Review

- Phone/player: http://100.101.49.30:3032/ (Tailscale connected; host Mac awake).
- Desktop Studio: http://localhost:3004/#project/r16-customer-handover
- Watch 30.208–35.083 seconds in the unchanged 71.5-second R15 sequence.

One request travels from customer to the owner's hands, pauses for nine frames, and reaches the team. On the narration's “not,” the owner is removed hypothetically. The customer, team, and completed request remain; a second request approaches an unresolved relationship. “Will customers stay?” and “If she leaves” make the question explicit without depicting customer loss as established fact.

This tests whether the animation makes a consequential dependency understandable within the existing 4.875-second slot. The remaining creative question is whether that before/after reads on first viewing at normal speed. The scene is a rough illustration, not a factual depiction of the filmed workshop's customer relationships.

## Evidence

- `VERIFICATION.json`: PASS. All 28 pinned R15 baseline files remain unchanged; 25 retained files are identical. All 18 clip declarations are preserved except the graphic identity. Original audio assets and placements are identical. Picture remains contiguous at 24 fps, 1,716 frames.
- Counterfactual begins at frame 781 / 32.541667 seconds, the nearest 24 fps frame to transcript “not” at 32.56 seconds.
- `.hyperframes/check-final.json`: strict check PASS with no lint, runtime, or sampled layout findings; all 10 sampled contrast checks pass. Motion assertions were disabled, so this is not a motion acceptance result.
- `snapshots/contact-sheet.jpg`: final full-frame stills cover owner contact, delivery to team, unresolved second request, and retained question, sting, title, and presenter scenes.
- `.hyperframes/request-route-final.png`: request pose-path diagnostic. Full-frame snapshots are the useful reference for the actual hand contact; diagnostic crops alone are insufficient.
- `.hyperframes/anim-map/animation-map.json`: final animation map generated. It reports 6 paced-fast and 25 collision flags. Its output includes child-local and mounted copies of tweens, and its long “dead zones” include video clips and deliberate holds. This is diagnostic output, not a clean motion pass.
- Live Chrome player inspected at desktop and 844 × 390 landscape viewport. Owner contact and unresolved state display correctly; backward and forward seeking restores their corresponding state. Playback advanced with narration enabled. No claim of a complete listening review, physical iPhone/Safari test, or encoded-compression QA.
- The phone player serves a staged set of 20 required runtime files. Each staged file matched its final source bytes and returned HTTP 200 through localhost and the Tailscale address. Stage, port, launcher, and hashes are recorded in `.hyperframes/phone-player.json`. Existing R15 player is preserved.

## Final source pins

- `index.html`: `1007c19ffcc2cce0496573479bc8d9f690bccf14acb65305f5cc3eddacc31348`
- `compositions/handoff.html`: `e162310d02fd193cd06658afe768ef3ed5a4f40ff42fb14c1a1b4719fa6e7e98`
- Remaining authored pins: `VERIFICATION.json`.

No paid generation, MP4 export, canonical gate update, commit, push, or publication was performed for R16.
