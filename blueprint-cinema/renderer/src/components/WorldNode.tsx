import type {CSSProperties} from 'react';
import type {WorldObject} from '../types';

type Props = {
  object: WorldObject;
  state: string;
  focused: boolean;
  contextual: boolean;
  carried: boolean;
  colors: Record<string, string>;
};

const dimensions: Record<WorldObject['kind'], {width: number; height: number}> = {
  zone: {width: 0, height: 0},
  actor: {width: 250, height: 108},
  token: {width: 238, height: 102},
  gate: {width: 258, height: 112},
  node: {width: 250, height: 108},
  destination: {width: 264, height: 112},
  ledger: {width: 264, height: 116},
  outcome: {width: 276, height: 116},
  money_flow: {width: 250, height: 106},
  state_marker: {width: 248, height: 106},
};

export const WorldNode: React.FC<Props> = ({object, state, focused, contextual, carried, colors}) => {
  if (object.kind === 'zone') {
    return null;
  }
  const size = dimensions[object.kind];
  const failed = state === 'failed' || state === 'suppressed';
  const resolved = state === 'resolved';
  const border = failed
    ? colors.negative
    : resolved
      ? colors.sage
      : focused
        ? colors.ledger_gold
        : 'rgba(245,240,230,0.34)';
  const style: CSSProperties = {
    position: 'absolute',
    left: object.position.x - size.width / 2,
    top: object.position.y - size.height / 2,
    width: size.width,
    height: size.height,
    border: `${focused ? 4 : 2}px solid ${border}`,
    borderRadius: 2,
    background: object.kind === 'outcome' ? colors.paper : 'rgba(20,38,62,0.94)',
    color: object.kind === 'outcome' ? colors.ink : colors.paper,
    boxSizing: 'border-box',
    padding: '11px 14px 28px',
    opacity: focused ? 1 : contextual ? 0.78 : carried ? 0.42 : resolved || failed ? 0.24 : 0.13,
    fontFamily: 'Arial, Helvetica, sans-serif',
    boxShadow: focused ? `0 0 0 8px ${colors.ledger_gold}22, 0 0 34px ${colors.ledger_gold}55` : undefined,
  };
  return (
    <div style={style} data-object-id={object.id}>
      <div style={{fontSize: 11, letterSpacing: 1.15, textTransform: 'uppercase', opacity: 0.62, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>
        {object.kind.replace('_', ' ')} · {object.id}
      </div>
      <div style={{fontSize: focused ? 21 : 19, lineHeight: 1.08, marginTop: 7, fontWeight: 800}}>{object.label}</div>
      <div
        style={{
          position: 'absolute',
          left: 14,
          bottom: 8,
          fontSize: 11,
          letterSpacing: 0.8,
          color: failed ? colors.negative : resolved ? colors.sage : colors.ledger_gold,
          textTransform: 'uppercase',
        }}
      >
        {state}
      </div>
    </div>
  );
};
