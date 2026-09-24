# EP007 Short 01 Original C salvage v1

## Result

`short01-final-original-c-salvage-v1.wav` is an isolated, lossless-prefix salvage of the Original C transfer. It keeps the locked 149-word script once and removes the repeated final 28-word passage by ending inside the quiet gap before the repetition.

This fixes only the duplicate. The salvage is `57.666667s`, still `13.820257s` longer than the locked `43.846410s` animatic. It is not a timing fix, owner acceptance, release approval, or permission to modify the animatic.

## Identity

| Item | SHA-256 | Duration | Format |
|---|---|---:|---|
| Source `../media/short01-final-original-c.wav` | `c90848bdfa3e0655eaa7cfa1595e351455a902e2df47456f5e898174e47bc851` | `67.6629375s` | 48 kHz, mono, PCM signed 16-bit LE |
| Salvage `short01-final-original-c-salvage-v1.wav` | `b4ab3903255b5b425f2adc88f81372f7072efc58eb842830c6dd600dc188d61c` | `57.666666667s` | 48 kHz, mono, PCM signed 16-bit LE |
| Locked script `../SCRIPT.txt` | `94988c28ca3aee85f14737e9214d63267c3aa1e7d91dc5deeb9e9a5d37dab2e2` | 149 words | exact-copy authority |
| Locked animatic `../../index.html` | `857723990ec48d6743dd2ea4e44b9456bfd8ece02851b8494b350a8e2833bdaa` | `43.846410s` | untouched |
| Locked timing `../../index.motion.json` | `1988229b8c3f1d3e2bdaac0f945db3ad8f63fed0abbc3f3e908f416834d14d4a` | `43.846410s` | untouched |

## Cut decision

- Kept source samples: `[0, 2,768,000)`.
- End: sample `2,768,000` = `57.666666667s` = frame `1,384` at the project’s 24 fps (`2,000` audio samples per frame).
- The first retained reading settles below -30 dBFS at `57.022917s`. The output therefore carries `0.643750s` of natural quiet after the final word.
- The duplicated reading has its strong waveform onset at approximately `58.09s`; the cut is about `0.423s` earlier.
- The last included source sample measures `-66.786908 dBFS`; the first excluded sample measures `-67.386173 dBFS`. The boundary is effectively quiet, so no fade or crossfade was added.
- Removed: `479,821` samples / `9.996270833s`.
- Existing local lexical evidence in `../VOICE-FIT-GATE.json` establishes that the first pass contains every locked word in order and that only the final 28-word passage repeats. Because this salvage is one contiguous prefix with no internal edit, it retains that complete first pass and excludes the later repetition.

The repeated passage is:

> The bigger question is whether an owner would pay someone to clear that map before a buyer appears. The full episode shows you how to build the service.

## Verification

- Strict FFmpeg decode: pass.
- Decoded PCM SHA-256 of `source -> atrim [0, 2,768,000)`: `1cb78be77ddbc69b6e4e6edf4b17b0b0b2d2cd3c4ca943cefbe7490084312ddd`.
- Decoded PCM SHA-256 of the salvage file: `1cb78be77ddbc69b6e4e6edf4b17b0b0b2d2cd3c4ca943cefbe7490084312ddd`.
- Exact PCM identity: pass. FFmpeg did not alter any retained sample.
- Output tail at `-30 dBFS`, minimum `80ms`: `57.022917–57.666667s` (`0.643750s`).
- Diagnostic output loudness, with no normalization applied: `-15.87 LUFS`, `-0.34 dBTP`, `3.10 LU` LRA.
- `source-boundary-waveform.png` visualizes source `56.5–58.5s`; the amber line is the cut at `57.666667s`. The retained first ending is left of the line; the duplicated restart is the large waveform to its right.
- `salvage-full-waveform.png` visualizes the complete output.

## Exact commands

Working directory for every command:

```text
/Users/brownmanbrain/GitHub/operator-economy
```

Create the master:

```bash
ffmpeg -hide_banner -nostdin -y -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/media/short01-final-original-c.wav -map_metadata -1 -af "atrim=start_sample=0:end_sample=2768000,asetpts=N/SR/TB" -c:a pcm_s16le -ar 48000 -ac 1 -fflags +bitexact -flags:a +bitexact studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/short01-final-original-c-salvage-v1.wav
```

Probe and strict-decode the output:

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate:stream=index,codec_name,sample_fmt,sample_rate,channels,bits_per_sample,duration -of json studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/short01-final-original-c-salvage-v1.wav
ffmpeg -hide_banner -nostdin -v error -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/short01-final-original-c-salvage-v1.wav -f null -
```

Verify retained PCM identity:

```bash
ffmpeg -hide_banner -nostdin -v error -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/media/short01-final-original-c.wav -af "atrim=start_sample=0:end_sample=2768000" -f hash -hash sha256 -
ffmpeg -hide_banner -nostdin -v error -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/short01-final-original-c-salvage-v1.wav -f hash -hash sha256 -
```

Measure the final silence:

```bash
ffmpeg -hide_banner -nostdin -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/short01-final-original-c-salvage-v1.wav -af "silencedetect=noise=-30dB:d=0.08" -f null -
```

Inspect the two samples around the chosen boundary:

```bash
ffmpeg -hide_banner -nostdin -v info -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/media/short01-final-original-c.wav -af "atrim=start_sample=2767999:end_sample=2768001,asetpts=PTS-STARTPTS,asetnsamples=n=1:p=0,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.Peak_level" -f null -
```

Measure diagnostic loudness without changing the file:

```bash
ffmpeg -hide_banner -nostdin -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/short01-final-original-c-salvage-v1.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null -
```

Render waveform evidence:

```bash
ffmpeg -hide_banner -nostdin -y -ss 56.5 -t 2.0 -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/media/short01-final-original-c.wav -filter_complex "aformat=channel_layouts=mono,showwavespic=s=2400x720:colors=0xE6E1D6:scale=sqrt,format=rgb24,drawbox=x=1400:y=0:w=5:h=720:color=0xF2A900:t=fill" -frames:v 1 studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/source-boundary-waveform.png
ffmpeg -hide_banner -nostdin -y -i studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/short01-final-original-c-salvage-v1.wav -filter_complex "aformat=channel_layouts=mono,showwavespic=s=2400x720:colors=0xE6E1D6:scale=sqrt,format=rgb24" -frames:v 1 studio/originate/exit-readiness-prep/shorts-hyperframes/short-01-thirty-days-no-owner/production/final-v1/rescue-v1/salvage-full-waveform.png
```

File hashes were recorded with `shasum -a 256`; media creation and analysis used FFmpeg/FFprobe only. No network or paid provider call was made.
