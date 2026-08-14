# Packaging an episode: title and thumbnail as one unit

Established on EP001 over ten rounds, 2026-08-13. Nine episodes packaged in a
batch came back as nine siblings; the sameness was structural, not a taste
failure, because one archetype run nine times is one photograph with the props
swapped.

**One episode at a time, and the title first.** The thumbnail is half of a pair
and cannot split work with a title nobody has chosen.

## The steps

**1. Context.** Read the script, not the topic line. What does the episode claim,
which numbers are load-bearing, and what is the POV only this operator could have
written? EP001: Accenture's $5.9B is audited and public, their other bookings are
flat, the solo equivalent is a ~$2K project, and the $40K/month figure is debunked
on camera.

**2. Lock the title.** Not a shortlist — one string.

    thumbnail_spec.py <script.json> --stage specs --title "<the chosen title>"

`--title` scores `reexpress` against that one title. Without it the model gets
three candidates and is asked to complement all of them, which means
complementing none: EP001 shipped a thumbnail restating its working title
verbatim, kicker and episode number included.

The split follows from a measurement. A title carries a number credibly because
text is legible at any size, and 0 of 20 register-lane winners carry one on the
image. **So the numbers go in the title and the picture is freed to carry the
idea.**

**3. Read the scores, then disagree with them.** The rubric ranks concepts; it
does not choose. On EP001 the top-scoring concept had the right SCENE and the
wrong WORDS. Scene and overlay are scored together and can be taken apart.

**4. Decide what KIND of picture this is.** This is the step that was missing for
six rounds, and it is where most of the leverage sits.

| archetype | what it is | when |
|---|---|---|
| `graphic` | a deliberate scale collision, photographed convincingly | **default for this channel** |
| `at-work` | one person absorbed in a task, unaware of the camera | the work is physical and photogenic |
| `flatlay` | crowded working surface, dense to all four edges | the customer's business is the subject |
| `object` | the thing itself, no people, no hands | there is a real recognisable object |
| `practitioner` | a PRESENTER addressing the lens | almost never — see below |

`practitioner` means "a person doing the work" in `thumbnail_spec.py` and "a
presenter talking to camera" in `generate_scene.py`. Given a scene reading "the
hands the only human presence in frame", the constraint won and the model
rendered both briefs at once — a man gesturing at the lens beside a pair of hands
under a desk. Two subjects, because two specs.

**5. Generate the ground, then check it for defects before you judge it.**

    generate_scene.py <slug> --archetype graphic --scene "..." --tag <tag> --n 4

Always `--n 4`. Two things go wrong often enough to be checked every time:

- **Hand count.** EP001 lost two rounds to three-handed anatomy — two hands on
  the device and a third forearm above. Count them.
- **People who were not asked for.** One of four "no person in frame" grounds came
  back with a person in it.

**6. Test the overlay, do not assert it.** One ground, many overlays, rendered and
read side by side at 120px. EP001 took more than twenty across ten rounds. Two
results that generalise:

- **Two tiers beat one long line.** A single line spans the frame and goes thin at
  browse width; an overline plus a short `big` gives the payload the full type
  size. `ONE PERSON` is legible at 120px where `EVERY BUSINESS NEEDS THIS` is not,
  and it is only one word shorter.
- **Never restate the image.** The photograph showed one person, so `ONE PERSON`
  spent the overlay on something the viewer could already see. The text says what
  the picture cannot.

**7. Render at 4K, through the wrapper.**

    render_thumbnail.py <props.json> <out.png>

It renders at `--scale 3` (3840x2160, the size A7 verified) and runs
`check_thumbnail.py` afterwards, because a thumbnail that has never been shrunk
to browse width has not been reviewed.

Do NOT fix the resolution by changing the Composition in `Root.tsx` to 3840x2160.
The layout is full of pixel constants and the checker shrinks to 120px to
simulate browse width; both only mean anything relative to a 1280-wide frame, so
tripling the composition silently changes what the shrink test tests. `--scale`
multiplies the output while rendering the same layout — verified at a mean
difference of 1.2/255 against a native 1280 render, which is antialiasing on type
edges, not movement.

**8. Read it at 120px before you like it.** Everything looks fine at reading size.
`check_thumbnail.py` is necessary and NOT sufficient — see Open problems.

## What the picture has to do

**Familiar but unexpected, and both halves in the same glance.** `recognisable`
(25) and `curiosity` (15) are scored independently and never tested for
COLLISION, so a concept passes both while the image itself is entirely expected
and all the surprise sits in the caption.

The failure mode this produces is subtle and cost four rounds: **a surprise the
viewer has to find.** An unattended hotel desk is genuinely unexpected, but the
unexpectedness is an ABSENCE, and absence needs a second glance. So does a small
object being installed. Browse width only ever gives one glance.

A scale collision is legible immediately, which is why `graphic` is the default:
a corporate tower standing in an open palm reads before you have decided to look
at it. Every episode has an incumbent that fits in a palm.

**The frame shows a job, not a problem.** This channel sells one business the
viewer could build, so the subject is work someone is paid to do. The market's
pain is why the job exists; it is not the picture. Amendment A9 — the rubric was
derived from CRITIQUE channels and imported their stance with their form.

**The words are a verdict, not a label.** `THE BUSINESS OF BORING` works because
boring is a surprising verdict. `THE BUSINESS OF SETUP` failed because setup is
just the noun for what the episode is about. If the payload word could appear in
the episode's own description, it is a label.

## Brands

Two rules, both learned the expensive way, both from the Modern MBA sheet.

**Brand as OBJECT IN THE SCENE, never as vector chip.** Their winning tiles are
full of brands — a Crumbl box, Mrs Fields, McDonald's arches, four eras of Xbox —
as physical product inside the frame. Our finding V5 ("logo collage is 5-for-5
bottom quartile") got applied as *avoid brands*, which is the wrong lesson. The
losing form is the floating rounded chip. Use `plate: false` and set the mark on
the photograph.

**The wordmark, not the glyph.** `fetch_logos.py` pulls Simple Icons, which ships
Accenture's bare chevron. Rendered, that is a purple `>` — it reads as a play
button and contributes nothing to the recognisability it was added for. Fetch the
wordmark separately.

Mechanics that follow: wordmarks are wide, so a scatter entry takes `ar`
(width/height, default 1) or a square chip shrinks it to a sliver. Put the mark
somewhere with a **light, low-detail ground** — on EP001 the palm gives black
type separation for free, where over a blurred street it needed the chip that was
the problem in the first place.

## Safe zone

Compute it, do not eyeball it. YouTube stamps duration in the bottom-right; keep
marks and type out of `x > 0.85 AND y > 0.85`. On EP001 "close to the bottom
right" and "clear of the bottom right" were about thirty pixels apart.

    w = 132 * s * ar / 1280 ;  right_edge = x + w/2   # must stay under 0.85

## Open problems

- **`check_thumbnail.py` cannot see type drowning.** It passed all nine batch
  thumbnails at `browse_range_on_white` 255/255 while most headlines were
  illegible at 120px. It measures the whole frame's luma range, which any
  cluttered photograph maxes out. Built against EP005's near-empty frame, blind
  to the opposite failure. A real fix measures the type region against its local
  ground.
- **Grounds are not reproducible.** `generate_scene.py` captures no seed and
  `remotion/public/thumbs/` is gitignored, so a deleted ground can only be
  replaced, never recreated.
