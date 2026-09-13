# Revision 10 replacement-script voice

Completed one continuous Algieba guide and one Original C transfer of the owner's replacement script. All 193 exact supplied script words are independently recognized and mapped to timestamps. There was no second guide, pickup, synthesis retry, forced duration or post-transfer speed processing.

The final [full Original C WAV](https://v3b.fal.media/files/b/0aaa35ee/-L-OSg2Vri4DStxgrcFHO_selfie-r10-final-ebda957ffd92f944.wav) is 55.0777291667 seconds: 2,643,731 samples at 48 kHz, mono 16-bit PCM. Local source: `media/revision-10/voice-r10.original-c.wav`. SHA-256: `ebda957ffd92f944ce180ffab455da84e48cfffd9ae775936be6cff3d085ba0f`. Hosted bytes matched local bytes on readback.

The exact script SHA-256 is `242ab0bedea72a8fc5d303191f9dc61569614dc70cfdbef759891a7fa94affd6`. `R10.style.json` directs an ordinary, varied conversation, quicker connective phrasing and a clearly paced GTM paragraph, without acted smile cues or a duration target. The guide returned 55.0509583333 seconds; transfer added 26.771 ms. Original C settings remain similarity 0.8, stability 0.4, style 0, speed 1, speaker boost on, seed 2026082501, noise removal off, and `pcm_48000` output.

`R10/FINAL-ASR.json` retains independent faster-whisper small.en output with VAD, no previous-text conditioning and no initial prompt. It recognizes `I'd still` and `you'd built`. Normalization accepts punctuation, apostrophe style, spelled acronyms and the established `gotta`/`got to` and `wanna`/`want to` transcription equivalents. It does not permit missing words or paraphrases. `R10/FINAL-WORD-TIMINGS.json` maps all 193 exact script words to the actual final-audio transcription.

The final word `business?` is recognized at 54.50–54.70 seconds. Final sample and last 10 ms RMS are zero; last 60 ms RMS is 0.0000106235. No final-audio samples reach full scale. These are endpoint and transcription checks, not listening or naturalness acceptance.

Candidate picture cuts occur in the requested paragraph gaps: frame 409 / sample 818000 / 17.0416667 seconds after word 60 (`time.`), and frame 902 / sample 1804000 / 37.5833333 seconds after word 129 (`way.`). Their 50 ms RMS levels are -89.31 and -64.46 dBFS. Contiguous source lengths are 17.041667, 20.541667 and 17.494396 seconds; all are below 29.5 seconds. No slicing was performed here. Root owns segmentation, video generation and final delivery.

`FINAL-VOICE.json` binds the source, hosted output, exact timings, candidate cuts and provider receipts. Raw provider bodies remain preserved under ignored `media/revision-10/`; exclusive stage intents prevent repeated generation. Authenticated requests use the original API hosts, reject redirects and disable retries. The guide's successful ASR was repeated only to retain a timing payload truncated by the tool transport; the speech itself was not regenerated.

No previous revision, canonical narration, caption record, clone settings, video job or commit was changed. Owner listening remains required to judge delivery and voice naturalness.
