# EP009 direction plan: a direct-booking practice

Status: director plan for the autonomous full build `EP009-FULL-BUILD-001`. Nothing here is built,
generated, spent or accepted. Agent reviewer verdicts on the built scenes are recommendations; the
owner reviews one full cut at the end (`ep009-autonomous-build-scope-v1`).

Machine contract: `SHOT-PLAN.json` in this folder. Where this file and the JSON disagree on a time,
the JSON wins; where they disagree on meaning, stop and ask the director.

## Authority and inputs

| Input | Path | SHA-256 |
|---|---|---|
| Narration master (1233.602 s, 48 kHz 16-bit mono) | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav` | `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944` |
| Word transcript (timing authority) | `.../02-narration-production/word-transcript.json` | `3c28411effaea94c4dffaac51e114f333f386170fe4716fa96b30d24e41384aa` |
| Intentional pause map | `.../02-narration-production/intentional-pause-map.json` | `62811b5f0ae93359d520f7adfec06ebf46404e8e146cedf274b1f327f9a5cd84` |
| Claims map (every on-screen number, source and caveat) | `.../01-editorial/claims-map.md` | `37f9f4727cde1b7e52fd75745117685336a28ec5f6756cf5f1be3dea1bb68798` |
| Build scope and spend caps | `blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records/2026-09-16-owner-build-scope.json` | `f6417f381836c406230ec06c8c90db6244de1ae03b02e275091718d3b9a3d845` |
| Precedent audit | `blueprint-cinema/episodes/EP009-direct-booking-recovery/review/PRECEDENT-AUDIT.md` | `4d10ce1a5592c833be52841ab5e0d570446e5f0ca0e5f1863aa107e30e50307d` |

Cue notation: `W001636 hypothesis 581.86` is word ID, token and master onset seconds from the word
transcript (always the onset, including where the text says "after" a word). Segment cut times in `SHOT-PLAN.json` were chosen on the waveform inside measured
silence and snapped to 1/24 s; builders never move a segment boundary.

EP007 precedents are cited by event or case ID with the condition under which they applied. None is
adopted as a rule. Where EP009's situation differs, the difference is stated.

## Visual thesis

One small inn, filmed at its front desk and drawn as the same place, shows where the second
commission comes from, why nobody at the desk is paid to stop it, and how four numbers set a
ceiling on what anyone can charge to do that job.

## The look (bound from EP007's accepted language)

- **Film:** photographed people at one physical front desk, narrated dramatization, never evidence.
  Kling v3 Pro image-to-video from an accepted establishing still, then from accepted frames
  (`lesson-start-frames-from-accepted-footage-v1`), one action per take
  (`lesson-i2v-ignores-timing-prompts-v1`).
- **Presenter:** the owner's V5 avatar recipe (wide study, navy shirt, glasses, forearms and hands
  visible), exact original narration restored after generation. Recipe and reference media IDs are
  in `SHOT-PLAN.json` `bound_references.presenter_recipe`.
- **Working Model:** rough authored pencil on cream paper, the construction of
  `hyperframes/reviews/r48-relationships` (workshop drawing, person grammar: circle head, open
  shoulders, short legs lines) and `r54-s11b` (neutral figures, pay lines drawn to one event).
  Handwriting only inside drawings; labels, numbers and receipts typeset in Supreme; framing headings
  in Boska or Zodiak as in R46 and R48. One oxide accent active at a time. Check oxide in rendered
  stills, not source (`lesson-svg-class-fill-beats-attribute-v1`).
- **Evidence surface:** the R53 and R54 A card: small caps kicker naming the source, serif headline
  figure in spoken rounding, a plain-language line, receipt and interest note at the foot. Receipt
  strings are the claims map's "On-screen source receipt" column, verbatim.
- **Identity:** the accepted EP007 sting and title card compositions, bound by hash in
  `SHOT-PLAN.json`. Continuity rule from `r40-owner-style-continuity-return-v1`: matching the palette
  is not enough; the drawn world, stroke construction and figure proportions must match.

## The persistent EP009 world

One model world carries the whole episode (`lesson-model-world-across-examples-v1`, which applied
when narration listed examples of one failure; here it applies because every section returns to the
same inn). Each object below has one drawn identity and changes only on its words.

| Object | First appears | Transforms | Pays off |
|---|---|---|---|
| **The inn** (drawn facade/cutaway: rows of room windows, a front desk inside, a door) and **the front desk** (filmed counter) | Film F01 at 0.000 (the counter); drawn at S03a `W000247 Start 87.86` | S03f gets the 20 to 40 room bracket; S05 its stay timeline; S11 becomes one of a handful of inns; S17 six inns on a route | S20 film returns to the same counter; S20e drawn inn receives a booking through its own page |
| **The innkeeper** (filmed woman, olive cardigan; drawn desk figure) | F01 | S08 job cards converge on her; S12 sits across from "You"; S18 owner's desk | S20 F10 writes the thank you by hand she could not send in S00 F03 |
| **The guest** (filmed man, navy rain shell; drawn figure with a small daypack mark, the only figure with that mark) | F01 | S00e returns a year later; S03b compares on his phone; S07a signs the old book; S13 "a guest who signed the book" | S20 F08 fills in the registration card, F09 signs the inn's book |
| **The guest book** (filmed cloth book at the counter end; drawn open book) | Filmed in F01 (background, never pointed at); drawn at S07a `W000856 guest 309.20` | S07c moves intact along the relay into the booking site on `W000945 now 340.64`; a dashed book of the inn's own appears at the desk on `W001008 of 362.66` | S15a the inn's own book turns solid on `W002297 comes 822.96`; S20 F09 filmed signature; S20e the site's copy stays where it is |
| **The registration card** (filmed blank cards and pen on the counter; drawn card with an email field) | Filmed in F01 background; foregrounded in F07 at 766.625 | S14c drawn card: own email field or relay | S15a card and wifi login ask for the guest's own email; S20 F08 he fills it in |
| **The relay address field** (drawn field on the reservation record: a string of letters and numbers ending `@guest.booking.com`, labelled illustrative) | S00d `W000049 It's 17.00` | S00e relay line stops short after checkout; S07b the partner help policy explains it; S07c the site's rules become a boundary in front of writing to it | S15b the boundary returns in front of the relay on `W002341 relay 840.40`; S20e the note goes to the guest's own email, not the relay |
| **The booking site** (a lit hall facing a crowd of travellers: a fair, rented audience; neutral steel, never a villain colour) | S00e as a simple building at frame right; S03c full form on `W000295 in 102.58` | S03d its commission tag layers; S07c holds the moved guest book; S09b its filed gross bookings form the floor | S15b stays connected on `W002365 leave 849.44`; S20e keeps its first introduction on `W003178 still 1151.40`: nobody leaves it |
| **Commission tags** (small drawn tag, no number in S00) | S00e first tag on the first booking; S00f second tag on `W000095 same 34.20`, identical size | S00h a dashed "a service" shape inside the second tag; S03c layers; S10 becomes the commission band | S20e the second tag's place is empty on `W003189 stopped 1156.16`; S21a the second tag opens onto the service on `W003197 service 1158.80` |
| **The inn's own page** (a small drawn page/door on the inn facade, dashed until a job makes it live) | S08b as a dashed path beside the free link | S11a Findable makes the free link live; Bookable sets equal rate tags | S20e the next booking arrives through it on `W003163 inn's 1144.22`, no tag attached |
| **The empty place after checkout** (dashed outline on the stay timeline that no pay line reaches) | S05a on `W000618 last 216.84` | S08e the list card with an empty owner line | S11a the practice figure fills it on `W001677 A 595.62` (R57 condition: an earlier on-screen absence the script names what fills) |
| **The ceiling slip and ceiling line** (drawn paper slip with four input boxes; a horizontal line with a retainer tag under it) | S00h as a blank slip with four empty boxes on `W000127 piece 46.44` | S10 fills with the illustrative inn's inputs and draws the line on `W001570 That's 562.35`; S11b six inns each under a small ceiling; S14a on real inputs; S15a retainer tag under it; S16a the opener | S21a four inputs cleared for any property; S23 presenter draws the same line in the air (P12) |
| **The three jobs** Findable, Bookable, Remembered (three drawn job cards) | S11a on `W001701 Findable, 604.58`, `W001708 Bookable, 606.88`, `W001716 Remembered, 610.32` | S13 Remembered's drafting shrinks, judgment does not; S15a Findable and Bookable kept current, Remembered enlarges | S20 filmed and drawn: card, book, thank you, October note, booking through the inn's own page |
| **The practice / "You"** (one drawn operator figure, not the presenter's likeness) | S11a fills the empty place | S11c shrinks aside and "You" arrives; S12 route to nearby inns; S17 six inns on a drivable route; S18 guest at the owner's desk | S19 timeline; S20a "Say the first retainer's running" as a dashed marker, never a result |

What the world must never imply: the site as an enemy, the guest as lost, the inn leaving the
sites, a measured direct-share gain, commission saved as an achieved result, or any figure for the
illustrative inn beyond the ones spoken.

## Rhythm across the episode

Film carries people and the physical desk (S00, S03b, S08d, S14b, S20). The presenter carries only
first-person lines, questions to the viewer, rulings and the close. Working Models carry operating
relationships; evidence cards carry sourced numbers. The longest model stretch without a person is
S13a to S16a (703.875 to 879.167); F07 at 766.625 gives it one filmed beat, and each part changes
the world state rather than adding panels. Adjacent presenter takes are never less than 30 s apart
except P11 to P13, which are one continuous close.

---

## S00 Cold open

Master 0.000 to 59.458. Segments seg001 to seg009.

- **Narrative job:** establish one guest's two stays and leave the cost and the job open.
- **Viewer before:** knows nothing. **After:** has seen a good guest, a relay address, the same
  guest return through the same site and a second identical commission, and wants to know what that
  second stay cost and who could be paid to stop it.

| Seg | Master | Form | Cues | Strongest simpler alternative, rejected because |
|---|---|---|---|---|
| seg001 F01 | 0.000-5.625 | Film, establishing two-shot at the counter: he slides the key back and nods | Opens on `W000000 An 0.08`; out in the pause after `W000013 nights, 5.04` | Opening on the drawn inn: the viewer must meet the people before the model uses them (early-03: establish people before a hand or object carries the transition) |
| seg002 F02 | 5.625-10.500 | Film: he leaves, her look follows and settles on the window trail | In before `W000014 tipped 5.84`; out after `W000031 again. 10.10` | One held two-shot for 10.5 s: "The kind of person she'd like to see again" is her feeling, so the shot needs her look, not a longer checkout |
| seg003 F03 | 10.500-16.833 | Film: she turns to the laptop, types, stops | In before `W000032 So 11.36`; out after `W000048 his. 16.10` | Cutting to the screen insert on "thank you note": the stop is the human consequence and must be seen before the field explains it |
| seg004 | 16.833-22.750 | Screen insert, drawn reservation record: the email field types out a string of letters and numbers on `W000051 string 17.50`; `@guest.booking.com` completes on `W000058 guest 19.56`; label "A relay" on `W000063 A 21.74`; hold through the 1.21 s pause | Out mid-pause after `W000064 relay. 21.82` | A filmed laptop screen: legible fabricated platform UI is forbidden (oe-film-direction); a drawn record with a clearly illustrative string is honest and joins the model world |
| seg005 | 22.750-32.042 | Model: the record's relay line runs from the inn to a simple booking-site building; on `W000073 stops 25.48` the line stops short a little after a small "checkout" tick (no day count, no break mark); on `W000075 A 27.00` a "A year later" calendar leaf turns; the same daypack guest figure walks to the site on `W000079 same 28.12`, route site to inn draws, the same room window lights on `W000083 same 29.44` | Out after `W000088 website. 31.24` | Film of a second arrival: the booking route and the site's role are relationships, not actions a camera can show |
| seg006 | 32.042-36.333 | Model: a first commission tag already rests at the site; a second tag of identical size travels inn to site on `W000090 she 32.68` and lands beside it on `W000095 same 34.20` | Out in the pause after `W000101 time. 36.06` | A price on the tag: no rate belongs to the cold open (beat sheet: no figure beyond twenty rooms) |
| seg007 F04 | 36.333-40.083 | Film: at the desk she reads the new reservation and recognises the name | In before `W000102 For 36.76`; holds through the 1.39 s pause after `W000109 name. 38.88` (pause map P02, protected) | Staying in the model: "a guest she already knows by name" is a caused reaction and a relationship the drawing cannot feel |
| seg008 | 40.083-50.292 | Model: back on the two tags; on `W000119 hiding 43.02` a dashed shape labelled "a service" draws inside the second tag; on `W000127 piece 46.44` a blank slip with four empty boxes and one unlabelled line appears beside it; nothing is calculated | Out after `W000139 it. 49.88` | Presenter from "There's a service": costs 9 more generation seconds and the "hiding inside" relation is spatial |
| seg009 P01 | 50.292-59.458 | Presenter P01: first-person search finding and the open question | In before `W000140 I 50.90`; out at 59.458 in silence after `W000165 it? 59.24` | Question card over the model: market-05 (the host asked the central question when the script asked it) and the first-person "I couldn't find" belong to the speaker who owns the claim (r53-s10-section-plan-v1) |

- **Must not imply:** any figure for the inn, a named guest or real email, the relay as a trap or
  lock, the site as a villain, any recovery or direct booking, that "a week or so" is a Booking.com
  rule (C008 is the inn's experience here; S07 attributes it), or the answer to either question.
- **Protected holds:** the 1.21 s pause after "A relay." (inside seg004) and pause map P02 after
  "name." (inside seg007).

## S01 Sting

Master 59.458 to 63.208. Segment seg010.

- **Job:** silent identity break between the cold open and the report. **Form:** the accepted EP007
  sting composition (`r36-buyer-demand/compositions/sting.html`, hash in the JSON), field and
  "THE Operator Economy" lockup entering over silence. Do not trim the 4 s room: EP009's master has
  it built in (narration spacing join 1). EP007 early-09 shortened empty identity waiting in review;
  that condition does not apply because EP009's 3.96 s is already the approved sting length.
- **Rejected:** a new EP009 sting: identity is a fixed show element (EP007-P03).

## S02 Brand and promise

Master 63.208 to 87.833. Segments seg011 (sting continues, no picture cut at 63.208) and seg012 (P02).

- **Job:** fixed brand string, name the business, promise the four-number result.
- **Viewer after:** knows the show, the practice's one-sentence definition and what they will be
  able to do.
- **seg011:** the lockup holds through `W000166 This 63.38`; BUILD, OWN, OPERATE appear on
  `W000180 build, 67.08`, `W000181 own, 67.64`, `W000183 operate 68.24` (the accepted EP007
  treatment, onsets snapped to frames); on `W000189 Today 71.00` the lockup is replaced by the
  accepted title card composition retitled "Direct-booking practice." with its oxide pencil rule.
  This title change is a composition-internal cue on a word onset, not a segment cut.
- **seg012 P02:** presenter carries the definition and the promise from `W000195 It 73.70` to
  `W000246 time. 86.68`, cut at 87.833 (room tone, -57 dBFS; the gap before "Start" is 0.14 s).
- **Alternative rejected:** model illustrating the definition: the promise addresses the viewer and
  EP007's accepted structure gives it to the host (early-07: identity, title and presenter have
  different jobs).
- **Must not imply:** that the practice exists as a category (claims map: proposed editorial label)
  or that it moves direct share.

## S03 Context runway

Master 87.833 to 188.667. Segments seg013 to seg018.

- **Job:** be fair to the platforms, show how commission is layered, name three changes and who
  feels them.
- **Viewer before:** knows one inn's story. **After:** understands the site rents the inn an
  audience it could not build, the commission has layers, three things changed, and the short-staffed
  20 to 40 room owner feels it.

| Seg | Form and choreography | Rejected alternative |
|---|---|---|
| seg013 model 87.833-93.750 | The drawn inn establishes: facade/cutaway, room windows, desk figure, guest book outline by the door (not yet named). "Being fair" shown by nothing yet; hold | Opening S03 on evidence: 100 s of cards becomes a dump (early-02, early-10) |
| seg014 F05 93.750-99.167 | Film: the same guest at home compares stays on his phone, screen never visible | A drawn traveller: the viewer already knows this guest; seeing him choose makes the site's value human, not abstract |
| seg015 model 99.167-113.750 | On `W000285 So 99.60` the inn's card is placed inside the booking site's lit hall among other listings; on `W000295 in 102.58` a crowd of traveller figures faces the hall; on `W000308 takes 105.60` one tag per stay moves inn to site; on `W000315 rents 108.12` a route crowd to inn draws; on `W000324 fair 110.52` the two flows (guests in, tag out) sit balanced; on `W000331 gets 113.14` the tag divides into four empty layers | A funnel from crowd to room: implies conversion rates the script never gives (decision-method funnel row) |
| seg016 evidence 113.750-140.625 | Card kicker "BOOKING.COM PARTNER HELP": "A set percentage of the whole booking" on `W000336 own 115.40`, "fees included" `W000348 fees 118.82`, "charged at checkout" `W000350 charged 119.90`, "rises with visibility programmes" `W000356 goes 121.74`, "Base rate: not published" `W000368 doesn't 125.36`. Receipt C004 verbatim. Second band, kicker "TRADE REPORTING · SECONDARY": the drawn tag's layers fill: "Base about 15% · most European markets" `W000377 around 128.42`; "Preferred +3 points" `W000385 preferred 131.51`; "Visibility Booster: extra, by slider" `W000389 visibility 132.34`; "Genius: a 10 to 20% discount the hotel funds" `W000396 Genius 134.56`. Receipt C005 verbatim. On `W000409 three 139.16` heading "Three things changed" | Stating 15% as Booking.com's figure (C004/C005 prohibited wording) |
| seg017 evidence 140.625-174.292 | One strip, three slots filled left to right on their words. 1: "about 63%" of independent hotel reservations through the sites, "worldwide, 2025", on `W000435 sixty 150.80`; interest note "Cloudbeds sells hotel software" on `W000412 Cloudbeds, 141.10`; receipt C001. 2: "Genius placement: relevance-based from early 2026" on `W000447 changed 156.00`, "the minimum discount no longer buys the visibility" on `W000454 minimum 158.72`; receipt C006, secondary. 3: "15,000+ European hotels joined a damages claim over price parity clauses" on `W000475 damages 166.14`; note "Europe, not here" on `W000486 Europe, 171.04`; receipt C037 | Three separate full-screen cards: the "then" order is the point, one strip keeps it |
| seg018 model 174.292-188.667 | Heading "Who feels it?" on `W000495 Who 174.96`; the drawn inn with a "20 to 40 rooms" bracket on `W000501 twenty 177.34` ("twenty to forty", see transcript); one desk figure; a "marketing" hook on the wall stays empty on `W000506 no 178.72` (not a vacant chair, which belongs to S05); a stack of small tasks on the desk on `W000514 short 180.83`. AHLA foot card on `W000517 two 182.60`: "About two thirds of surveyed hotels reported staffing shortages"; receipt C013; note "not size-specific" | A filmed overloaded desk: F06 is reserved for S08, where the specific jobs are named |

- **Must not imply:** a US or band-specific share (C001 is worldwide), 15% as Booking.com's own
  figure, damages proven or US hotels suing (C037), that platforms are unfair (the script calls the
  trade fair), or that AHLA's figure is size-specific.

## S04 The question

Master 188.667 to 205.083. Segment seg019, presenter P03.

- **Job:** ask the central question. **Viewer after:** holds the question without an answer.
- **Form:** presenter, one continuous take from `W000532 Which 189.05` to `W000583 it? 204.56`
  (audio ends in silence from 204.91). Condition from market-05: the host asks when the script asks,
  and the answer is revealed only when narration reaches "Nobody".
- **Rejected:** question card over the model: the question is addressed to the viewer and a card
  would sit between two model scenes, blurring S03's evidence into S05's answer.
- **Must not imply:** the answer. No model object behind or after the presenter hints at a gap.

## S05 Earned thesis

Master 205.083 to 236.292. Segments seg020 (model), seg021 (P04).

- **Job:** answer "nobody", protect the owner from blame, show the gap is a job with a price.
- **Viewer after:** sees an unpaid place in an otherwise working stay, understands why each party
  leaves it, and hears it can be sold for what it recovers.
- **seg020 model:** a left-to-right stay timeline under the drawn inn: "booking", "stay", "checkout",
  then open space, then "next booking". On `W000584 Nobody 205.44` nothing new appears; the timeline
  simply has no line into the space after checkout. On `W000591 not 207.72` the desk figure is shown
  busy on the stay (check-in, housekeeping marks) so the absence cannot read as negligence. On
  `W000597 paid 209.70` the site's pay line draws to the "booking" event only (r54-s11b-room-model-v1:
  a shared payment trigger shown as lines to one event, which applied to advisers paid at closing).
  On `W000606 hand 212.46` the relationship line stays at the site. On `W000613 short 215.04` the
  desk figure's work stays inside the stay. On `W000618 last 216.84` a dashed empty place draws in
  the space after checkout, labelled "writing to last year's guests"; nothing reaches it. On
  `W000634 introduction 221.84` the S00 second commission tag lands on "next booking". On
  `W000642 gap 225.00` the dashed place gains the oxide label "A job" on `W000645 job. 225.58`, and
  holds through pause map P03 (protected) to the cut at 226.208.
- **seg021 P04:** presenter ruling from `W000646 I 226.62` to `W000678 inn. 235.62`.
- **Alternatives rejected:** an empty chair at the desk: EP007's vacancy was a missing role in a
  room of advisers (r54-s11cd-phrase-and-vacancy-v1); here the missing thing is a task after the
  guest leaves, so a place on the timeline is the literal structure. Presenter for "Nobody at the inn
  is": the answer should be seen in the structure (market-06: make absence specific, then the
  mechanism producing it).
- **Must not imply:** negligence ("not a lapse"), the site withholding for motive (C007), or that the
  job never gets done anywhere.

## S06 How much is rented

Master 236.292 to 305.667. Segments seg022 to seg024.

- **Job:** size the rented share honestly: a range, the missing US figure, cancellations.
- **Viewer after:** believes half to two thirds, knows the 30-room US figure is unpublished and that
  measuring it is the audit's first job.

| Seg | Form and cues | Rejected |
|---|---|---|
| seg022 evidence 236.292-269.667 | Left card kicker "CLOUDBEDS": "about 63%" on `W000708 sixty 247.68`, "of independent hotel bookings through the sites" on `W000705 sites 246.54`, "worldwide" on `W000711 worldwide. 249.14`, "from about 90 million bookings" on `W000692 ninety 241.94`; receipt C001. Interest note on `W000715 software 251.58`: "Cloudbeds sells the software hotels use to take bookings direct" (no dentist graphic; the voice carries the joke). Right card, beside, not nested (r36-s07-buyer-demand-v1: separate populations stay separate), kicker "HOTREC · EUROPEAN HOTEL ASSOCIATION" on `W000740 HOTREC, 260.02`: "3,000+ hotels" `W000746 three 263.54`, "direct channels: about half of overnight stays" `W000755 about 267.34`, "Europe" label; receipt C002 | One combined bar: implies one population |
| seg023 model 269.667-286.542 | The drawn inn's bookings as a row of small booking marks; on `W000764 half 272.28` a bracket from half, on `W000767 thirds 273.22` its far edge to two thirds, the band between them shaded as a range, not a point; a small commission tag attaches to the band on `W000776 commission 276.74`. On `W000779 nobody 278.56` an unfilled field "30-room inn, United States: not published" draws with a dashed empty box; on `W000798 audit 285.12` the label "first thing the audit measures" | Showing 63% as the inn's share: the script refuses a US figure (C001, C002 boundaries) |
| seg024 evidence 286.542-305.667 | Card "CLOUDBEDS · SAME DATA": two short bars, "Through the sites: about 22% cancelled" on `W000811 about 291.32`, "Direct: about 11%" on `W000817 about 294.40`; receipt C003. On `W000833 renting 300.54` cut within the composition to the drawn inn with its range band, the tag on `W000838 at 302.80`, and on `W000844 its 304.68` its own-number field blank | Universal cancellation rates: the card names the dataset |

- **Must not imply:** a US or 20 to 40 room share, HOTREC applying to the US, the unknown as zero,
  cancellation rates as universal.

## S07 What the site keeps

Master 305.667 to 368.000. Segments seg025 to seg027.

- **Job:** introduce the guest book as the episode's persistent object and show the design
  constraint before any tool.
- **Viewer after:** understands the book moved to the platform under stated rules and that the inn
  first needs a book of its own that the guest chooses to sign.
- **seg025 model:** heading "What the site keeps" on `W000848 what 306.70`; on `W000856 guest 309.20`
  the drawn guest book appears by the inn's door; the daypack guest signs on `W000862 signed 311.00`;
  three handwritten lines appear inside the page: a name on `W000868 your 312.64`, a town on
  `W000872 come 313.94`, a small envelope mark on `W000876 reason 314.94`; on `W000882 book 316.78`
  the book sits clearly inside the inn outline.
- **seg026 evidence:** kicker "BOOKING.COM PARTNER HELP": quote "we don't share private email
  addresses" on `W000894 doesn't 321.33`; the S00 relay string beside "Both sides see an alias" on
  `W000903 alias 325.60`; "Partners are asked to keep the conversation on the platform" on
  `W000919 on 331.40`; receipt C007. Lower band "TRADE PRESS · SECONDARY": "Messaging window: about
  7 days after checkout" on `W000931 seven 335.08`; "Expedia: about 45 days" on `W000939 forty 338.10`;
  receipt C008.
- **seg027 model:** on `W000945 now 340.64` the drawn guest book slides intact along the S00 relay
  line into the booking site's hall and rests there, labelled "at the booking site"; nothing is torn,
  locked or greyed. On `W000957 doesn't 344.56` the inn's email field shows only the relay string. On
  `W000968 design 349.08` heading "A design constraint"; on `W000977 win 352.66` a pencil line from the
  inn toward the relay address draws and stops at a boundary labelled "the site's rules" that appears
  on `W000991 not 356.52` (r59-s14-plan-v1: a boundary in front of one action only, which applied to
  licensing in front of selling). On `W001001 an 360.27` a small "email tool" card appears and is
  moved aside, not struck. On `W001008 of 362.66` a dashed guest book outline appears at the inn's
  desk; on `W001018 chooses 365.94` the daypack guest figure stands beside it with a pen not yet
  touching the page. Hold to the cut.
- **Rejected:** a lock or cage on the book (claims motive, C007 prohibited inference); the book
  shredded or faded (claims loss); showing the inn's book already signed (pays off S15 and S20 early).
- **Must not imply:** that the site sells or hides data for commercial motive, that 7 and 45 days are
  the platforms' own figures (R001 open), consent rates, or that contacting the relay is a good idea.

## S08 Fair question

Master 368.000 to 410.042. Segments seg028 to seg032.

- **Job:** answer "why doesn't the inn just do it" with cheap parts and one overloaded person.
- **Viewer after:** the direct path is a list of small jobs that belongs to nobody.
- **seg028 P05:** presenter raises the objection (`W001021 Fair 368.32` to `W001038 it? 372.96`).
  r55-s12-plan-v1 condition: the presenter voices an objection the script frames as the viewer's.
  EP009's "Fair question here." is 2.6 words per second, so EP007's rushed-phrase repair
  (`lesson-rushed-phrase-revoice-not-pause-v1`) is not expected.
- **seg029 evidence:** heading "The parts are cheap" on `W001039 The 373.72`. Row 1, "GOOGLE HOTEL
  CENTER HELP": "Free booking links: no fee" on `W001047 free 376.50`, "for a property connected
  through a partner" on its words; receipt C009. Row 2, "SMALL-PROPERTY BOOKING ENGINE": "about $29
  to $39 a month plus 1%, or about $109" on `W001070 booking 384.26`; note "public tool pricing, not a
  quote for your property"; receipt C010.
- **seg030 model:** on `W001085 The 389.12` the drawn desk figure; on `W001099 set 393.54` a "free
  link" card, on `W001104 check 395.14` a "direct rate" card start moving toward her.
- **seg031 F06:** film under "write the thank you, and read the reservation report is the same person
  checking in the guest and finding a plumber": she takes a call at the desk with the report pages
  under her hand. Condition from market-04: cut to a person when the argument turns to their stake.
- **seg032 model:** back to the drawing: four cards ("free link", "direct rate", "thank you",
  "reservation report") rest on her desk; on `W001133 isn't 405.04` no system diagram forms; on
  `W001138 list 406.72` the cards stack into one list card whose owner line is drawn empty on
  `W001145 belongs 408.88`.
- **Rejected:** a busy-desk montage (keyword illustration); a price comparison implying a quote.
- **Must not imply:** that every property is eligible for free links without a partner, that tool
  prices are service demand, or that she is disorganised (the jobs converge; she is not failing).

## S09 Already sold at two scales

Master 410.042 to 480.042. Segments seg033 to seg035.

- **Job:** the job is bought at other scales; nobody sells it to the 20-room inn, and the reason is
  arithmetic.
- **Direct analog:** r55-s12-plan-v1 (EP007 S12 "the job at other scales"), condition: the objection
  that someone would already sell it, answered by showing the job at larger scales while the small
  business keeps its empty place.
- **seg033 model:** heading "The obvious objection" on `W001151 obvious 411.22`, its line "somebody
  would already be selling it" on `W001159`. On `W001167 at 417.52` a horizontal scale axis from small
  to large with the drawn inn at the small end, still showing S08's empty owner line. Tier 1 on
  `W001170 Independent 419.14`: a larger hotel outline with an "outsourced revenue manager" figure on
  a monthly loop on `W001179 revenue 423.08`; evidence tag "Almost all quote privately" on
  `W001197 quote 430.40`, receipt C012. Tier 2 on `W001203 marketing 433.80`: an agency figure; tag
  "One publishes its entry price: $1,500 a month" on `W001218 fifteen 440.78`, "lists past-guest
  email and direct-share reporting" on `W001225 past 443.52`; receipt C011. No line from either tier
  reaches the drawn inn.
- **seg034 model:** on `W001243 sites 450.14` the booking site's hall at the large end; tags
  "Booking Holdings: $186.1 billion" and "Expedia Group: $119.6 billion", "2025 gross bookings, by
  their own filings" on `W001255 hundred 455.16`, "blended across everything they sell" on
  `W001264 blended 458.58`; never summed; receipt C014. On `W001271 floor 461.66` a baseline draws
  under the whole axis. On `W001282 paid 466.18` a bracket spans tiers 1 and 2: "paid for by
  properties big enough to fund it".
- **seg035 P06:** presenter first-person finding and the arithmetic reason (`W001291 I 469.64` to
  `W001322 is. 479.38`).
- **Must not imply:** that the $1,500 agency serves 20 to 40 room inns, revenue-management prices or
  uplift, the filings as commission, or that nobody anywhere does it.

## S10 The ceiling

Master 480.042 to 589.875. Segments seg036 (model), seg037 (P07), seg038 and seg039 (model).

- **Narrative job:** compute what the job can recover for one made-up inn, and show that it is a
  ceiling on price, not an income, with its hypothesis visible.
- **Viewer before:** knows the job is unowned and bounded by recovery. **After:** can name the four
  inputs, knows the commission total is the wrong number, sees the ceiling of about $1,000 to $1,400 a
  month for this illustrative inn, knows the 10 points is an unmeasured hypothesis, and knows two
  things that move it.
- **No accepted EP007 analog.** Nearest conditions: r49-concentration-model-v1 (relative weight
  without share figures, applied where no sourced share existed) and r60-s15-ai-v1 (a bar the fee
  cannot cover). Here sourced and modeled figures exist and are spoken, so they appear, labelled.
- **Strongest simpler alternative:** a static table (the Canvas ceiling table) on screen while the
  narration runs. Rejected because the argument's turn is structural: the viewer must see the
  commission total set aside and a much smaller slice taken from the rented share, and a table
  presents both rows with equal weight. The table does become the ceiling slip's back face at S21.

### Persistent layout

Left two thirds: the **build column**, a pencil-drawn vertical stack. Right third: the **ceiling
slip**, a pencil-outlined paper slip holding four input boxes in a column: Rooms, Rate, Occupancy,
Share through the sites. Top-left, typeset and never absent from any frame of seg036, seg038 or
seg039: **"ILLUSTRATIVE MODEL · a made-up inn · swap in real inputs"**. Foot receipt, never absent in
the same segments: "the ceiling table with every input, "ILLUSTRATIVE MODEL", D-EDGE 3.5 percent
2025-02-24 for the low bound, C016 to C021". The slip is the same object as the blank slip from S00h.

Scale rule: the stack is not proportional across stages. When the build moves from the commission
band to the hypothetical slice, the slice is lifted into its own **enlarged panel** joined by two
construction lines and labelled "enlarged"; a proportional drawing would make the ceiling
invisible, and a precise-looking scale would overstate certainty.

### Build order, seg036 (480.042-520.417)

| Cue | Object change |
|---|---|
| `W001325 compute 480.87` | Empty build column outline and empty slip draw in (pencil construction, 0.5 s). |
| `W001327 Here's 482.02` | Slip title "The ceiling" (handwritten inside the slip). |
| `W001331 illustrative, 483.44` | Top-left label "ILLUSTRATIVE MODEL" types on; "a made-up inn" on `W001333 making 484.64`; "swap in real inputs" on `W001338 every 486.30`. Receipt at foot appears with it. |
| `W001349 Twenty 490.68` | Rooms box fills: "20". A small drawn inn with twenty windows sits above the column. |
| `W001351 A 491.67` | Rate box: "$180 a night". |
| `W001360 Seventy 494.36` | Occupancy box: "70%". |
| `W001366 That's 496.94` | The column fills to full height: "Room revenue about $920,000" (small exact "$919,800" under it). |
| `W001377 Say 500.60` | Share box: "63%" with the dashed word "say". |
| `W001378 sixty 501.01` | The lower 63% of the column shades (rented). |
| `W001388 Cloudbeds 503.82` | Tag on the Share box: "the Cloudbeds figure, worldwide". |
| `W001390 That's 505.50` | Label on the shaded part: "Rented bookings about $580,000" (small exact "$583,153"). |
| `W001401 At 509.54` | A thin band on top of the rented part hatches as a range with two edges: "Commission 18% to 22%". |
| `W001412 my 513.12` | Tag on the band: "my assumption from the reported bands". |
| `W001418 the 515.60` | Band label: "about $105,000 to $130,000 a year" (small exact "$104,968 to $128,294"). Hold to the cut. |

### seg037 P07 (520.417-532.250)

Presenter turn, `W001438 That's 521.02` to `W001475 shift. 531.54`: the old argument stops at the
commission total; the wrong number; the inn needs the sites. Condition from r53-s10-section-plan-v1:
the interpretation belongs to the speaker who owns it, and "It's the wrong number" otherwise lands on
a diagram with no one interpreting it (precedent audit risk). The model state is preserved exactly
for the return.

### Build order, seg038 (532.250-569.542)

| Cue | Object change |
|---|---|
| 532.250 (first frame) | Same frame as seg036's last, except the commission band has receded to 40% opacity with the note "not all of it moves" (not struck). The label, receipt and slip are present from the first frame. |
| `W001476 Say 532.58` | Inside the rented part, a **dashed** 10-point slice outline draws at its top. Tag, oxide, dashed border: "Say 10 points · hypothesis". This dashed treatment never becomes solid in this episode. |
| `W001484 from 535.02` | Share box shows "63%"; `W001490 fifty 537.04` a dashed ghost "53%" appears beside it with an arrow, still dashed. |
| `W001492 That's 538.49` | The slice lifts into the **enlarged panel** at centre-right joined by two construction lines: "about $92,000 of revenue, if it moved" (small exact "$91,980"). |
| `W001503 Commission 542.26` | Inside the panel, a hatched range band: "18% to 22% on that slice". |
| `W001513 is 545.40` | Band label: "about $16,500 to $20,000 a year" (small exact "$16,556 to $20,236"). The words "commission saved" are spoken but not written; the label names what the figure is. |
| `W001525 Take 548.88` | A thinner band subtracts from it: "minus direct channel cost". |
| `W001534 call 551.42` | "3.5% to 5%"; `W001543 the 553.60` tag "low end: one vendor's own figure". |
| `W001551 What's 556.20` | Remainder band: "about $12,000 to $17,000 a year" (small exact "$11,957 to $17,017"). |
| `W001562 A 559.75` | Converts: "about $1,000 to $1,400 a month" (small exact "$996 to $1,418"). |
| `W001570 That's 562.35` | A horizontal pencil **ceiling line** draws across the panel at the top of the remainder band, labelled "Ceiling". Hold pause map P05 after `W001572 ceiling. 562.80` with no motion. |
| `W001575 most 564.10` | Sub-label under "Ceiling": "the most this inn can rationally pay for the job". |
| `W001590 retainer 567.88` | A small retainer tag with no price slides in and settles **under** the line on `W001594 under 568.84`. |

### Sensitivity, seg039 (569.542-589.875)

| Cue | Object change |
|---|---|
| `W001596 Two 569.86` | Heading in the panel: "Two things move it". |
| `W001600 A 571.32` | A second, ghosted copy of the slip's Rooms box reads "40"; `W001604 doubles 572.40` a **ghost ceiling** line (steel, 50%) draws above the solid one: "40 rooms: about $2,000 to $2,800 a month" (small exact "$1,993 to $2,836"). |
| `W001616 A 576.14` | A ghost of the dashed slice at half width; `W001623 halves 578.06` a second ghost ceiling below the solid one: "5 points: about $500 to $700 a month" (small exact "$498 to $709"). |
| `W001631 The 580.86` | Both ghosts fade to 20%. The dashed 10-point slice and its tag become the one oxide accent; tag text extends: "a hypothesis nobody has measured" on `W001636 hypothesis 581.86`. |
| `W001640 But 583.98` | Oxide returns to the ceiling line. |
| `W001646 four 585.52` | The four input boxes on the slip light in sequence, one per 0.15 s, and stay lit. |
| `W001648 whether 586.58` | Hold. The solid ceiling, the dashed slice, the label and the receipt remain to the cut. |

- **Always labelled:** "ILLUSTRATIVE MODEL" and the receipt for every frame of seg036, seg038 and
  seg039; "hypothesis" on the 10-point slice from `W001476` to the cut; "my assumption" on the
  commission band; "one vendor's own figure" on the direct cost.
- **Sensitivity shown as:** two ghost ceilings beside the solid one, never replacing it, never
  animated as a moving result.
- **Must not imply:** that any property achieves a 10-point shift, commission saved as a service
  result, the ceiling as the operator's income, RevPAR or direct share gained, 63% as a US figure,
  or that the inn should reduce its site bookings to zero.

## S11 The complete company

Master 589.875 to 649.000. Segments seg040 to seg042.

- **Job:** picture the mature practice: one person, a handful of inns, three jobs, one number, six
  properties each under its own ceiling; name the gap as opportunity, then turn to the viewer.
- **Direct analog:** r57-s13ab-company-in-gap-v1 and r57-s13cd-maturity-bridge-v1, condition: the
  script names what fills an absence the viewer has already seen on screen.
- **seg040:** return to the S05 stay timeline with its dashed empty place. On `W001662 picture 590.46`
  the dashed place's outline brightens; on `W001677 A 595.62` a drawn practice figure steps into it,
  labelled "A direct-booking practice"; on `W001685 handful 598.68` three more inn outlines appear
  around, each with a thin line to the practice. On `W001701 Findable, 604.58` the first job card
  attaches to the S05 inn: a search result with the free link now solid to the inn's own page. On
  `W001708 Bookable, 606.88` second card: two blank rate tags, one on the site, one on the inn's page,
  joined by "=". On `W001716 Remembered, 610.32` third card: the guest book, a thank-you note on
  `W001723 thank 612.62`, a small seasonal leaf on `W001726 reason 613.40`; on
  `W001732 guest's 615.52` a consent tick box on the card; on `W001737 sites' 617.56` the S07 rules
  boundary stands in front of the relay field.
- **seg041:** on `W001740 one 619.04` a monthly report slip: "Direct share of bookings: before ___
  after ___" with both blanks; on `W001757 six 625.56` the handful becomes six inns, each gaining a
  small ceiling line with a blank retainer tag under it on `W001764 its 627.98`; on
  `W001771 learns 630.26` a room-count axis under them with a dashed, unlabelled marker on
  `W001783 starts 633.42`. On `W001786 Nobody 635.06` an earnings slot beside the practice draws
  dashed and empty: "not published". No heading on "opportunity, not a category"; hold through pause
  map P06.
- **seg042:** on `W001806 that's 643.72` a pencil outline encloses the model with the heading "The
  business"; on `W001809 The 645.52` ("The question now") the model shrinks to the left and a full-size
  figure labelled "You" arrives right on `W001816 person 647.50` (R57 bridge condition: the
  next section is personal and opens on the viewer).
- **Rejected:** presenter bridge "So that's the business..." (6.9 s): P08 follows within 18 s and
  the "You" figure hands S12's skill picture a subject.
- **Must not imply:** measured direct-share gains, earnings, that the practice exists today, or the
  threshold room count.

## S12 Why you

Master 649.000 to 703.875. Segments seg043 (model), seg044 (P08), seg045 (model).

- **Direct analog:** r59-s14-plan-v1, condition: a long first-person passage where the presenter
  carries the admission and the picture carries the skill.
- **seg043 model:** "You" figure. On `W001827 revenue 651.52` a credential card sets aside, dashed and
  light (R59 finance card). On `W001835 write 654.30` a handwritten thank-you note (pencil lines, no
  readable words) on the right; on `W001858 name 660.06` a newsletter card with a stuck-on name tag on
  the left; on `W001865 faster 661.70` the daypack guest figure's attention line goes to the
  handwritten note, and the newsletter stays where it is (not crossed out). On `W001878 talk 665.52`
  "You" and a drawn owner sit across a small table with the ceiling slip between them.
- **seg044 P08:** presenter, one continuous 22.875 s take from `W001881 I 667.48` to
  `W001955 pitch. 688.62`: Coqui Coqui (H001), the three limits (H002) in one breath, "That's the
  test, not the pitch." Editorial crop change from wide to closer on `W001927 So 681.26` from the
  continuous source. Condition from r47-transfer-criterion-presenter-v1: keep one take where a
  sentence-boundary cut would be artificial.
- **seg045 model:** on `W001958 properties 690.32` a pencil route from "You" to three nearby inns
  ("drive to"); on `W001977 know 695.52` one inn gains a small handshake mark (someone you know); on
  `W001989 back 699.48` its back office door opens onto the guest book; on `W001996 a 701.78` a tool
  card stays outside the door.
- **Must not imply:** hotel ownership, revenue management, any sale of this service or client result
  (H003, H004 blocked), or that no experience is needed.

## S13 The machine and you

Master 703.875 to 741.958. Segments seg046, seg047.

- **Direct analog:** r60-s15-ai-v1, condition: show a technology's capability by shrinking only the
  tasks it compresses, never the ones the script says it does not touch.
- **seg046:** question heading "What does the machine do, and what do you do?" on `W002001 What 704.30`
  (a heading, not a presenter insert, to keep presenter spend on rulings). Two columns. On
  `W002012 The 708.26` ("The software does the repetitive half") the left column fills with three full-size
  blocks: "thank you", "review request" on `W002026 review 713.02`, "note about the trail in the fall"
  on `W002032 trail 715.04`; each shrinks and relabels "drafted" on `W002021 drafts 711.66` onward as
  it is named. On `W002037 automation 716.87` a "schedule" block with a checkout-date tick shrinks on
  `W002043 checkout 718.72`.
- **seg047:** right column, full weight, not shrinking: "the voice" on `W002055 set 725.08`, "who gets
  a message" on `W002060 who 727.08` with three guest figures, two receiving a note and one not. On
  `W002071 signed 730.82` the guest book with a signature; on `W002084 drip 734.13` a dashed chain of
  identical envelopes appears detached from the book (never connected). On `W002092 one 737.90` six
  small inns link to one figure. On `W002096 drafting 739.42` the left column label "cheap"; on
  `W002100 judgment 740.90` the right column is outlined "judgment".
- **Must not imply:** that AI moves direct share (C023 capability, not outcome), that AI decides who
  gets a message, a robot or agent icon.

## S14 The first sale

Master 741.958 to 804.750. Segments seg048 to seg051.

- **Analog (pending in EP007):** r61-s16-wedge-v1, condition: a fixed-scope first product shown as a
  card with its limits; and decision-method "a no-build is valid".
- **seg048 model:** heading "What do you sell first?" on `W002102 What 742.40`; a retainer card on
  `W002107 Not 744.82` sets aside; "The audit" card fills on `W002110 The 746.56` and holds pause map
  P07. Card rows on their words: "one property" `W002112 One 748.26`, "fixed fee" `W002116 fixed 749.76`,
  "in the model: $1,200" `W002123 twelve 751.54`, "about 12 hours" `W002128 twelve 752.62`, label
  "modeled" (C024). Steps: two report sheets slide in on `W002133 site's 755.14` and
  `W002137 property 756.74` (unreadable); the S10 ceiling slip in miniature with blank "real inputs"
  on `W002142 commission 759.16`; a drawn phone with a route search to the inn's own page to a booking
  step on `W002155 as 763.94`, steps unchecked.
- **seg049 F07:** film close at the counter: a blank registration card and pen slide into view, under
  "And you check one thing at the front desk."
- **seg050 model:** the drawn registration card on `W002172 registration 771.08` with a field
  "guest's own email" on `W002177 guest's 773.60` and, on `W002184 only 777.02`, the relay string in
  the same field as the alternative; neither ticked. On `W002195 has 780.22` the audit card's three
  deliverables: "baseline", "ceiling in their own numbers" `W002201 their 782.62`, "written
  recommendation" `W002206 written 783.64`.
- **seg051 model:** three branches of equal size and weight from the recommendation: "retainer" on
  `W002209 that's 786.10`, "audit only" on `W002214 audit 788.00`, "this property can't fund it" on
  `W002221 can't 791.08` with its reason on `W002227 base 792.96` and "recoverable: a few hundred a
  month" on `W002241 few 796.18` (C025, modeled). On `W002245 That's 798.18` all three are outlined
  together as "The product" (R60 outline condition: the product is the judgment, not one branch).
- **Must not imply:** $1,200 as a market price, the retainer as the only success, that such
  properties are common.

## S15 The retainer

Master 804.750 to 861.750. Segments seg052, seg053.

- **Job:** what the monthly retainer is, where the guest book returns, the rules, one honest number.
- **seg052:** on `W002261 audit 805.98` the "retainer" branch from S14; on `W002267 the 808.64` the
  three job cards attach; on `W002271 at 810.98` the property's ceiling line draws and the retainer tag
  settles under it on `W002275 that 812.18`. On `W002278 Findable 814.08` Findable and Bookable cards
  shrink slightly with a small refresh loop on `W002285 kept 816.94`. On `W002287 Remembered 818.64`
  the Remembered card enlarges. On `W002297 comes 822.96` the dashed guest book at the inn's desk
  (from S07c) turns solid: the inn's own book. The site's copy stays at the site. On
  `W002303 The 824.84` ("The registration card") and `W002308 wifi 826.52` a registration card and a wifi
  sign each show an "own email" field with a consent tick box on `W002313 guest's 828.64`.
- **seg053:** after-checkout strip: thank-you note on `W002319 a 832.92` ("a thank you"), seasonal leaf
  note on `W002324 seasonal 834.18`. Heading "Inside the rules" on `W002334 Inside 837.76`; the S07
  boundary stands in front of the relay field on `W002341 relay 840.40`, "No marketing to the relay
  address, ever" on `W002343 ever. 841.40`. Labels on the list: "US email law" on
  `W002349 American 843.56`, "EU rules for EU guests" on `W002353 European 845.12`, note "not legal
  advice". On `W002365 leave 849.44` the booking site's route to the inn stays solid with the note
  "the sites stay". Report slip "1st of the month · Direct share of bookings" on `W002373 first 852.58`
  with a blank value; on `W002383 isn't 856.18` a handwritten "not moving" appears in the value box as
  an allowed report, and on `W002396 decorating 860.52` nothing is added.
- **Must not imply:** a rising line or result, legal advice, leaving the sites, marketing to the
  relay, that consent rates are known.

## S16 The first owner

Master 861.750 to 903.333. Segments seg054 to seg056.

- **seg054 model:** heading "How does the first owner arrive?" on `W002398 How 862.02`; on
  `W002404 Lead 864.16` two figures at a table with the ceiling slip; "four inputs the owner already
  knows" as the slip's boxes on `W002408 Four 865.56`; "what the job could be worth" on
  `W002422 could 870.14`. On `W002431 unproven 872.74` two dashed routes toward the practice, not
  connected to it and with no rates: "innkeeper associations" `W002433 Innkeeper 874.32`, "PMS partner
  lists" `W002437 partner 876.56`.
- **seg055 P09:** presenter refusal to invent a conversion rate (`W002444 Those 879.56` to
  `W002462 one. 885.22`).
- **seg056 model:** "Kill condition" heading on `W002466 kill 886.72`, a drawn phone on
  `W002468 one 887.62`; condition box on `W002476 retain 890.56`: "agencies already retain 30-room
  inns at $1,500 a month" and "owners prefer it" on `W002486 owners 894.36` (C027, C011); on
  `W002493 no 897.00` the small inn's front door on the practice route stays dashed with "no front door
  at this size" as the conditional outcome; on `W002499 Ask 899.22` two call lines to two agency
  figures, answer field "smallest retained property: ___" blank.
- **Rejected:** a funnel (decision-method funnel row, and the script refuses one).
- **Must not imply:** conversion rates, that agencies serve the band, or that the condition is met.

## S17 The operator's arithmetic

Master 903.333 to 1008.333. Segments seg057, seg058 (model), seg059 (P10), seg060 (model).

- **Narrative job:** show the operator's side of the modeled scenario, base and stress case at equal
  weight, then rule it a foothold at the bottom of the band.
- **Viewer before:** has the property's ceiling. **After:** knows that at six properties the modeled
  bottom of the band is a side income, the stress case nearly erases the remainder, the top of the
  band becomes a business, and the requirement is six owners on a route, not a market share.
- **No accepted EP007 analog.** Nearest condition: r60-s15-ai-v1's billable-hours bar (time against a
  fee). **Strongest simpler alternative:** presenter reading the numbers with one summary card.
  Rejected: the stress case must be seen at equal weight to the base case, and a single card makes the
  base case the headline.

### Persistent layout

Top band, typeset, never absent from any frame of seg057, seg058 or seg060: **"MODELED SCENARIO ·
Modeled scenario, not observed performance or an earnings forecast."** (Canvas section 10 string,
verbatim). Left: a **price rail** of drawn tags. Centre: **six drawn inns** in a row with the S11
small ceiling lines. Right: the **ledger strip**, one handwritten-style operation line per spoken
sentence, typeset numbers, each new line pushing the previous up; no running total animates upward.
Foot note: "C024, C028 to C033 · Canvas section 10".

### Build order, seg057 (903.333-946.167)

| Cue | Object change |
|---|---|
| `W002512 Your 904.98` | Heading "Your side of the arithmetic". |
| `W002523 modeled 908.06` | Top band types on and stays. |
| `W002525 Not 909.36`, `W002528 not 911.12` | Its second sentence completes with the voice; hold through pause map P08 (protected). |
| `W002532 Audit 913.28` | Price rail: "Audit $1,200". |
| `W002536 Retainer 914.76` | "Retainer $600 a month · 20 rooms"; `W002547 rising 917.84` "$1,000 or $1,250 · 40 rooms". |
| `W002557 Call 921.08` | "Blend $800" tag, which all six inns carry. |
| `W002562 Six 923.22` | Six inns draw in with blend tags under their ceilings. |
| `W002566 Eight 925.12` | Under each inn "8 h a month"; `W002572 twelve 926.82` "audit 12 h". |
| `W002576 Six 928.44` | Ledger line 1: "6 × $800 × 12 = $57,600 a year". |
| `W002591 Add 933.34` | Line 2: "+ 6 audits × $1,200 = $64,800 gross". |
| `W002605 Take 938.82` | Line 3: "− tools and overhead, about $6,000". |
| `W002615 and 941.84` | Line 4: "= $58,800 before you pay yourself". Hold to the cut. |

### Build order, seg058 (946.167-976.542)

| Cue | Object change |
|---|---|
| `W002627 Now 946.30` | Price rail adds "Your time: $60 an hour" with tag "the model's number" on `W002633 model's 947.58`. |
| `W002638 Six 949.96` | A drawn hours bar under the six inns; `W002647 about 953.26` label "about 650 hours" (576 retainer + 72 audit hours is not shown; only the spoken figure). |
| `W002653 At 955.26` | Ledger line 5: "650 h × $60 = about $39,000". |
| `W002661 So 958.34` | The ledger splits into **two equal columns** headed "Base: 8 h a property" and, dashed until its cue, "Stress: 12 h a property". Base column line: "about $20,000 left" on `W002670 about 960.88`. |
| `W002674 And 962.92` | The stress column heading turns solid; its hours bar lengthens on `W002679 twelve 964.00`. |
| `W002686 the 966.26` | Stress tag "the stress case". |
| `W002689 that 967.48` | Stress column line: "about $2,640 left" on `W002693 about 968.80`. Both columns identical in size, type and weight. |
| `W002699 Six 971.24` | Both columns recede to 50%. A new row: "6 × 20-room inns × $600 × 12 = $43,200 a year of retainer" on `W002709 forty 974.62`. Hold to the cut. |

### seg059 P10 (976.542-982.875)

Presenter ruling, `W002714 That's 976.66` to `W002732 business. 982.30`, including pause map P09
after "It is not a living." (protected). Condition from r35-s06-presenter-conclusion-v3 and the audit:
a named ruling belongs to the host; the $43,200 figure is already on screen before the cut so the
ruling interprets a visible number.

### Build order, seg060 (982.875-1008.333)

| Cue | Object change |
|---|---|
| 982.875 (first frame) | seg058's last frame restored, top band present. |
| `W002733 Six 983.50` | A second row beside the $43,200 row, same size: "6 × 40-room properties × $1,250 × 12 = $90,000 a year of retainer, before costs" on `W002741 ninety 986.78`. No highlight, no upward arrow between rows. |
| `W002749 Six 990.78` | Everything except the six inns recedes. |
| `W002751 Not 991.96` | No pie, no share. |
| `W002755 The 993.40` | Evidence tag "AHLA: 33,200+ small-business lodging properties" on `W002760 thirty 995.56`; receipt C015; note "AHLA definition, not a room band". |
| `W002771 nobody 1000.12` | A dashed empty field "in this band: not counted". |
| `W002780 You 1003.88` | The six inns join by a pencil route to "You" on `W002789 route 1006.62`. Hold to the cut. |

- **Always labelled:** the top band in every model frame of S17; "the model's number" on $60; "the
  stress case" on the stress column; "before costs" on $90,000.
- **Sensitivity shown as:** base and stress in equal columns; 20-room and 40-room rows side by side,
  not a rising line.
- **Must not imply:** earnings, a wage, a forecast, that 40-room owners pay $1,250, a share of 33,200,
  or that six owners are easy to find.

## S18 The hard parts

Master 1008.333 to 1064.333. Segments seg061, seg062.

- **seg061:** heading "What's genuinely hard" on `W002799 genuinely 1011.07`, three blank slots on
  `W002803 Three 1013.15`. Slot 1 on `W002806 ceiling 1014.64`: an inn with a low ceiling line, "a few
  hundred a month" on `W002824 few 1020.88`; the practice figure turns and walks away courteously on
  `W002830 walk 1022.23` (no slammed door, no cross). On `W002834 viable 1024.06` the room-count axis
  from S11 with a window between "too small" on `W002839 Too 1026.26` and "already served by an agency"
  on `W002845 served 1028.18`; both window edges dashed, and on `W002855 how 1031.40` a width label
  "unknown".
- **seg062:** slot 2 "Renewal" on `W002860 Renewal. 1033.50`: a calendar with a highlighted summer
  on `W002862 good 1034.74` and a separate "baseline" sheet kept in a folder on `W002876 keep 1039.16`;
  no data line. Slot 3 "Access" on `W002887 And 1043.58`: the practice figure on the guest side of the
  owner's desk, the owner holding the accounts on `W002894 owner's 1046.86`; "You're a guest" on
  `W002900 You're 1049.20`. On `W002903 If 1050.82` a fork: "no owner funds $600 a month" and "agencies own
  the band" on `W002918 already 1054.60` lead to "stop" and "move up" on `W002922 stop, 1056.06`. On
  `W002926 Forty 1058.12` the axis extends to "40 to 80 rooms: the redesign" with agency figures
  already present on `W002942 their 1063.36`.
- **Must not imply:** a good summer as a result, the redesign as proven, the band width as known.

## S19 The first 30 and 90 days

Master 1064.333 to 1123.625. Segments seg063, seg064.

- **No close analog.** Form: a pencil timeline on the same objects, with checkboxes that stay
  unchecked (audit risk: checked boxes imply outcomes).
- **seg063:** "Days 1 to 30" band on `W002951 first 1067.32`, "building, not thinking" on
  `W002955 building, 1068.58`. On `W002958 Build 1070.44` the audit card from S14 with three parts:
  "checklist" `W002962 checklist, 1071.68`, "ceiling calculator" (the slip) `W002964 ceiling 1072.54`,
  "phone-side test" (the phone) `W002968 phone 1073.74`. Three inns on `W002975 three 1075.94`: "free,
  an owner you know" `W002980 One 1077.88` with a stopwatch mark on `W002989 start 1080.54`, two "at
  the audit fee" `W002992 Two 1081.98`. Ceiling line with a retainer tag under it in front of each
  owner on `W002997 Put 1083.58`; "write down the answer" blank line on `W003011 write 1086.92`. Five call
  lines on `W003016 make 1088.68`: two to PMS partner managers `W003019 Two 1090.36`, one to an
  innkeeper association `W003027 innkeeper 1093.28`, two to agencies `W003035 Two 1097.26`.
- **seg064:** "Success at day 30" with three unchecked boxes: "one paid audit" `W003047 one 1103.18`,
  "one yes to a retainer under the ceiling" `W003050 one 1104.48`, "an audit inside 15 hours"
  `W003061 inside 1108.08`. "Days 31 to 90" band on `W003064 Days 1110.20`: "deliver the first
  retainer"; "8 h assumption → real hours" on `W003079 real 1115.44`; "rerun the arithmetic" on
  `W003081 rerun 1116.58`; a three-way decision with no choice marked: "keep going"
  `W003086 Keep 1119.22`, "move the band up" `W003088 move 1120.28`, "sell the audit only"
  `W003093 sell 1122.11`.
- **Must not imply:** any box checked, a guaranteed yes (C035).
- **Ear check carried:** the S19 to S20 seam. Measured: "only." decays into digital silence from
  1123.45 to 1123.77 before "Say" (0.32 s, not the aligner's 0.03 s). The cut sits at 1123.625, mid
  silence. The assembler still listens to master 1122.8 to 1127.5 before sign-off.

## S20 The callback

Master 1123.625 to 1157.792. Segments seg065 to seg069.

- **Job:** return to the cold open's inn and guest as an illustrative continuation, not a result.
- **Condition from r57-s13ab-company-in-gap-v1 and market-02:** pay off an earlier on-screen absence in
  the same persistent world.
- **seg065 model** (continuous with seg064's composition, no picture cut at 1123.625): on
  `W003097 Say 1123.83` a dashed marker "Say: first retainer running" appears on the day 31 to 90 band.
  Dashed means supposed.
- **seg066 F08:** hard cut on the silence after "running." to the filmed counter under "Go back to the
  inn."; the same guest at the counter fills in the registration card through "This time the
  registration card asks for his email."
- **seg067 F09:** he signs the inn's guest book under "The guest book is back, and it's the inn's."
- **seg068 F10:** after he has gone, the innkeeper writes a short thank you by hand under "After
  checkout there's a thank you that sounds like the innkeeper wrote it." This answers S00 F03, where
  she stopped at the laptop.
- **seg069 model:** the S00 model world. On `W003146 In 1139.84` a small note with a leaf and a trail
  line, labelled "October", goes to the guest's own email field (not the relay). On
  `W003157 the 1142.88` ("the next booking") the daypack guest's route runs to the inn's own page on
  `W003163 inn's 1144.22`; no commission tag attaches, shown by the empty tag outline on
  `W003167 no 1146.00`. On `W003176 The 1150.51` the booking site's first-introduction line and first
  tag stay solid; on `W003183 Nobody 1154.06` the site stays connected; on `W003189 stopped 1156.16`
  the second tag's place (from S00f) is an empty dashed outline. Small label throughout:
  "illustrative". Hold pause map P10.
- **Rejected:** film of the guest booking on the inn's website (fabricated legible web page).
- **Must not imply:** a measured result, that the inn left the platform, a savings figure, triumph.

## S21 The payoff

Master 1157.792 to 1175.042. Segment seg070.

- **Condition from r51-underlying-model-v1 and lesson-model-world-across-examples-v1:** redirect an
  existing object rather than recap panels.
- On `W003195 That's 1158.26` the S00 second commission tag opens and the S11 practice card sits
  inside it on `W003197 service 1158.80` (the dashed "a service" from S00h now solid). On
  `W003203 now 1161.36` the tag slides aside and the S10 ceiling slip comes forward. Its four boxes
  highlight and **clear to blank** on `W003208 Rooms, 1163.24`, `W003209 rate, 1163.94`,
  `W003210 occupancy, 1164.54`, `W003211 share 1165.60`. "Four numbers" on `W003215 Four 1167.16`; the
  ceiling line on `W003217 a 1168.36`; a blank retainer tag under it on `W003225 fit 1170.60`. On
  `W003237 ten 1174.12` hold. No figures remain: the tool, not the made-up inn.
- **Must not imply:** that ten minutes yields a result for any property beyond its own ceiling.

## S22 to S24 Verdict, first move, ask

Master 1175.042 to 1233.602. Segments seg071 to seg075; presenter takes P11, P12, P13.

- **Job:** the bounded verdict, the honest limit, the first move, the ask.
- **Form:** presenter throughout. Condition from r35-s06-presenter-conclusion-v3 and the precedent
  audit: a verdict and its push belong to the host in continuous takes; do not cut mid-sentence to
  manufacture emphasis. Three takes because the passage is 58.6 s: P11 ends in the 0.84 s pause after
  `W003294 month. 1195.74` where the verdict turns to its limit; P12 runs through "Run the ceiling."
  and ends in the 0.62 s pause; P13 carries the close and the ask. Crop changes come from continuous
  source only: P11 closer for "build. Bounded." (`W003241 is` to `W003243 Bounded.`); P12 wide then
  closer from `W003319 The 1204.81` (seg073); P13 close then wide for the ask on `W003374 If 1226.54`
  (seg075).
- **Rejected:** model inserts under "Ask for four numbers. Run the ceiling.": they would duplicate S21
  seconds earlier and hide a paid presenter source; P12's air-drawn ceiling line is the callback.
- **Must not imply:** proof of demand or income; "including me" and "Right now nobody knows" carry
  equal weight with the verdict (C036).

---

## Presenter take set

Recipe: V5 (EP007-PRESENTER-001 acceptance), Seedance 2.5 omni-reference with the IMAGE for identity
and study, the two behaviour VIDEOs for settling and articulation, the exact master excerpt as AUDIO;
Fal Sync v3 restoration; each output aligned to its own restored audio in three windows; mono upmixed
to stereo at unity. Prompt template: `r59-s14-why-you/presenter/AVATAR-PROMPT-A.txt`, with the
performance paragraph replaced by the brief in `SHOT-PLAN.json`.

Two EP007 items trigger now and are planned as a set:

- `next-recording-head-variety-v1` (owner deferred head variety "until next avatar recording").
- `r40-owner-movement-test-authorization-v1` and `r40-next-avatar-visible-hands-v1` (visible natural
  hand movement in any rebuilt avatar).

| Take | Master | Audio s | Gen s | Credits | Head pattern | Hand pattern |
|---|---|---|---|---|---|---|
| P01 | 50.292-59.458 | 9.17 | 11 | 99 | small recall tilt left, then level; still on question | single palm up on "anyone", total stillness through the question |
| P02 | 73.542-87.833 | 14.29 | 16 | 144 | upright, one settle, slight forward lean on "By the end" | both hands hold a small sheet-sized space on "four numbers"; flat hand lowers on "honestly pay" |
| P03 | 188.667-205.083 | 16.42 | 18 | 162 | turn right then centre, slow lean-in, small tilt on "nobody" | two placements on the table (site, inn); outward palm on "outside" |
| P04 | 226.208-236.292 | 10.08 | 12 | 108 | upright, one firm nod on "number" | touch to chest on "I think"; air-drawn flat ceiling line on "recovers" |
| P05 | 368.000-373.375 | 5.38 | 7 | 63 | concession tilt, back to centre | both palms up on "just do it?" |
| P06 | 469.292-480.042 | 10.75 | 12 | 108 | look-away down-left on recall, weighing side-to-side | fingertips together, release to empty open hands |
| P07 | 520.417-532.250 | 11.83 | 13 | 117 | lean back, forward, one downward nod on "wrong number" | set-aside sweep; flat hands; short sliding "shift" |
| P08 | 666.583-689.458 | 22.88 | 24 | 216 | quietest: near-still, one reflective look-away on "a decade ago", small nod on "test" | at rest; one hand lifts and turns out on "I don't know..." |
| P09 | 879.167-885.875 | 6.71 | 8 | 72 | tilt right on "hypotheses", firm upright on "I won't" | spread flat hand lowered onto the table |
| P10 | 976.542-982.875 | 6.33 | 8 | 72 | stillness through "not a living", slow nod on "foothold", chin lift on "Up the band" | at rest; one small upward step of the palm |
| P11 | 1175.042-1196.458 | 21.42 | 23 | 207 | centred, nod on "build", no movement on "Bounded", turn left on "directions" | two-hand box on "Bounded"; alternating palms; thin pinch on "thin"; forward open hand on "build the audit" |
| P12 | 1196.458-1213.875 | 17.42 | 19 | 171 | candid lean back, level on "including me", lighter tilt on "first move" | hand to chest on "me"; single raised finger on "one innkeeper"; air-drawn ceiling line on "Run the ceiling" (callback to P04) |
| P13 | 1213.875-1233.602 | 19.73 | 21 | 189 | warm forward; considering side-to-side; complete stillness on "Right now nobody knows" | open hand on "pay"; low palm-down wave-off on "Not to close them"; size shape on "at their size"; small open hand on "like" |
| **Total** | | 172.39 | **192** | **1,728** | | |

Set rules: no head shake, no finger pointing at the lens, no repeated nod pattern (each take has at
most one nod, P11 one); the ceiling line gesture appears exactly twice (P04, P12) by design; eyes near
lens on every promise (P02, P04 end, P12 "day thirty", P13 "nobody knows"); look-aways only on recall
lines (P06, P08). Reviewers check the set across takes, not each take alone. Generation seconds are
`ceil(audio) + 1`; if a take exceeds the provider maximum, use its listed fallback split in the JSON.

## Film takes and stills

| Still | World | Used by | Est credits |
|---|---|---|---|
| ST01 | the inn front desk, spring daylight | F01 to F04, F06 to F10 (directly or through accepted frames) | 30 (cap 40) |
| ST02 | the guest's living room, evening | F05 | 30 (cap 40) |

ST01 must be reviewed before any motion: guest book at the counter end nearest the entrance,
registration cards and pen, laptop screen invisible, window with trail, no readable text, a cast
distinct from EP007's workshop owner and buyer. Only two stills because every later desk take starts
from accepted F01 or F02 frames.

| Take | Segment | Slot s | Single action | Start frame |
|---|---|---|---|---|
| F01 | seg001 | 5.63 | guest slides the key back and nods | ST01 |
| F02 | seg002 | 4.88 | guest leaves; her look settles on the window | F01 last frame |
| F03 | seg003 | 6.33 | she types and stops | F02 last frame |
| F04 | seg007 | 3.75 | recognition while reading the screen | F03 frame before typing |
| F05 | seg014 | 5.42 | guest compares on his phone | ST02 |
| F06 | seg031 | 7.25 | she lifts the desk phone to her ear | F02 last frame |
| F07 | seg049 | 3.71 | a blank registration card and pen slide into view | crop of F02 last frame |
| F08 | seg066 | 6.67 | guest fills in the registration card | F01 first frame |
| F09 | seg067 | 2.96 | guest signs the guest book | F08 last frame |
| F10 | seg068 | 4.04 | she writes a thank you by hand | F02 last frame |

Ten 8 s Kling v3 Pro requests, about $8.96. A take that misses its action is not retried beyond the
film lane cap; the segment falls back to holding accepted frames of the nearest take or to the
adjacent model state, and the fallback is recorded.

## Review checks for the agent reviewers

1. Every model frame of S10 shows "ILLUSTRATIVE MODEL" and the receipt; every model frame of S17
   shows the modeled-scenario band.
2. No on-screen number, source name or caveat that is not in the claims map or spoken in the locked
   narration; receipts verbatim.
3. The guest book is never destroyed, locked or taken back from the site; the site is never shown as
   left.
4. Nothing checked, rising or "saved" is drawn as an achieved result.
5. Presenter set: head and hand patterns differ across adjacent takes; hands visibly move in every
   take except where stillness is specified; restored audio is the master.
6. Every segment boundary matches `SHOT-PLAN.json`, and the four continuous boundaries show no picture
   jump.
7. Whole-cut repetition: no two adjacent model scenes open with the same heading entrance.
