# Design specification

## Concept angle

One locked source window becomes a phone-readable proof bench: the episode's real software capture
stays intact while motivated viewports focus the exact state the narration names.

## Visual system

- Canvas: 1080 by 1920 at 24 fps.
- Material: Boundary Ledger paper (`#f5f0e6`) with raised paper (`#fbf8f1`) and mineral ink
  (`#204440`). Oxide (`#b5482f`) is reserved for the active caption rule and the final judgment word.
- Typography: Georgia for the institutional identity and Montserrat for phone-readable captions;
  IBM Plex Mono for source and truth-boundary labels.
- Focal element: the active real source viewport. It occupies the upper two-thirds and remains the
  only large moving object.
- Edge anchors: a small publisher mark at the upper edge and the source-truth strip at the lower edge.
- Supporting detail: one quiet caption rail between the media and platform-safe bottom band.
- Background: still paper with hairline rules; no gradients, ambient drift, decorative motion, or
  invented interface furniture.

## Motion and edit

- Source hard cuts stay hard cuts at the exact r8 frame boundaries.
- Camera motion is limited to slow, deterministic crop adjustments that make real interface text
  readable. It never changes source time or invents a UI state.
- The final returned-draft shot uses two synchronized crops of the same exact source frame: one for
  the edited draft and one for `awaiting human review · no sending available`.
- Captions enter by a short opacity and vertical settle. No word bounce or duplicate kinetic text.

## Safety and truth

- `FICTIONAL FIXTURE`, `AWAITING HUMAN REVIEW`, and `NO SENDING AVAILABLE` are retained as the
  persistent boundary. They are already present in the locked source.
- No platform action, message send, real guest data, public URL, new claim, or approval state is shown.
