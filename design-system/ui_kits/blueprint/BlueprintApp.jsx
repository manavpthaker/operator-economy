/* BlueprintApp — Operator Blueprint PDF. Paper, title block, mono
   tables, annotated data, full source list. Real operator documentation
   a VP would save and annotate. Composes DS primitives. */
const OE_B = window.TheOperatorEconomyDesignSystem_bf951d;
const { TitleBlock: BTitle, SheetHeader: BSheet, DataTable: BTable, BarChart: BChart, Stat: BStat, CitationChip: BCite, Badge: BBadge, Annotation: BAnno } = OE_B;

function DocFooter({ page }) {
  return (
    <div style={{
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      borderTop: '1px solid var(--border)', paddingTop: 12, marginTop: 40,
    }}>
      <span className="oe-caps">The Operator Economy · Blueprint №004</span>
      <span className="oe-caps">Sheet {page} of 3</span>
    </div>
  );
}

function Sheet({ children, page }) {
  return (
    <section style={{
      background: 'var(--paper-0)', border: '1px solid var(--border)',
      boxShadow: 'var(--shadow-md)', width: 820, margin: '0 auto 32px',
      padding: '56px 64px',
    }}>
      {children}
      <DocFooter page={page} />
    </section>
  );
}

function BlueprintApp() {
  return (
    <div style={{ padding: '40px 20px 64px' }}>
      {/* SHEET 1 — cover / title block */}
      <Sheet page={1}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 40 }}>
          <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.1 }}>
            <span className="oe-caps">The</span>
            <span style={{ fontFamily: 'var(--font-serif)', fontWeight: 600, fontSize: 20, color: 'var(--ink-900)' }}>Operator Economy</span>
          </div>
          <BBadge tone="accent">Operator Blueprint</BBadge>
        </div>

        <h1 style={{ font: 'var(--type-display)', fontSize: 52, color: 'var(--ink-900)', margin: '0 0 16px', lineHeight: 1.05 }}>
          AI Implementation<br />as a Service
        </h1>
        <p style={{ font: 'var(--type-lead)', color: 'var(--text-body)', maxWidth: '52ch', margin: '0 0 40px' }}>
          Who pays, what they pay for, the real numbers at both ends of the market, the exact tool stack, and a step-by-step plan to a first client.
        </p>

        <BTitle
          docNumber="Operator Blueprint №004"
          title="AI Implementation as a Service"
          fields={[
            { label: 'Date', value: '2026-06-14' },
            { label: 'Revision', value: 'B' },
            { label: 'Sources', value: '11' },
            { label: 'Difficulty', value: 'Med' },
          ]}
        />
      </Sheet>

      {/* SHEET 2 — unit economics */}
      <Sheet page={2}>
        <BSheet sheet={2} total={3} title="Unit economics"
          subtitle="The same service exists at three scales. The only variable is who's buying." />

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40, margin: '36px 0' }}>
          <div>
            <div className="oe-label" style={{ marginBottom: 16 }}>Accenture GenAI bookings</div>
            <BChart prefix="$" unit="B"
              data={[{ label: 'FY24', value: 3.0 }, { label: 'FY25', value: 5.9, highlight: true }]}
              source="Accenture Annual Report 2025" height={180} />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
            <BAnno label="Proves demand" side="left">
              <BStat prefix="$" value="5.9" unit="B" label="Enterprise ceiling" emphasis="gold" size="md" />
            </BAnno>
            <BAnno label="Where you start" side="left" color="var(--sage-700)">
              <BStat prefix="$" value="5–6K" unit="/mo" label="Freelancer floor" size="md" />
            </BAnno>
          </div>
        </div>

        <div className="oe-label" style={{ margin: '8px 0 12px' }}>Pricing across the market</div>
        <BTable
          columns={[
            { key: 'tier', label: 'Tier' },
            { key: 'first', label: 'First project', numeric: true },
            { key: 'retainer', label: 'Monthly retainer', numeric: true },
            { key: 'clients', label: 'Typical clients', numeric: true },
          ]}
          rows={[
            { tier: 'Freelancer', first: '$2,000', retainer: '$500–2,000', clients: '1–3' },
            { tier: 'Boutique agency', first: '$8,000', retainer: '$3,000–5,000', clients: '5–10' },
            { tier: 'Enterprise (ref.)', first: '$5.9B', retainer: '—', clients: 'Global 2000' },
          ]}
          source="Multiple creator reports; ranges consistent — estimate"
        />
      </Sheet>

      {/* SHEET 3 — the stack + sources */}
      <Sheet page={3}>
        <BSheet sheet={3} total={3} title="The stack & the plan"
          subtitle="Under $100/mo in tooling. The margin is your judgment, not your infrastructure." />

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, margin: '32px 0' }}>
          {[
            { l: 'The brain', v: 'Claude / ChatGPT', p: '$20–40/mo' },
            { l: 'The runtime', v: 'n8n · Make · Zapier', p: '~$0–50/mo' },
            { l: 'Client layer', v: 'Airtable / Notion', p: '$0–20/mo' },
          ].map((s) => (
            <div key={s.l} style={{ border: '1px solid var(--border)', borderTop: '2px solid var(--drafting-blue)', borderRadius: 'var(--radius-xs)', padding: '16px', background: 'var(--paper-100)' }}>
              <div className="oe-label" style={{ marginBottom: 8 }}>{s.l}</div>
              <div style={{ fontFamily: 'var(--font-sans)', fontWeight: 600, fontSize: 15, color: 'var(--ink-900)', marginBottom: 6 }}>{s.v}</div>
              <div className="oe-mono" style={{ fontSize: 13, color: 'var(--gold-700)', fontWeight: 600 }}>{s.p}</div>
            </div>
          ))}
        </div>

        <div className="oe-label" style={{ margin: '32px 0 14px' }}>Sources</div>
        <ol style={{ margin: 0, padding: 0, listStyle: 'none', counterReset: 'src', display: 'flex', flexDirection: 'column', gap: 8 }}>
          {[
            'CIO Dive — Accenture GenAI bookings, FY2025',
            'Constellation Research — enterprise AI services analysis, Q1 FY2026',
            'Accenture Annual Report 2025',
            'Medium / The AI Studio — solo agency report, Mar 2026 (unverified)',
            'Public tool pricing — Anthropic, OpenAI, n8n, Make, Zapier',
          ].map((src, i) => (
            <li key={i} style={{ display: 'flex', gap: 12, fontFamily: 'var(--font-mono)', fontSize: 13, color: 'var(--ink-700)' }}>
              <span style={{ color: 'var(--drafting-blue)', fontWeight: 600 }}>[{String(i + 1).padStart(2, '0')}]</span>
              <span>{src}</span>
            </li>
          ))}
        </ol>

        <div style={{ marginTop: 28, display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <BCite source="CIO Dive" date="FY2025" />
          <BCite source="Creator reports" estimate />
        </div>
      </Sheet>
    </div>
  );
}

window.BlueprintApp = BlueprintApp;
