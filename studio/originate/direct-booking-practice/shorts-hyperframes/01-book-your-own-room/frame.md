# Design truth: EP009 Short 01

Brand authority is **Boundary Ledger 2.0** (`design-system/boundary-ledger/`), not HyperFrames house
style. Nothing here is invented: every rule below is read off the Ledger's invariant register, its
scene contracts and its narrated picture/audio binding. Where the Ledger is provisional, this file
says so.

## Surface binding

- Social, 9:16, exactly 1080x1920, 24 fps.
- The Ledger's social binding requires composition and UI-collision checks, because platform chrome
  changes the practical safe area. Keep the rightmost 180px and bottom 300px clear of content.
- U-08: recompose across aspect ratios. Do not crop a landscape model into 9:16; compose for
  portrait.

## The constraint that shapes this scene

**U-12: generated plates are not evidence.** Its failure example is "using AI-created UI or documents
as source material." **U-04: visual polish never upgrades evidence**, failing on "a generated receipt
presented as proof."

Short 01's screens movement describes a phone check: search an inn as a guest would, look for the
free link to its own site beside the site rates, compare the direct rate, try to finish a direct
booking. The obvious treatment is a realistic search result and booking page. **That treatment is
forbidden here.** A convincing fake Google result or Booking.com page is an AI-created UI standing in
for source material, and it would also read as proof of a specific property's behavior, which no
claim supports.

The Ledger's answer is in its own translation table: "No photography as episode imagery. Documentary
footage is valid in Reality World; **Working Model remains the designed identity**." So this movement
is a designed schematic of the check the viewer will run, drawn in the Working Model language. It
reads as an instruction, not as a screenshot. That is both compliant and the better read, because
the viewer is being handed a procedure, not shown someone else's result.

## Scene mode

`silent_graphic`, per the Ledger's narrated picture/audio binding and matching EP007's accepted
Short 01, whose middle frames carried the same mode. The binding requires a silent graphic to
declare **before state, operation, after state and settle**, which the storyboard does per frame.

- Language carrier: the owner-accepted Original C narration, continuously, across every movement.
- Visible speech: none anywhere in this movement.
- Mute diagnostic: on mute the viewer must not wait for a missing line. The progression has to carry
  the procedure on its own.

## Motion

- U-05: motion changes state, then settles. No ambient drift, no endless pulsing.
- U-10: stillness is an authored state. Nothing moves because the narrator is talking.
- U-01: one focal point, one active commitment. Two competing active marks in one frame is a failure.
- Hard cuts at movement boundaries, per the owner-ruled grammar. No crossfade, whip, zoom punch.
- The Ledger's motion binding is explicitly **provisional**: "motion and sound bindings are specified
  but not encoded or mixed as production references." So motion here follows the semantic rules and
  does not claim to implement a verified motion reference.

## Type

- U-03: rough model, typeset institution. Handwritten captions or source labels are a failure, so
  on-screen labels are typeset even where the model is drawn rough.
- U-06: text labels or lands meaning. Duplicating the narration as kinetic type is a failure, which
  is the same rule as the grammar's no-double-tracking: a phrase that lands as embedded on-screen
  type drops from the caption rail for that moment, and a proof card never repeats an overlay
  verbatim.
- Fonts are the Ledger's own, in `design-system/boundary-ledger/fonts`, embedded locally rather than
  fetched, so rendering stays deterministic and does not depend on an unbundled display face.

## Colour roles

Roles carry meaning, values are bindings (U-02). Read the six roles from `semantic-core.json` and the
values from `tokens.css`; do not treat a hex value as the idea. One oxide path only: a single
commitment event or thesis locus is active at a time.

## What this file does not settle

- The beat assignment itself. The owner ruled the three-movement grammar; which paragraph sits in
  which movement is an agent reading, recorded in `ep009-shorts-picture-grammar-v1`.
- Any claim. On-screen numbers, sources and caveats come only from `claims-map.md`. For this Short
  that means the free-link beat must show a property **connected through a partner** (C009), and
  nothing may imply universal eligibility.

No em dashes in anything written for this build.
