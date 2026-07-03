#!/usr/bin/env bash
# Clean voice-clone training samples for ElevenLabs PVC retraining.
# Chain: mono 44.1k → 70Hz highpass (rumble) → two-pass loudnorm to a
# CONSISTENT -19 LUFS / -2dBTP / LRA 7 → 192k MP3.
# Consistency across samples matters more than any single target number.
# Usage: clean_voice_samples.sh input.mp3 output.mp3 [--denoise]
set -euo pipefail
IN="$1"; OUT="$2"; DN="${3:-}"
PRE="highpass=f=70"
[ "$DN" = "--denoise" ] && PRE="$PRE,afftdn=nf=-28"
M=$(ffmpeg -hide_banner -i "$IN" -af "$PRE,loudnorm=I=-19:TP=-2:LRA=7:print_format=json" -f null - 2>&1 | tail -12)
II=$(echo "$M" | grep input_i | sed 's/[^0-9.-]//g')
IT=$(echo "$M" | grep input_tp | sed 's/[^0-9.-]//g')
IL=$(echo "$M" | grep input_lra | sed 's/[^0-9.-]//g')
ITH=$(echo "$M" | grep input_thresh | sed 's/[^0-9.-]//g')
OFF=$(echo "$M" | grep target_offset | sed 's/[^0-9.-]//g')
ffmpeg -hide_banner -y -i "$IN" -af "$PRE,loudnorm=I=-19:TP=-2:LRA=7:measured_I=$II:measured_TP=$IT:measured_LRA=$IL:measured_thresh=$ITH:offset=$OFF:linear=true" -ar 44100 -ac 1 -b:a 192k "$OUT"
echo "DONE: $OUT"
