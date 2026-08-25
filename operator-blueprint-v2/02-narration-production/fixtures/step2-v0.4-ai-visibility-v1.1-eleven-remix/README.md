# Step 2 v0.4 AI Visibility ElevenLabs performance-voice experiment

Status: owner selected C and saved it as a separate private voice. A first over-limit performance
prompt failed closed; the repaired 440-character request returned three private candidates that
passed technical QA and await owner audition. This fixture does not authorize a replay, candidate
save, directed TTS calibration, full episode capture, Step 2 lock, Step 3, publication, or
replacement of the incumbent narrator.

## Question

Can a low-strength remix of the owner-controlled `OE Narrator Manav IVC v1` establish a more
camera-ready Operator Economy baseline while remaining unmistakably Manav?

This experiment does not reopen the AI Visibility v1.1 script, claims, thesis, Canvas, or scene
structure. Canonical `W` remains frozen.

## Why a remix

The incumbent voice preserved identity, but the retained N4A calibration was creatively revised
for contained energy. A prior firmer remix over-enunciated and flattened the delivery. V0.4 tests
one narrower intervention: a low-strength, nuance-rich remix whose energy comes from curiosity,
contrast, dry recognition, and earned conviction rather than speed, volume, or diction.

The incumbent voice remains untouched. Voice Design is excluded because it invents a voice rather
than adapting the owner's existing voice. A new IVC recording is a fallback only if remixing cannot
hold identity and energy together.

## External actions remain separate

1. Generate one bounded remix-preview batch from the existing voice. Preserve every returned
   preview; make no automatic selection and create no library voice.
2. Owner review selects one preview or rejects the batch.
3. Only a later, separately consumed authorization may save the selected preview as a new voice.
4. Only another later authorization may run the incumbent-versus-remix directed calibration.

Approval of this experiment is not permission to collapse those actions, regenerate the full
episode, retry a consumed action, or spend beyond the recorded ceilings.

## Frozen remix input

- Incumbent voice ID: `yUXeTfC1IFOCSjGc96sQ`
- Proposed variant name after owner selection: `OE Narrator Manav Performance v1`
- Remix prompt: [`remix/voice-remix-direction.txt`](remix/voice-remix-direction.txt)
- Preview passage: [`remix/preview-text.txt`](remix/preview-text.txt)
- Prompt strength: low, `0.25`
- Guidance scale: `2.0`
- Loudness: `0.0`
- Seed: fixed in the machine plan
- Automatic text generation: disabled
- Preview streaming: disabled
- Preview format: documented provider-native `mp3_44100_192`, preserved byte-for-byte
- Preview media status: audition evidence only; never a narration source, working master, or delivery master

The preview passage is the exact locked C01B post-sting promise at W tokens `[139,236)`, with only
nonlexical paragraph restoration. It is held out from the later scored P01/P02 comparison so the
voice-selection listen does not rehearse either bakeoff passage.
The Voice Remix endpoint documents preview audio as base64 MP3. That preview-only boundary does not
weaken the narration acquisition rule: the later directed TTS calibration still requests native
PCM first and allows `mp3_44100_192` only after an explicit PCM-capability rejection.

## Advancement rule

The remixed voice advances only when it:

- remains recognizably Manav with no identity regression;
- reaches at least `80/100` in the existing blind score;
- improves camera-ready energy by more than five points over the incumbent under identical
  directed transport;
- avoids announcer, trailer, newsreader, corporate-training, motivational, sales, over-enunciated,
  or artificially cheerful delivery; and
- later passes multi-chunk continuity and a separately generated pickup.

No preview result alone authorizes library save, directed calibration, full capture, or production
selection.

## Current result

AUTH-R1 was consumed once and returned three private previews. The success receipt and all three
provider files hash-match. They are mono 44.1 kHz, 192 kbps MP3 audition evidence, not narration
masters. Full decode and codec checks pass. The incumbent voice was not modified, and AUTH-R1 did
not create a library voice.

The owner review used four loudness-matched labels: three remix previews plus the historical
incumbent C01B control. The sealed mapping is in `reviews/AUTH-R1-LISTENING-ORDER.json`. The owner
selected C, which resolves to preview 01, generated voice ID `scMbPZwQjr40V1MzL3Nj`, and audio
SHA-256 `d46f8335e71bac3cf6c2b6396d3da7bdab4d82bd11db64f696fda8b5ede18392`.

AUTH-R2 saved that exact preview as the separate private voice `OE Narrator Manav C Base v1`.
The provider returned a successful new-voice receipt and did not modify the incumbent. AUTH-R3
then attempted one separately authorized low-strength performance refinement from the saved C
voice. The provider returned HTTP `403`; the runtime did not retry and created no audio or further
voice. The bounded disposition is in
[`reviews/AUTH-R3-PERFORMANCE-REFINEMENT-DISPOSITION.md`](reviews/AUTH-R3-PERFORMANCE-REFINEMENT-DISPOSITION.md).

The owner then authorized one materially repaired request using the exact 440-character prompt in
[`remix/voice-remix-direction-v3.txt`](remix/voice-remix-direction-v3.txt). AUTH-R4 returned three
private candidates from saved C. All three receipt hashes match, fully decode, are mono 44.1 kHz
192 kbps MP3, and measure within `0.4` LU of one another. No candidate was selected or saved. The
technical review is in [`reviews/AUTH-R4-TECHNICAL-QA.md`](reviews/AUTH-R4-TECHNICAL-QA.md).
