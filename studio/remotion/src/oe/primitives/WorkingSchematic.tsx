import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * WorkingSchematic — the persistent navy drafting panel that "assembles"
 * across the episode. This is a scaffolded first cut: nodes are dropped
 * in progressively via a `nodes` timeline, wires connect adjacent nodes
 * once both have landed, sage RUNNING pulse in the header.
 *
 * The full spec expects nodes/wires to be declared per-episode in
 * assets.json (a `schematic` block that `plan_assets.py` doesn't emit
 * yet). For v2 launch, callers can pass a derived list (e.g. one node
 * per stack-section beat) so the animation exists even without pipeline
 * changes.
 *
 * TODO Phase 2: add `schematic` field to assets.json + a Python emitter.
 */
export type SchematicNode = {
  id: string;
  step: string; // "01 · Intake"
  name: string;
  figure: string; // "$0/mo" | "$2,000"
  appearAtFrame: number;
  status?: 'live' | 'running' | 'idle';
  goldFigure?: boolean;
};

export type WorkingSchematicProps = {
  nodes: SchematicNode[];
  sheetLabel?: string; // "Sheet 03 of 07 — The stack"
  margin?: string; // "≤ $100/mo"
  running?: boolean;
  height?: number; // pixels
};

const NODE_H = 96;
const NODE_W = 340;
const WIRE_H = 34;

export const WorkingSchematic: React.FC<WorkingSchematicProps> = ({
  nodes,
  sheetLabel,
  margin,
  running = true,
  height,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const runningPulse = 0.55 + 0.45 * (0.5 + 0.5 * Math.sin((frame / fps) * 2 * Math.PI * 0.9));

  return (
    <div
      style={{
        background: COLORS.navy,
        backgroundImage: `repeating-linear-gradient(0deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px), repeating-linear-gradient(90deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px)`,
        padding: '48px 56px',
        borderTop: `1px solid ${COLORS.borderOnInk}`,
        borderBottom: `1px solid ${COLORS.borderOnInk}`,
        position: 'relative',
        height,
        overflow: 'hidden',
      }}
    >
      {/* Head */}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 44}}>
        <span
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: 'rgba(245,240,230,0.65)',
          }}
        >
          {sheetLabel ?? ''}
        </span>
        {running && (
          <span
            style={{
              display: 'inline-flex',
              gap: 10,
              alignItems: 'center',
              fontFamily: FONTS.mono,
              fontSize: TYPE.microLabel,
              letterSpacing: `${TRACK.caps}em`,
              textTransform: 'uppercase',
              color: COLORS.sage,
              opacity: runningPulse,
            }}
          >
            <span
              style={{
                width: 10,
                height: 10,
                borderRadius: 999,
                background: COLORS.sage,
              }}
            />
            Running
          </span>
        )}
      </div>
      {/* Chain */}
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 0, position: 'relative'}}>
        {nodes.map((node, i) => {
          const t = spring({
            frame: frame - node.appearAtFrame,
            fps,
            config: {damping: 200, stiffness: 100},
            durationInFrames: 20,
          });
          const wireT = interpolate(frame - node.appearAtFrame, [-6, 8], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const nodeFigureColor = node.goldFigure ? COLORS.goldBright : 'rgba(245,240,230,0.92)';
          const statusColor =
            node.status === 'live' || node.status === 'running' ? COLORS.sage : 'rgba(245,240,230,0.55)';
          return (
            <React.Fragment key={node.id}>
              {i > 0 && (
                <div
                  style={{
                    width: 1,
                    height: WIRE_H,
                    background: COLORS.schemWire,
                    marginLeft: 44,
                    transformOrigin: 'top',
                    transform: `scaleY(${wireT})`,
                  }}
                />
              )}
              <div
                style={{
                  width: NODE_W,
                  border: `1px solid ${COLORS.schemNodeBorder}`,
                  background: COLORS.schemNodeBg,
                  padding: '18px 22px',
                  opacity: t,
                  transform: `translateY(${(1 - t) * 12}px)`,
                }}
              >
                <div style={{display: 'flex', justifyContent: 'space-between', gap: 10, marginBottom: 8}}>
                  <span
                    style={{
                      fontFamily: FONTS.mono,
                      fontSize: 14,
                      letterSpacing: `${TRACK.caps}em`,
                      textTransform: 'uppercase',
                      color: 'rgba(245,240,230,0.55)',
                    }}
                  >
                    {node.step}
                  </span>
                  {node.status && (
                    <span
                      style={{
                        fontFamily: FONTS.mono,
                        fontSize: 14,
                        letterSpacing: `${TRACK.caps}em`,
                        textTransform: 'uppercase',
                        color: statusColor,
                      }}
                    >
                      ● {node.status.toUpperCase()}
                    </span>
                  )}
                </div>
                <div
                  style={{
                    fontFamily: FONTS.sans,
                    fontSize: 22,
                    fontWeight: 500,
                    color: COLORS.onInk,
                    marginBottom: 8,
                  }}
                >
                  {node.name}
                </div>
                <div
                  style={{
                    fontFamily: FONTS.mono,
                    fontSize: 26,
                    color: nodeFigureColor,
                    fontFeatureSettings: "'tnum' 1",
                  }}
                >
                  {node.figure}
                </div>
              </div>
            </React.Fragment>
          );
        })}
      </div>
      {margin && (
        <div
          style={{
            position: 'absolute',
            right: 56,
            top: 120,
            fontFamily: FONTS.mono,
            fontSize: 20,
            color: 'rgba(245,240,230,0.85)',
          }}
        >
          Margin {margin}
        </div>
      )}
    </div>
  );
};
