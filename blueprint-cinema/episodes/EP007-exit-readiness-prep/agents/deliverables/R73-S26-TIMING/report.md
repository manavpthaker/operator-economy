# R73 S26 final-line timing audit

**Use149picture frames from master1131.75 to1137.958333. Keep all296519remaining master samples; add1481zero samples after EOF if matching audio length to picture.** The extra30.854167ms follows the exact source ending and does not alter narration. All four input pins match live files.

## All20word cues

| Word | ID | Master seconds | S26 local seconds | Nearest onset frame |
|---|---|---:|---:|---:|
| If | W003166 | 1131.840–1131.920 | 0.090–0.170 | 2 |
| you | W003167 | 1131.980–1132.060 | 0.230–0.310 | 6 |
| want | W003168 | 1132.100–1132.270 | 0.350–0.520 | 8 |
| more | W003169 | 1132.300–1132.520 | 0.550–0.770 | 13 |
| blueprints | W003170 | 1132.540–1132.980 | 0.790–1.230 | 19 |
| taken | W003171 | 1133.020–1133.200 | 1.270–1.450 | 30 |
| apart | W003172 | 1133.240–1133.480 | 1.490–1.730 | 36 |
| like | W003173 | 1133.520–1133.700 | 1.770–1.950 | 42 |
| this | W003174 | 1133.740–1133.910 | 1.990–2.160 | 48 |
| one, | W003175 | 1133.960–1134.420 | 2.210–2.670 | 53 |
| including | W003176 | 1134.460–1134.910 | 2.710–3.160 | 65 |
| the | W003177 | 1134.940–1135.040 | 3.190–3.290 | 77 |
| parts | W003178 | 1135.080–1135.370 | 3.330–3.620 | 80 |
| that | W003179 | 1135.380–1135.490 | 3.630–3.740 | 87 |
| do | W003180 | 1135.500–1135.550 | 3.750–3.800 | 90 |
| not | W003181 | 1135.620–1135.770 | 3.870–4.020 | 93 |
| survive | W003182 | 1135.820–1136.160 | 4.070–4.410 | 98 |
| the | W003183 | 1136.220–1136.280 | 4.470–4.530 | 107 |
| arithmetic, | W003184 | 1136.320–1136.840 | 4.570–5.090 | 110 |
| subscribe. | W003185 | 1137.320–1137.750 | 5.570–6.000 | 134 |

These are locked forced-alignment timestamps; source PCM can begin before an aligned onset and extend beyond an aligned end. No spoken word or pause should be retimed to match the nearest frame.

## Exact EOF and frame arithmetic

The mono48kHz PCM16 master contains54620519samples, ending at1137.927479166667. S26 begins at sample54324000, masterframe27162 /1131.75. Its296519source samples last6.177479166667seconds.149frames equal298000samples /6.208333333333seconds, so exactly1481additional zero samples /30.854166667ms align its audio stream with the picture endpoint. Padding is a derived output choice, not an edit to the locked master.

The last nonzero original sample is index54619774 at1137.911958333333. The remaining744source samples are zero. The final picture frame starts at1137.916667: it contains519original zero samples plus1481post-EOF zero samples, making one entirely silent final frame. Every original sample is preserved.

The148-frame alternative would end at1137.916667 and omit519original zero samples /10.8125ms. It would not truncate a nonzero sample, but149frames is the conservative full-source option and is recommended. The149-frame picture endpoint is masterframe27311 /1137.958333. Hold the final picture through that frame; no fade is required to solve a nonexistent audio-tail problem.

## Complete-clause review lead

Recommend master1125.25 /frame27006, using accepted S25 frames [570,726). This is156frames /6.5seconds before S26. It includes the complete “and right now nobody does” clause (1125.66–1127.64), followed by the full recorded4.2-second aligned gap before “If” at1131.84. The accepted diagram is already settled at this entry, so its blank diagnostic-time record supplies the referent for “nobody does.”

The proposed lead boundary is low energy: adjacent PCM16 samples−24 |−17; the following frame has RMS65.356 /32768, about−54.0dBFS. It starts410ms before the aligned “and,” before the stronger activity leading into that word. This avoids cutting at1125.625, immediately before stronger speech. There is no digital-silence span here; the timing and energy support a complete-clause cut but do not prove the identity or completeness of every breath without listening.

Context assembly: S25 [570,726) plus S26 [0,149) =305frames /12.708333seconds. S26 begins at contextframe156 /6.5seconds. Original context audio is [54012000,54620519),608519samples, then1481zero samples if padded to the610000samples corresponding to305frames. The source remains continuous at1131.75.

The longer “Because at the end…” lead would require about12.71seconds before S26 and adds information already visible in the accepted diagram. It is unnecessary for the requested6–10second context.

## Pause and reading holds

Keep all4.2seconds after S25's “does”:4.11seconds remain under the accepted S25 picture and90ms precede aligned “If” under S26. Source energy rises before the1131.84alignment, so retain the1131.75scene start rather than cutting at the first word. The transition is low energy, not digital silence.

The invitation lasts only6.208333seconds. “Subscribe” begins at local5.570 and ends6.000; revealing essential invitation copy only on that word leaves about638ms to the picture end, or about388ms after a six-frame reveal. Make the invitation readable earlier and let the spoken “subscribe” land on an established, settled frame. Preserve the480ms pause after “arithmetic,” local5.090–5.570. Avoid adding a second late movement that competes with the final word or obscures the tail.

No render, provider call, shared source/log edit, canonical mutation or creative acceptance occurred. No continuous normal-speed listening verdict is claimed. `endpoint-audio.json` records exact sample counts, candidate lead boundaries, scene-entry bins and final partial-frame evidence.
