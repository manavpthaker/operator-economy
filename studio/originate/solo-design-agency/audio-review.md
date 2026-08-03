# Audio review — solo-design-agency

## Engineer read on broadcast chain (2026-08-02)

**Verdict:** rolled out. Broadcast chain (bright+weighty, hi-pass 70–85 Hz, gentle 200 Hz cut, presence 3.2 kHz +1.2, air 10.5/13.5 kHz +1/+1.5, light de-ess, −2 dBTP peak limit, loudnorm −14 LUFS) chosen over Auphonic + warm.

### Measured targets (final .mp3, per section, pre-mix)

| section | LUFS | TP (dBTP) | LRA |
|---|---|---|---|
| hook | −15.8 | −1.9 | 2.2 |
| economics | −16.2 | −2.1 | 2.8 |

Both in engineer's recommended −15 to −16 LUFS band, TP under the −2 cap. `master_final.py` normalizes the mixed video to −14 LUFS after render.

### Plosive spot-check candidates (in-context review)

Isolated low-frequency burst candidates the engineer flagged. Only escalate to Pedalboard/dynamic EQ if audibly distracting in the finished video against the music bed + visuals:

- **hook**: ~14.9s
- **economics**: ~30.1s, ~44.3s, ~75.7s

### Why static ffmpeg over dynamic (Pedalboard)

Static EQ trade-off accepted per engineer: "For The Operator Economy, the voice needs to retain calm authority and body. A slightly exposed P-pop is less damaging than making the narration feel thin or over-processed." Dynamic EQ (Pedalboard) remains the escalation path if in-context review reveals distracting plosives.

### Follow-ups queued

- `trim_vo_lead.py` — trim leading silence per section + update `timeline.json` + shift `words-<section>.json` timestamps atomically. Engineer flagged 100–150 ms lead-in target.
- Pedalboard-based mastering script — script real pro plugins in Python (dynamic EQ, transient shaper) if the ffmpeg ceiling starts hurting.

### Legacy masters preserved

Every section's pre-broadcast master lives at `vo/<section>.legacy.mp3`. Contains the ORIGINAL master_vo.sh output (highpass + de-esser + loudnorm). Restore with:

```bash
cd originate/solo-design-agency/vo
for s in cta economics evidence hook playbook stack thesis; do
  mv "$s.mp3" "$s.broadcast.mp3"
  cp "$s.legacy.mp3" "$s.mp3"
done
```
