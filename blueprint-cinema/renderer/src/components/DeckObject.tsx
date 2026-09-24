import type {CSSProperties} from 'react';

export type DeckRole = 'guest' | 'ota' | 'hotel' | 'operator';

type Props = {
  id: string;
  role: DeckRole;
  label: string;
  eyebrow: string;
  left: number;
  top: number;
  active: boolean;
  colors: Record<string, string>;
  note?: string;
};

const iconFor = (role: DeckRole, colors: Record<string, string>) => {
  const stroke = colors.paper;
  if (role === 'guest') {
    return (
      <svg viewBox="0 0 160 120" width={160} height={120} aria-hidden="true">
        <circle cx={80} cy={34} r={22} fill="none" stroke={stroke} strokeWidth={8} />
        <path d="M37 108c5-35 21-52 43-52s38 17 43 52" fill="none" stroke={stroke} strokeWidth={8} />
        <path d="M125 62h25v38h-25zM131 62v-9h13v9" fill="none" stroke={colors.ledger_gold} strokeWidth={6} />
      </svg>
    );
  }
  if (role === 'ota') {
    return (
      <svg viewBox="0 0 160 120" width={160} height={120} aria-hidden="true">
        <path d="M30 108V45c0-22 18-39 40-39h20c22 0 40 17 40 39v63" fill="none" stroke={stroke} strokeWidth={9} />
        <path d="M12 108h136M56 108V60h48v48" fill="none" stroke={stroke} strokeWidth={9} />
        <path d="M52 35h56" stroke={colors.ledger_gold} strokeWidth={9} />
      </svg>
    );
  }
  if (role === 'hotel') {
    return (
      <svg viewBox="0 0 160 120" width={160} height={120} aria-hidden="true">
        <path d="M18 108h124M34 108V35l46-27 46 27v73" fill="none" stroke={stroke} strokeWidth={8} />
        <path d="M62 108V70h36v38M51 43h16v16H51zM93 43h16v16H93z" fill="none" stroke={colors.ledger_gold} strokeWidth={7} />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 160 120" width={160} height={120} aria-hidden="true">
      <circle cx={80} cy={30} r={21} fill="none" stroke={stroke} strokeWidth={8} />
      <path d="M42 108V80c0-19 15-34 34-34h8c19 0 34 15 34 34v28" fill="none" stroke={stroke} strokeWidth={8} />
      <path d="M18 108h124M105 70h35v27h-35z" fill="none" stroke={colors.ledger_gold} strokeWidth={7} />
    </svg>
  );
};

export const DeckObject: React.FC<Props> = ({id, role, label, eyebrow, left, top, active, colors, note}) => {
  const style: CSSProperties = {
    position: 'absolute',
    left,
    top,
    width: 270,
    minHeight: 270,
    boxSizing: 'border-box',
    background: colors.schematic_navy,
    border: `${active ? 8 : 3}px solid ${active ? colors.ledger_gold : colors.drafting_blue}`,
    color: colors.paper,
    padding: '20px 22px 18px',
    opacity: active ? 1 : 0.82,
    boxShadow: active ? `14px 14px 0 ${colors.ledger_gold}33` : 'none',
    fontFamily: 'Arial, Helvetica, sans-serif',
  };
  return (
    <div style={style} data-object-id={id} data-deck-role={role}>
      <div style={{fontFamily: 'Courier New, monospace', fontSize: 15, fontWeight: 700, letterSpacing: 2.1, opacity: 0.7}}>
        {eyebrow}
      </div>
      <div style={{height: 128, display: 'grid', placeItems: 'center'}}>{iconFor(role, colors)}</div>
      <div style={{fontSize: 31, lineHeight: 1.02, fontWeight: 900, letterSpacing: -0.7}}>{label}</div>
      {note ? <div style={{fontSize: 15, lineHeight: 1.2, marginTop: 9, color: colors.ledger_gold}}>{note}</div> : null}
    </div>
  );
};
