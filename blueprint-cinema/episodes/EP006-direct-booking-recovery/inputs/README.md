# Inputs

This folder is reserved for generated input diagnostics and ignored, hash-verified episode-local staging when needed. Canonical source artifacts remain in `studio/originate/direct-booking-recovery/`; the current renderer stages verified VO under its own ignored `public/generated/` boundary.

The runtime never stages upstream media before verifying it against `input-lock.json`. No input artifacts are staged in this episode-local folder for the current greybox.
