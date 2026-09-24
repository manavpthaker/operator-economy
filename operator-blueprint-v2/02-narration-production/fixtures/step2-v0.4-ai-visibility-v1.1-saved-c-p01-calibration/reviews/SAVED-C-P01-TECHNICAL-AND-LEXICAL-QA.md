# Saved-C P01 technical and lexical QA

Status: **technical PASS for private owner audition.** Creative approval and the human exact-word
gate remain pending; candidate B has an unresolved offline-ASR discrepancy.

## Capture and conversion

The consumed authorization produced exactly two native `pcm_48000` candidates: two calls, 1,684
authorized transport characters, two outputs, no fallback, no retry, and no redirect. The provider
run receipt is SHA-256 `c8305697c9468e0f3091241ef277dd32680f2a3c7bbdb18a8840173205594968`;
the preceding consumption record is SHA-256
`740654672842741bf295b27c1d91b924bb5e9f3b1f1a9caeb5315eb14287c41b`.

The first WAV wrappers were malformed local conversion artifacts and are excluded by
`AUTH-SC-P01-20260825T145935Z-invalid-pipe-wav-disposition.json`. The immutable raw PCM was not
changed and ElevenLabs was not called again. Only these corrected files are eligible for review:

| Candidate | Raw SHA-256 | Nominated WAV SHA-256 | Conversion receipt SHA-256 | Duration | Integrated loudness | LRA | True peak | Strict decode |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| A | `d0faf8f9a577af44cb890721d817f9666e33387bd7a5bc99cabb5c963d44ec29` | `e7d01f1c443d6da19b5dbc5561ae2d133544241a81f90fc74345c0bd765e88d9` | `e9e674d0429bae9ce6aa18c23b2a8cd0e99552f4360dbbba4de51fc886a9eeba` | 52.72 s | -19.13 LUFS | 3.60 LU | -1.28 dBTP | pass |
| B | `2f899556dd1fd4c21da0aeb7944d764c987d1c9c56f014bfefd576777cacc244` | `8f0d66551035045b99bcd869f28ef71dd5093fe96d22ea1c6473c9bdbebba1ad` | `8ed92001681fad30c3e802dbf52ac6428de06c88cec4a0f430e61e39dc1c2f52` | 48.32 s | -18.35 LUFS | 3.70 LU | -0.64 dBTP | pass |

Both nominated files are mono 48 kHz, 24-bit PCM WAVs, mode `0600`, with normal RIFF/data sizes.
Strict full-file decoding exits `0`. Decoding each back to signed 16-bit PCM reproduces the exact
immutable raw SHA-256. Neither has a full-scale clipped sample, material DC offset, flatlining, or
a machine-detected dropout.

Candidate B is about 4.4 seconds faster and approximately 0.8 LU louder. Its final word has a
tighter tail than A: truncation was not detected, but the ending deserves an explicit owner listen.

## Offline lexical diagnostic

Four credential-free local Whisper Small English passes were run with no initial prompt: default
beam and greedy/no-fallback, once for A and once for B. Normalization used lowercase
alphanumeric/apostrophe tokens against the locked 139-token P01 text.

| Candidate | Decoder | Normalized tokens | Edit distance | Diagnostic result |
| --- | --- | ---: | ---: | --- |
| A | default beam | 139 | 0 | exact normalized match |
| A | greedy/no-fallback | 139 | 0 | exact normalized match |
| B | default beam | 131 | 8 | omitted `That missing view is where this business starts.` |
| B | greedy/no-fallback | 107 | 32 | omitted that 8-token sentence plus the 24-token `One experienced operator ... deserves action.` sentence |

No pass detected the direction words `curious`, `sarcastic`, `excited`, or `warmly`. Both B passes
still ended with **“Let’s work that out.”**

This conflict is unresolved evidence, not proof that B changed or omitted the spoken words. It may
be an ASR miss, but B cannot receive an exact-word PASS from automation. The owner must listen for
both omitted-sentence regions, all 139 words, the six critical tokens `2022`, `may`, `one`, `can`,
`before`, and `whether`, any faint spoken direction tag, and B's final “out” decay.

## Owner decision still required

Listen without music or visuals and decide:

1. Confirm candidate B includes both sentences flagged by offline ASR; reject it if either is
   actually missing.
2. Does either take retain recognizable Manav identity while adding the intended camera-ready
   energy?
3. Do curiosity, dry irritation, consequence, and the payoff tease land without an announcer or
   motivational cadence?
4. Prefer A, prefer B, or reject both?

Neither technical QA nor offline ASR grants creative approval, full-episode capture, Step 2 lock,
Step 3, sharing, or publication.
