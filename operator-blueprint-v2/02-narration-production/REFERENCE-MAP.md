# Step 2 Authority and Reference Map

Status: proposed v0.2.

This map prevents useful V1 narration practice from silently becoming V2 canon.

## Live authority entering Step 2

| Authority | Purpose |
| --- | --- |
| [`../01-editorial/STEP1-v1.5-APPROVAL.md`](../01-editorial/STEP1-v1.5-APPROVAL.md) | Establishes the current approved Step 1 system and AI Visibility fixture boundary. |
| Per-episode `01-editorial/editorial-lock.md` | Freezes the exact approved script package. |
| Per-episode `01-editorial/narration-handoff.md` | Supplies spoken-word count, hashes, pronunciations, direction risks, and blockers. |
| Per-episode `01-editorial/editorial-voice-conformity.md` | Proves the locked words already satisfy the reviewed OE/Manav editorial-language authorities. |
| [`02-direction/OE-NARRATOR-PROFILE.md`](02-direction/OE-NARRATOR-PROFILE.md) | Proposes the actual Studio-derived narrator identity, voice ID, model, settings, and non-lexical performance baseline for Step 2 calibration. |

The AI Visibility v1.1 fixture has an authorized fixture lock and ready narration handoff without
being promoted or numbered. A real episode still requires valid Step 0 promotion and full Step 1.
`content-os/voice.md` and `studio/config/speech-profile.md` are upstream Step 1 editorial-language
authorities. Step 2 receives their result through the locked words; it does not use them to rewrite.

## Retained V1 lessons — reference only

| V1 source | Durable lesson retained | V2 limitation |
| --- | --- | --- |
| [`../../docs/vo-first-production-flow.md`](../../docs/vo-first-production-flow.md) | Lock final narration and word timing before visual translation. | Its wider production discussion is not a Step 2 stage contract. |
| [`../../studio/ORIGINATE.md`](../../studio/ORIGINATE.md) | Separate script approval, voice production, transcription, and downstream visual work. | Old stage names, state values, and provider assumptions are not V2 authority. |
| `../../studio/scripts/originate/build_v3_direction.py` | Performance notation must not alter spoken lexical content. | The old parser and tag vocabulary are not automatically adopted. |
| `../../studio/scripts/originate/generate_vo.py` | Historical evidence that raw provider output and job metadata matter. | **Prohibited V2 execution/import.** Its rewrite behavior and contracts are incompatible with v0.2. |
| `../../studio/scripts/originate/ingest_recorded_vo.py` | Human narration needs the same manifest, validation, and transcript discipline as synthetic narration. | Its existing implementation is not the V2 workflow. |
| `../../studio/scripts/originate/master_vo_local.py` | Master locally and preserve source media rather than overwriting it. | Its processing chain and loudness assumptions are not automatically canonical. |
| `../../studio/config/blueprint.json` | Configuration should be explicit and reproducible. | Current voice identifiers, 44.1 kHz MP3 delivery, provider settings, and other episode-production values are not V2 defaults. |

## Explicitly not ported as V2 canon

- ElevenLabs or any other provider as mandatory.
- Existing voice IDs, model IDs, or provider presets becoming V2 authority merely because they appear in mutable V1 configuration. The explicit proposed narrator profile is the only current calibration exception. Credentials are never ported.
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
3. the approved OE narrator profile and episode-specific voice-and-capture lock; and
4. V1 reference material for lessons and implementation evidence only.

Until Step 2 is explicitly approved, this folder is a testable proposal rather than production authority.

Workflow Operations remains historical and is expected to fail N1. It is not a second positive
Step 2 control and may not be silently upgraded inside this stage.
