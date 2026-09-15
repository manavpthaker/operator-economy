import type {AssetTicket} from '../types';

export const TicketSlate: React.FC<{ticket: AssetTicket; colors: Record<string, string>}> = ({ticket, colors}) => {
  return (
    <div
      style={{
        width: 430,
        border: `3px dashed ${colors.negative}`,
        borderRadius: 2,
        background: colors.paper,
        color: colors.ink,
        padding: 18,
        boxSizing: 'border-box',
        fontFamily: 'Arial, Helvetica, sans-serif',
      }}
    >
      <div style={{fontSize: 16, fontWeight: 800, letterSpacing: 2, color: colors.negative}}>
        UNFILLED ASSET TICKET
      </div>
      <div style={{fontSize: 25, fontWeight: 800, marginTop: 8}}>{ticket.id}</div>
      <div style={{fontSize: 15, lineHeight: 1.35, marginTop: 10}}>{ticket.required_semantic_content}</div>
      <div style={{fontSize: 13, lineHeight: 1.35, marginTop: 12, opacity: 0.72}}>
        Placeholder only · {ticket.preferred_source_route} · {ticket.status}
      </div>
    </div>
  );
};

