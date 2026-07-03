#!/usr/bin/env bash
# Master VO sections for broadcast crispness: rumble cut, presence bell,
# air shelf, gentle de-ess, two-pass loudnorm to -14 LUFS.
# Usage: master_vo.sh <vo_dir>   (processes *.mp3 in place, keeps .raw backups)
set -euo pipefail
DIR="$1"
CHAIN="highpass=f=70,anequalizer=c0 f=4200 w=1400 g=2.5 t=1|c0 f=11500 w=4000 g=3 t=1,deesser=i=0.28,loudnorm=I=-14:TP=-1.5:LRA=9"
for F in "$DIR"/*.mp3; do
  [ -e "${F%.mp3}.raw.mp3" ] && continue  # already mastered
  cp "$F" "${F%.mp3}.raw.mp3"
  ffmpeg -hide_banner -y -loglevel error -i "${F%.mp3}.raw.mp3" -af "$CHAIN" -ar 44100 -b:a 192k "$F"
  echo "mastered: $F"
done
