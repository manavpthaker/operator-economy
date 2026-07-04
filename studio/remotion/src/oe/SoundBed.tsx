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
  /** Seconds of video time before content t=0 (bookends J-cut layout).
   *  When SoundBed sits ABOVE the bookends (music from frame 0), screen
   *  lookups shift by this much, and t<0 = intro cards (chords, louder). */
  timeOffsetS?: number;
};

const dbToLinear = (db: number) => Math.pow(10, db / 20);
// Levels raised 2026-07-04 ("you can't even tell it's stopping"): the
// bed must be PRESENT for its silences to register as edits.
const LEVELS = {
  calm: dbToLinear(-13),
  build: dbToLinear(-8),
  silence: 0,
} as const;
const INTRO_LEVEL = dbToLinear(-6); // under brand sting + title card, pre-VO
const SFX_VOLUME: Record<string, number> = {
  tick: dbToLinear(-18),
  whoosh: dbToLinear(-12),
  hit: dbToLinear(-6),
};

export const SoundBed: React.FC<SoundBedProps> = ({
  screens,
  musicDir = null,
  sfxDir = null,
  timeOffsetS = 0,
}) => {
  const {fps} = useVideoConfig();

  const musicVolume = React.useCallback(
    (frame: number): number => {
      const t = frame / fps - timeOffsetS;
      const preLap = 0.5;
      if (t < 0) {
        // Intro cards: chords carry the open, then hand off as VO enters.
        return t > -0.6 ? LEVELS.calm + (INTRO_LEVEL - LEVELS.calm) * (-t / 0.6)
                        : INTRO_LEVEL;
      }
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
    [fps, screens, timeOffsetS],
  );

  return (
    <>
      {musicDir && (
        <Audio
          src={staticFile(`${musicDir}/bed.mp3`)}
          volume={musicVolume}
          loop
        />
      )}
      {sfxDir &&
        screens.flatMap((screen) =>
          (screen.sfx ?? []).map((cue, i) => {
            const from = Math.round((cue.at + timeOffsetS) * fps);
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
