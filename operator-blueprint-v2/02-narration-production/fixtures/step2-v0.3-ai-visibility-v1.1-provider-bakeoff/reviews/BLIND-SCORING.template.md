# Blind Provider Bakeoff Scoring

Status: template; no audio or result exists

## Blind setup

- Review ID:
- Review date:
- Blind-map custodian, excluded from scoring:
- Listener:
- Listening system and room:
- Loudness-matching method:
- Neutral candidate IDs supplied:
- Provider/model/voice metadata hidden: yes / no
- File metadata removed from review copies: yes / no
- Music, pictures, captions, and waveform hidden: yes / no
- Randomized playback order recorded by custodian: yes / no

One custodian maps neutral IDs to provider outputs. The owner and independent listener score only
the neutral review files. Do not infer a provider from filenames, timing sheets, tags, request IDs,
or cost.

## Hard gates

Any `fail` removes that candidate before preference scoring.

| Candidate | Words: no addition, omission, repeat, substitution, or reorder | No audible direction/tag | Names, numbers, negations, and qualifications intact | No clipping, truncation, watery consonants, brittle sibilance, or synthetic artifacts | Rights and provenance bound | Understandable without music or visuals | Gate result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B01 | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail |
| B02 | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail |
| B03 | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail |
| B04 | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail |
| B05 | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail |
| B06 | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail |
| B07 | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail |
| B08 | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail |

Record every suspected addition, omission, substitution, reorder, pronunciation ambiguity, or
spoken tag with a timecode. ASR may help find issues but cannot decide this gate.

## Performance score

Give each dimension a whole-number rating from 1 to 5. `1` means unusable; `3` means acceptable
but generic; `5` means distinctly right for Operator Economy. Convert the rating into the points
available for that dimension with `(rating / 5) x allocated points`. For example, a rating of `4`
on a 25-point dimension contributes `20` points. Sum the six dimension-point values for the
`/100` total. Keep full precision while calculating and round only the final total to two decimal
places.

| Dimension | Weight | What the listener is judging |
| --- | ---: | --- |
| Manav identity | 25 | sounds recognizably like Manav speaking his own view, not a generic narrator |
| Camera-ready energy without announcer voice | 25 | has intentional forward pull and presence without trailer, newsreader, sales, or motivational cadence |
| Documented argument and performance turns | 20 | the planned questions, observations, rules, callbacks, caveats, actions, and verdicts land as distinct turns |
| Natural, credible, and sustainable for a full episode | 15 | feels spoken across a table and could remain believable without fatigue or mannerism over long form |
| Distinguishes evidence, caveats, action, and verdict | 10 | changes stance appropriately while keeping dense logic, negations, and qualifications clear |
| Editability and pickup continuity | 5 | has stable identity, timbre, pace, and phrasing that can support bounded pickups and clean edits |

### Score sheet

| Candidate | Identity /25 | Camera energy /25 | Turns /20 | Natural full episode /15 | Functions /10 | Editability /5 | Total /100 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B01 |  |  |  |  |  |  |  |
| B02 |  |  |  |  |  |  |  |
| B03 |  |  |  |  |  |  |  |
| B04 |  |  |  |  |  |  |  |
| B05 |  |  |  |  |  |  |  |
| B06 |  |  |  |  |  |  |  |
| B07 |  |  |  |  |  |  |  |
| B08 |  |  |  |  |  |  |  |

## Passage-specific notes

For `P01-S00`, note whether the opening is alert without melodrama, the stale-2022 observation has
dry disbelief rather than customer contempt, the business promise feels credible, and the final
question remains genuinely open.

For `P02-S11-S12`, note whether the ask-first rule, three gates, stop rule, callback, `BUILD`
verdict, and final invitation each land as a different thought while remaining one continuous
conversation.

## Preference decisions

- Best `P01-S00` candidate and why:
- Best `P02-S11-S12` candidate and why:
- Any provider identity suspected before unblinding:
- Confidence: low / medium / high
- Scorer recommendation: advance best blind clips / do not advance / revise
- Scorecard signed by/date:
- Frozen signed scorecard path/SHA-256:

Unblind only after all signed score sheets are frozen and hashed. A passage win advances a path to
long-form confirmation; it does not authorize production capture.

This scorer-local record ends at signature. It must not contain the sealed map, provider identity,
post-unblind arithmetic, operational comparison, or selection decision.
