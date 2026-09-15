#!/bin/sh
set -eu

start_image="assets/images/shot-01b-buyer-cut-in-start-b3.generated.png"
candidate_image="assets/images/shot-01b-buyer-cut-in-end-b3.edit-candidate.generated.png"
output_image="assets/images/shot-01b-buyer-cut-in-end-b3.composited.png"

ffmpeg -hide_banner -loglevel error -y \
  -i "$start_image" \
  -i "$candidate_image" \
  -f lavfi -i "color=black:s=1672x941:r=1" \
  -filter_complex "[0:v]format=gbrp[base];[1:v]format=gbrp[edit];[2:v]format=gray,geq=lum='if(lte(((X-1200)*(X-1200))/(280*280)+((Y-205)*(Y-205))/(220*220)\\,1)*lte(Y\\,315)\\,255\\,0)',gblur=sigma=8,geq=lum='if(lte(Y\\,340)\\,p(X\\,Y)\\,0)'[mask];[base][edit][mask]maskedmerge,format=rgb24[out]" \
  -map "[out]" \
  -frames:v 1 \
  "$output_image"

printf '%s\n' "$output_image"
