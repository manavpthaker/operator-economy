# EP007 Shorts 03–04 sound-on implementation plan v1

## Locked direction

Adapt the owner-accepted Short 01 grammar: clean full-frame presenter, content-specific working
screens, presenter return, exact foreground captions, and a separate two-second visual-only episode
route. Do not restore persistent branding rails and do not clone Short 01’s worksheet mechanism.

## Prepared now

| Short | Original C | Spoken frame end | Final duration | Caption coverage | Presenter source state |
|---|---:|---:|---:|---|---|
| 03 · How You Charge | 37.616333s | 37.625s | 39.625s | 98/98 once; 80 rail + 18 exact scene text | browser-safe muted opening bound; return missing and held |
| 04 · Test the Front Door | 46.114833s | 46.125s | 48.125s | 126/126 once; 101 rail + 25 exact scene text | opening missing and held; browser-safe muted return bound |

The per-short `ASSEMBLY-MANIFEST.json` files contain the exact scene windows and word-aligned local
reveal beats. The current silent `index.html` and scene files remain untouched.

## Implementation order after owner retry direction

1. Complete only the missing Short 03 return and Short 04 opening presenter sources; restore each to
   browser-safe, audio-free H.264 and bind its hash.
2. Derive new host overlay variants from the current static-plate scenes. Remove only the static
   identity image/disclosure; preserve the content-specific foreground graphics. Short 04’s return
   variant must resolve the existing phrase panel’s collision with the exact caption rail.
3. Derive word-aligned variants of the working-screen scenes using the local beats in each assembly
   manifest. VO retiming reopens every seam; do not mutate the accepted silent sources.
4. Create a new sound-on root index per Short: muted presenter video, retimed screen variants,
   caption sub-composition at track 60, one continuous Original C WAV as the only audio at track 100,
   and the existing two-second route after the spoken frame end.
5. Run the scaffold check, HyperFrames full check, motion/seam verification, targeted snapshots, and
   private sound-on phone review. Stop for owner acceptance before any render delivery, upload,
   Related Video binding, release, or publication.

## Current stop condition

Do not mount or render. The picture source set is incomplete: Short 03 return and Short 04 opening
remain on hold pending owner retry direction.
