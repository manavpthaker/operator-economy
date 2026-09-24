# R71 S24 timing audit

**Retain master [1078.5,1101.5): 552 frames / 23 seconds at 24 fps.** Master frame range [25884,26436); PCM sample range [51768000,52872000). The issued script, word-transcript and master WAV hashes match live files. Narration is unchanged.

## Phrase windows

| Phrase | Master seconds | S24 local seconds | Nearest onset frame |
|---|---:|---:|---:|
| My verdict is build | 1079.060–1080.740 | 0.560–2.240 | 13 |
| Not because this is proven | 1081.840–1083.020 | 3.340–4.520 | 80 |
| because it is not | 1083.520–1084.620 | 5.020–6.120 | 120 |
| Nobody in my research | 1085.300–1086.520 | 6.800–8.020 | 163 |
| had run this practice | 1086.530–1087.540 | 8.030–9.040 | 193 |
| and published what it earns | 1087.550–1088.720 | 9.050–10.220 | 217 |
| The base case in my own model | 1089.230–1090.780 | 10.730–12.280 | 258 |
| does not clear | 1090.840–1091.500 | 12.340–13.000 | 296 |
| the number I set for it | 1091.540–1092.659 | 13.040–14.159 | 313 |
| Build means | 1093.400–1094.690 | 14.900–16.190 | 358 |
| this is worth constructing carefully enough to find out | 1094.720–1097.910 | 16.220–19.410 | 389 |
| and I have told you | 1098.660–1099.600 | 20.160–21.100 | 484 |
| the two things that would end it | 1099.640–1101.000 | 21.140–22.500 | 507 |

The complete word-level data, including exact word IDs, onset/end times and nearest 24 fps onset frames, is in `cues.json`. Onset frame quantization is an editing aid, not a change to the aligned audio.

Key interior word onsets (local seconds): build 1.880; proven 4.160; second not 5.860; research 7.560; run 8.260; published 9.240; earns 9.940; base 10.860; model 11.980; does 12.340; not 12.580; clear 12.780; number 13.140; set 13.640; worth 16.600; constructing 16.940; carefully 17.760; find 18.900; out 19.240; two 21.280; things 21.520; end 22.140; final it 22.340.

## Cut and source-audio evidence

The last aligned “it” ends at master 1101.000, local 22.500. Its PCM tail ends later: the last nonzero sample before the cut is 52852418 at 1101.092041667. A continuous digital-zero run then spans samples [52852419,52875121), master [1101.0920625,1101.565020833). The proposed 1101.5 cut lies inside that 472.958 ms zero run, 65.021 ms before subsequent nonzero source activity. Both samples directly adjacent to the cut are zero.

S25 “Here” is aligned at 1101.660, 160 ms after the cut; substantial source energy begins earlier than the word timestamp. Assigning S25 the original audio from 1101.5 preserves its preceding intake/activity. The final full frame of S24 begins at 1101.458333 and ends exactly at 1101.5. There is no reason to move the cut to the word boundary or shorten the source. `endpoint-audio.json` records every original 24 fps PCM bin around the cut and the exact zero-run evidence.

The incoming 1078.5 boundary is the accepted S23 endpoint. Unlike this outgoing cut, the incoming boundary is a low-energy nonzero valley; this report does not relabel it as digital silence.

## Three timing movements

These are timing recommendations for root's direction, not implemented animation or creative approval. They can be changes within one persistent composition.

1. **Verdict and qualification, frames 0–163 / local 0–6.791667.** Establish the verdict frame; reveal “Build” near its spoken onset at frame 45 / 1.875. A compact “Unproven” qualification can enter at frame 80 / 3.333333 on “Not because,” giving 3.458333 seconds before the next movement. Do not reveal a bare “Proven” and negate it later. Preserve the 1.10-second spoken pause after the first “build.”
2. **Why it remains unproven, frames 163–358 / local 6.791667–14.916667.** Introduce the research limit with “Nobody,” then add the personal model's shortfall near frame 258 / 10.750. If both lines remain, the first has 8.125 seconds and the second 4.166667 seconds before the definition. Keep “in my research” and “my own model / my target” attached to their respective statements; neither is a universal market verdict.
3. **What build means, frames 358–552 / local 14.916667–23.** Allow 8.083333 seconds for the practical definition. A six-frame reveal would leave 7.833333 seconds settled. “Find out” finishes at local 19.410, followed by a 750 ms pause before “and.” Preserve that pause. The phrase “two things” starts only at local 21.280, leaving 1.72 seconds until the cut. A short reminder such as “2 stop conditions” can fit; two new explanatory cards cannot be read responsibly in that remaining time. If the full conditions must return, establish them earlier in this last movement, or keep the full explanation in its already accepted S21 passage.

## Meaning limits relevant to timing

“Build” means worth constructing carefully enough to learn; it is not demonstrated viability. The research sentence concerns what the narrator found, not proof that nobody anywhere operates such a practice. The base case misses the narrator's chosen target; it does not prove that every possible model fails.

If either kill condition is repeated, preserve S21's OR logic: owner agreement followed by deferral **or** brokers already supplying the work free in the relevant market. They are unverified conditions, not two observed findings, and the sequence must not imply both are required.

No visual build, render, provider call, shared-file edit, log update or acceptance action was performed. No continuous normal-speed listening verdict is claimed; the cut recommendation is supported by exact transcript and PCM evidence.
