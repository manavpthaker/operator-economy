#!/usr/bin/env bash
set -euo pipefail

# Build the same 17.5–27.5 master-context window used by the A/B review while replacing only
# master frames 16–201 with the 186-frame B6 narration-first proof. The context plate's original
# 10-second AAC track is copied bit-for-bit; only the picture is re-encoded.
ffmpeg -hide_banner -y \
  -i renders/EP007-A-CLIP-FIRST-context-17.5-27.5.mp4 \
  -i renders/EP007-BL-NARRATION-FIRST-006.mp4 \
  -filter_complex "[0:v]trim=start_frame=0:end_frame=16,setpts=PTS-STARTPTS[pre];[1:v]trim=start_frame=0:end_frame=186,setpts=PTS-STARTPTS[test];[0:v]trim=start_frame=202:end_frame=240,setpts=PTS-STARTPTS[post];[pre][test][post]concat=n=3:v=1:a=0,format=yuv420p[v]" \
  -map "[v]" \
  -map 0:a:0 \
  -c:v libx264 \
  -preset slow \
  -crf 16 \
  -r 24 \
  -vsync cfr \
  -c:a copy \
  -movflags +faststart \
  renders/EP007-B6-NARRATION-FIRST-context-17.5-27.5.mp4
