# Saved-C P01 calibration results

Status: `captured_technical_pass_creative_fail_revise`

| State | Result |
| --- | --- |
| Saved-C owner selection | exact local copy hash-matches v0.4 source; original C selected |
| Saved-C library save | exact local copy hash-matches v0.4 source; voice `scMbPZwQjr40V1MzL3Nj` |
| Voice ownership and consent | Manav Thaker confirmed as owner and consent owner in the bounded calibration-rights receipt |
| Provider-reported ownership | unreported in the R2 save response; not inferred |
| TTS calibration rights | owner-approved 24-hour authority was consumed before the first request; no reusable authority remains |
| Exact P01 identity | runtime-validated against canonical W `[0,139)` |
| Provider-neutral envelope | runtime-validated; one passage |
| ElevenLabs adapter | runtime-validated; saved C, `eleven_v3`, exact tags/settings |
| Hume entry | inert and schema-required only |
| Deterministic compilation | CLI-generated; request set `70ae263d4a2d843df2ab072179af63916b50de6cb2b8864c2255204d30f7d75d` |
| Primary Eleven scope | 2 calls; 1,684 characters; 2 native-PCM outputs |
| Absolute Eleven ceiling | 4 calls; 3,368 characters; 2 outputs; conditional MP3 fallback only |
| Frozen request set | `70ae263d4a2d843df2ab072179af63916b50de6cb2b8864c2255204d30f7d75d`; two fixed seeds |
| Provider execution | 2 calls; 1,684 transport characters; 2 native `pcm_48000` outputs; $0.1684 modeled |
| Fallback, retry, redirect | none |
| Provider-reported character-cost | 510 per request; 1,020 total; recorded separately from conservative authorization accounting |
| Corrected working masters | A and B `.v2.wav`; 48 kHz, 24-bit, mono PCM; strict full decode pass |
| First WAV wrappers | retained as failed evidence; explicitly superseded and ineligible for listening/scoring |
| Offline lexical diagnostic | A exact normalized 139/139 in beam and greedy; B is 131/139 in beam and 107/139 in greedy; no direction tags detected |
| Human exact-word gate | no candidate advances; B remains uncertain and its two ASR-flagged sentence regions were not explicitly cleared |
| Owner creative decision | reject both: both are flat, with no inflection or emotion |
| Selected candidate | none |
| Calibration-method verdict | creative `FAIL / REVISE`; both candidates are ineligible for advancement |

R2 selection and save permission were not reused as TTS permission. The calibration-specific
authority is consumed and cannot be replayed. Technical validation and offline ASR do not silently
advance this fixture to creative approval. The owner's rejection grants no new provider authority,
retry, pickup, or generation permission. Neither candidate may advance to long-form confirmation
or full-episode capture, and this result does not lock Step 2 or authorize Step 3, sharing, or
publication. Candidate B's lexical uncertainty remains recorded despite its independent creative
rejection.

## Frozen hashes

| Artifact | SHA-256 |
| --- | --- |
| Performance envelope | `36cc45786d2d1b8819d4f74fc284ca75e8c8ef87fdce0d55bcd78c41e03984b9` |
| ElevenLabs adapter | `3834fbd860ff8275e68f227929b31e382a813e7ff010551899bd82f2c8b22cb2` |
| Hume inert adapter | `92f9fa382c36ed500dc886c9e34616541e3e86d2550a69db251b52c6b14923f4` |
| Provider plan | `eb4acd6bb70f5e5d5f654298aa3fd2b9060cf8e6ef5dc8497a614521c51a707f` |
| Compiled dry run | `a7001dfd6e6e47c4790fee0208d3e01592cc068dfac4135128e53ba333b8a0dc` |
| Zero-authority draft | `8aa1614623204ce13aa9c2cbd9174f6fa27e21cd931ffecb65118fb8592ff0f4` |
| Owner-selection event record | `850b47a5419424fee37e9bff73a96b9e1da1c31feee13d20013869e4f3092702` |
| Saved-voice event record | `859b80a525d1d59ad531420f4c4ee496a0e41f6d91f0ee34ba895eb171dc7885` |
| Calibration-rights receipt | `5c46c6385f81ea8c15bf902957da7ba12ba6bf0313b7af23777dd031bafe5aa6` |
| Consumed active authorization | `b2bb22edf27860beac5c53b1b759fb0da6f8b970a26fb4905db2bc1ebd651978` |
| Authorization consumption | `740654672842741bf295b27c1d91b924bb5e9f3b1f1a9caeb5315eb14287c41b` |
| Provider run receipt | `c8305697c9468e0f3091241ef277dd32680f2a3c7bbdb18a8840173205594968` |
| Candidate A raw PCM | `d0faf8f9a577af44cb890721d817f9666e33387bd7a5bc99cabb5c963d44ec29` |
| Candidate B raw PCM | `2f899556dd1fd4c21da0aeb7944d764c987d1c9c56f014bfefd576777cacc244` |
| Candidate A nominated `.v2.wav` | `e7d01f1c443d6da19b5dbc5561ae2d133544241a81f90fc74345c0bd765e88d9` |
| Candidate B nominated `.v2.wav` | `8f0d66551035045b99bcd869f28ef71dd5093fe96d22ea1c6473c9bdbebba1ad` |
| Candidate A v2 conversion receipt | `e9e674d0429bae9ce6aa18c23b2a8cd0e99552f4360dbbba4de51fc886a9eeba` |
| Candidate B v2 conversion receipt | `8ed92001681fad30c3e802dbf52ac6428de06c88cec4a0f430e61e39dc1c2f52` |
| Invalid-wrapper disposition | `00b87099604e980fb378252059f0d9f245f19179426348609fe2d9b243c7ca8d` |
| Technical and lexical QA | `1525cfa862b3a924d53945a6546e8ef7ab674ebb9234004513ba928ab7999888` |
| Owner creative disposition | `de18e0f6384ddd09052d7df108b26348a350c79d2d7d66da46828aa9a17b5f01` |
