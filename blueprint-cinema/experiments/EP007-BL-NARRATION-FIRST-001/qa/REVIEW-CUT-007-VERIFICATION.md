# Review Cut 007 verification

Status: **technically passed and ready for owner comparison.** This is an internal generated-film
test, not a V4 pass, production select, Step 4 authorization, or publication approval.

## What this cut tests

Whether a short generated human scene can carry the buyer's absence question through performed
causality rather than an illustrative pose:

1. the owner completes competent work;
2. an ordinary staff exception routes through her;
3. the buyer's question makes her look across the operation and register the dependency.

No caption, claim label, graphic annotation, dialogue, generated audio, slow motion, or post-camera
move is present.

## Exact conform

| Shot | Timeline frames | Selected source frames | Editorial action |
| --- | ---: | ---: | --- |
| competence | `[0,62)` | shot 1 `[34,96)` | caliper release through completed placement in the tray |
| dependency revealed | `[62,117)` | shot 2 r2 `[20,75)` | one turn, one low cue, then shared attention on the held part |
| recognition | `[117,186)` | shot 3 r2 `[27,96)` | held buyer eyeline, one turn across the operation, then a 12-frame settle |

All selections run at 1×, 24 fps, with no interpolation. The final look in shot 3 is approximately
60 degrees rather than the prompted 8–12 degrees. That is a prompt-fidelity miss, but it makes the
operation legible and remains one continuous attention change with no rebound. Owner review must
decide whether that broader turn feels like recognition or overperformance.

## Encoded artifacts

- Isolated scene: `hyperframes/renders/EP007-BL-NARRATION-FIRST-007.mp4`
  - SHA-256: `e2ec1167e1efcbe8a8304cf20d4e75c2aba7b1fa239e06c76786ff1e27456aa0`
  - 12,043,934 bytes
  - H.264 High, 1920×1080, progressive `yuv420p`, constant 24 fps
  - 186/186 frames decoded; 7.750 seconds
  - AAC-LC, 48 kHz stereo; locked narration source is 7.740 seconds
- Same-context scene: `hyperframes/renders/EP007-REVIEW-CUT-007-context-17.5-27.5.mp4`
  - SHA-256: `852fb746248b60bf6f356cbe1f59d1a017e74787b8b1b547702a2ccc419b8df8`
  - 7,635,294 bytes
  - 240/240 frames decoded; 10.000 seconds at constant 24 fps
  - audio packet hash exactly matches the Variant A context:
    `cf702e521c96e62d27f57be9ff82adcfa5e372381641bfd5694b3b1764011027`

Both files passed strict audio/video decode. The isolated scene has no black frames, no exact
duplicate decoded frames, and no freeze of 0.5 seconds or longer. Context-only freeze detections
are the pre-existing held evidence card before the insertion and the held paper frame after it.
Both outputs are true constant 24 fps with no variable-frame-rate findings. Isolated audio is
continuous at `-16.9 LUFS` integrated and `-4.3 dBFS` true peak; the expected final 10 milliseconds
are near-silent padding from placing a 7.740-second source on a 24 fps picture lattice.

## Frame and seam evidence

The three complete encoded selections match their declared source windows after scaling and
encoding at aggregate SSIM `0.9870–0.9891`; each is materially closer than an adjacent off-by-one
window. The six endpoint checks individually measured SSIM `0.9867–0.9895`:

- encoded `f0` / source shot 1 `f34`;
- encoded `f61` / source shot 1 `f95`;
- encoded `f62` / source shot 2 r2 `f20`;
- encoded `f116` / source shot 2 r2 `f74`;
- encoded `f117` / source shot 3 r2 `f27`;
- encoded `f185` / source shot 3 r2 `f95`.

`hyperframes check --strict` passed with zero lint errors, warnings, runtime errors, layout issues,
or motion findings. Visual and encoded-frame inspection found real hard cuts—not holds or
blends—at `f62` and `f117`, and clean context insertion boundaries at `f16` and `f202`. Context
frames `[16,202)` match the isolated render at aggregate SSIM `0.993389`.

Review evidence:

- `hyperframes/qa/rc007-final/story-contact-sheet.png`
- `hyperframes/qa/rc007-final/cut-contact-sheet.png`
- `hyperframes/qa/rc007-final/context-seam-contact-sheet.png`

## Known limitations

- The generated owner turns farther than directed in the final close-up. Do not record this as an
  exact performance-contract pass.
- The buyer and staff member are similarly cast and dressed, so the second man can momentarily read
  as a generated duplicate. The over-the-shoulder geography still separates their roles.
- The owner's cue reads more clearly toward the held component than toward a specific jig, drawer,
  or written procedure. The dependence is legible; its exact operating mechanism is less precise.
- Shot 1 is brighter than the reverse angles. It is plausible as the doorway-side angle but remains
  a visible exposure change for owner review.
- Generated live-action-style film remains illustrative `humanContext`, not documentary evidence.
- This verifies one 7.74-second passage. It does not validate the rest of EP007 or the provisional
  Step 3 process.
