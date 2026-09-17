# EP009 presenter regeneration: crop plan

Method follows `presenter/CROP-PLAN-R1.md`: every crop is a hard size change on continuous source time or on a part boundary; crops are centred horizontally on the part's median nose x (face mesh), clamped to the frame, top-aligned (y 0) so headroom is kept. 720p parts use wide or medium only.

## Sizes

| Code | 1080p source | 720p source | Scale vs wide | Shows |
|---|---|---|---|---|
| W | 1920x1080 | 1280x720 | 1.00 | seated at the table, both hands |
| M | 1536x864 | 1024x576 | 1.25 | waist up; raised hands in, table hands at the lower edge |
| C | 1280x720 | not used | 1.50 | chest up |

## Per segment (film order)

| Seg | Parts | Crop sequence | Why |
|---|---|---|---|
| seg009 | P01 (720p) | W | First appearance establishes the new room and look. |
| seg012 | P02a, P02b | C, then W at 79.667 | Definition close; the promise widens so the "four numbers" hand lift shows. |
| seg019 | P03a, P03b | M, then C at 194.750 | "The question" medium with the open palm in frame; the question itself narrows. |
| seg021 | P04 | W | The flat hand lowering onto the table shows. |
| seg028 | P05 (720p) | M | Short objection; both palms up sit in frame. |
| seg035 | P06 | C | First-person recall; the hand to chest reaches the lower edge. |
| seg037 | P07a, P07b (720p) | W, then M at 523.708 | Short setup wide; the turn medium with the set-aside motion in frame. |
| seg044 | P08a, P08b, P08c | W, then C at 676.042, then M at 681.042 | Credentials wide; the admission close; "So I know" medium with the open palm. |
| seg055 | P09 (720p) | W | Plain refusal, no gesture. |
| seg059 | P10 | M | Ruling; the small step up on "Up the band" stays in frame. |
| seg071 | P11a, P11b | C, then W at 1186.167 | Verdict close; the reasons widen so the flat hand onto the table shows. |
| seg072 | P12a | M | Candid limit; hand to chest in frame. |
| seg073 | P12b | W | First move; the hand lift off the table shows. |
| seg074 | P13a, P13b (720p) | M, then W at 1223.833 | Ask with the open palm medium; "Right now nobody knows" wide. |
| seg075 | P13b (720p) | M | Same continuous source as the end of seg074; a size change on continuous time at 1225.875 for the ask. |

## Adjacency (outgoing size to incoming size across presenter appearances)

seg009 W to seg012 C; seg012 W to seg019 M; seg019 C to seg021 W; seg021 W to seg028 M; seg028 M to seg035 C; seg035 C to seg037 W; seg037 M to seg044 W; seg044 M to seg055 W; seg055 W to seg059 M; seg059 M to seg071 C; seg071 W to seg072 M (contiguous, part join); seg072 M to seg073 W (contiguous, part join); seg073 W to seg074 M (contiguous, part join); seg074 W to seg075 M (continuous source). No two adjacent presenter appearances share a size, and every part join changes size.

Opening sizes of the 15 segments: W 6, M 6, C 3. 720p parts: W or M only.

This plan is set before generation. If a gesture lands outside its planned crop or a crop change cuts through a hand action, the conform record says so; sizes stay as planned unless adjacency is kept.
