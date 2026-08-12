# The Packaging Design Language

*(Filename kept as `thumbnail-design-language.md` so existing references resolve. It outgrew the name on 2026-08-12, when the cold open made the thumbnail and the first two seconds of video one surface rather than two.)*

**Derived, not invented.** Written 2026-08-11 from `research/thumbnails/visual-findings.md` — 78
comp-set thumbnails read at reading size and at 120px browse width — and keyed to `design-system/`
Rev C. Reference render: `design-system/surfaces/thumbnail-flatlay-reference.png`.

Companion to `docs/thumbnail-rubric.md`, which governs *what a thumbnail says*. This governs *how it
is built*. Where they conflict the rubric's amendments win, because those are tied to measurement.

**Scope, as of 2026-08-12.** This covers the two surfaces a cold viewer meets in their first three
seconds: the thumbnail, and the opening of the video it points at. They are one decision. A
thumbnail that wins the click and loses the first ten seconds is a net loss under Test & Compare,
which picks the **watch-time** winner — so packaging that does not carry through is worse than
packaging that never won the click.

## Why this exists, and why it is not a style guide

Two approaches were tried before this one and both failed in recorded ways.

**Inventing a language from principles.** That is what produced the original rubric: a
general-audience creator checklist, six amendments inside a month, one of which reversed its own
rule 3, and eight generation rounds spent guessing. `thumbnail_spec.py` admitted in its own comment
that its weights were "a belief … inferred from what YouTube surfaces on a cold feed."

**Copying one channel outright.** Doesn't scale. A franchise phrase (`THE ECONOMICS OF …`) is
somebody's brand, a palette borrowed wholesale means every frame reads as an imitation, and the
subject categories that carry Modern MBA — food, retail, consumer goods — are not ours.

**What actually worked** was neither. Decompose a *measured* winner into the structural facts that
made it work, discard everything surface-level, then re-key those facts to our own tokens. Modern
MBA's `THE ECONOMICS OF COOKIES` — 8.21× its channel median, the highest multiple in the register
lane — gave us the structure. Rev C gave us the palette, the type and the schematic vocabulary. The
result looks nothing like the source and is built on the same skeleton.

That is the method this document formalises. **Structure from evidence. Surface from the system.**

## Layer 1 — structural invariants

These come from measurement and are not stylistic preferences. Each cites its evidence.

| # | Invariant | Evidence |
|---|---|---|
| S1 | **One focal mass.** Count the elements a viewer must resolve separately: one, or it fails. | Five multi-node compositions in the comp set, five bottom quartile, none in any top |
| S2 | **Never a comparison.** No two figures, no split panel, no before/after, no versus. | Same five. Also EP002, our own worst mechanical performer |
| S3 | **Dense to all four edges.** Objects cut off by the frame, overlapping, rotated. Nothing centred, contained, or squared up. | No thumbnail in the 78, either band, is an object isolated in empty space |
| S4 | **Human presence.** A face, a figure, or at minimum hands in frame. | 36 of 39 top-quartile thumbnails. Table stakes, not a differentiator — see the note below |
| S5 | **A recognisable subject.** A household brand, a familiar trade, or an everyday physical object. | The largest measured effect: identical title grammar, 15× apart on Crumbl vs OpenAI |
| S6 | **Marks scatter, never row.** Varied scale, varied rotation, allowed to overlap objects. | A logo collage as the subject is 5/5 bottom quartile; marks as a supporting layer are MagnatesMedia's whole top quartile |
| S7 | **Type overlaps the objects.** It does not sit in reserved space or in a panel that eats the frame. | Modern MBA and How Money Works both; a panel large enough for a verdict at comp type size covers most of the frame |
| S8 | **A figure is optional and usually wrong.** If present, exactly one, believable, in the smallest honest unit. | 0 of 20 register-lane top-quartile thumbnails carry a hero number. Believable beat big 4.9× and 18.8× |
| S9 | **Survives 120px** on both a white and a black ground. | The ship gate. `check_thumbnail.py` measures it |

**On S4, because it is the one that was missed.** A8 measured what *separates* winners from losers
and correctly found form features do not. It never asked what is *universal*. A feature present in
~100% of both bands has zero discriminative power by construction, so a differential test scores it
"does not matter" when it is actually the price of entry. Human presence, density and saturation are
all in that class. **A null result means "does not differentiate," never "is not required."** Any
future measurement must ask both questions.

## Layer 2 — token bindings

Structure is fixed above. This is how it is rendered, and every value resolves to `design-system/`.

**Ground.** A photograph, never a flat fill. It carries S3, S4 and S5 at once, so its density is not
decoration. The Working Schematic reads as a *photographed* drafting surface — cream table, navy
hand-drawn process diagrams, unlabelled boxes joined by connector lines — rather than as a grid
overlay. Diffusion renders that cleanly because there is no lettering in it.

**Type is ground-keyed, not fixed.** The theme rule is ink + paper (or navy) + ONE accent per frame,
and which of ink and paper carries the fill depends on what is underneath. Cream type vanishes on a
cream drafting table exactly as navy type vanishes on dark wood, so `groundTone` picks and the
stroke always takes the opposite. Gold is the offset, never the fill — it has too little value
contrast against either ground to carry a headline.

| | light ground | dark ground |
|---|---|---|
| headline fill | `navy` | `paper` |
| stroke | `paper`, 14px | `ink`, 14px |
| overline fill | `goldOnPaper` | `paper` |
| offset | `goldFill` then black | `goldFill` then black |

**Scale.** Headline 196px on a two-tier flatlay; on a single-tier photo the ramp runs 200 → 96 by
character count. Overline 76px with a 10px stroke — 66px went to mush at browse width and is the
floor to stay above. Marks 172px base, scaled 0.62–1.00, rotated ±21°.

**Type family.** `FONTS.sans` (Supreme 800) throughout. Boska and Zodiak are the brand's display
serifs and both fail the thin-stroke test at browse width; the 40px Boska floor is a page rule, not
a thumbnail rule.

## Layer 3 — the layouts

Four, keyed to the archetypes in `thumbnail_spec.py` so generation and rendering cannot drift apart.

| layout | when | ground | text |
|---|---|---|---|
| `flatlay` | the episode has a stack, a process, or assembled pieces | overhead, hands from the bottom edge, dense | two tiers, centred, rotated −2°, overlapping |
| `bleed` | a verdict over a single scene | press photograph with a quiet zone | one tier, bottom-left, hard shadow, no panel |
| `block` | the ground is busy or pale and contrast cannot be guaranteed | any | one tier in a navy panel |
| `product` | one manufactured object is the whole argument | object at scale, real texture | one tier |

`flatlay` is the default for this channel. It is the only one that satisfies S3, S4 and S6 by
construction rather than by luck.

## Layer 4 — the join

Rendering four frames of a finished episode beside its thumbnail found two surfaces sharing nothing:

| | thumbnail | video, before the fix |
|---|---|---|
| medium | photograph | no photography anywhere — vector cards |
| typeface | Supreme 800 at 196px | Boska serif at ~48px |
| density | dense to all four edges | 70–85% empty |
| colour | cream + navy + real brand marks | navy/ink/cream, hairline gold |
| cap height | ~15% of frame | body copy ~1.5% of frame |
| human presence | hands in frame | none, anywhere |

Every variable flips. Somebody clicks a tactile overhead photograph and lands on a silent navy
slide reading `SHEET 04 OF 56`.

**J1. The first frame is the ground the thumbnail was built on.** Not a lookalike — the same file,
read from the episode's thumbnail props by `prepare_longform.py`. A different photograph of a
similar desk does not make the join; it makes a continuity error.

**J2. It costs no extra time.** The cold open lives *inside* the existing 1.8s brand sting, not
before it. That constraint is load-bearing and predates this work: `Bookends.tsx` sets the sting at
1.8s because long pre-hook branding is punished by retention. A cold open that adds four seconds
would trade a fixed retention loss for a speculative continuity gain.

**J3. The ground dissolves into the register rather than cutting.** Photograph holds clean ~10
frames so the eye registers it as the thing just clicked; navy closes over it; the drafting grid
draws on top. The viewer watches the thing they clicked *become* the diagram the episode is drawn
in. A hard cut would read as two shots and make the mismatch louder, not quieter.

**J4. Type arrives with the ground it sits on, never before.** The first build had the wordmark
fully lit by frame 12 while the scrim was ~20% in — white serif on a cream drafting table. Over a
photograph, type is keyed to the scrim ramp.

**Unresolved, and the larger half.** J1–J4 fix the first two seconds. The rest of the video still
runs body copy at ~1.5% of frame height in a serif, which is unreadable on a phone and poor on a
TV — and TV is ~42% of watch time. That is the `screen` register below, and it is not built.

## Registers — the design-system change this implies

Rev C applies **one register to every surface**, and that is the root cause of the mismatch. A
blueprint PDF and a YouTube frame have opposite constraints: a PDF is read at arm's length with
time; a video frame is glanced at on a phone or across a room. The Working Schematic was designed
for the first and is being asked to do the second.

The fix is not a repaint — everything in the reference render is Rev C, and no new colours were
needed. It is documented **intensity levels** for the same tokens:

| register | surfaces | type scale | photography | brand marks |
|---|---|---|---|---|
| `document` *(exists)* | blueprint PDF, newsletter, site | small, generous margins, hairlines, serif | no | no |
| `screen` *(not built)* | video frames | 2–3× document | yes | yes |
| `feed` *(built here)* | thumbnails, Shorts covers | maximum; cap height ~15% of frame | required | scattered, ≤4 |

And one rule across them: **adjacent surfaces in a viewer's journey share at least two of {ground,
subject medium, type treatment}.** Thumbnail → first five seconds is the join that matters most and
the one that shared zero.

`design-system/surfaces/thumbnail.html` was replaced on this basis; it specified a card that was
almost exactly EP002, the worst thumbnail the channel has shipped.

## Re-rendering the back catalogue

The 27 locked candidates live in `research/thumbnails/variants/`, one per episode per archetype,
each reproducible from `studio/originate/<slug>/render_data/thumb-<archetype>.json`.

**Locked means locked.** Those props carry a `_locked` note because `thumbnail_specs.json` gets
regenerated whenever the rubric is touched, and newer spec text is a different *sample* from the
same rubric rather than a better one. Re-render from the props to reproduce; changing them is a
deliberate act, not a refresh.

**The grounds are the fragile part.** Each render composites over a diffusion image in
`studio/remotion/public/thumbs/`, gitignored and generated **without a captured seed**. One was
already lost this way: `boring-automation-agency-a.png` was overwritten by an untagged batch run,
and the BORING cover survives only because the composed render was committed and a sibling `-b`
happened to remain. Until `generate_scene.py` records seeds, the composed renders in
`research/thumbnails/variants/` are the record and the grounds are not reproducible.

To bring an existing episode onto this language:

```bash
python scripts/originate/fetch_logos.py <slug>            # real marks, --names if the stack is prose
python scripts/originate/thumbnail_spec.py originate/<slug>/script.json
python scripts/originate/generate_scene.py <slug> --rank N --tag flatlay
# write thumb-flatlay.json, render, then:
python scripts/originate/check_thumbnail.py <render>.png
python scripts/originate/prepare_longform.py …           # picks up cold_open_image itself
```

## What we do not copy

The structure is fair game; these are not. A franchise phrase (`THE ECONOMICS OF …`) is a brand
asset. A palette taken wholesale makes every frame read as imitation. A subject category that is
not ours — food, consumer retail — buys recognisability we have not earned and cannot sustain.
Third-party marks appear only as the episode's real stack, fetched by `fetch_logos.py`, never
decoratively: a wrong mark is a factual claim about someone else's product.

## Keeping it honest

**This is versioned against evidence, and the evidence has a shelf life.** The comp set was pulled
2026-08-11 and describes what six channels were doing that month. Re-run
`studio/scripts/research/build_contact_grids.py` and re-read it before treating any invariant above
as still true.

**Everything here is inference from other people's channels.** Views are not CTR, banding within
channel controls for subscriber base and nothing else, and no part of this has been tested on our
own audience. Test & Compare is the instrument that settles it, it judges by watch time rather than
clicks, and it needs roughly 1,000 impressions per variant. Until then the invariants are ranked by
how they were established: **S1, S2, S6 and S8 rest on negative results and are the strong ones.**
S4 and S5 rest on positive ones and are weaker. S3 and S7 are structural observation.

**Prose rots.** The original rubric needed six amendments in a month; what held was the machine
layer. So the load-bearing parts of this document live in code, and this file is the explanation
rather than the enforcement:

| Layer | Lives in |
|---|---|
| S1, S2, S8 as scored dimensions | `studio/scripts/originate/thumbnail_spec.py` |
| S9, plus alpha, aspect and file size | `studio/scripts/originate/check_thumbnail.py` |
| S3, S4 as generation constraints | `studio/scripts/originate/generate_scene.py` |
| S6 as a scatter table | `studio/remotion/src/ThumbnailComposition.tsx` |
| Layer 2 bindings | `design-system/tokens/`, mirrored in `studio/remotion/src/oe/theme.ts` |

**Not yet enforced anywhere.** S5 needs eyes. S7 is a layout convention. And nothing checks across
episodes: `too-small-to-bother` and `small-cohort-business` independently landed on a single chair
in an empty room, which no per-episode gate can see. That check is the known gap.
