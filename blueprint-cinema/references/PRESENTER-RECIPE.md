# Presenter Recipe

The single source for generating Manav's avatar. It applies to every surface that shows him: OE long-form episodes, OE Shorts, and Content OS signed videos. Those runbooks point here for the presenter steps and add only what their surface needs (aspect ratio, number of shots, where the lock lives).

Consolidated 2026-09-24 from what EP007, its four Shorts, EP009 and the Content OS signed-video builds actually did. Where an older runbook disagrees with this file on the presenter, this file wins.

## 1. Lock the look first (owner gate)

A **project** is whatever gets its own look: an OE episode (and its Shorts, unless the owner wants the Shorts in a different look), or a Content OS signed video. Each project gets a new location and outfit. Only the kit and this recipe carry over.

1. Generate look candidates as stills only, from the accepted likeness. They cost cents; explore here, not in video.
2. The owner picks one.
3. `blueprint-cinema/bin/oe-cinema lock-look <project_dir> --ref <still>=<url or Higgsfield media ID> --location "..." --outfit "..." --locked-by Manav`

`<project_dir>` is the OE episode or experiment folder, or the Content OS video package's working folder. Changing a locked look needs `--supersede "<reason>"`, and the orphaned presenter jobs are recorded. Don't reopen the look after presenter video exists unless the owner raises it.

## 2. Inputs to every take

| Input | Role | Source |
|---|---|---|
| Locked look still | `image_references` | `presenter/LOOK-LOCK.json` |
| K01 neutral delivery, 9 s | `video_references` (first) | `b796a739-5036-4242-8fa9-cd61e9e19a0c` |
| K08 listening, 6 s | `video_references` (second) | `0f63cbdf-7579-46f9-aab5-ba7af28c85e4` |
| Exact narration slice | `audio_references` | The locked narration master |

The kit media IDs and their local files and hashes are in `PRESENTER-REFERENCE-KIT.md` ("Standing references"). Don't use the old call-recording behavior clips, or the fixed EP007 "V5" look, for new work.

**Audio slice.** Cut exact PCM from the locked master at near-zero samples between words. Pad only with digital zero to the request length. Keep a lead silence of 0.25–2.34 s, padded to whole seconds: with no lead, the mouth starts before the body settles. Make an MP3 companion for upload and ASR-check it against the expected words. A slice that starts on a rising waveform clicks.

**Length.** Keep each take at 12 s or under; split longer lines at a word boundary. Long takes drift out of sync.

**New words need new takes.** Approved footage can't be reused under different words. Every sync model fails on it.

## 3. The request

Model `seedance_2_5`, mode `omni_reference`, 1080p, `generate_audio: true`, `use_unlim: false`, count 1. Use aspect 16:9 for long-form and 9:16 for Shorts and signed videos. Duration is the padded slice length.

The prompt describes the look and frame from the locked still: identity, glasses, outfit, room, light, framing with hands visible if the surface shows them. Then include this reference sentence verbatim:

> The first VIDEO supplies connected public-facing articulation to the lens. The second VIDEO supplies relaxed listening stillness and ordinary blinks. They are behavior references only. Do not copy their clothing, room, lighting, unrelated speech or mouth timing.

Then say that the IMAGE controls identity and setting, and the AUDIO controls words, voice, cadence and pauses. Quote the exact words, lip sync as the priority, one or two earned gestures at most, then a hold after the last word with no extra speech. Head motion can't be prompted away (measured 2026-09-23); fix it in selection and framing. EP009 P08 (`experiments/EP009-FULL-BUILD-001/presenter-kit-test/TEST.json`) is a worked example.

## 4. Gate, quote, submit, ledger

Every paid call is gated, capped and ledgered before money moves.

- **Through the API** (`HF_KEY` or `FAL_KEY` set): `oe-cinema generate <project_dir> --lane presenter ...` runs the look-lock check, the lane cap, the intent row, the job and the done/failed row.
- **Through the Higgsfield connector** (the current route for Seedance, because there's no `HF_KEY` yet):
  1. Run the same command with `--dry-run` and the connector's `medias` list in `--args`. That applies the look lock (media IDs are checked) and the cap without spending.
  2. Get the quote (`get_cost`) and read back the balance.
  3. Append an intent row to `ledger/presenter.jsonl`.
  4. Submit once.
  5. Append the done row with job ID and credits, taken from the transactions list.

No automatic retries. A rejection without a job ID, or an uncertain outcome, stops the lane until the owner decides. Record rejected items too.

## 5. Review the native take

Download it, probe it, do a full decode, and review a 1 fps contact sheet: identity, glasses, eyeline, hands, mouth closure, held frames. `experiments/EP009-FULL-BUILD-001/presenter-kit-test/compare.py` scores word timing against the narration and finds frozen runs.

## 6. Sync and deliver

The model's own audio is never delivered. The locked narration is the only program audio; picture is placed over it.

- **Offset only** when the native mouth timing already reads right. Measure where speech starts in the native clip and start the picture at that offset.
- **Otherwise run fal Sync:** `fal-ai/sync-lipsync/v3`, `sync_mode: silence`, with the generated video plus the exact audio slice. It goes through `oe-cinema generate --lane presenter`. First write a one-line `SYNC-NEED` naming the observed timing error.
- **Make it browser-safe:** H.264 High, yuv420p, 24 fps, audio stripped, not retimed or recropped. Full-decode and hash the result.

## 7. Disclosure

Generated presenter footage is illustrative performance, never evidence. Check YouTube's altered/synthetic disclosure on every upload that uses it. For Content OS, record the avatar as a reconstructed element in `provenance.json`.
