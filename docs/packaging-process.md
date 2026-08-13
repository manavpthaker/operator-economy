# Packaging an episode: title and thumbnail as one unit

Established on EP001, 2026-08-13, because nine episodes packaged in a batch came
back as nine siblings. The sameness was structural, not a taste failure: one
archetype run nine times produces one photograph with the props swapped.

**One episode at a time, and the title first.** The thumbnail is half of a pair
and cannot split work with a title nobody has chosen.

## The steps

**1. Context.** Read the script, not the topic line. What does the episode
actually claim, which numbers are load-bearing, and what is the POV that only
this operator could have written? EP001: Accenture's $5.9B is audited and public,
their other bookings are flat, the solo equivalent is a ~$2K project, and the
$40K/month figure is debunked on camera.

**2. Lock the title.** Not a shortlist — one string. The split follows from a
measurement: a title can carry a number credibly because text is legible at any
size, and 0 of 20 register-lane winners carry a number on the image. So the
numbers go in the title and the thumbnail is freed to carry the job.

    thumbnail_spec.py <script.json> --stage specs --title "<the chosen title>"

`--title` scores `reexpress` against that one title. Without it the model is
handed three candidates and asked to complement all of them, which means
complementing none: EP001 shipped a thumbnail restating its working title
verbatim, kicker and episode number included.

**3. Read the scores, then disagree with them.** The rubric ranks concepts; it
does not choose. On EP001 the top-scoring concept had the right SCENE and the
wrong WORDS — hands installing an automation box behind a hotel front desk,
captioned `PICK ONE INDUSTRY / NOT ALL OF THEM`, which is playbook advice rather
than the episode's spine. Scene and overlay are scored together and can be taken
apart.

**4. Generate the ground from the winning scene.**

    generate_scene.py <slug> --archetype at-work --rank 0 --tag <tag> --n 2

Pick the archetype deliberately. `practitioner` is a PRESENTER addressing the
lens; `at-work` is somebody absorbed in a task who does not know the camera is
there. They are not interchangeable and the wrong one fights the scene.

**5. Test the overlay, do not assert it.** One ground, two or three overlays,
rendered and read side by side at 120px. This is the cheap step and it is the one
that settles arguments. EP001's two-tier `THEY PAY YOU TO / FINISH IT` beat both
the single-line version and the rubric's own words, because the payload word gets
the full type size.

**6. Read it at 120px before you like it.** Everything looks fine at reading
size. `check_thumbnail.py` is necessary and NOT sufficient — it measures the
whole frame's luma range, which any cluttered photograph maxes out whether or not
the type survives.

## The rule that generates the words

The channel sells one business the viewer could build, so the frame shows **a job
someone is paid to do**, never the market's problem that makes the job exist. The
pain is the setup; it is not the picture.

This had to be written into the rubric because the comp set fought it. The
register lane we measured — How Money Works, MagnatesMedia, Modern MBA — are
CRITIQUE channels, and their top quartile is flat editorial judgement:
`CANCELLED`, `WE NEVER LEARN`, `THE MATH IS NOT MATHING`. Copying that form
imports its pessimism. EP001's first pass scored `A QUARTER OF INCOME / ONE
CLIENT GONE` highest, which is the comp lane's stance wearing our clothes.

Take the withheld-verdict FORM without the stance. Amendment A9.
