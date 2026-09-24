# EP006 deck-style greybox rejected diagnostic

- Scope: locked VO opening, 0.000-90.000 seconds
- Composition: `BlueprintCinemaDeckPrototype`
- Render-data hash: `7d4fec2ed85e9e8d621a210551696e97cd3900f2959a66a4abfd4cc41bfeaa15`
- 90-second deck prototype review MP4 rendered: yes
- 90-second deck prototype media: h264 960x540 at 30/1, aac 2 channels at 48000 Hz, 90.048000s container duration, 4598932 bytes
- 90-second deck prototype SHA-256: `0665fc2261723b5587a6e3babc765b62c61e84fdc7297109c4e5660d1b751048`
- Current production state: `greybox_ready`

## What it proved

Press **Play**. The test is whether the same few objects remain recognizable while their relationship changes:

`guest/stay -> OTA -> hotel -> commission -> broken return relationship -> guarded direct route`

Ignore drawing quality. You should not need to decode a network map or read a technical caption to understand which route works, which relationship is broken, and why the direct path is not open until audit, permission, and human review occur.

The opening now includes two deliberate bookends:

- `27.733-32.558`: **The Operator Economy** show-identity screen with the canonical typographic wordmark and `Build. Own. Operate.` tagline.
- `32.558-40.090`: **EP006 - Direct Booking Recovery** title screen with the fair first-booking/return-booking thesis.

There is no separate icon because the canonical design system does not define one. These screens are structural greybox plates, not polished title animation.

The last slides deliberately switch to the fragmented operator handoffs described by the VO. They were useful for testing object persistence, bookend timing, and the difference between a complete network map and a smaller composition.

## Why it was rejected

The boxes still function as labeled concepts rather than observable operations. Their spatial relationship does not consistently express what the VO says at that moment, and the renderer lacks exact shot-level composition, text-emphasis, motion-cue, evidence, and transition decisions.

## Decision boundary

This is a rejected 90-second diagnostic, not a whole-episode deck, an approved greybox, polished asset work, generated evidence, a production master, or a release artifact. It must not be extended or used as a visual input. The next bounded review begins with validated `scene-directions.json`; no prompt or prototype advances `production-state.json` automatically.
