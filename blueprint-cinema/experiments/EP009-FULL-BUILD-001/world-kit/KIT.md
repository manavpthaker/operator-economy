# EP009 world kit

Status: shared build asset for `EP009-FULL-BUILD-001`, written by the world kit lane 2026-09-16. Agent
work, not owner accepted. Every model and evidence builder imports from here so four act builders
produce one continuous-looking episode.

## Files

| Path | What it is |
|---|---|
| `kit.svg` | 63 `<g>` definitions with stable `kit-*` ids, defs only. Generated; do not hand edit. |
| `tools/build_kit.py` | The generator. Change geometry here, then `python3 tools/build_kit.py`. |
| `tools/kit_defs.py` | Copies definitions into a composition (`list`, `defs`, `inject`, `inline`). |
| `evidence-surface.html` | Reusable evidence card composition (R53/R54 A card), JSON-configured. |
| `showcase/` | HyperFrames project laying out every object (frames A, B) plus frame C in the R57 layout. |
| `showcase/evidence-{single,pair,rows}/` | The evidence surface rendered in its three layouts. |
| `showcase/comparison/` | Builds the side-by-side still. |
| `showcase/qa/` | Rendered mp4s and stills: `frame-0.5.png` (A), `frame-1.5.png` (B), `frame-2.5.png` (C), `evidence-*.png`, `comparison-ep007-r57-vs-kit.png`. |

## Where the construction comes from

Bound from accepted EP007 frames (decision-method "bind a nearby accepted animation frame"): R60 S15 part 1,
R57 S13ab, R54 S11b and S11cd, R48 relationships, R46 revenue machine, evidence R53 and R54 A.

- `kit-person`, `kit-table`, `kit-practice-card`, `kit-empty-place`, `kit-sheet` and both checkboxes are
  **verbatim** EP007 geometry. Every EP009 figure is `kit-person` plus at most one small mark inside or
  beside its silhouette. Proportions never change.
- The inn, booking site, tags, slip, book and cards are new objects drawn in the EP007 workshop
  construction (case early-01): short partial strokes with gaps, open corners, overshoot, unequal steel
  retraces, sparse hatch, paper-backed fills. Offsets are seeded at build time, so geometry is fixed and
  nothing wobbles at render time.

## Continuity rules (never change these)

Palette: paper `#F5F0E6` (page background), sheet `#FBF8F1`, card `#EDE5D6`, ink `#173530`, steel
`#586D74`, muted text `#33464C`, oxide `#B5482F`.

| Mark | Stroke | Use |
|---|---|---|
| Figure and object contour | ink 3 (cards 3.5, inn/site walls 2.2 to 2.8) | primary form |
| Construction retrace | steel 1.0 to 1.3 | lighter second pass, never a filter |
| Relationship / route line | steel 2.5 | `.kit-route` |
| Hypothesis or not-yet route | steel 2.5, `stroke-dasharray: 10 8` | `.kit-route-dashed` (S10 slice, "Say" marker) |
| Pay line firmed to its event | ink 4 | `.kit-pay` (R54) |
| Empty place / absent object | ink 3, dash `12 9`; steel 2, dash `6 5` for small absences | R57 gap outline |
| Boundary | 5, one vertical stroke | R59 |
| Bar (hours, fee) | 12, butt cap | R60 |

Type (fonts: Boska 700, Supreme 400/500 from `public/fonts`):

| Role | Spec |
|---|---|
| Heading | Boska 700, 60 to 64 px, centred at top 22 to 55 px, `#173530` |
| Label | Supreme 500, 27 px, ink |
| Small label / note | Supreme 400, 22 px, `#33464C` |
| Kicker | Supreme 500, 21 px, letter-spacing 2 px, uppercase, `#33464C` |
| Inside-object labels | Supreme 400 20 px (slip labels, field names), values Supreme 500 24 to 28 px |

Rules:

1. **One oxide accent at a time**, only on the accountable action. Oxide-capable objects use
   `currentColor` (`kit-ceiling-line`, `kit-boundary`, `kit-checkbox-checked` mark): set
   `color="#173530"` on the `<use>` by default, `color="#B5482F"` for the one accent. Everything else is
   hard-coded ink or steel. Check oxide in the rendered still (a CSS class `fill` beats an attribute).
2. **Scale uniformly only** (`scale(s)`), never stretch. Figures: 1.0 at a desk, 0.6 in a row of roles,
   0.34 to 0.42 in groups. Below scale 0.5 use `kit-inn-mini` instead of `kit-inn`.
3. **One identity per object.** The guest is the only figure with a daypack; the innkeeper is the only
   figure with the cardigan V; the practice / You is the only figure holding the practice card. Every
   commission tag is `kit-commission-tag` at the same size.
4. **Handwriting only as pencil marks inside drawings** (book entries, signature, notes). Every word,
   number, name, receipt and caveat is typeset.
5. **Allowed motion:** translate, uniform scale, opacity (recede to 0.35 to 0.5, never below 0.2 for a
   persistent object), stroke draw-on of a part from an inline copy, dashed to solid on the object's
   word. Restore a dashed pattern after a dashoffset draw-on and confirm it in a still.
6. **Never:** tear, lock, cage, grey out or cross the guest book; red or villain treatment of the booking
   site; logos; a checked S19 box; a rising line or arrow implying a result; idle wobble or jitter.
7. Paper background is the page (`background:#F5F0E6` on the root), not part of any object.

## How to import

Put these markers inside an inline hidden SVG in your composition, then inject only the ids you need
(dependencies such as `kit-person` come along automatically):

```html
<svg id="s05-defs" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<!-- KIT:DEFS:BEGIN -->
<!-- KIT:DEFS:END -->
</defs></svg>
<svg viewBox="0 0 1280 720" role="img" aria-label="...">
  <use href="#kit-desk" transform="translate(130,450)"/>
  <use href="#kit-innkeeper" transform="translate(250,392)"/>
  <use href="#kit-guest" transform="translate(600,236) scale(.6)"/>
  <use href="#kit-inn" transform="translate(820,330) scale(.625)"/>
  <use href="#kit-ceiling-line" transform="translate(700,300)" color="#B5482F"/>
</svg>
```

```bash
K=blueprint-cinema/experiments/EP009-FULL-BUILD-001/world-kit
python3 $K/tools/kit_defs.py inject scenes/seg020/index.html kit-inn kit-desk kit-innkeeper kit-empty-place
python3 $K/tools/kit_defs.py inline kit-ceiling-slip-filled --prefix s10-slip   # animate single parts
cp $K/kit.svg scenes/seg020/public/art/kit.svg   # keep the source copy the conventions ask for
```

- Injected definitions are one line per object (keeps the file under the HyperFrames length lint).
- `<use>` clones cannot be animated part by part. To draw one box, one tspan or one page entry, paste
  the `inline` output into your SVG (ids renamed `prefix__part`) and animate those ids.
- Text in kit objects sets `font-family="Supreme, sans-serif"` as an attribute; your composition must
  declare the Supreme `@font-face`. A global `text{}` CSS rule in your file would override it; do not
  write one.
- CSS for your own lines (copy as is):

```css
.kit-route{stroke:#586D74;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round}
.kit-route-dashed{stroke:#586D74;stroke-width:2.5;stroke-dasharray:10 8;fill:none;stroke-linecap:round}
.kit-pay{stroke:#173530;stroke-width:4;fill:none;stroke-linecap:round}
.kit-light{stroke:#586D74;stroke-width:1.3;fill:none;stroke-linecap:round;stroke-linejoin:round}
.kit-label{font-family:Supreme,sans-serif;fill:#173530;font-size:27px;font-weight:500}
.kit-small{font-family:Supreme,sans-serif;fill:#33464C;font-size:22px;font-weight:400}
.kit-kicker{font-family:Supreme,sans-serif;fill:#33464C;font-size:21px;font-weight:500;letter-spacing:2px}
```

Coordinates below are native units; origin is top-left unless stated. Figures use the EP007 origin:
(0,0) mid-torso, head top at y -108, hands line at y 39, width -64 to 64. A figure sits at a desk or
table when its origin is 120 px right of the top's left end and 58 px above it.

## Objects

### People

| id | Depicts | States / parts | Native size |
|---|---|---|---|
| `kit-person` | generic person (EP007 verbatim) | none | 128x147, figure origin |
| `kit-guest` | the guest, daypack mark | none | figure origin, pack to x 83 |
| `kit-innkeeper` | the innkeeper, cardigan V | none | figure origin |
| `kit-practice-figure` | the practice / "You" (not the presenter) | none | figure origin, card to x 77 |
| `kit-crowd` | nine travellers at 0.34 | none | about 245x100 |

### Places and furniture

| id | Depicts | States / parts | Native size |
|---|---|---|---|
| `kit-desk` | the inn's front desk counter, bell, card stack | none | 240x100, origin at top line left |
| `kit-table` | small table (EP007 verbatim) | none | 240x68, origin at top line left |
| `kit-inn` | the inn: 20 room windows (two rows of ten), lobby cutaway with desk, door, porch | overlays below | 480x304 (chimney to y -5) |
| `kit-inn-window-lit` | one room window lit | place at x = 38 + i*42, y = 88 or 144 | 24x28 |
| `kit-inn-own-page-dashed` / `kit-inn-own-page` | the inn's own page before / after a job makes it live | place at (372, 214) in inn units | 54x63 |
| `kit-inn-mini` | same inn, half size, for groups of inns | none | 240x152 |
| `kit-hotel-large` | larger independent hotel (S09) | none | 220x216 |
| `kit-booking-site` | the booking site: lit hall, six lit bays, neutral | listing slots at bay centres x = 58 + i*64, y = 180 | 440x286 |
| `kit-booking-site-simple` | the booking site, S00 simple form | none | 160x126 |
| `kit-listing-card` / `kit-listing-card-inn` | listing inside the hall; the inn's has a gable glyph | none | 35x26 |
| `kit-wall-hook` | empty "marketing" hook | none | 16x26 |

In inn units the lobby desk top centre is (154, 261), the door centre (308, 258).

### Tags, lines and markers

| id | Depicts | States / parts | Native size |
|---|---|---|---|
| `kit-commission-tag` | commission tag, no number | solid | 64x40, string to x -16 |
| `kit-commission-tag-empty` | the empty place of a tag | dashed steel | same footprint |
| `kit-tag-service` | dashed "a service" shape inside a tag | overlay at tag origin; solid in S21 via inline copy | 32x22 |
| `kit-commission-tag-layers` | the tag enlarged with four layer rows | rows y 12-46, 46-84, 84-120, 120-156, text from x 96 | 252x156 |
| `kit-rate-tag` | blank room-rate tag | none | 56x34 |
| `kit-retainer-tag` | retainer tag, no price | none | 96x45 |
| `kit-ceiling-line` | the ceiling line | `currentColor` | 360 wide |
| `kit-ceiling-line-ghost` | sensitivity ghost ceiling, steel 50% | none | 360 wide |
| `kit-boundary` | boundary in front of one action ("the site's rules") | `currentColor`; label centred at (0, 236) | 5x196 |
| `kit-route-solid` / `kit-route-dashed` / `kit-pay-line` | line style samples | draw your own geometry with the CSS above | 200 wide |
| `kit-timeline-line` / `kit-tick` | stay timeline and event ticks | none | 900 wide / 24 tall |
| `kit-empty-place` | the empty place after checkout (R57 gap outline) | none | 150x170 |
| `kit-checkbox-empty` / `kit-checkbox-checked` | checkboxes (R46) | checked mark is `currentColor` | 24x26 |

### Paper

| id | Depicts | States / parts | Native size |
|---|---|---|---|
| `kit-ceiling-slip-blank` | slip, four empty boxes, one unlabelled line (S00h, S21 cleared) | parts `__title-line`, `__box1..4`, `__line` | 300x440 |
| `kit-ceiling-slip-labelled` | slip with Rooms, Rate, Occupancy, Share through the sites | + `__label1..4` | 300x440 |
| `kit-ceiling-slip-filled` | slip with 20, $180 a night, 70%, 63% (S10 illustrative inn only) | + `__value1..4` | 300x440 |
| `kit-job-findable` | job card: search, free link, own page | `__title` | 250x180 |
| `kit-job-bookable` | job card: two blank rate tags joined by "=" | `__title` | 250x180 |
| `kit-job-remembered` | job card: guest book, thank-you note, leaf | `__title` | 250x180 |
| `kit-practice-card` | the practice card (EP007 verbatim) | none | 150x170 |
| `kit-guest-book-closed` | guest book, closed, intact | none | 134x106 |
| `kit-guest-book-open` | guest book, open, blank pages, intact | none | 200x122 |
| `kit-guest-book-open-dashed` | the inn's own book not yet signed | turns solid (swap to `kit-guest-book-open`) in S15a | 200x120 |
| `kit-guest-book-entries` | name, town, envelope mark on the left page | overlay; parts `__name`, `__town`, `__envelope` | book units |
| `kit-signature` | signature on the right page | overlay | book units |
| `kit-registration-card` | card with two write-in lines and an Email field | parts `__label`, `__field`; field text at (34, 164) | 360x200 |
| `kit-text-own-email` | typeset "guest's own email" | origin at baseline | about 185 wide |
| `kit-text-relay` | typeset relay string for the card field | tspans `__local`, `__domain` | about 290 wide |
| `kit-relay-field` | reservation relay field `k7m2q9x4@guest.booking.com`, label "illustrative" | tspans `__local`, `__domain`, text `__illustrative` | 420x90 |
| `kit-reservation-record` | drawn reservation record (S00d screen insert) with the relay field in the Email row | none | 596x324 |
| `kit-report-slip` | report slip, "Direct share of bookings", one value box | `__title`, `__box`, empty `__value` | 380x208 |
| `kit-report-slip-before-after` | report slip with blank before and after boxes (S11b) | `__title`, `__box1`, `__box2` | 380x208 |
| `kit-sheet` | generic sheet (R46 verbatim) | none | 331x144 |
| `kit-card-small` | small dog-eared label card | text from x 16, baseline 46 | 200x110 |
| `kit-thank-you-note` | handwritten note, no readable words | none | 120x80 |
| `kit-seasonal-note` | leaf and trail note ("October" typeset by builder) | none | 120x80 |
| `kit-leaf` / `kit-envelope` | small marks | none | 30x36 / 48x32 |
| `kit-phone` | drawn phone, blank screen area x 8-68, y 16-116 | none | 76x136 |
| `kit-calendar-leaf` | calendar page | none | 120x132 |
| `kit-wifi-sign` | wifi login sign with email field (x 14-106, y 64-86) | none | 121x146 |

The relay string is invented and must always sit beside the typeset label "illustrative".

## Evidence surface

`evidence-surface.html` is the R53/R54 A card: kicker (Supreme 21 uppercase), source name (Boska 62),
steel rule at y 196, headline figure (Boska 105; 88 in pair, 64 in rows), plain-language line (Supreme
29), qualifier (Supreme 24 muted), interest note (right column, "Interest" label), receipt at the foot
(Supreme 21 muted). Copy it to your project root, edit only the `#ev-config` JSON plus the root
`data-composition-id` and `data-duration`, and add the audio at the AUDIO marker:

```html
<audio id="ev-narration" src="public/audio/narration.wav" data-start="0" data-duration="DURATION" data-media-start="0" data-track-index="100" data-volume="1"></audio>
```

Config keys: `layout` (`single`, `rows`, `pair`), `kicker`, `source`, `figure`, `line`, `qualifier`,
`interest {label,text}`, `receipt`, `rows [{figure,line,at}]` (max 4), `cards [{kicker,source,figure,line,
qualifier,receipt,cues}]` (exactly 2, separate populations), `recede {at,selector}`, `cues {source,
figure, line, qualifier, interest, receipt}` in seconds from composition start. Every item enters with a
8/24 s fade and 8 px rise, the accepted R53 motion. Receipts are the claims map "On-screen source receipt"
column verbatim; long receipts wrap to two lines. Rendered examples: `showcase/qa/evidence-single.png`,
`evidence-pair.png`, `evidence-rows.png` (sample strings from C001, C002, C004 and the plan).

The plan's other evidence shapes (S03 three-slot strip, S06 cancellation bars, S09 tags on the scale
axis) are not layouts of this file; build them from the same type specs and receipt foot.

## Verification record

- `npx --yes hyperframes@0.8.36 check --strict`: showcase and the three evidence projects pass (0 errors,
  0 warnings; one info-level caption overflow note was fixed).
- Stills looked at: frames A, B, C and the three evidence cards; fixes made after looking: a lobby window
  that read as a rising chart line was redrawn as a hill and tree; a head mark on the innkeeper that
  changed the figure's silhouette was replaced by a cardigan V inside the torso; inn windows moved off
  the wall lines; inn contours strengthened to match the workshop's weight; pair cards and row figures
  no longer overlap.
- Not judged: motion (the kit is static), phone-size legibility of steel 1.0 retraces, and whether the
  owner reads the booking site's pediment as neutral. Nothing here is owner acceptance.
