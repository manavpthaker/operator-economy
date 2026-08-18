import React from 'react';
import {AbsoluteFill, interpolate, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * BRollScene renders approved long-form footage. Missing media remains a
 * deliberately conspicuous render blocker so a search-query ticket cannot be
 * mistaken for a finished scene during review.
 */
export type BRollSceneProps = {
  searchQuery: string;
  caption?: string;
  startFrame: number;
  sourceVideo?: string;
  sourceIn?: number;
  sourceOut?: number;
  crop?: string;
  focalPosition?: string;
  playbackRate?: number;
};

const isExternalSource = (source: string) => /^(https?:|data:|blob:)/i.test(source);

const positionFromCrop = (crop?: string): string | undefined => {
  if (!crop) return undefined;
  const normalized = crop.toLowerCase().replace(/[_-]+/g, ' ');
  if (/\btop left\b/.test(normalized)) return 'left top';
  if (/\btop right\b/.test(normalized)) return 'right top';
  if (/\bbottom left\b/.test(normalized)) return 'left bottom';
  if (/\bbottom right\b/.test(normalized)) return 'right bottom';
  if (/\bcenter left\b|\bleft\b/.test(normalized)) return 'left center';
  if (/\bcenter right\b|\bright\b/.test(normalized)) return 'right center';
  if (/\btop\b/.test(normalized)) return 'center top';
  if (/\bbottom\b/.test(normalized)) return 'center bottom';
  if (/\bcenter\b/.test(normalized)) return 'center center';
  return undefined;
};

export const BRollScene: React.FC<BRollSceneProps> = ({
  searchQuery,
  caption,
  startFrame,
  sourceVideo,
  sourceIn = 0,
  sourceOut,
  crop,
  focalPosition,
  playbackRate = 1,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rel = frame - startFrame;
  const fadeIn = interpolate(rel, [0, 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const drift = interpolate(rel, [0, 120], [1.0, 1.04], {extrapolateRight: 'clamp'});

  if (sourceVideo) {
    const src = isExternalSource(sourceVideo) ? sourceVideo : staticFile(sourceVideo.replace(/^\/+/, ''));
    const startFrom = Math.max(0, Math.round(sourceIn * fps));
    // `endAt` is evaluated on the composition timeline. When a short source is
    // slowed to fill a longer screen, scale the cutoff too; otherwise Remotion
    // removes the video at the unscaled out-point and exposes the ink ground.
    const endAt = sourceOut === undefined
      ? undefined
      : Math.max(
          startFrom + 1,
          startFrom + Math.round(((sourceOut - sourceIn) / playbackRate) * fps),
        );
    const objectPosition = positionFromCrop(focalPosition) || focalPosition || positionFromCrop(crop) || 'center center';

    return (
      <AbsoluteFill style={{background: COLORS.ink, overflow: 'hidden'}}>
        <OffthreadVideo
          src={src}
          startFrom={startFrom}
          endAt={endAt}
          playbackRate={playbackRate}
          muted
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition,
          }}
        />
        {caption ? (
          <div
            style={{
              position: 'absolute',
              right: 72,
              bottom: 56,
              maxWidth: 720,
              padding: '14px 20px',
              background: 'rgba(11, 21, 35, 0.78)',
              borderLeft: `4px solid ${COLORS.goldBright}`,
              color: COLORS.onInk,
              fontFamily: FONTS.sans,
              fontSize: TYPE.body,
              lineHeight: 1.25,
            }}
          >
            {caption}
          </div>
        ) : null}
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill
      style={{
        background: COLORS.ink,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 160px',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          border: `1px solid ${COLORS.borderOnInk}`,
          padding: '48px 64px',
          maxWidth: 1300,
          opacity: fadeIn,
          transform: `scale(${drift})`,
          transformOrigin: 'center',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: '#ff6b5f',
            marginBottom: 28,
          }}
        >
          Media required · render blocker
        </div>
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 46,
            color: COLORS.onInk,
            lineHeight: 1.2,
            fontFeatureSettings: "'tnum' 1",
          }}
        >
          &ldquo;{searchQuery}&rdquo;
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
