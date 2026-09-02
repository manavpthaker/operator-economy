# Boundary Ledger component contracts

These contracts define required anatomy and behavior. They are framework-neutral so the production
site can adopt them without making this reference package a second application runtime.

## Core DOM contract

The three signature components use this class and source-order contract. The docket and working
model remain valid as standalone elements; only direct children of `EpisodeFeature` receive grid
placement and the 16px attachment.

```html
<section class="bl-episode-feature">
  <div class="bl-episode-feature__rail">...</div>
  <div class="bl-episode-feature__intro">...</div>

  <aside class="bl-docket" aria-labelledby="episode-title">
    <div class="bl-docket__head">...</div>
    <div class="bl-docket__body">
      <span class="bl-docket__identity">...</span>
      <h2 id="episode-title">...</h2>
      <p>...</p>
    </div>
    <dl class="bl-docket__rows">
      <div class="bl-docket__row"><dt>Published</dt><dd>...</dd></div>
      <div class="bl-docket__row"><dt>Sources</dt><dd>...</dd></div>
      <div class="bl-docket__row"><dt>Canvas status</dt><dd>...</dd></div>
    </dl>
  </aside>

  <figure class="bl-working-model">
    <img src="..." alt="..." width="1536" height="1024" />
    <figcaption><span>...</span><span>3:2 · complete composition</span></figcaption>
  </figure>
</section>
```

## `Masthead`

- Contains the Operator Economy wordmark and no more than the primary editorial actions.
- Uses publication typography, not handwritten or blueprint-styled navigation.
- Collapses without introducing a second navigation system.

## `WorkingModel`

Required inputs:

- `src`: a versioned asset with an episode illustration manifest.
- `alt`: a relationship-level description; required unless the image is genuinely redundant.
- intrinsic `width` and `height`: normally `1536 × 1024`.
- optional caption and accountable format note.

Required behavior:

- Render inside a semantic `figure` when a caption is present.
- Preserve the complete 3:2 composition with `object-fit: contain`.
- Never use the artwork as a cropped background image.
- On narrow screens, bleed the paper to the viewport edge while keeping the docket inset.
- Redraw for another aspect ratio if the central relationship or oxide path stops reading.

## `AccountableDocket`

Required inputs:

- sheet role and live state;
- episode number and artifact family;
- thesis title and one-sentence operating promise;
- publication date, source count, and Canvas status.

Required behavior:

- Use deep mineral as the accountable surface.
- Keep the three metadata rows; do not grow a collection of status chips.
- Keep dates, source counts, episode numbers, and statuses in the data face.
- Never imply publication when the content state does not support it.

## `EpisodeFeature`

Required anatomy:

1. optional editorial rail;
2. concise thesis copy;
3. `AccountableDocket`;
4. `WorkingModel`.

Required behavior:

- The docket overlaps exactly `--bl-overlap` (16px) into blank top paper.
- The docket must not obscure a meaningful mark.
- Desktop may use the `120px / editorial / docket` composition.
- Mobile stacks copy and docket, keeps 24px page gutters, then makes the illustration full bleed.
- Reading order must remain correct without CSS.

## `LedgerRow`

- Use for comparable material roles or accountable record fields.
- Prefer rules and spacing to card containers.
- Labels identify function, not decorative taxonomy.

## `EvidenceReceipt`

- Separates sourced evidence from modeled economics.
- States what the evidence supports and what remains an estimate.
- Source count is accountable data, not a badge.

## `DecisionNote`

- Records one decision, exception, or unresolved operating question.
- Oxide may mark the decision edge or phrase; it cannot color the whole page hierarchy.

## `EditorialAction`

- Uses a direct verb and an honest destination.
- Must have a visible oxide focus indicator on paper and bright oxide on mineral.
- Avoid pill shapes and ornamental iconography.

## `SubscriptionBand`

- Uses deep mineral as a single, deliberate conversion surface.
- Contains one promise, one supporting sentence, and one primary action.
- Does not compete with the episode docket in the same viewport when avoidable.

## `DisclosureBlock`

- States the evidence, estimate, AI, or publication boundary in plain language.
- Uses a quiet rule-based treatment; it is not an alert card unless there is actual risk.
