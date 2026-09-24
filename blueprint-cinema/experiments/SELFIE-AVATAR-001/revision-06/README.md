# R6 lip-sync correction candidate

[Watch the captioned R6 review version](https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/8a1c0bf7-4a89-4ca4-9b32-8c6f3949f1f2.mp4).

The owner reported that R5 lip sync was inaccurate intermittently. R5 remains
unchanged. This candidate rebuilds the lip sync independently for each of its
three continuous native picture sections, with exactly matched audio/video
lengths and cut_off duration handling. It preserves the full Original C voice,
script, home olive setting, existing expressions and highlighted Archivo style.

There were exactly three fresh Sync v3 submissions and no retries. All three
returned soundtracks match their source slices at zero measured insertion;
the prior 342.125 ms insertion is absent. The final edit uses one continuous
source WAV at zero, with 49,266 zero samples after the existing speech ends.
It preserves 1,293 frames, 24 fps, 720 × 1280 and 53.875 seconds. Captions are
rebased 342.125 ms earlier to the fresh voice clock, preserving all 184 words
and 49 cues. The caption render copies the clean output soundtrack exactly.

Final SHA-256: `cf0ef750eb1826cfb59063658620b287d9420f6d1171472dd90c4fcb6fd27fbb`.
Final size: 8,863,943 bytes. Hosted bytes were downloaded and verified.

DIAGNOSIS.json records why a blind global audio advance was rejected.
MATCHED-INPUTS.json and lip-sync/ASSEMBLY-EVIDENCE.json bind the exact source
segments and returned clocks. ASSEMBLY.json and AUDIO-QA.json bind the final
continuous waveform. captions/REPORT.json and TIMING-REBASE.json bind the
burn. DELIVERY.json records the final output and review limits.

The new version removes duration padding as a variable. It does not establish
a successful perceptual fix: sampled consonant closures are present, but
their relationship to approximate ASR word starts does not demonstrate a
clear improvement over R5. The tools did not provide reliable simultaneous
audio perception and video inspection. Owner playback judgment remains needed.
Do not call this accepted, locked, published or fully synchronized based on
technical checks alone, and do not start further generation blindly.
