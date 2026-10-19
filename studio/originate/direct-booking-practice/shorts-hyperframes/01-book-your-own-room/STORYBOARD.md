---
format: 1080x1920
duration: 45.333s
message: "You can run the findable-and-bookable half of a direct-booking audit on any property tonight, from the guest side"
arc: "Opportunity → Subject → Guest position → The free link → The rate and the attempt → What broke is the finding → Episode"
audience: "a prospective operator weighing whether to build a direct-booking practice"
mode: collaborative
fps: 24
total_frames: 1088
design_truth: frame.md
brand_authority: design-system/boundary-ledger
picture_audio_mode_default: silent_graphic
language_carrier: "assets/audio/narration.wav, owner-accepted Original C, continuous under every frame"
---

Seven frames. Frames 1 and 6 are the presenter movements and have **no footage**: presenter
generation is paid provider work and is not authorized, so they are built as labelled holds that
carry the narration and state plainly what will replace them. Frames 2 to 5 are the screens movement
this run builds. Frame 7 is the episode bridge.

Every boundary below is measured, not chosen: movement cuts come from `BEAT-TIMING-V1.json`, the
internal screen cuts from `assets/data/internal-cuts.json`. Each lands on a 24 fps frame at the
incoming word's onset, so the outgoing word is never clipped.

The frame grid makes the piece 1088 frames, which is 45.333s, not the 45.328s that the accepted
43.328s of audio plus a 2.000s bridge implies. The 0.005s is the cost of snapping the presenter
return to frame 793; it sits inside the post-word hold, where there is nothing but silence. Picture
runs to 1088 and the audio simply ends 0.005s before the bridge's last frame.

**The constraint that shapes frames 3 to 5** is `frame.md`'s reading of Boundary Ledger U-12 and
U-04: a convincing search result or booking page would be an AI-created UI standing in for source
material. These frames are a designed schematic of the check the viewer will run, in the Working
Model language, not a simulated screenshot.

## Frame 1 — Presenter opens

- status: outline
- src: compositions/01-presenter-open.html
- duration: 11.625s
- frames: 0 to 279
- transition_in: cut
- picture_audio_mode: presenter_address
- scene: Placeholder hold. Manav names the practice and says the first piece can be run tonight.
- voiceover: "You can build a practice that helps a small hotel get its returning guests to book direct, instead of paying a booking site to meet them again. You can run the first piece tonight, on your phone."
- placeholder: true
- replaced_by: "matched presenter performance, unauthorized paid provider work"

Carries the narration with a plain typeset hold naming the movement and its intended content, so the
piece renders end to end and the screens can be judged in context against real audio. Not a design.
No stand-in avatar, no stock face, no generated portrait: a placeholder that looked like a presenter
would invite review of a performance that does not exist.

## Frame 2 — The subject

- status: outline
- src: compositions/02-the-subject.html
- duration: 3.875s
- frames: 279 to 372
- transition_in: cut
- picture_audio_mode: silent_graphic
- scene: One drawn inn settles in the Working Model language, with the room band as a typeset label.
- voiceover: "Pick an independent property near you, twenty to forty rooms."
- motion: waterfall-entry
- before_state: empty field
- operation: the subject enters and settles
- after_state: one inn, labelled with its band
- settle: holds into the cut

The viewer's subject, not a specific property. Rough model, typeset label (U-03). One focal point
(U-01). "Twenty to forty rooms" is the qualified-buyer band from the editorial contract, so the
label states the band and claims nothing about any real inn.

## Frame 3 — Take the guest's position

- status: outline
- src: compositions/03-guest-position.html
- duration: 2.083s
- frames: 372 to 422
- transition_in: cut
- picture_audio_mode: silent_graphic
- scene: The vantage moves from outside the inn to the guest's side of the transaction.
- voiceover: "Search for it the way a guest would."
- motion: anchored-layout-expand
- before_state: the inn seen plainly
- operation: the frame adopts the guest's position
- after_state: the inn seen from where a guest meets it
- settle: brief, then cut

The shortest frame and the hinge of the whole instruction: the audit works because the operator
stops looking at the business and looks from where its customers arrive. One operation only.

## Frame 4 — Does the free link appear

- status: outline
- src: compositions/04-free-link.html
- duration: 10.458s
- frames: 422 to 673
- transition_in: cut
- picture_audio_mode: silent_graphic
- scene: Two routes to the same inn stand side by side; the one through the inn's own site is marked as carrying no fee, and as conditional on a partner connection.
- voiceover: "Does a free link to the hotel's own site show up beside the site rates? Google shows one for a property connected through a partner, and charges nothing for it."
- motion: svg-path-draw, discrete-text-sequence
- before_state: the inn, reachable only through the booking site
- operation: the second route is drawn, then qualified
- after_state: two routes, one of them the inn's own and fee-free, with its condition attached
- settle: holds through the qualification into the cut
- claims: C009
- claim_constraint: "must show a property connected through a partner; may not imply universal eligibility"

The longest and only claim-bearing frame. The free route is drawn as a path (one oxide path, U-01),
and the partner condition enters as an attached typeset record that holds, which is the Ledger's own
translation of the 16px docket: an accountable record enters once, attaches to its subject, and
holds. The condition is not a footnote that flashes; it stays as long as the claim does.

The mute test for this frame is the strict one: a viewer with the sound off must read two routes and
a condition, not wait for a sentence.

## Frame 5 — Compare the rate, try the booking

- status: outline
- src: compositions/05-rate-and-attempt.html
- duration: 5.0s
- frames: 673 to 793
- transition_in: cut
- picture_audio_mode: silent_graphic
- scene: The two routes resolve into two rates set against each other, then the direct one is followed to its end and the attempt either completes or stops.
- voiceover: "Compare the direct rate to the site's. Try to finish a direct booking yourself."
- motion: comparison-split, stat-bars-and-fills
- before_state: two routes, unpriced
- operation: each route carries a rate, then the direct route is followed through
- after_state: a comparison and an attempt whose outcome is the finding
- settle: holds into the presenter return

No numbers. The rates are shown as relative quantities with no figure attached, because no claim
supports a rate for any property and the instruction is to go and find out. That is also why the
attempt's outcome is left open here: the finding belongs to the viewer's own property.

## Frame 6 — Presenter lands the finding

- status: outline
- src: compositions/06-presenter-close.html
- duration: 10.292s
- frames: 793 to 1040
- transition_in: cut
- picture_audio_mode: presenter_address
- scene: Placeholder hold. Manav returns beside the settled graphic, reduced to three stable labels, and names what ten minutes bought.
- voiceover: "Whatever breaks is your finding. Not findable, not bookable, or a direct rate that costs the guest more. Ten minutes, and you have half an audit."
- placeholder: true
- replaced_by: "matched presenter performance, unauthorized paid provider work"
- intended_graphic: "the frame 5 state reduced to three stable labels beside the presenter: not findable, not bookable, direct costs more"

The owner-ruled grammar requires the presenter to return **beside the settled graphic**, which
reduces to a small number of stable labels and is never replayed or replaced with success icons. The
three labels are buildable now and are worth building into this placeholder, because their legibility
beside a presenter is a real design question the owner can judge without any footage existing.

## Frame 7 — Episode bridge

- status: outline
- src: compositions/07-episode-bridge.html
- duration: 2.0s
- frames: 1040 to 1088
- transition_in: shared-element match cut
- picture_audio_mode: silent_graphic
- scene: The grouping mark from frame 6 survives the cut and anchors a declarative route to the episode.
- voiceover: none; the standalone payoff is already complete
- copy_intent: "states what the Short resolved and names what the episode adds; declarative, never a question"
- link_boundary: "no URL, no link capsule, no fake button. Native Related Video is the click path and EP009 has no launch/links.json, so nothing may be drawn as a link."

Begins only after the full 0.288s post-word hold. Declarative by rule: the retired cliffhanger
standard is what put an unanswered question on the last card of every earlier EP009 Short.

## Registry note

A catalog search ran before this plan. `comparison-split` and `panel-reveal` are real candidates for
frame 5. Several of the nearest matches for OE's rough-model look are hand-lettered
(`marker-checklist-card`, `hw-callout-circle`), and Boundary Ledger U-03 forbids handwritten captions
and source labels, so they cannot carry any label here even though their gesture is close. Frames 2
to 4 are therefore hand-authored in the Working Model language, and any block installed for frame 5
gets its labels replaced with typeset ones.

## What this plan does not settle

The beat assignment is an agent reading, recorded in `ep009-shorts-picture-grammar-v1`. The owner
ruled the three-movement grammar, not which paragraph sits in which movement. Frames 2 to 5 are a
further subdivision inside the screens movement and are entirely this plan's proposal.

No em dashes in anything written for this build.
