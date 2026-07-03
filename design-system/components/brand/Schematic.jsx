import React from 'react';

/**
 * Schematic — the navy working-schematic panel: drafting grid,
 * sheet tag, live status, nodes wired in sequence, optional
 * measurement bracket and sourced footer. Children (usually
 * SchematicNodes) are automatically joined by wires.
 * RULE: the panel must cite its sources (source prop) and every
 * node must carry a real figure.
 */
export function Schematic({
  sheet = 1,
  total = 5,
  title,
  running = 'Running',
  bracket,
  source,
  footer,
  width,
  children,
  style,
  ...props
}) {
  const kids = React.Children.toArray(children);

  return (
    <div
      style={{
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        background: 'var(--surface-schematic)',
        backgroundImage:
          'repeating-linear-gradient(0deg, var(--schem-grid) 0 1px, transparent 1px 36px),' +
          'repeating-linear-gradient(90deg, var(--schem-grid) 0 1px, transparent 1px 36px)',
        padding: '22px 26px',
        width,
        ...style,
      }}
      {...props}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
        <span
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '10.5px',
            letterSpacing: 'var(--tracking-caps)',
            textTransform: 'uppercase',
            color: 'rgba(245,240,230,0.65)',
          }}
        >
          Sheet {String(sheet).padStart(2, '0')} of {String(total).padStart(2, '0')}{title ? ` — ${title}` : ''}
        </span>
        {running && (
          <span
            style={{
              display: 'inline-flex',
              gap: '7px',
              alignItems: 'center',
              fontFamily: 'var(--font-mono)',
              fontSize: '10px',
              letterSpacing: 'var(--tracking-label)',
              textTransform: 'uppercase',
              color: 'var(--status-live)',
            }}
          >
            <span className="oe-pulse" style={{ width: '6px', height: '6px', borderRadius: 'var(--radius-pill)', background: 'var(--status-live)' }}></span>
            {running}
          </span>
        )}
      </div>

      <div style={{ display: 'flex', alignItems: 'stretch', gap: '18px' }}>
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          {kids.map((child, i) => (
            <React.Fragment key={i}>
              {child}
              {i < kids.length - 1 && (
                <span
                  aria-hidden="true"
                  style={{
                    display: 'block',
                    width: '1px',
                    height: '24px',
                    background: 'var(--schem-wire)',
                    marginLeft: '44px',
                  }}
                ></span>
              )}
            </React.Fragment>
          ))}
        </div>
        {bracket && (
          <div style={{ display: 'flex', alignItems: 'stretch', gap: '9px' }}>
            <span
              aria-hidden="true"
              style={{
                width: '9px',
                border: '1px solid rgba(245,240,230,0.4)',
                borderLeft: 'none',
              }}
            ></span>
            <span
              style={{
                alignSelf: 'center',
                writingMode: 'vertical-rl',
                fontFamily: 'var(--font-mono)',
                fontSize: '9px',
                letterSpacing: 'var(--tracking-label)',
                textTransform: 'uppercase',
                color: 'rgba(245,240,230,0.6)',
                whiteSpace: 'nowrap',
              }}
            >
              {bracket}
            </span>
          </div>
        )}
      </div>

      {(source || footer) && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '16px', marginTop: '24px' }}>
          {source ? (
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px',
                padding: '4px 10px',
                fontFamily: 'var(--font-mono)',
                fontSize: 'var(--text-2xs)',
                background: 'rgba(26,26,26,0.5)',
                border: '1px solid rgba(245,240,230,0.22)',
                borderLeft: '2px solid var(--gold-bright)',
                color: 'rgba(245,240,230,0.8)',
              }}
            >
              <span style={{ fontSize: '9.5px', letterSpacing: 'var(--tracking-caps)', color: 'var(--gold-bright)' }}>SOURCE</span>
              {source}
            </span>
          ) : <span></span>}
          {footer && (
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'rgba(245,240,230,0.85)' }}>
              {footer}
            </span>
          )}
        </div>
      )}
    </div>
  );
}
