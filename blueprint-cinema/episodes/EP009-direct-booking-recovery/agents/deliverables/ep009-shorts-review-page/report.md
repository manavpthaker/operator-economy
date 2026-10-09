# EP009 Shorts private review page

Created `index.html` as a mobile-first, same-origin review surface for the four 9:16 preview compositions.

## Review order

Short 02 is presented first and marked **Recommended first review** because it shows the real tool workflow and tests whether the software remains legible in the vertical composition.

## Exact candidate durations

- Short 01 — The second commission — `59.458333` seconds
- Short 02 — What the machine does — `20.5` seconds
- Short 03 — The guest book moved — `33.583333` seconds
- Short 04 — The commission number is wrong — `22.5` seconds

## Contact-sheet inputs

The page accepts these relative, same-origin paths from its own directory:

- `contact-sheets/short-01.png`
- `contact-sheets/short-02.png`
- `contact-sheets/short-03.png`
- `contact-sheets/short-04.png`

Missing images produce an explicit placeholder. Absolute, protocol-relative, and cross-origin image sources are rejected by the page script.

## Boundaries

- Preview compositions only.
- Contact sheets only; no finished Short render is represented.
- No release, upload, publication, public-copy, or canonical approval is implied.
- No server was started and no canonical QA file was changed.
