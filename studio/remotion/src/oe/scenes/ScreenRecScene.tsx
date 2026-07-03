import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * ScreenRecScene — placeholder until real captures are wired. Styled as
 * a shot-list ticket: tool name, action, filename slot. Once
 * upload_youtube.py's Phase C is running, this scene will accept a
 * source_video and render OffthreadVideo with a lower-third label.
 */
export type ScreenRecSceneProps = {
  tool: string;
  action: string;
  caption?: string;
  startFrame: number;
};

export const ScreenRecScene: React.FC<ScreenRecSceneProps> = ({tool, action, caption, startFrame}) => {
  const frame = useCurrentFrame();
  const rel = frame - startFrame;
  const t = interpolate(rel, [0, 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill
      style={{
        background: COLORS.ink,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 160px',
      }}
    >
      <div
        style={{
          border: `1px solid ${COLORS.borderOnInk}`,
          padding: '56px 72px',
          maxWidth: 1300,
          opacity: t,
          transform: `translateY(${(1 - t) * 14}px)`,
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: COLORS.goldBright,
            marginBottom: 32,
          }}
        >
          Pending screen recording
        </div>
        <div
          style={{
            fontFamily: FONTS.sans,
            fontWeight: 500,
            fontSize: 44,
            color: COLORS.onInk,
            marginBottom: 20,
          }}
        >
          {tool}
        </div>
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 32,
            color: COLORS.onInkMuted,
            fontFeatureSettings: "'tnum' 1",
          }}
        >
          &rarr; {action}
        </div>
        {caption && (
          <div
            style={{
              fontFamily: FONTS.sans,
              fontSize: TYPE.body,
              color: COLORS.onInkMuted,
              marginTop: 28,
            }}
          >
            {caption}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
