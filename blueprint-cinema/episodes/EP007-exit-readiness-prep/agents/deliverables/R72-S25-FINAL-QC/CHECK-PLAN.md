# R72 S25 final-QC preflight

Read-only review of finish.py SHA256 `a58a6cbe97a94736a2c2cd15b68e2273fca02c2c7cc0e13410f6799907981de9`. No execution of the assembly script.

Arithmetic matches the timing recommendation: S24 [352,552) =200frames /8.333333seconds, followed by S25 [0,726) =726frames /30.25seconds, total926frames /38.583333seconds. The review starts at masterframe26236,1093.166667seconds. S25 starts at contextframe200, masterframe26436,1101.5seconds. Final exclusive masterframe27162 is1131.75seconds.

Continuous source audio [52472000,54324000) =1852000samples at48kHz, exactly926frames of2000samples. Staged S25 PCM uses [52872000,54324000),1452000samples. Last scene/context frames725/925 display master1131.708333–1131.75.

Source-ready required before final encoded checks. Planned compact independent checks: supplied current S24/S25/context hashes; actual decoded counts and selected lead/cue/end frames; staged PCM equality; seam-window and retained end-pause metrics stated as measurements, without an arbitrary universal correlation threshold; direct encoded image inspection. No continuous listening, gate, paid call or owner-acceptance action.
