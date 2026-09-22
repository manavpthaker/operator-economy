# Copy applied, and what changed against COPY-PACKAGE

Source of truth for the approved copy:
`blueprint-cinema/experiments/EP009-SHORTS-003/COPY-PACKAGE.json` (sha256
`4bcc0b1ebdcf3a563d0f1cda8dab340fdd44ff1d288d63277b6dd720c8058da7`) and its `.md`
counterpart. The package was written against the r3 cuts and explicitly said its
`replace` and `add` lines were copy specifications, not builds. This revision builds them.

**Titles are applied unchanged**, all four. So are all descriptions except where the re-cut
changed what the Short says (noted below), and every `[EPISODE_URL]` is still the literal
placeholder. The episode URL stays a placeholder until `launch/links.json` originates one;
EP009's slug is `direct-booking-practice`. The live August episode URL is not restated here
or anywhere in this revision.

## Applied as specified

| Short | Cue | Copy | Where it now lands |
|---|---|---|---|
| 01 | `s01-proof-headline` | Booked again. Billed again. | Proof card headline, 4.125–11.125 s. Replaces the verbatim repeat of the opening overlay. |
| 02 | `s02-hook` | Cheap parts. The job isn't. | 6.458–10.333 s (was specified for 0.000–3.875 s; see below) |
| 02 | `s02-boundary` | Priced to what it recovers | 17.817–19.637 s, on the spoken "But only for what it recovers" |
| 03 | `s03-hook` | A small inn. A repeat guest. | 0.000–1.792 s |
| 04 | `s04-constraint` | Capped by what it recovers | 9.540–10.690 s, on the spoken "what the job recovers" |

All four `keep` lines are kept: "Same guest. Second commission.", "The missing arithmetic.",
"Illustrative small-inn story", "The tool can draft.", "Node-RED + OpenAI · recorded workflow",
"Fictional guest. Awaiting human review. No sending available.", "Booking site → Guest's
email", "Returning guest → The inn?", "TOTAL BOOKING-SITE COMMISSIONS", "≠ Recoverable
opportunity", "How much can actually shift?".

No figure that the copy package dropped appears anywhere on screen. `C020`, `C018`, `C001`,
`C019`, `C024` and `C028` are absent from every title, overlay, card and description. The only
numbers in the package are in 04's pinned comment (20 rooms, $180, 70 percent) and in 01's and
04's descriptions ("illustrative 20-room inn"), all as the copy package published them.

## Minimal changes the re-cut forced, and why

**1. Short 02's hook line moves from 0.000 s to 6.458 s.** The package specified
"Cheap parts. The job isn't." at 0.000–3.875 s because the r3 cut opened on the spoken
"If the parts to fix this are cheap…". The r4 cut adds an orientation beat in front of that
question, so the line now sits on the question beat it describes. Same words, later placement.

**2. Short 02 gains one on-screen line: "A direct-booking practice" (25 chars).** The new
orientation beat speaks "It helps a small hotel…", and this line supplies the referent for
"It". It is the episode's own spoken name (`COPY-PACKAGE.json.episode_spoken_name`), not a new
claim.

**3. Short 02's description is rewritten to match the new opening.** The package's line 1
opened on the cheap parts; the Short now opens on the small hotel paying a booking site to meet
its own returning guests, so line 1 leads with that and the cheap parts follow. Substance,
claims and sources unchanged.

**4. Short 01's description line 2 gains "on a guest it already had."** The re-cut adds the
spoken sentence "For a guest she already knows by name.", so the description now says what the
Short says.

**5. Short 03's cliffhanger note is void and its conditional end card is not used.** The
package offered `s03-end-card-alt` — "Nobody is, yet." — *only if* the cut was not extended.
It was extended, so the card states the spoken line instead: "Nobody at the inn is."

**6. Short 01's pinned comment now opens "Full episode: [EPISODE_URL]".** Two reasons. The
package's own EP002 lesson requires the URL to lead the comment, which it still does. And
`shorts_contract.py`'s `PIN_ROUTE_RE` requires a routing word; "[EPISODE_URL]" alone does not
match one, because the underscore leaves no word boundary after "EPISODE". Shorts 02, 03 and 04
already say "The full episode" in prose and were not touched. This is the only wording change
made to satisfy the validator, and it adds two words rather than a claim.

**7. `cliffhanger` is dropped from every manifest.** It is retired by
`docs/content-rubric.md`. The package's per-Short `cliffhanger` blocks are superseded, and
their assessments are answered in `STANDARD-JUDGMENT.md`.

**8. Every end card became declarative.** The package did not specify end cards; it recorded
them as existing reinforcement for the cliffhangers. With the cliffhanger retired, all four
cards now state what the Short resolved and route to what the episode adds:

| Short | New end card headline | New routing line |
|---|---|---|
| 01 | The inn pays the commission again. | EP009 runs the arithmetic on an illustrative inn. |
| 02 | I think it can be sold from outside. | For what it recovers. EP009 designs the job around that drafting step and computes that number on an illustrative inn. |
| 03 | Nobody at the inn is. | EP009 asks whether somebody outside the property can be |
| 04 | The inn can only pay what the job recovers. | EP009 runs that number on an illustrative inn. |

02's card keeps the narration's hedge ("I think") rather than flattening it into a flat claim.

## Unchanged package decisions

- No hashtags on any Short. Every `hashtags` array is empty by decision.
- Publish order 01, 04, 02, 03. Nothing in the re-cut changes the reasoning the package gave,
  and 03 now resolves something, so an owner may reasonably move it up; that is an owner call,
  not a writer's, and the package's order is carried forward unamended.
- Register: `operator_economy` documentary, not the signed first-person register. 02's end card
  is the one first-person line in the package, and it is first person because the narration is.
- No em dash and no emoji anywhere. No question is used as a title.
