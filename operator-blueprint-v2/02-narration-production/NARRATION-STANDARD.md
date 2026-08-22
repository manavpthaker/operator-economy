# V2 Narration Production Standard

Status: proposed v0.1; test before approval.

## Purpose

Narration is the episode's final spoken timeline. Step 2 must preserve the editorial truth and exact words established in Step 1 while producing a performance that sounds human, confident, useful, and natural enough to carry the episode without visuals.

The target is an experienced operator explaining a serious opportunity in plain language—not an announcer, a sales voice, a synthetic-demo voice, or a flat script reading.

## 1. The script is lexically locked

The approved Step 1 script is the word authority.

Step 2 may change:

- pace;
- pauses and breath placement;
- emphasis and restraint;
- sentence energy and emotional turn;
- pronunciation, using a separately recorded pronunciation alias; and
- non-spoken performance notation, punctuation, capitalization, or spacing stored outside the canonical script.

Step 2 may not silently:

- add, remove, replace, or reorder words;
- turn written qualifications into inaudible delivery;
- improvise connective phrases or filler words;
- simplify evidence, economics, risk, or uncertainty language; or
- change the promised business, buyer, operator, or outcome.

Spoken fillers such as “well,” “so,” “you know,” or “basically” are lexical additions unless they already exist in the locked script. A natural performance is created through phrasing, not unapproved words.

If a wording problem appears during performance, record it as a Step 1 change request. Do not repair it inside the audio edit.

## 2. Perform the locked editorial voice; do not recreate it

The Step 1 script already owns the Operator Economy message-delivery voice and Manav spoken-language fingerprint. Step 2 receives the exact approved words, their editorial-voice conformity report, and the narration handoff.

Step 2 translates those words into vocal performance. It does not add conversational vocabulary, contractions, jokes, asides, analogies, sentence starts, or connective phrases to make the script sound more like Manav.

The performance should remain:

- practical, specific, and calm;
- commercially literate without sounding corporate;
- curious but not credulous;
- aspirational about the opportunity and honest about what remains unproven;
- down-to-earth, as if an experienced operator is walking one person through a blueprint; and
- paced for comprehension, especially around evidence, economics, and the first validation test.

The approved OE narrator profile and episode voice-and-capture lock govern voice identity, provider/model settings, timbre continuity, and non-lexical performance treatment.

Avoid:

- trailer voice, hype, artificial urgency, or forced gravitas;
- identical intensity across the full episode;
- false intimacy, exaggerated warmth, or a motivational-speaker cadence;
- speed-reading dense proof;
- audible certainty that exceeds the words on the page; and
- overacting transitions that the script has already made clear.

Qualifications and uncertainty must be audible. They cannot be rushed, dropped in volume, or treated as disposable parentheticals.

## 3. Direct the episode as a changing argument

Performance direction is created before full capture. It should identify:

- the listener and the narrator's relationship to that listener;
- the episode's central promise;
- the major emotional and intellectual turns;
- where the narrator is diagnosing, proving, teaching, warning, or inviting action;
- sentences that require restraint rather than emphasis;
- dense passages that require additional space;
- pronunciations, acronyms, numbers, and proper nouns; and
- the intended landing point of the final case.

Do not annotate every word. Direction should make the argument more legible, not produce a robotic emphasis map.

## 4. Lock one narration identity

An episode has one primary narration identity. It may be:

- an authorized human narrator; or
- an authorized synthetic voice with documented usage rights and consent.

The voice-and-capture lock must be approved before the full run.

For a human narrator, freeze at minimum:

- narrator identity and consent;
- room and acoustic treatment;
- microphone, placement, interface, and recording chain;
- sample rate and bit depth;
- approximate mouth-to-microphone distance;
- monitoring method; and
- a short room-tone capture.

For a synthetic narrator, freeze at minimum:

- provider and model/version when exposed;
- authorized voice identity and rights basis;
- generation settings;
- pronunciation aliases;
- chunking strategy and context method;
- output format; and
- provider job or generation identifiers.

Do not clone a third party, imitate a living person without authorization, or mix narration identities to conceal a continuity problem. A voice change requires an explicit exception decision and a new consistency review.

## 5. Calibrate before the full run

Approve short calibration reads before generating or recording the full script. The calibration set must include:

1. the cold open or a comparable high-attention passage;
2. a dense evidence passage;
3. an economics or uncertainty passage; and
4. a pronunciation passage containing difficult names, numbers, acronyms, or technical terms.

Review calibration for:

- listener fit and trust;
- natural phrasing;
- differentiation between argument modes;
- intelligibility and pronunciation;
- consistency with the frozen capture setup; and
- technical cleanliness.

Full capture starts only after the calibration decision is recorded.

## 6. Preserve raw takes and provenance

Raw recordings and provider outputs are immutable evidence. Register and hash them before destructive processing.

Each take record must identify:

- script revision and hash;
- section or line range;
- narrator and capture-lock revision;
- file path and SHA-256;
- creation date;
- human session or provider job identifier;
- known defects; and
- review state.

Never overwrite a raw take with a cleaned, trimmed, denoised, or mastered version.

## 7. Review takes on three separate axes

Every candidate take is evaluated independently for:

### Performance

- Does it sound like a person thinking through the idea?
- Are the promise, proof, blueprint, and final case distinct in energy?
- Are the important words clear without theatrical over-emphasis?
- Does the pace leave enough time to understand evidence and numbers?
- Does the performance remain credible over the full duration?

### Lexical conformity

- Does it contain every locked spoken word in the correct order?
- Are there additions, omissions, substitutions, repeated words, or truncated lines?
- Are qualifications and negations preserved?
- Are pronunciation aliases spoken as the canonical word intends?

### Technical quality

- Is the recording free of clipping, distortion, dropouts, and unrecoverable noise?
- Are edits, breaths, and room-tone changes unobtrusive?
- Is the voice timbrally consistent across takes and pickups?
- Is there enough clean signal for downstream finishing?

A technically clean take is not automatically a good performance. A strong performance with a truth-changing word error cannot pass.

## 8. Use pickups narrowly

Pickups repair a bounded performance, lexical, pronunciation, or technical defect. They must preserve the same locked words and voice-and-capture identity.

The pickup log records:

- triggering defect;
- exact locked words and section;
- replacement take;
- continuity notes;
- conformity result; and
- edit location in the narration master.

A pickup that requires new wording is a Step 1 change, not a pickup.

## 9. Edit dialogue without flattening it

The narration edit may:

- choose between approved takes;
- remove false starts, accidental repeats, mouth noise, and unusable breaths;
- shape pauses without changing meaning;
- apply conservative corrective processing;
- repair bounded noise where the voice remains natural; and
- join approved pickups with room-tone and tonal continuity.

The narration edit should not:

- quantize every pause;
- remove all breaths and human texture;
- over-denoise, over-compress, de-ess aggressively, or brighten into harshness;
- use music or sound effects to hide edit problems;
- add final-program limiting; or
- chase a publishing loudness target that belongs to the finished mix.

Every splice and source selection must be represented in the narration edit decision list.

## 10. Deliver a clean narration master

Preferred production master:

- PCM WAV;
- 48 kHz;
- 24-bit;
- mono;
- no clipping;
- true peak at or below -3 dBTP;
- no music, sound effects, ambience, or baked-in scene treatment; and
- no final-program limiter.

Measure and record integrated loudness, loudness range, true peak, duration, channel count, sample rate, and bit depth. Integrated loudness is a diagnostic here, not the final episode target. Resolve/Fairlight owns the final program mix and delivery loudness.

An MP3 may be created for convenient review, but it must be marked non-master and must never replace the WAV authority.

## 11. Conform the final master to the script

Lexical conformity is run against the final edited master—not merely the raw takes.

The report must account for:

- exact spoken words in order;
- punctuation-normalization rules;
- numerals, abbreviations, contractions, and hyphenation;
- approved pronunciation aliases;
- all detected additions, omissions, substitutions, repeats, and truncations; and
- the human disposition of every mismatch.

The default passing condition is zero unresolved spoken-word mismatches. Tool uncertainty may be resolved by a documented human listen; a confirmed lexical mismatch cannot be waived inside Step 2.

## 12. Time the words from the final master

The word-level transcript is derived from the exact narration master named in the narration lock.

Timing rules:

- integer milliseconds;
- half-open intervals: `[start_ms, end_ms)`;
- `start_ms < end_ms` for every word;
- monotonically increasing, non-overlapping word intervals;
- all intervals bounded by the master duration;
- canonical spoken token plus any normalized display form kept separately; and
- confidence or review state recorded where alignment is uncertain.

Raw provider timestamps, draft transcript timing, or timing from pre-edit takes cannot become the Step 3 authority.

Any sample-level change to the narration master invalidates the word-level transcript, narration lock, and Step 3 timing handoff. A byte-identical copy does not.

## 13. Lock only after independent review

The Step 2 lock requires:

- an approved performance;
- zero unresolved lexical mismatches;
- a technically conforming narration master;
- a valid word-level transcript tied to that master hash;
- resolved pickup and edit records;
- an independent eyes-closed listen; and
- explicit owner approval.

The independent listener asks one practical question: does the episode work, remain understandable, and preserve trust when heard without visuals?

The lock names every authoritative file and hash. Step 3 receives those exact artifacts and may not retime speech, choose alternate takes, or replace the narrator.
