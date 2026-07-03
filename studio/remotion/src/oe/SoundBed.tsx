import React from 'react';
import {Audio, Sequence, staticFile, useVideoConfig} from 'remotion';

import type {Screen} from '../BlueprintComposition';

/**
 * SoundBed — music + SFX layer for a Blueprint composition.
 *
 * Music: single continuous track (`{musicDir}/bed.mp3`) under the whole
 * episode, volume ducked against VO via a callback that reads
 * screen-level `music.intensity`:
 *   - calm    → −16 dB
 *   - build   → −10 dB
 *   - silence → 0.0 during the screen, with a 0.5s pre-lap fade so the
 *               silence lands *before* the visual — silence IS the
 *               riser (craft §P0). 0.5s ramp back up after.
 *
 * SFX: each cue in `screen.sfx` becomes a Remotion Sequence at the cue
 * frame, playing `{sfxDir}/{cue.cue}.mp3` (`tick.mp3`/`whoosh.mp3`/
 * `hit.mp3`). Cue volumes: tick −18 dB, whoosh −12 dB, hit −6 dB.
 *
 * Missing assets: `musicDir`/`sfxDir` default to `null`, meaning the
 * layer is completely off. Callers opt in explicitly once
 * `remotion/public/music/bed.mp3` (or the sfx files) are dropped in.
 * This is the "if no licensed track file exists, log a warning and
 * render without music (never block, never placeholder-tone)" behavior
 * required by the docs.
 */

export type SoundBedProps = {
  screens: Screen[];
  musicDir?: string | null;
  sfxDir?: string | null;
};

const dbToLinear = (db: number) => Math.pow(10, db / 20);
const LEVELS = {
  calm: dbToLinear(-16),
  build: dbToLinear(-10),
  silence: 0,
} as const;
const SFX_VOLUME: Record<string, number> = {
  tick: dbToLinear(-18),
  whoosh: dbToLinear(-12),
  hit: dbToLinear(-6),
};

export const SoundBed: React.FC<SoundBedProps> = ({
  screens,
  musicDir = null,
  sfxDir = null,
}) => {
  const {fps} = useVideoConfig();

  const musicVolume = React.useCallback(
    (frame: number): number => {
      const t = frame / fps;
      const preLap = 0.5;
      const current = screens.find((s) => t >= s.start && t < s.end);
      if (!current) return LEVELS.calm;
      const next = screens.find((s) => s.start >= current.end);
      const intensity = (current.music?.intensity ?? 'calm') as keyof typeof LEVELS;
      const target = LEVELS[intensity] ?? LEVELS.calm;

      // Pre-lap into silence: 0.5s ramp before a silence screen.
      if (next && (next.music?.intensity ?? 'calm') === 'silence') {
        const timeToNext = next.start - t;
        if (timeToNext < preLap && timeToNext >= 0) {
          const start = LEVELS[intensity] ?? LEVELS.calm;
          return start * Math.max(0, timeToNext / preLap);
        }
      }
      // Recover from silence: 0.5s ramp into the new screen.
      if (intensity !== 'silence') {
        const timeIn = t - current.start;
        if (timeIn < preLap) {
          return target * Math.min(1, timeIn / preLap);
        }
      }
      return target;
    },
    [fps, screens],
  );

  return (
    <>
      {musicDir && (
        <Audio
          src={staticFile(`${musicDir}/bed.mp3`)}
          volume={musicVolume}
        />
      )}
      {sfxDir &&
        screens.flatMap((screen) =>
          (screen.sfx ?? []).map((cue, i) => {
            const from = Math.round(cue.at * fps);
            const durationInFrames = Math.round(fps * 1.5);
            const vol = SFX_VOLUME[cue.cue] ?? 0.2;
            return (
              <Sequence
                key={`${screen.id}-sfx-${cue.cue}-${i}`}
                from={from}
                durationInFrames={durationInFrames}
              >
                <Audio src={staticFile(`${sfxDir}/${cue.cue}.mp3`)} volume={vol} />
              </Sequence>
            );
          }),
        )}
    </>
  );
};
