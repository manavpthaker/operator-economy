---
workflow: general-video
flow: companion
storyboard: yes
message: "You can run the findable-and-bookable half of a direct-booking audit on any property tonight, from the guest side"
destination: youtube-shorts
aspect: 1080x1920
language: en
audience: "a prospective operator weighing whether to build a direct-booking practice"
length: 45.328s
narration: supplied
---

## Intent

Short 01 of four owner-locked companion Shorts for EP009, a direct-booking practice. A cold viewer
is told in the first lines that they can build a practice helping a small hotel get its returning
guests to book direct, then handed one instrument they can run tonight on their phone: search an
independent inn the way a guest would, look for the free link to the hotel's own site beside the
site rates, compare the direct rate, try to finish a direct booking. Whatever breaks is the finding.

Documentary register, not promotional. The viewer is the operator who could build the service; the
hotel owner is the customer. The host may say with authority what can be built and how to begin,
while demand and pricing stay open.

Every field above is settled by owner decisions already in the repository, so no brief questions
were asked. `length` is measured, not chosen: it is the accepted narration plus the two second end
bridge.

## Assets

- `assets/audio/narration.wav` — the owner-accepted Original C narration, sha256 `dccf637f…`, 43.328s. LOCKED. Do not regenerate, retime, trim or re-voice it. Picture is cut to this audio.
- `assets/data/beats.json` — measured movement boundaries and frame-snapped cuts from `BEAT-TIMING-V1.json`.
- `assets/data/script.json` — the owner-locked spoken words and their exact anchors.

## Customizations

- **Three movements, in this order, and no fourth.** Presenter opens, full-screen designed proof owns the mechanism, presenter returns to land the conclusion. Then a 2.0s silent end bridge. This is the owner-ruled EP007 clean-frame grammar; the full rule set is `shorts-net-new/PICTURE-GRAMMAR-V1.md`.
- **Movement boundaries are fixed by measurement.** Presenter 0 to 11.625s, screens 11.625 to 33.042s, presenter 33.042 to 43.328s, bridge 43.328 to 45.328s. Cuts land on frames 279 and 793 at 24fps, on the incoming word's onset. Do not move them.
- **This run builds the screens movement only.** The two presenter movements have no footage: presenter generation is paid provider work and is not authorized. Build them as plain labelled holds so the piece renders end to end and the screens can be judged against real narration in context.
- **Hard cuts at every boundary.** No crossfade, whip pan, zoom punch, ambient drift or pulse. The end bridge is the one exception: it enters on a shared-element match cut.
- **Clean frame.** No persistent heading and no persistent footer. The owner's words were "do we need the heading through the whole thing? do we want to make it seem more natural less produced".
- **No double-tracking.** When a phrase lands as embedded on-screen type it drops from the caption rail for that moment. A proof card must never repeat an overlay verbatim.
- **Protected holds.** A resolved graphic holds into its cut, and the completed answer holds after the last word before anything routes away. The post-word hold here is 0.288s.
- **End bridge copy is declarative, not interrogative.** It states what the Short resolved and names what the episode adds. No URL, no link capsule, no fake button: native Related Video is the click path and EP009 has no `launch/links.json` yet, so nothing may be drawn as a link.
- Keep the rightmost 180px and bottom 300px clear of content, for platform UI.

## Notes

- **Claim constraint carried into the picture, not just the words.** The free-link beat must show a property *connected through a partner*; `claims-map.md` C009 forbids implying every small property is eligible without one. A frame can breach a claim the script respects.
- The screens movement covers paragraphs 3 and 4 of the locked script: the phone search and free-link check, then the rate comparison and the booking attempt. It has to make a guest-side phone result legible at phone size.
- The presenter returns beside the settled graphic reduced to three stable labels: not findable, not bookable, direct costs more. The mechanism is not replayed and is never replaced with success icons.
- Four of the eight movement cuts across the four Shorts are very tight, under 0.12s of silence. Short 01's first cut has 0.08s. Cutting on the incoming word's onset keeps the outgoing word complete, which is why the boundaries are where they are.
- Reference for structure, never for surface imitation: EP007's accepted `short-01-thirty-day-map-v3`. That project pins hyperframes 0.8.61 and is owner-accepted and frozen; it must not be modified or re-rendered. This project starts current at 0.8.141.
- Nothing in this project is owner-accepted. The beat assignment itself is an agent reading, recorded in decision event `ep009-shorts-picture-grammar-v1`, and the owner ruled the grammar but not the per-paragraph assignment.
- No em dashes in anything written for this build.
