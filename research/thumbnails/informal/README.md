# The informal treatment across the set — 2026-08-13

Nine episodes, the flat-lay TREATMENT (angled heading at the top, marks scattered
among the objects, ground crowded to every edge) carried onto a non-overhead
camera. Each episode's scene is its own `flatlay` spec scene with the camera
language stripped; the camera comes from `--shot`, balanced across the five
non-overhead types.

**Not locked, and not a replacement for `../variants/`.** The 27 reviewed renders
are untouched. Props are `studio/originate/<slug>/render_data/thumb-informal.json`.

## What worked

The camera genuinely varies now. The previous sheet was nine overhead desks
because the archetype text said "overhead flat-lay"; with that removed, `--shot`
finally does something. The informality, the density and the scatter all survive
the move off the desk.

Logo hierarchy was fixed here: the chips were rendering at 172px and were the
most legible thing in the frame at browse width, which is the inversion V5 warns
about — marks survive as subordinate texture and die as the subject. Base is now
132px and the type outranks them.

## What did not

**Read `contact-120px.jpg` before using any of these.** At browse width most of
the headings do not survive. Only `BORING` (1 word) and `ROOM OF ONE` (3) hold
together. The rest reduce to grey mush, and two of them break rule 2 outright:

| episode | words | |
|---|---|---|
| ai-implementation-consulting | 6 | `EVERY FIX EXPOSES THE NEXT MESS` |
| solo-design-agency | 5 | `THE GAP IS THE PRODUCT` |

Those two are also the least readable tiles, which is not a coincidence.

This is V4 restated: one focal mass survives 120px, a multi-node composition does
not. A busy ground and a long headline compete for the same attention, and at
120px the ground wins. The comp set's one exception — Modern MBA's dense food
scenes — stops being legible and stays *categorisable* by colour and texture.
None of these are categorisable that way; they are all beige desks.

So the treatment is not finished. It needs either headlines cut to =3 words, or
grounds with a colour signature strong enough to identify the episode without
reading anything.

## A checker gap this exposed

`check_thumbnail.py` passes all nine, with `browse_range_on_white` at 255 of a
possible 255. It measures the luma range of the WHOLE FRAME at 120px, and any
cluttered photograph maxes that out whether or not the type on top of it
survives. It was written against EP005, a near-empty thumbnail, and is blind to
the opposite failure. It cannot currently tell these apart from a good one.
