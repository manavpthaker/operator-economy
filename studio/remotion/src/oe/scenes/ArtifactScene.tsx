import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';
import {CitationChip} from '../primitives/CitationChip';

/**
 * ArtifactScene — a framed representation of an authored artifact:
 * a network map, a workflow diagram, a mockup card. Renders as a
 * pre-baked SVG/asset when provided; falls back to a labeled framed
 * placeholder that still reads as a made-thing (not stock).
 *
 * Composition: framed box (1.5px rule), overline label, title inside,
 * optional annotation callouts along the frame, source chip lower-left.
 * The `nodes` prop lets the caller author a simple network of labels
 * that render as boxes connected by hairlines — this is what covers
 * the "operator credibility → warm intro → first install" moment.
 */
export type ArtifactNode = {
  id: string;
  label: string;
  sub?: string;
  emphasis?: boolean;
};

export type ArtifactSceneProps = {
  overline?: string; // "Operator asset" / "Attach path"
  title?: string;
  nodes?: ArtifactNode[]; // when 3 nodes are provided, renders as a → chain
  callout?: string; // small annotation right of the frame
  source?: string;
  onInk?: boolean;
};

export const ArtifactScene: React.FC<ArtifactSceneProps> = ({
  overline,
  title,
  nodes,
  callout,
  source,
  onInk = false,
}) => {
  const frame = useCurrentFrame();
  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const rule = onInk ? 'rgba(245,240,230,0.28)' : COLORS.ruleStrong;
  const gold = onInk ? COLORS.goldBright : COLORS.goldOnPaper;
  const accent = onInk ? COLORS.goldBright : COLORS.draftingBlue;

  const overlineT = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const titleT = interpolate(frame, [4, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const chipT = interpolate(frame, [50, 62], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: onInk ? COLORS.ink : COLORS.paper,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '80px 160px 220px',
      }}
    >
      <div
        style={{
          width: 1600,
          border: `1.5px solid ${rule}`,
          background: onInk ? 'rgba(245,240,230,0.03)' : COLORS.paperLifted,
          padding: '56px 72px',
          position: 'relative',
        }}
      >
        {overline && (
          <div
            style={{
              fontFamily: FONTS.mono,
              fontSize: TYPE.microLabel,
              letterSpacing: `${TRACK.caps}em`,
              textTransform: 'uppercase',
              color: accent,
              opacity: overlineT,
              marginBottom: 24,
            }}
          >
            {overline}
          </div>
        )}
        {title && (
          <h2
            style={{
              fontFamily: TYPE.h2 >= 40 ? FONTS.display : FONTS.heading,
              fontWeight: 700,
              fontSize: 60,
              lineHeight: 1.08,
              letterSpacing: `${TRACK.heading}em`,
              color: strong,
              margin: 0,
              opacity: titleT,
              transform: `translateY(${(1 - titleT) * 12}px)`,
            }}
          >
            {title}
          </h2>
        )}

        {nodes && nodes.length > 0 && (
          <div
            style={{
              display: 'flex',
              alignItems: 'stretch',
              gap: 24,
              marginTop: 56,
            }}
          >
            {nodes.map((node, i) => {
              const nodeStart = 22 + i * 10;
              const t = interpolate(frame, [nodeStart, nodeStart + 14], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
                easing: Easing.bezier(...EASE.standard),
              });
              const isPeak = node.emphasis || i === nodes.length - 1;
              return (
                <React.Fragment key={node.id}>
                  <div
                    style={{
                      flex: 1,
                      border: `1px solid ${rule}`,
                      background: onInk ? 'rgba(245,240,230,0.06)' : 'rgba(255,255,255,0.5)',
                      padding: '24px 28px',
                      opacity: t,
                      transform: `translateY(${(1 - t) * 10}px)`,
                    }}
                  >
                    <div
                      style={{
                        fontFamily: FONTS.mono,
                        fontSize: TYPE.microLabel,
                        letterSpacing: `${TRACK.caps}em`,
                        textTransform: 'uppercase',
                        color: isPeak ? gold : muted,
                        marginBottom: 12,
                      }}
                    >
                      Node {String(i + 1).padStart(2, '0')}
                    </div>
                    <div
                      style={{
                        fontFamily: FONTS.sans,
                        fontWeight: 500,
                        fontSize: 28,
                        color: strong,
                        lineHeight: 1.24,
                      }}
                    >
                      {node.label}
                    </div>
                    {node.sub && (
                      <div
                        style={{
                          marginTop: 8,
                          fontFamily: FONTS.mono,
                          fontSize: TYPE.small,
                          color: muted,
                        }}
                      >
                        {node.sub}
                      </div>
                    )}
                  </div>
                  {i < nodes.length - 1 && (
                    <div
                      style={{
                        alignSelf: 'center',
                        fontFamily: FONTS.mono,
                        fontSize: 40,
                        color: accent,
                        opacity: interpolate(frame, [nodeStart + 8, nodeStart + 20], [0, 1], {
                          extrapolateLeft: 'clamp',
                          extrapolateRight: 'clamp',
                        }),
                      }}
                    >
                      →
                    </div>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        )}

        {callout && (
          <div
            style={{
              marginTop: 40,
              fontFamily: FONTS.mono,
              fontSize: TYPE.small,
              color: muted,
              maxWidth: '68ch',
            }}
          >
            {callout}
          </div>
        )}

        {source && (
          <div style={{marginTop: 32, opacity: chipT}}>
            <CitationChip source={source} onInk={onInk} />
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
