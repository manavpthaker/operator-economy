# Final-Master Intentional Pause Map

Template version: proposed Step 2 v0.2.

This map distinguishes approved semantic silence from a missing word or an editor gap. It is derived
from the exact final narration master and does not modify the canonical `W` sequence.

## Authority

- Episode or fixture ID:
- Locked script SHA-256:
- Ordered `W`-token count/SHA-256:
- Narration master path/SHA-256:
- Master duration in integer milliseconds:
- Word-transcript path/SHA-256:
- Map revision:
- Reviewer/date:

## Pauses

| Pause ID | Previous `W` ID | Next `W` ID | Start ms inclusive | End ms exclusive | Function | Source intent | Preserve for Step 3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0001 | | | | | identity / thought / contrast / comprehension / landing | Step 1 / direction / approved edit | yes / no |

## Invariants

- Every interval satisfies `0 <= start_ms < end_ms <= master_duration_ms`: yes / no
- Pause intervals do not overlap canonical word intervals: yes / no
- Previous and next `W` IDs are valid and ordered: yes / no
- Every listed pause is heard and intentionally approved: yes / no
- Silence caused by dropout, corruption, or missing speech is excluded and repaired: yes / no
- Master hash and duration match the final word transcript: yes / no

## Decision

- Result: passed / failed / revise
- Uncertain or disputed pauses:
- Transcript editor/signature/date:

Any sample-level master change invalidates this map. Step 3 may design around a preserved pause but
may not fill, shorten, or remove it by changing the narration master.
