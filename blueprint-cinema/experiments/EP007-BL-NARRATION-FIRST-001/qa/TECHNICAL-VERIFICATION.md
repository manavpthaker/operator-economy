# Narration-first encoded verification

Status: **technical pass; Shot 1 behavioral fail.** This is not a production or gate approval.

## Encoded artifact

- Asset: `hyperframes/renders/EP007-BL-NARRATION-FIRST-001.mp4`
- SHA-256: `100994c4e207378edb1eaceeffcf3161e7eb9fdb7c96f798d804b5c8e315faad`
- H.264 High, 1920×1080, progressive, 24 fps CFR
- 186 declared and decoded frames; 7.750-second picture
- AAC-LC, 48 kHz stereo; 7.740-second program audio
- Full video and audio decode: pass
- Black frames or intervals: none
- Exact consecutive duplicate frames: none
- Freeze of 0.5 seconds or longer: none
- `repeat_pict`: zero throughout
- BT.709 matrix and limited range are tagged; transfer and primaries are unset

The ten-millisecond picture tail is normal video-frame and AAC-block quantization. Decoded audio is
byte-identical to the isolated A arm: PCM SHA-256
`98b18a062770a3fd4ed5f14e6dbc035725b695ff6b5eb84ef0edfc7d7da2735c`.

## Direction-plan review

### Shot 1 — fail

The buyer's gaze move is smooth and phrase-correct: it begins around `1.2–1.3s` on “somebody,”
settles toward the workshop around `2.1s`, and holds through “looks.” But his mouth and jaw visibly
articulate during the move, especially frames 28–52 (`1.167–2.167s`). The owner also breaks the
locked eyeline and looks down near the end of the shot.

That violates the buyer-only action and no-lip-movement rules. It is a blocking failure because it
can make the image read as silent consultation rather than scrutiny.

### Shot 2 — technical pass, perceptual risk

The owner stays sharp through “Back to her question, then.” The rack begins around `5.9s` during
“here,” resolves across “if you are not around,” and holds through “for a month.” It lands on the
parts drawers, tools, and repair bench rather than the buyer or general blur.

The blind review nevertheless read the late owner softness as possible synthetic facial
degradation. That is a perceptual risk to test in the owner's normal-speed review, not a mechanical
focus failure.

## Cuts and boundaries

- The internal cut quantizes to frame 62 at `2.583333s`, immediately after “looks.” There is no
  black frame, blend, duplicate, gap, or flash.
- Both surrounding Boundary Ledger cuts are mechanically clean.
- The exit into the rough operating model is semantic but not a convincing graphic match: the
  sharp tool-drawer geometry does not align clearly with the first broken pencil baseline.

## Portrayal and prohibited implications

The owner remains calm and competent. Exactly two people remain present. No gross anatomy failure,
readable document, logo, price, handshake, key exchange, contract, sale, agreement, business
failure, or resolved outcome appears.

