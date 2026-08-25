# Step 2 Authority and Reference Map

Status: proposed v0.5 synthetic-guide-to-Saved-C transfer microtest. G1 transport is installed but
has no active authority; V1 remains blocked. V0.3 and v0.4 remain frozen historical evidence.

This map prevents useful V1 narration practice from silently becoming V2 canon.

## Live authority entering Step 2

| Authority | Purpose |
| --- | --- |
| [`../01-editorial/STEP1-v1.5-APPROVAL.md`](../01-editorial/STEP1-v1.5-APPROVAL.md) | Establishes the current approved Step 1 system and AI Visibility fixture boundary. |
| Per-episode `01-editorial/editorial-lock.md` | Freezes the exact approved script package. |
| Per-episode `01-editorial/narration-handoff.md` | Supplies spoken-word count, hashes, pronunciations, direction risks, and blockers. |
| Per-episode `01-editorial/editorial-voice-conformity.md` | Proves the locked words already satisfy the reviewed OE/Manav editorial-language authorities. |
| [`02-direction/OE-NARRATOR-PROFILE.md`](02-direction/OE-NARRATOR-PROFILE.md) | Retains the technically proven but creatively revised ElevenLabs baseline as one v0.3 comparison method. |
| [`TOOL-AUDIT-AND-BAKEOFF.md`](TOOL-AUDIT-AND-BAKEOFF.md) | Defines the v0.3 performance envelope, sample gate, four initial authorizations, blind scoring, later long-form test, and asymmetric method-selection rule. |
| [`STEP2-v0.5-CHANGE-PROPOSAL.md`](STEP2-v0.5-CHANGE-PROPOSAL.md) | Defines the isolated, non-authorizing Gemini-guide and Original-C Voice Changer method test. It does not change `STAGE-GATES.md`. |

The AI Visibility v1.1 fixture has an authorized fixture lock and ready narration handoff without
being promoted or numbered. A real episode still requires valid Step 0 promotion and full Step 1.
`content-os/voice.md` and `studio/config/speech-profile.md` are upstream Step 1 editorial-language
authorities. Step 2 receives their result through the locked words; it does not use them to rewrite.

## Retained V1 lessons — reference only

| V1 source | Durable lesson retained | V2 limitation |
| --- | --- | --- |
| `../../docs/vo-first-production-flow.md` | Lock final narration and word timing before visual translation. | Historical source path; it is not present in this isolated branch and its wider production discussion is not a Step 2 stage contract. |
| [`../../studio/ORIGINATE.md`](../../studio/ORIGINATE.md) | Separate script approval, voice production, transcription, and downstream visual work. | Old stage names, state values, and provider assumptions are not V2 authority. |
| `../../studio/scripts/originate/build_v3_direction.py` | Performance notation must not alter spoken lexical content. | The old parser and tag vocabulary are not automatically adopted. |
| `../../studio/scripts/originate/generate_vo.py` | Historical evidence that raw provider output and job metadata matter. | **Prohibited V2 execution/import.** Its rewrite behavior and contracts are incompatible with V2 Step 2. |
| `../../studio/scripts/originate/ingest_recorded_vo.py` | Human narration needs the same manifest, validation, and transcript discipline as synthetic narration. | Its existing implementation is not the V2 workflow. |
| `../../studio/scripts/originate/master_vo_local.py` | Master locally and preserve source media rather than overwriting it. | Its processing chain and loudness assumptions are not automatically canonical. |
| `../../studio/config/blueprint.json` | Configuration should be explicit and reproducible. | Current voice identifiers, 44.1 kHz MP3 delivery, provider settings, and other episode-production values are not V2 defaults. |

## Explicitly not ported as V2 canon

- ElevenLabs or any other provider as mandatory.
- Existing voice IDs, model IDs, or provider presets becoming V2 authority merely because they appear in mutable V1 configuration. The explicit narrator profile is a retained comparison baseline, not selected authority. Credentials are never ported.
- Synthetic narration as the default over an authorized human recording.
- 44.1 kHz MP3 as the production master.
- Any lossy source other than the strictly handled `mp3_44100_192` fallback after native PCM is
  unavailable.
- Representing PCM converted from MP3 as native PCM acquisition.
- Mixed voice identities across an episode without an approved exception.
- Provider-specific performance tags as canonical script content.
- A per-track `-14 LUFS` target as the final program loudness decision.
- Music, sound effects, ambience, scene treatment, or final limiting in the narration master.
- Raw provider timestamps after narration editing.
- ASR-derived wording replacing the Step 1 v1.5 whitespace-delimited `W` sequence.
- Visual planning, B-roll sourcing, scene direction, or motion design inside Step 2.

## Authority order

For Step 2 decisions, use this order:

1. current Step 1 v1.5 editorial lock and narration handoff, including an explicitly authorized fixture pair;
2. approved V2 Step 2 standard and stage gates, once owner-locked;
3. the approved provider-agnostic performance envelope, method-selection record, and
   episode-specific N3 voice-and-capture lock;
4. the retained OE narrator profile only as comparison evidence until a method is selected; and
5. V1 reference material for lessons and implementation evidence only.

Until Step 2 is explicitly approved, this folder is a testable proposal rather than production authority.

## Current provider capability references

These live vendor documents support the proposed bakeoff boundaries. They do not become permanent
V2 authority, prove account access, confer commercial rights, or authorize an action.

| Provider source | Current use | Required caution |
| --- | --- | --- |
| [ElevenLabs TTS API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert) | Request construction and output-format capability. | V0.3 compiles but does not execute bakeoff requests; provider success would not be creative approval. |
| [Eleven prompting](https://elevenlabs.io/docs/best-practices/prompting), [v3 creative playground](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech), and [request stitching](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching) | Provider-adapter treatment of allowlisted non-spoken audio tags and the v3 multi-request boundary. | Tags stay out of canonical `W`; a spoken tag is a hard failure; do not claim v3 request stitching. |
| [Eleven voice metadata](https://elevenlabs.io/docs/api-reference/voices/get) and [sample audio](https://elevenlabs.io/docs/api-reference/voices/samples/get) | Read-only metadata and exact original-sample retrieval design. | Zero or multiple samples block; retrieval needs AUTH-01 and exact sample selection. |
| [Hume TTS overview](https://dev.hume.ai/docs/text-to-speech-tts/overview), [acting instructions](https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions), [continuation](https://dev.hume.ai/docs/text-to-speech-tts/continuation), [JSON synthesis endpoint](https://dev.hume.ai/reference/text-to-speech-tts/synthesize-json), and [file synthesis endpoint](https://dev.hume.ai/reference/text-to-speech-tts/synthesize-file) | Separate utterance text/description, two generations through `POST /v0/tts`, 48 kHz PCM/WAV, and continuation review. | Octave 1 needs local forced alignment; timestamps are Octave 2-only. |
| [Hume voice cloning](https://dev.hume.ai/docs/voice/voice-cloning) | Human-audio clone flow. | Current public path is UI-mediated; login is not upload/clone authority. |
| [Hume Create Voice API](https://dev.hume.ai/reference/voices/create) | Documents saving a voice from a TTS generation ID. | Do not misrepresent it as a public human-audio upload-clone API. |
| [Hume pricing](https://www.hume.ai/pricing) | Commercial-tier gate. | Free/Starter is not accepted for OE commercial production; verify current paid terms before action. |
| [Google Cloud Gemini TTS](https://cloud.google.com/text-to-speech/docs/gemini-tts), [Text-to-Speech synthesize API](https://cloud.google.com/text-to-speech/docs/reference/rest/v1/text/synthesize), and [pricing](https://cloud.google.com/text-to-speech/pricing) | Separate acting prompt and exact dialogue through the Cloud GA endpoint, `LINEAR16` guide acquisition, request limits, modeled authorization ceiling, and the installed G1 transport. | The executor enforces the reviewed caps locally, but the committed G1 draft authorizes zero; two requests remain stochastic, and provider success is not lexical or creative approval. |
| [ElevenLabs Voice Changer](https://elevenlabs.io/docs/overview/capabilities/voice-changer) and [speech-to-speech API](https://elevenlabs.io/docs/api-reference/speech-to-speech/convert) | Best-effort transfer of a selected guide's performance into the existing Original C identity, with native PCM requested first. | It accepts audio rather than an acting prompt or transcript. Exact words, identity, and performance transfer require new QA. Upload is blocked until the exact guide, rights, current opt-out or ZRM state, and separate authorization are verified. |

Recheck every live source and active account term before issuing an authorization.

Workflow Operations remains historical and is expected to fail N1. It is not a second positive
Step 2 control and may not be silently upgraded inside this stage.
