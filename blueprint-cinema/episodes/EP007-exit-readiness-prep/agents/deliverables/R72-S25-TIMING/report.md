# R72 S25 timing and review-lead audit

**Keep S25 master [1101.5,1131.75): 726 frames / 30.25 seconds at 24 fps. Recommend review lead-in at master1093.166667, using accepted S24 frames [352,552).** That supplies200frames /8.333333seconds of context, including the complete aligned “Build means” phrase, and makes a926-frame /38.583333-second context. These are timing recommendations only; no render or source edit was performed.

All four source pins match live: locked script, transcript, master WAV and intentional-pause-map.

## Exact phrase windows

| Phrase | Master seconds | S25 local seconds | Nearest onset frame |
|---|---:|---:|---:|
| Here is the first move | 1101.660–1102.660 | 0.160–1.160 | 4 |
| and it costs you nothing | 1103.140–1104.440 | 1.640–2.940 | 39 |
| Write the checklist | 1106.640–1107.700 | 5.140–6.200 | 123 |
| Then find one owner | 1108.690–1110.130 | 7.190–8.630 | 173 |
| you already know | 1110.280–1111.660 | 8.780–10.160 | 211 |
| and run the diagnostic for free | 1111.680–1114.340 | 10.180–12.840 | 244 |
| Not to be generous | 1114.500–1115.580 | 13.000–14.080 | 312 |
| To start a stopwatch | 1116.700–1118.000 | 15.200–16.500 | 365 |
| Because at the end of it | 1119.040–1120.660 | 17.540–19.160 | 421 |
| you will know | 1120.760–1121.720 | 19.260–20.220 | 462 |
| the one number | 1121.800–1123.340 | 20.300–21.840 | 487 |
| this entire business turns on | 1123.360–1125.110 | 21.860–23.610 | 525 |
| and right now | 1125.660–1126.880 | 24.160–25.380 | 580 |
| nobody does | 1126.940–1127.640 | 25.440–26.140 | 611 |

All56 words, exact IDs, local/master onsets and ends, and nearest24fps onset frames are retained in `cues.json`. Key interior onsets (local): Write5.140; checklist5.600; one8.080; owner8.360; already9.040; know9.540; run10.400; diagnostic10.700; free11.600; start15.340; stopwatch15.800; at17.780; end18.120; know19.620; one20.580; number21.160; right24.340; now24.560; nobody25.440; does25.790. Final aligned word ends26.140.

## Review lead that avoids clipping the phrase

The aligned “Build” starts1093.400, but substantial original waveform activity occurs earlier, beginning within1093.208333–1093.250. Cutting at1093.25 would start near−1970 in PCM16 amplitude, well above the local noise floor. The1093.375 sample is closer to zero, but is immediately followed by strong speech and would discard that earlier activity. Neither is as conservative as1093.166667.

The chosen frame26236 has RMS32.632 /32768 (about−60.0dBFS), peak87. Adjacent boundary samples are70 |71; this is low energy, **not digital silence**. It starts233.333ms before the aligned “Build,” preserving the earlier rise in activity. PCM alone does not identify every sound as breath versus phoneme, so this is a source-preserving timing judgment rather than a listening verdict. It does not promise preservation of the whole preceding intake.

Exact review assembly: S24 [352,552), then S25 [0,726). Review audio is one continuous master interval [52472000,54324000) at48kHz. S25 begins at contextframe200 /8.333333seconds. No word or pause needs to be removed or retimed.

## Outgoing cut and retained pause

The pause map explicitly retains1127.64–1131.84 after W003165 “does”:4.2seconds /201600samples. This is an aligned gap with low-level source noise and activity preceding the next aligned word, not4.2seconds of digital zero. Keep the entire source interval.

S25's1131.75 outpoint is in the low-energy region before the sharp increase in the1131.791667–1131.833333 frame. Samples across the proposed cut are−16 |−25 in PCM16; the following frame's RMS is28.910 (about−61.1dBFS), whereas the next frame rises to3402.483. “If” is aligned at1131.840. The cut therefore leaves90ms before the next aligned word and preserves its earlier sound with S26. This cut is **not silent**.

Picture ownership splits the4.2-second gap into4.11seconds at the end of S25 and90ms at the start of S26. That is not a shortened gap. The last S25 frame begins1131.708333 and ends1131.75. S25 audio is exactly [52872000,54324000):1452000samples at48kHz. `endpoint-audio.json` contains both candidate-lead comparisons, outgoing24fps bins, exact boundary samples and retained-pause evidence.

## Readable hold recommendations

Three timing movements are sufficient:

1. **First move, frames0–123 /0–5.125seconds.** Let the opening instruction land and preserve the full2.2-second pause after “nothing” (local2.940–5.140). Keep a purposeful held picture rather than filling that pause with extra claims.
2. **Checklist and one known owner, frames123–365 /5.125–15.208333.** Add the checklist at frame123; known-owner step near173; diagnostic step near250. Keep the earlier steps present as later steps arrive. Clearing “Write the checklist” at “Then” would allow only about2.08seconds; a cumulative composition allows roughly10seconds to read the instruction. The explicit free qualifier should be visible with the diagnostic instruction.
3. **Measure the work, frames365–726 /15.208333–30.25.** This gives15.041667seconds for the stopwatch purpose and the unanswered number. “Start” aligns near368, “stopwatch”379, “Because”421. Preserve the1.04-second pause after “stopwatch.” The final unknown should remain through the4.11-second S25 portion of the retained ending pause; do not insert an invented measured result.

Timing does not establish a measurement outcome. A ticking clock would be illustrative, not observed delivery time; avoid a completed elapsed-time value or an85-hour result. If the prior85-hour assumption is recalled, it must stay an assumption. The owner's free diagnostic is an initial measurement exercise, not proof of demand or a reliable population estimate. These are interpretation boundaries, not additions to the locked narration.

No continuous normal-speed listening, visual build, render, provider call, shared-file/log edit, gate action or owner-acceptance claim occurred. Root owns final picture direction and playback.
