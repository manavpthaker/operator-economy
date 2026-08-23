# V2 Narration Production Standard

Status: proposed v0.2; test before approval.

## Purpose

Narration is the episode's final spoken timeline. Step 2 must preserve the editorial truth and exact words established in Step 1 while producing a performance that sounds human, confident, useful, and natural enough to carry the episode without visuals.

The target is an experienced operator explaining a serious opportunity in plain language—not an announcer, a sales voice, a synthetic-demo voice, or a flat script reading.

## 1. The script is lexically locked

The approved Step 1 script is the word authority.

Step 2 reproduces the Step 1 v1.5 ordered narration identity as whitespace-delimited `W` tokens.
That lexical identity is authoritative even when an aligner later represents one `W` token with
several subordinate acoustic parts. An ASR transcript, provider prompt, pronunciation alias, or
performance-marked copy may not replace the `W` sequence.

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

## 4. Freeze one narration identity and acquisition configuration

An episode has one primary narration identity. It may be:

- an authorized human narrator; or
- an authorized synthetic voice with documented usage rights and consent.

N3 freezes a proposed narrator identity and acquisition configuration before any calibration call
or recording. The freeze makes the test reproducible; it is not creative approval. N4A approves
the calibration performance, and only then may N4B full capture begin.

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

Synthetic generation, chunking, and regeneration follow
[`02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md`](02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md).
Neither this standard nor an N3 configuration freeze authorizes a provider call. Every external
call requires a separate explicit authorization naming the episode or fixture, voice,
provider/model, and whether the scope is calibration or full capture.

The V1 `studio/scripts/originate/generate_vo.py` path is prohibited in V2. It may rewrite or
performance-mark lexical content and does not enforce the V2 source-format, authorization, state,
or invalidation contracts. V2 must neither invoke nor import it.

## 5. Calibrate before the full run

Approve short calibration reads at N4A before generating or recording the full script. The
calibration set must include:

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

Each calibration passage receives separate lexical and technical findings plus an owner creative
decision. A technically clean output with the wrong delivery does not pass calibration. Full
capture starts at N4B only after N4A approval is recorded against the frozen N3 configuration.

## 6. Preserve raw takes and provenance

Raw recordings and provider outputs are immutable evidence. Register and hash them before destructive processing.

Each take record must identify:

- script revision and hash;
- section or line range;
- narrator and capture-lock revision;
- file path and SHA-256;
- creation date;
- human session or provider job identifier;
- native acquisition container, codec, sample rate, bit depth when meaningful, channel count, and
  lossy or lossless status;
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

## 8. Use interim ASR only as a diagnostic

Interim ASR may run after calibration acquisition and after each full take, synthetic chunk, or
pickup. Its job is to find likely additions, omissions, substitutions, repeats, truncations, and
pronunciation risks early enough to repair them efficiently.

Interim ASR output:

- is tied to the raw file or take hash it reviewed;
- remains explicitly `diagnostic` and non-authoritative;
- cannot establish lexical conformity;
- cannot become the Step 3 word-level transcript; and
- never replaces the required human disposition of a suspected mismatch.

After the dialogue edit, freeze one narration-master candidate. Generate the final-master ASR and
alignment from that exact hash, run lexical conformity, then finalize the word-level transcript and
intentional-pause map. If a pickup or edit changes any sample, discard those final results and rerun
them from the new master candidate.

## 9. Use pickups narrowly

Pickups repair a bounded performance, lexical, pronunciation, or technical defect. They must preserve the same locked words and voice-and-capture identity.

The pickup log records:

- triggering defect;
- exact locked words and section;
- replacement take;
- continuity notes;
- conformity result; and
- edit location in the narration master.

A pickup that requires new wording is a Step 1 change, not a pickup.

For synthetic narration, a pickup is a new immutable provider output with its own job identity. It
must use the same locked words, narrator, model, settings, pronunciation rules, and approved
context method. A one-line regeneration may not be hidden inside an earlier batch when its timbre,
pace, acoustic character, or prosody does not match. Regenerate a larger bounded chunk or the full
batch when continuity cannot be proven.

## 10. Edit dialogue without flattening it

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

## 11. Separate native acquisition from the delivery master

The native acquisition file is the exact human-recorder or provider output before local format
conversion or destructive processing. Its actual container, codec, sample rate, bit depth when
meaningful, channel count, and lossy or lossless status must be recorded from inspection rather
than inferred from a filename or requested setting.

Request native PCM first. If the selected ElevenLabs account and model cannot return it, the only
permitted fallback is `mp3_44100_192`. Preserve that MP3 unchanged, hash it, disclose its lossy
origin, and complete an audible artifact review. Decode and resample it exactly once into the PCM
working path. No later lossy intermediate may enter the editorial chain. A codec-damaged fallback
does not pass merely because it can be converted.

The delivery master is the clean editorial export used downstream. Its default contract is:

- PCM WAV;
- 48 kHz;
- 24-bit;
- mono;
- no clipping;
- true peak at or below -3 dBTP;
- no music, sound effects, ambience, or baked-in scene treatment; and
- no final-program limiter.

Converting `mp3_44100_192` into a 48 kHz, 24-bit WAV satisfies only the delivery-container contract.
It does not create native PCM quality. The source-format record must name the lossy acquisition and
the single conversion. A WAV derived from MP3 is a lossless delivery file with lossy origin; it may
never be represented as native lossless acquisition.

Measure and record integrated loudness, loudness range, true peak, duration, channel count, sample rate, and bit depth. Integrated loudness is a diagnostic here, not the final episode target. Resolve/Fairlight owns the final program mix and delivery loudness.

An MP3 may be created for convenient review, but it must be marked non-master and must never replace the WAV authority.

## 12. Conform the final master to the script

Lexical conformity is run against the final edited master—not merely the raw takes.

The report must account for:

- exact spoken words in order;
- punctuation-normalization rules;
- numerals, abbreviations, contractions, and hyphenation;
- approved pronunciation aliases;
- all detected additions, omissions, substitutions, repeats, and truncations; and
- the human disposition of every mismatch.

The default passing condition is zero unresolved `W`-token mismatches. Tool uncertainty may be
resolved by a documented human listen; a confirmed lexical mismatch cannot be waived inside Step 2.

## 13. Time words and intentional pauses from the final master

The word-level transcript is derived from the exact narration master named in the narration lock.

Timing rules:

- integer milliseconds;
- half-open intervals: `[start_ms, end_ms)`;
- `start_ms < end_ms` for every word;
- monotonically increasing, non-overlapping word intervals;
- all intervals bounded by the master duration;
- canonical Step 1 `W` token plus any normalized display form kept separately;
- optional `alignment_parts` subordinate to one `W` token when acoustic realization requires it;
- confidence or review state recorded where alignment is uncertain.

The intentional-pause map records approved semantic pauses separately from gaps inferred by the
aligner. It carries the same master hash and duration as the transcript. Silence is not a missing
word, and a pause label may not modify the lexical identity.

Raw provider timestamps, draft transcript timing, or timing from pre-edit takes cannot become the Step 3 authority.

Any sample-level change to the narration master invalidates the final alignment, lexical result,
word-level transcript, intentional-pause map, technical pass, creative approval, narration lock,
and Step 3 timing handoff. A byte-identical copy does not.

## 14. Separate technical pass from creative approval

`technical_pass` applies only to one exact master hash. It requires:

- complete raw and edit provenance;
- truthful native-acquisition and delivery-format disclosure;
- the delivery-master technical contract;
- zero unresolved spoken-word mismatches;
- a valid final-master transcript and intentional-pause map; and
- passing technical measurements and listening inspection.

`creative_approved` is a separate named-owner decision about whether the performance feels human,
credible, understandable, appropriately paced, and trustworthy over the complete episode. It
requires a current `technical_pass` and the independent eyes-closed listen. Automated validation,
provider success, export success, or a technical review cannot grant it.

## 15. Lock only after independent review

The Step 2 lock requires:

- an approved performance;
- zero unresolved lexical mismatches;
- a technically conforming narration master;
- a valid word-level transcript tied to that master hash;
- a valid intentional-pause map tied to that master hash;
- resolved pickup and edit records;
- an independent eyes-closed listen; and
- explicit owner approval.

The independent listener asks one practical question: does the episode work, remain understandable, and preserve trust when heard without visuals?

The lock names every authoritative file and hash. Step 3 receives those exact artifacts and may not retime speech, choose alternate takes, or replace the narrator.

The machine-validation and state contract is defined in
[`CLI-VALIDATION-CONTRACT.md`](CLI-VALIDATION-CONTRACT.md). A narration lock requires
`technical_pass` and `creative_approved` against the same master hash.
