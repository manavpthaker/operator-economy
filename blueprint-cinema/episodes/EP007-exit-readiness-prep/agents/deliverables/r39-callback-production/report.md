# R39 corrected callback production

Both authorized calls succeeded, with no retries. The callback now says **“Back to his question, then.”** The native media and every derivative remain in this owned packet. No runtime, master narration, skill, decision log, or canonical state file was edited.

## Delivery

- `context-guide.wav`: the single Google Algieba / Gemini 2.5 Pro TTS / candidate-C4 contextual read, 10.051 seconds at 24 kHz.
- `context-original-c.wav`: the single ElevenLabs Original C voice transfer, 10.077 seconds at 48 kHz, mono signed 16-bit PCM WAV.
- `callback-only.wav`: exact native PCM samples **0–86,000**, half-open, **1.791667 seconds / 43 frames at 24 fps**. No signal changes.
- `callback-level-matched.wav`: separate derivative of that cut at **−2.56 dB**. No retiming or fades. This is a starting level for seam listening, not a claim of perceptual matching.

Integrate the callback into S08 local **0–1.791667**, review **247.625–249.416667**, corresponding to the replaced original source interval **250.625–252.416667**. Keep original question audio from master 252.416667 onward. No timing extension is needed. The new “Back” begins earlier within that slot than the old recording; the accepted prefix itself remains untouched. Root should judge that new sentence entrance against the previous line while checking the level.

## Word and boundary checks

Local `whisper-cli` with the downloaded open Whisper tiny.en model independently transcribed the cropped callback as **“back to his question then.”** In the cropped recognition, “then” spans approximately 1.20–1.49 seconds. Signal energy falls below −48 dB around 1.5803 seconds and remains there until the following “What” begins around 2.2228 seconds in the uncut contextual take. The 1.791667-second endpoint is inside that pause and includes the complete callback.

The full contextual guide's end was marginal on the capture helper's tail test (0.023 against a 0.02 threshold). Its voice transfer ends cleanly (0.0001). Only the first sentence is used, and the callback boundary is independently clear. The contextual question and small-talk recordings are discarded from the edit; the locked original question remains the avatar audio.

The unadjusted callback measures approximately 2.56 dB louder than the replaced callback using 20 ms RMS windows above −35 dBFS. Whole-slot RMS differs by 3.92 dB, partly because the new sentence has less leading silence. The gain derivative uses the gated comparison. Source-level and recognition checks do not prove timbre, naturalness, or seam quality; listen with the original neighboring narration before final selection.

## Cost and receipts

Google returned HTTP 200. Using the approved rates and conservatively treating every input character as one input token, the computed cost is approximately **$0.00609**, below the **$0.05** cap. The response contains no invoice; this remains a calculation.

ElevenLabs returned HTTP 200 and **`character-cost: 122`**, below the **250-credit** cap. Request ID: `G409UPJpmoJnc8h5ungz`. The immediate account count did not change, so the exact response cost header is the billing evidence; the zero account delta must not be reported as zero cost.

Before submission, live account and voice metadata confirmed the selected generated voice, `OE Narrator Manav C Base v1`, with no library sharing. Official documentation identifies custom multipliers with shared Voice Library voices, which generated voices cannot be. The standard 1,000-credit/minute rate therefore supplied a conservative preflight ceiling of 168 credits. The API did not expose a numeric multiplier field; `TRANSFER-COST-DECISION.json` records the inference explicitly. Exact response billing was lower.

## Manifest exception

The standard agent-deliverable schema hardcodes `external_writes`, `paid_services`, and `synthetic_generation` to false. This issued work order explicitly authorizes those actions. The packet records truthful true values and includes a local schema copy permitting those three values; the shared schema is untouched. The base-schema mismatch is documented in `SCHEMA-EXCEPTION.json`, not hidden as a pass. All other standard manifest structure and input-pin checks pass.
