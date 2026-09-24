# R70 S23 payoff timing audit

**Recommend S23 master[1068.9166666666667,1078.5000000000000):230frames /9.583333seconds at24fps.** Start at the owner-locked S22 outpoint, frame25654; end at frame25884. Preserve original audio continuously. All three issued input hashes match.

## Exact S23 cues

| Cue | Word ID | Master | Local from1068.916667 |
|---|---|---:|---:|
| “There” |W003016|1069.300|0.383333|
| “it is” ends |W003018|1069.780|0.863333|
| “The work in the pause” starts |W003019|1070.260|1.343333|
| “work” |W003020|1070.440|1.523333|
| “pause” starts |W003023|1071.220|2.303333|
| “pause” ends |W003023|1071.639|2.722333|
| “And now” starts |W003024|1072.660|3.743333|
| “honestly” |W003030|1073.920|5.003333|
| “costs” |W003031|1074.460|5.543333|
| “roughly” |W003035|1075.980|7.063333|
| “charge” |W003040|1076.940|8.023333|
| “worth” |W003043|1077.600|8.683333|
| “doing” starts |W003044|1077.880|8.963333|
| Final aligned word end |W003044|1078.120|9.203333|

The first two sentence gaps are part of the performance:480ms after “There it is” and1.021s after “pause.” Keep them. The full final sentence runs1072.660–1078.120. `cues.json` contains every word, not just these anchors.

## Why1078.5 is the outpoint

The final aligned word ends1078.12, but original PCM remains audible in its tail. The proposed cut retains380ms after that alignment. Frame1078.458333–1078.500000 is the lowest local-energy bin: RMS1.906 and peak9 in16-bit PCM, about−84.7dBFS. Samples directly across the boundary are0 |0. This is a near-zero valley, **not a stretch of digital silence**: the preceding frame has1,339nonzero samples.

Low-level activity rises in the following1078.500000–1078.541667 frame and becomes substantial by1078.625–1078.708333, consistent with preparation/intake for the next sentence. S24's aligned “My” begins1079.06; actual speech energy is already present by1079.0. Starting S24 at1078.5 keeps that pre-word activity with its line and avoids making an edit at the aligned word onset. PCM energy alone does not prove the physical cause of every residual, so this remains a reasoned cut recommendation requiring normal-speed listening rather than a claimed listening verdict.

## S24–S26 planning only

| Section | Word range / speech | Proposed source range | Frame count |
|---|---|---|---:|
| S24 verdict |W003045–W003109;1079.06–1101.00|1078.50–1101.50|552 /23.00s|
| S25 first action |W003110–W003165;1101.66–1127.64|1101.50–1131.75|726 /30.25s|
| S26 close |W003166–W003185;1131.84–1137.75|1131.75–1137.9274791666667 source end|6.177479s source; see delivery note|

S24/S25 boundary1101.5 is in verified digital silence. Full frame bins1101.125–1101.541667 are zero; next intake appears within1101.541667–1101.583333.1101.5 leaves one silent frame before the intake.

The4.2-second gap after S25's “does” (1127.64–1131.84) is explicitly retained in the **intentional-pause-map**, after W003165. It contains low-level source noise rather than digital zero. Preserve it; the proposed1131.75 boundary assigns most of that hold to S25 while cutting before S26's speech energy appears in1131.791667–1131.833333. This boundary is low energy, not silent. Different picture ownership of that pause is an editorial choice; shortening locked audio is not part of this audit.

The exact master duration is1137.9274791666667, from54,620,519sample frames at48kHz; transcript metadata rounds it to1137.927. The last nonzero sample is54,619,774 at1137.9119583333334. Everything after it is zero. The148-frame S26 endpoint1137.916667 would discard519samples/10.8125ms of trailing digital silence; the conservative source-preserving option is to retain the full master and let a149-frame picture window end at1137.958333,30.854167ms after audio EOF. That last delivery choice is for root; neither requires altering spoken audio.

## Limits and handoff

No new visual direction, media generation, source edit, shared log or gate was performed. Actual normal-speed listening and the S23 image choice remain with root. `endpoint-audio.json` records original24fps-aligned PCM bins, boundary samples and exact final-master duration. `deliverable.json` binds all sources. S24–S26 ranges are planning recommendations, not locked cuts or creative approval.
