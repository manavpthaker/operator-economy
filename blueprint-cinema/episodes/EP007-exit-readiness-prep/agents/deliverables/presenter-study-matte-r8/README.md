# EP007 presenter matte R8: isolated preprocessing candidate

The full G portrait mask is complete. It preserves G's existing performance by changing alpha only. No face, mouth, body, audio, timing, or source RGB was generated or rewritten by this packet. This is a technical candidate, not an approved composite or production gate.

## Outputs

- `media/full-mask-765f.mkv`: lossless FFV1, full-range 8-bit grayscale, 608×1080, 25fps, 765 frames, 30.600s, no audio. SHA-256 `6889b1f78d0de405392f2516132c4fe78e470780a5b9ea5a7055009d4f9d2d58`.
- `media/diagnostic-mask-100f.mkv`: first 4.000s / 100 frames, independently processed. Decoded masks are byte-identical to the full run's first 100 frames.
- `media/diagnostic-alpha-f010.png`, `-f050.png`, `-f085.png`: straight-alpha PNG diagnostics, with original decoded RGB behind the alpha channel.
- `media/full-alpha-f*.png`: six sampled straight-alpha PNGs, including the final source frame.
- `media/diagnostic-contact-sheet.jpg` and `media/full-contact-sheet.jpg`: source / mask / dark-background QA views. The flat dark color is a diagnostic background only.
- `media/reference-person-mask.png`: separate, full-range grayscale mask for the supplied study/shoulder reference; 1672×941. SHA-256 `35feb908cb14bda26d12820a2d0cee7308a611b08304636c10a32f4abf34dc7b`.
- `alignment.json`: single-frame landmark alignment between the supplied 0.4s source portrait and study reference.
- `qa-report.json`, `diagnostic-metrics.json`, `full-metrics.json`, `checksums.json`: technical evidence and provenance.

All generated media remains ignored. The 4-second FFV1 alpha diagnostic movie was decoded and checked, then deleted with the orchestrator's explicit authorization to recover disk space. Its hash, probe and pixel checks remain in `qa-report.json`. The local compiler cache was also removed; no unrelated file was deleted.

## Method and exact mapping

`PersonMatte.swift` uses the installed macOS 26.2 Vision `VNGeneratePersonSegmentationRequest`, revision 1, accurate quality, one reused stateful request and `VNSequenceRequestHandler`. FFmpeg decodes source G to BGRA and crops **608×1080 at x=656, y=0**. Output mask frame N corresponds exactly to source video frame N, beginning at zero. There is no retiming or audio transformation.

Vision returned 1512×2016 masks. The script scales masks to 608×1080 with center-aligned bilinear interpolation and performs no erosion, dilation, blur, color treatment or temporal postprocessing. Black 0 is background; white 255 is foreground. A receiver must treat this as full-range mask data, not limited-range luma, and apply it to the same crop. Preserve straight RGB when creating an alpha plate.

The 100-frame test took 7.324s. The 765-frame pass took 57.232s, 13.367 processing frames/second. Swift 6.2.3 was used. Each final movie passed full FFmpeg decoding and exact frame-count/dimension/timebase checks. The temporary alpha movie preserved every decoded RGB value and every mask value at the two checked frames, 10 and 85. This is sampled pixel verification; `qa.py` records its exact scope.

The mask never becomes completely empty or solid. Opaque area varies from 50.659% to 53.545% of the portrait. Whole-frame normalized adjacent-mask difference is 0.128% median, 0.334% at the 95th percentile, and 0.706% maximum (frame 198, 7.92s). These differences contain real motion; they do not prove the absence of edge chatter.

## Observed limits

The sampled early/middle/final views keep face, glasses, ears and shirt intact. A thin light fringe remains around portions of the hair, glasses and ears on the dark diagnostic background. Fine hair is simplified. No continuous playback approval or clean shoulder seam is claimed.

The original portrait cuts both shoulder sides and lower body at its boundaries. Matting cannot recover those missing pixels. This packet creates no replacement torso. The separately supplied study reference contains synthetic shoulders and a synthetic face; its mask is only an extraction aid. The compositor must discard all generated face/neck regions before using an outer-shirt extension. Reference clothing alignment across moving source frames is unverified.

## Alignment aid

`FaceAlignment.swift` uses Vision eye, nose and nose-crest centroids, with top-left pixel coordinates. It fits isotropic scale and translation only, using one 0.4s frame; it does not track G.

Source portrait → native 1672×941 reference: `x' = 0.9821018813*x + 536.8108057`, `y' = 0.9821018813*y - 166.4062213`. Anchor RMS residual is 0.556 reference pixels.

If the reference is scaled uniformly to width 1920, source → reference placement becomes scale `1.1277724953`, x `616.4334611`, y `-191.0884838`. The scaled reference height is 1080.574, so the receiving composition must account explicitly for its chosen final vertical crop. This fit does not establish a safe clothing seam, natural motion, or final composition.

## Reproduction

Run only inside this packet. Recreate local `cache/tmp`, `cache/clang`, `cache/swift`, and `bin` directories, then compile with `swiftc -O -module-cache-path "$PWD/cache/swift"`, `TMPDIR="$PWD/cache/tmp"`, and `CLANG_MODULE_CACHE_PATH="$PWD/cache/clang"`. The two Swift sources document arguments. PersonMatte takes input MP4, output MKV, frame count, and metrics JSON. Its FFmpeg writer refuses to overwrite a file.

`qa.py` uses the already installed bundled NumPy/Pillow runtime. It checks the diagnostic alpha movie before authorized cleanup; regenerate that temporary alpha movie from the diagnostic mask and source crop before replaying that part of QA. No package, model, provider, or browser operation is required.
