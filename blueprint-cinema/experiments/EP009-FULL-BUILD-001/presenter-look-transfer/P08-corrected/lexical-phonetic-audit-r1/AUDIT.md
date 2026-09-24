# P08A lexical and acoustic timing audit

The earlier **4.60–4.66 s “I” is not a reliable phonetic boundary**. Both full-context ASR runs assign that ordinary offset, but cropped-context ASR moves it to 4.88–4.92 s. Three explicitly enabled DTW runs converge on an approximate “I” token event at 4.92–4.94 s and “know” at 5.08–5.10 s. No transcript prompt was supplied.

| Approximate token event | Full small.en | Full medium.en | Cropped medium.en, global time |
|---|---:|---:|---:|
| I | 4.92 | 4.94 | 4.93 |
| know | 5.08 | 5.10 | 5.09 |
| this | 5.30 | 5.28 | 5.27 |
| business | 5.58 | 5.60 | 5.65 |
| out | 6.84 | 6.90 | outside crop |

The unchanged waveform and spectrogram show low-energy interphrase activity followed by strong periodic voicing around 4.81 s. RMS at 4.60–4.68 s is −46.12 dBFS, versus −19.81 dBFS at 4.81–4.94 s. This does not positively identify a quiet “I” at 4.60 s. **Low RMS is not proof of silence.**

DTW is not a phoneme boundary: the installed whisper.cpp header describes an experimental, approximate moment when a token was output. The small model collapses two earlier tokens to one event, demonstrating a limitation. The three related-model runs corroborate the later location without providing independent phonetic ground truth.

The pause picture is a reasonable comparison candidate; its later wide-to-narrow sequence must be judged as motion, not passed because its maximum matches a DTW timestamp. Natural anticipatory articulation remains a plausible competing explanation for the original picture. Precise /aɪ/ and /noʊ/ boundaries and final perceptual sync remain unresolved. No audio listening or normal-speed audiovisual review is claimed.

The bound JSON retains all input/result/tool/model hashes, crop and ASR commands, complete token events, acoustic evidence, and exact PCM identity with r3 master samples [31840000,32186000). Only diagnostic copies were resampled. No narration, failed gate, selection, or acceptance was changed; no paid call was made.
