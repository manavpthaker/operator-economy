# EP009 r8 Shorts editorial map

## Result

Four current-r8 candidates are selected and ranked. All spoken text is a contiguous verbatim range from the locked r8 carrier. No historical Short copy was promoted into the current packet.

| Rank | Candidate | Word IDs | 24 fps source frames | Cut duration | Unresolved handoff |
|---:|---|---|---|---:|---|
| 1 | The second commission | `W000000` to `W000165` | `[0, 1427)` | 59.458 s | What did the repeat stay cost, and who gets paid to stop it? |
| 2 | What the machine does | `W002001` to `W002053` | `[16619, 17111)` | 20.500 s | What human judgment makes the automation hospitality? |
| 3 | The guest book moved | `W000941` to `W001038` | `[8070, 8876)` | 33.583 s | If the parts are cheap, why does the inn not do this itself? |
| 4 | The commission number is wrong | `W001401` to `W001475` | `[12150, 12690)` | 22.500 s | What portion can the recovery service actually shift? |

The machine passage ranks second because it uses the clarified r8 software-demo section and ends before the episode explains the judgment rules. The commission passage ranks fourth because its figures need more visual room and careful caption handling on a narrow canvas.

## Timing method

The word transcript supplies first-word and last-word times. Cut frames use `[in_frame, out_frame_exclusive)` at 24 fps. The first candidate starts at episode frame 0. The other starts floor to the frame containing the first word; every end ceils past the last word. This retains the full timed word range while adding no narration.

The r3 timemap is the current output clock. `SHOT-PLAN.json` describes scene intent and lanes, but its authored frame numbers predate the brand excision and corrected hospitality paragraph. They were not used as r8 cut coordinates.

## Historical briefs

The prior `shorts_briefs.json` was reviewed only for provenance. Its four proposed hooks were rejected as current copy:

- The thirty-percent commission line is absent from r8. The current episode uses an explicitly labeled eighteen-to-twenty-two-percent model assumption.
- The named-provider RevPAR-uplift language is absent from r8.
- The website-only hook is absent from r8 and is less precise than the locked front-desk constraint.
- The Coqui Coqui and fifty-person claims are absent from the corrected r8 narration.

## Boundaries

This is an editorial extraction map. It does not approve public titles or comments, select a portrait layout, alter captions, render media, or change episode state. Any episode link in a future pinned comment must come from the canonical launch links record.
