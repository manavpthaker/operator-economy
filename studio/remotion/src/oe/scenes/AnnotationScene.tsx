import React from 'react';
import {AbsoluteFill} from 'remotion';
import {AnnotationRail} from '../primitives/AnnotationRail';
import {COLORS} from '../theme';

/**
 * AnnotationScene — replaces the v1 "slide" grammar. Editorial paper
 * ground with a Zodiak/Boska title and 2–4 annotated body lines.
 */
export type AnnotationSceneProps = {
  title?: string;
  overline?: string;
  bullets: string[];
  onInk?: boolean;
  startFrame: number;
};

export const AnnotationScene: React.FC<AnnotationSceneProps> = ({
  title,
  overline,
  bullets,
  onInk = false,
  startFrame,
}) => (
  <AbsoluteFill
    style={{
      background: onInk ? COLORS.ink : COLORS.paper,
      justifyContent: 'center',
      alignItems: 'flex-start',
      padding: '120px 200px 260px',
    }}
  >
    <AnnotationRail
      title={title}
      overline={overline}
      bullets={bullets}
      onInk={onInk}
      startFrame={startFrame}
    />
  </AbsoluteFill>
);
