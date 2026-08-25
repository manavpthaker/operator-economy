# AUTH-R4 technical QA

Status: `PASS_FOR_OWNER_AUDITION`

Creative selection: pending

## Bound result

- Authorization SHA-256: `720021e51008b295694036c1b4f441143cfcc6851812e231ae27ae7d4b5a6d23`
- Consumption SHA-256: `c6a3805667b5324bba52eef9e52b50ed5a8ea897063cfa78d91cdf1079dba79c`
- Preview receipt SHA-256: `0b30f3fe6ca24a1c2ecd574a66ea9245e46b33f52bfa00b8dcfaffe18279f92e`
- Source voice: `scMbPZwQjr40V1MzL3Nj`
- Exact prompt characters: `440`
- Exact preview-text characters: `570`
- Provider calls: `1`
- Returned previews: `3`

The authorization was consumed before the network request. The provider returned three previews;
the runtime preserved all three, selected none, saved none, and did not modify the source voice.

## Media checks

| File | SHA-256 | Duration | Codec | Loudness | True peak | Full decode |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `preview-01.mp3` | `7ec3d22e4e189003f59e83488d0189746c16d525b488bf25e2c3717143043978` | 40.124 s | mono MP3, 44.1 kHz, 192 kbps | -20.46 LUFS | -1.38 dBTP | pass |
| `preview-02.mp3` | `5753f45fc8216cac98fa72e74aa60f71503309c1ab87fd0ca49e7b9e271539c0` | 40.281 s | mono MP3, 44.1 kHz, 192 kbps | -20.37 LUFS | -2.27 dBTP | pass |
| `preview-03.mp3` | `c13f0b903bb7bb69518e7257882dc6ef9e296b2f44f909b5ade98f7b17d32c61` | 40.359 s | mono MP3, 44.1 kHz, 192 kbps | -20.79 LUFS | -2.70 dBTP | pass |

The media hashes and byte counts match the immutable provider receipt. All files are owner-only
mode `0600`. Their loudness differs by only `0.4` LU, so no additional lossy normalization was
introduced for the owner listen.

## Boundary

This is a technical pass for private audition only. It does not establish lexical fidelity,
creative preference, long-form continuity, production suitability, or approval of any candidate.
No replay, save, TTS generation, full capture, Step 2 lock, Step 3, sharing, or publication is
authorized.
