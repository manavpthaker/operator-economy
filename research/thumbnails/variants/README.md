# Thumbnail candidates — 2026-08-11

27 renders, 9 episodes x 3 hypotheses (`flatlay`, `verdict`, `object`), all passing
`check_thumbnail.py`. JPEG q3 for review; the PNG masters are not kept.

**These are the record, because they are not reproducible.** The props regenerate
exactly (`studio/originate/<slug>/render_data/thumb-<archetype>.json`), but each one
composites over a diffusion-generated ground in `studio/remotion/public/thumbs/`,
which is gitignored and generated without a captured seed. Delete those grounds and
these images cannot be recreated -- only replaced with different ones.

That is a real gap. Either `generate_scene.py` should record the seed fal returns, or
the grounds should stop being gitignored. Not fixed yet.

Read them at 120px before judging: `docs/thumbnail-design-language.md` S9.
