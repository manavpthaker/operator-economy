# SELFIE-AVATAR-003 — production recipe

Written down because the last attempt spent a session re-deriving decisions
that already existed. Read this before generating anything.

## Assembly is already solved — do not hand-roll it

`blueprint-cinema/experiments/SCREEN-LISTICLE-001/build/` has `generate.py`,
`template.tpl` and a `package.json` that runs
`npx --yes hyperframes@0.8.38 render --fps 24 --quality high --crf 16`.
That template already contains caption grouping (`phrases(ws, max_chars=26)`),
the `#hook-title` staggered GSAP reveal, and the compositing structure.
This experiment's job is to produce that pipeline's INPUTS, not to rebuild it.

## Voice — locked

- Guide: Google `gemini-2.5-pro-tts`, voice **Algieba**.
- Transfer: ElevenLabs `eleven_multilingual_sts_v2`, voice **Original C**
  (`scMbPZwQjr40V1MzL3Nj`).
- Settings: similarity 0.8, stability 0.4, style 0, speed 1, speaker_boost on,
  seed 2026082501, `pcm_48000`, `remove_background_noise` false.
- Gate: faster-whisper `small.en` AND `medium.en`, beam 5, VAD on, no
  previous-text conditioning, no initial prompt. A miss on BOTH engines is a
  real failure; a miss on one is an artifact.
- Accepted take: `media/voice/voice-w4g.original-c.wav`, 64.366s, 198 words.
- Word timings: `voice/asr-final/FINAL-WORD-TIMINGS.json` (198:198, two
  documented repairs).

## Avatar shots — Seedance then sync

Architecture matters: Seedance must NOT act out the speech and then have sync
paint over a moving mouth. Generate the take, then sync.

    model            seedance_2_5
    mode             omni_reference
    resolution       720p
    bitrate_mode     high          <- easy to forget, visibly worse without it
    generate_audio   false
    aspect_ratio     9:16

Then one pass of `fal-ai/sync-lipsync/v3` with `sync_mode: "silence"`.
**v3, not v2**, and the sync_mode is not optional.

Framing: WIDE reads better than close-up. `motion-test-01` (wide desk) held up;
`avatar-close-02` did not — its own record says lip-sync models over-animated
when repairing a close-up. Keep takes short; the 11s take drifted, and every
take in `media/sections/SHOT-PLAN.json` is now under 7.3s.

### Two prompt rules learned the hard way

**Ask for ordinary blinks, not for none and not for slow ones.** Saying "slow
natural blinks" makes Seedance *perform* blinking — deliberate, held-closed eyes
that read as wrong. But the correction "eyes open and steady, no deliberate
blinking" is worse: a person who does not blink for seven seconds is uncanny,
and that version was rejected as stiff. The wording that works is "blinks
naturally and unremarkably, as often as anyone does — ordinary quick blinks,
never slow, held or emphasised."

**The take must ARRIVE and then ANCHOR.** This is the single biggest thing, and
it is not in this file by accident — it was diagnosed in the v8 work and then
ignored here for three rounds. From
`content-os/.../tuesday-video-v1/avatar/MOTION-REFERENCE.json`:

> The swivel was reproduced; the settle was not. In v8 the lean onto the desk is
> what ends the move and anchors the subject for the whole spoken section. Ours
> has nothing settling it, so the head floats for thirteen seconds, which also
> gives the lip sync a less stable face to drive.

So: the opening take starts in a DIFFERENT position (sitting back, turned toward
the window), swivels to camera, brings the hands up, lowers the forearms onto
the table and leans in, arriving by ~2.5s — and never sits back up. Every other
take starts already anchored with forearms on the table. Stillness has to be
*earned* by a move that resolves into it; a take that is simply still from frame
one reads as a mannequin, however good the lip sync is.

The anchored pose lives at `media/reference/selfie-anchored.png`. Note that
`selfie-rest.png` has his hands below the frame — nothing settles him — which is
exactly the floating-head failure. Do not drive takes from it.

**Small human movement is required, not optional.** Weight shifts, a head tilt,
fingers moving on the table, shoulders settling. Prompts that say only what must
NOT move produce a corpse with a moving mouth.

**Start and end frames must be at the SAME camera distance.** The closing shot
paired a wide start (`table-closing-still`) with a tight end (`table-cover-still`,
a close-up of the cover) and the model resolved the mismatch by GROWING the book
— the shut book ended up wider than the open spread, which is impossible.
`table-closed-still` exists purely to be a correctly-scaled end frame, and its
prompt says so. When an object changes shape during a shot, also say which way
its size must go: "as it closes it becomes NARROWER, about half the width".

## Book shots — stills first, then motion

Never generate a book shot straight to video. Make the still, look at it, then
animate it. Same Seedance block as above with the still as `start_image`, and
prompts that say explicitly what must NOT move — the printed words warp the
moment the model thinks it has licence to move the page.

Stills: `littlefables/scripts/render-mockups/_bookshots.ts <shot>…`
(takes shot keys so a re-run cannot overwrite an approved still).

The pages on screen must be **Mikey's pages**, not a demo book's — the script
is about that book. Generated by:

    littlefables/scripts/render-mockups/_mikey-spread.ts    # art plates
    littlefables/scripts/render-mockups/mikey-spreads.sh    # typeset spreads

Spread pages are chosen against the voiceover, not at random: p30 under "she
tells him she's wanted to be a moto", p33 under "they both want to be the
thing the other one already is".

## What is NOT in this video, and why

**A range-of-books shot was cut on 2026-09-23.** The plan had `book-range`
(44.46–56.62) showing six covers under "So I make them for other people's kids
now." Only two books in the repo are illustrated — `azad-and-the-cheetah` and
`one-step-then-me`, and the second belongs to a real customer's household and
carries a real child's name. Six invented demo covers under that line would
claim delivered work that does not exist. That is the same class of claim the
Etsy listing had stripped out the same week ("personalized", "book in 3–4
days", the questionnaire-deletion promise). The Etsy listing can show the demo
covers because it carries an ABOUT THE IMAGES disclaimer; a video does not.

Replaced by `avatar-howitworks` (44.46–48.42, cut on the comma after "right
now,") and `book-closing` (48.42–56.62), which claim nothing. The original plan
is kept at `media/sections/SHOT-PLAN.v1.json`.

Note also that **Mikey has no illustrations in the repo** — the covers and
spreads in this video were generated for it. That was a knowing choice by the
author about his own son's book; it is not a precedent for showing other
people's books that do not exist.

## Cost

Seedance 720p/high, 7s vertical: **49 credits**. Balance was 3,198 (Max plan).
Not a constraint — an earlier note quoting 31 credits was stale.
