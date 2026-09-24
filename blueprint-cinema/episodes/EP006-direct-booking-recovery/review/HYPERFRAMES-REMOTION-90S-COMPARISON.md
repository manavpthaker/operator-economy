# EP006 90-second HyperFrames / Remotion comparison

## Outcome

Both 0-90 second treatments rendered successfully against the same hash-verified EP006 narration. The Remotion control is the clearer blueprint/story explanation. The native HyperFrames candidate gives a substantially better indication of the intended finished visual language: editorial typography, physical objects, deliberate reveals, a clear show-identity card, and a clear episode-title card.

This is a creative/runtime comparison, not a production-gate decision. The HyperFrames candidate is 1080p while the existing Remotion control is a low-resolution 540p review render, so image sharpness is not a fair runtime discriminator. The useful comparison is composition, motion language, hierarchy, and comprehension.

## Shared test basis

- Episode: `EP006-direct-booking-recovery`.
- Window: exactly `0.000-90.000` seconds.
- Narration source: `studio/originate/direct-booking-recovery/vo/full-episode.mp3`.
- Locked narration SHA-256: `95e90a1ebb5dfbc6e13bc2efd12915cea9f15807199b0301cd3f63d59cb8e468`.
- No generated voice, music, sound effects, captions, stock, AI imagery, third-party UI, vendor logo, or fake evidence was added.
- The 60 percent statement remains a conspicuous proof/source-ticket boundary, not approved evidence artwork.

## Rendered outputs

| Treatment | File | Media facts | SHA-256 |
|---|---|---|---|
| Remotion control | `delivery/generated/EP006-greybox-deck-brand-title-prototype.mp4` | H.264, 960x540, 30 fps, AAC stereo 48 kHz, 90.048s container, 4,598,932 bytes | `0665fc2261723b5587a6e3babc765b62c61e84fdc7297109c4e5660d1b751048` |
| Native HyperFrames | `delivery/generated/EP006-hyperframes-native-90s.mp4` | H.264, 1920x1080, 30 fps, AAC stereo 48 kHz, exactly 90.000s, 10,094,247 bytes | `4eb40bfc8a264150035963830a0b5ef96999447656eb1045a3f2b6eba1163b81` |

The matched visual sheet is `review/generated/runtime-comparison/EP006-remotion-vs-hyperframes-contact-sheet.png`. Its first two rows are Remotion and its final two rows are HyperFrames; columns sample 5, 12, 19, 25, 30, 36, 47, 60, 78, and 88 seconds.

## What the visual test shows

### Remotion control

- Strength: the cause-and-effect story is explicit, with large declarative sentences and obvious guest -> OTA -> hotel -> repeat-payment relationships.
- Strength: the show identity and episode title now exist at the proper VO handoff.
- Limitation: it still reads like a well-designed storyboard or presentation prototype. The repeated diagram vocabulary and explanatory labels make the construction visible.
- Best use: Blueprint Cinema data contracts, deterministic integration, and a comprehension control.

### HyperFrames candidate

- Strength: it reads more like an authored editorial film made from composed slides, not a camera wandering around a system map.
- Strength: the brass key, guest token, inn, OTA gate, and commission ledger recur without forcing the whole network onto the screen.
- Strength: `THE OPERATOR ECONOMY` appears as a dedicated identity plate around 28-33 seconds, followed by `EP006 / DIRECT BOOKING RECOVERY` around 33-40 seconds.
- Strength: the final accumulation sequence makes fragmented hotel ownership visually legible without generating software interfaces.
- Limitation: it is a bounded opening treatment, not yet connected to the full 915.55-second Blueprint Cinema timeline or downstream asset/evidence approvals.
- Best use: the leading look-and-feel candidate for the next greybox iteration.

## Validation and render evidence

- HyperFrames CLI: `0.8.4`.
- Storyboard assembly: 9 frames, 90.000 seconds, six verified cross-track transitions.
- `npm run lint`: pass with 0 errors; 120 non-blocking authoring warnings, mainly frame-prefixed numeric IDs, optional Studio edit IDs, and composition-size guidance.
- `npm run check`: pass; 0 runtime errors, 0 layout errors, 0 motion errors, and all 51 sampled text checks pass WCAG AA.
- Snapshot QA: 11 deterministic snapshots plus two contact sheets; visually inspected at 5, 12, 19, 25, 30, 36, 47, 60, 78, 87.3, and 88 seconds.
- Preview server: returned HTTP 200 at `http://127.0.0.1:3018` during validation.
- HyperFrames full render: all 2,700 frames rendered; video and audio both report 90.000 seconds.
- Media QA: no detected black interval of 0.5 seconds or longer and no detected audio silence of 1.0 second or longer below -45 dB.
- Rendered narration loudness probe: -12.95 LUFS integrated, -2.10 dBTP, 3.70 LU LRA; audio was not remastered in this comparison.
- Blueprint Cinema tests: 43 passed.
- Existing Remotion renderer: TypeScript check passed.
- Current state check: `greybox_ready`; blocking gate remains `greybox_approved`.

## Agent packets and root integration

Nine frame-scoped work orders (`hf90-frame-01` through `hf90-frame-09`) ran in three waves of no more than three concurrent workers. Every declared input hash matched, all nine work orders and all nine deliverables validated, and every deliverable records `approval_claimed: false` and `production_state_changed: false`. No packet was rejected.

Root integrated the packets serially and made bounded project-level corrections after integration: safe element selection for numeric IDs, precomputed SVG path lengths, local OE font staging/paths, deterministic GSAP initialization, removal of layout-property animation, intentional overlap annotations, a darker accessible brass text role, and final guest/ticket spacing. Workers did not edit the comparison project, canonical episode JSON, production state, approval records, or shared renderer entry points.

## Tool-install boundary

The user-requested `npx skills add heygen-com/hyperframes --full-depth` installed 26 local skill packages under repository `.agents/skills/`. HyperFrames initialization also installed its nine core skill packages into the user's `~/.agents/skills` and `~/.claude/skills` locations. HyperFrames authentication remained signed out; it was not required because the comparison used local HTML/GSAP, existing OE fonts, and the locked local VO. No cloud generation or paid service ran.

## Recommendation and next command

Use the HyperFrames treatment as the stronger visual-language candidate, while retaining Blueprint Cinema's hash locks, world/plan validation, asset tickets, and gate authority. Do not declare HyperFrames the canonical renderer from this 90-second sample alone; first watch both treatments and decide whether the editorial motion language should be extended into a longer greybox section.

```bash
open blueprint-cinema/episodes/EP006-direct-booking-recovery/delivery/generated/EP006-greybox-deck-brand-title-prototype.mp4 blueprint-cinema/episodes/EP006-direct-booking-recovery/delivery/generated/EP006-hyperframes-native-90s.mp4
```

No approval was recorded and no production gate advanced.
