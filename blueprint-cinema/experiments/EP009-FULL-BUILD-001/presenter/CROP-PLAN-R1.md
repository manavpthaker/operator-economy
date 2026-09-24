# EP009 presenter crop plan, fix round 1 (edit lane)

Findings: B-23 (one wide frame across the set), A-13 (P04 held hand), B-04 (P08 still hands), B-21 (P12 to P13 same-crop cut), A-07 (P01 picture lead).
Built by `presenter/_tools/edit_r1.py` from each take's existing `restored.mp4`. No generation. Every crop change is a hard size change on continuous source time, placed on a low-motion frame between words (motion = mean lower-frame difference, all cut frames at or below 0.3 on the lane's scale). Audio is the sample-exact master excerpt in every clip.

## Sizes (1920x1080 source, centred on the take's median nose x, measured with face mesh)

| Code | Crop | Scale vs wide | Shows |
|---|---|---|---|
| W | full frame | 1.00 | whole body, hands on the table |
| M | 1536x864, y 0 | 1.25 | waist up; table hands out, raised gestures in |
| C | 1280x720, y 0 | 1.50 | chest up (the build's existing close) |
| C2 | 1152x648, y 24 | 1.67 (1.11 upscale) | P08 admissions only, so M to C2 is a 1.33x change |

## Per segment (segment frames; master seconds)

| Seg | Take | Crop sequence | Why |
|---|---|---|---|
| seg009 | P01 | W 0-219 | First appearance establishes the room and the "anyone" gesture. Picture slipped 6 frames (A-07). |
| seg012 | P02 | C 0-151 (73.542-79.875); W 152-342 | The service sentence is close; "By the end" widens for the four-numbers sheet gesture. |
| seg019 | P03 | C 0-37; W 38-332 (190.250-202.542); C 333-393 | Opens close on "the question"; wide for the two placements (site, inn); narrows on "can somebody from outside get paid". |
| seg021 | P04 | W 0-95; C 96-169 (230.208-233.292); W 170-241 | Chest touch and the ceiling line are drawn in wide; the held line runs close; "By the end" returns wide as the hand lowers (A-13). |
| seg028 | P05 | M 0-128 | Short question; both palms up stay in frame at the lower edge. |
| seg035 | P06 | C 0-99; W 100-257 (473.458-) | Recall admission close; wide from "It's that" for the separating hands. |
| seg037 | P07 | M 0-107; W 108-283 (524.917-) | Lean-back sentence medium; wide from "because" for the set-aside sweep and the slide on "can shift". |
| seg044 | P08 | M 0-229; C2 230-349 (676.167-681.167); W 350-548 | Credentials medium; admissions narrow (I've never owned ... anybody); wide from "So" so the one hand turn (685.1-686.3) shows (B-04). |
| seg055 | P09 | M 0-160 | Medium-close throughout (B-23); the flat palm on the table is out of frame. |
| seg059 | P10 | W 0-32; C 33-151 (977.917-) | Closer from "It's a foothold" (B-23); the palm step on "Up the band" is out of frame. |
| seg071 | P11 | W 0-29; C 30-96; W 97-448; C 449-513 (1193.750-1196.458) | Existing close on "is build. Bounded." kept; new close from "and it costs you three properties and a month" so the join into P12 is a size change. |
| seg072 | P12 | W 0-190 (unchanged) | |
| seg073 | P12 | C 0-226 (unchanged) | |
| seg074 | P13 | W 0-287 | Take change P12 to P13 now coincides with close to wide, and P13's pay, wave-off and size gestures show (B-21). |
| seg075 | P13 | W 0-185 (unchanged) | Same continuous source as seg074; there is no cut at 1225.875, so the shared size is one shot, not a join. |

## Adjacency check (outgoing crop to incoming crop across presenter appearances)

seg009 W to seg012 C; seg012 W to seg019 C; seg019 C to seg021 W; seg021 W to seg028 M; seg028 M to seg035 C; seg035 W to seg037 M; seg037 W to seg044 M; seg044 W to seg055 M; seg055 M to seg059 W; seg059 C to seg071 W; seg071 C to seg072 W (contiguous take join, 1196.458); seg072 W to seg073 C (same take, crop change); seg073 C to seg074 W (contiguous take join, 1213.875). No two adjacent presenter segments open and close on the same size, except seg074 into seg075, which is one uninterrupted shot.

Opening crops across the 13 takes: W 6, M 4, C 3 (was W 12, close 1). Wide-only takes: 2 of 13 (P01, P13), was 9. No crop change cuts through a hand action: every change frame sits in a stretch with motion at or below 0.3.

## A-07 measurement (P01, and P03, P05 checked)

Method: MediaPipe face mesh inner-lip distance (landmarks 13 and 14, normalised by face height) per frame of `restored.mp4`, against the file's own audio RMS per frame; plus event matching at pauses.

- P01: the mouth opens widest (10 percent) on restored frames 17 to 22, in silence, and is nearly closed on the loud "I couldn't" (frames 24 to 31). Mouth closures at 25-31, 44-46, 84-86, 89-90 match audio dips 6 frames later (32-33, 52-54, 90, 94). Zero-lag correlation over frames 14-100 was -0.42. Picture led by about 6 frames (250 ms). Later in the take the evidence is weaker (closures at the 99-119 pause and the end fit 0 to +2 frames), so the slip was chosen from the first 4 s, where the fault is visible.
- Fix: seg009 now starts at restored frame 7 instead of 13. After the slip the widest opening lands on segment frames 11 to 15, with "I" audio starting at segment frame 11; the 0.46 s of silence shows a relaxed mouth with hands on the table and the gesture begins with the word. Whole-take lip/energy correlation moved from -0.07 at zero lag (best -8) to +0.08 at zero lag (best +1). Strips: `P01/qa/sync-r0-12fps-mouth.png`, `P01/qa/sync-r1-12fps-mouth.png`.
- P03: mouth closed through the silence and opens on the first audio frame of "Which" (restored 18 to 19). Onset aligned within one frame. No change.
- P05: mouth closed through the silence and opens on the first audio of "Fair" (restored 17 to 18); whole-take best lag 0. No change.

Limits: lip-opening against audio energy is a coarse signal (P01 peaks near 0.25 even after the slip). Nobody has watched these at normal speed with sound; that remains the check that decides sync. A-13's held hand still appears at the lower left of the close frame (no crop that excludes it avoids a 2x upscale).
