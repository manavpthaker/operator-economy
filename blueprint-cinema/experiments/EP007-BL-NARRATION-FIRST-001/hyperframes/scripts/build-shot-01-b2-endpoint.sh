#!/bin/sh
set -eu

start_image="assets/images/cast-environment-anchor.generated.png"
candidate_image="assets/images/shot-01-end-keyframe-b2.edit-candidate.generated.png"
output_image="assets/images/shot-01-end-keyframe-b2.composited.png"

ffmpeg -hide_banner -loglevel error -y \
  -i "$start_image" \
  -i "$candidate_image" \
  -f lavfi -i "color=black:s=1672x941:r=1" \
  -filter_complex "[0:v]format=gbrp[base];[1:v]format=gbrp[edit];[2:v]format=gray,geq=lum='if(lte(((X-1250)*(X-1250))/(175*175)+((Y-150)*(Y-150))/(125*125)\\,1)*lte(Y\\,230)\\,255\\,0)',gblur=sigma=7,geq=lum='if(lte(Y\\,250)\\,p(X\\,Y)\\,0)'[mask];[base][edit][mask]maskedmerge,format=rgb24[out]" \
  -map "[out]" \
  -frames:v 1 \
  "$output_image"

printf '%s\n' "$output_image"
