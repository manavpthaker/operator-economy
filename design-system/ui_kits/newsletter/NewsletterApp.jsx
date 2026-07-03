/* NewsletterApp — the Monday email styled as a research note.
   Doc number, date, reading time, sources. Single reading column.
   Composes DS primitives from the bundle. */
const OE_N = window.TheOperatorEconomyDesignSystem_bf951d;
const { Badge: NBadge, CitationChip: NCite, Stat: NStat, DataTable: NTable, SheetHeader: NSheet, Button: NButton } = OE_N;

function MastheadN() {
  return (
    <div style={{ borderBottom: '2px solid var(--ink-900)', paddingBottom: 16, marginBottom: 32 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
        <span style={{ fontFamily: 'var(--font-serif)', fontWeight: 600, fontSize: 22, color: 'var(--ink-900)' }}>The Operator Economy</span>
        <span className="oe-caps">Issue №004 · Monday</span>
      </div>
      <div style={{ display: 'flex', gap: 18, marginTop: 8 }}>
        <span className="oe-caps">2026-06-16</span>
        <span className="oe-caps">·</span>
        <span className="oe-caps">9 min read</span>
        <span className="oe-caps">·</span>
        <span className="oe-caps">11 sources</span>
      </div>
    </div>
  );
}

function Para({ children }) {
  return <p style={{ font: 'var(--type-body)', color: 'var(--text-body)', margin: '0 0 20px', fontSize: 18, lineHeight: 1.7 }}>{children}</p>;
}

function NewsletterApp() {
  return (
    <article style={{ maxWidth: 680, margin: '0 auto', padding: '56px 32px 80px' }}>
      <MastheadN />

      <div className="oe-label" style={{ color: 'var(--drafting-blue)', marginBottom: 14 }}>This week's thesis</div>
      <h1 style={{ font: 'var(--type-h1)', fontSize: 40, color: 'var(--ink-900)', margin: '0 0 24px', lineHeight: 1.1 }}>
        You can sell AI implementation to businesses drowning in it.
      </h1>

      <Para>
        Last year, Accenture booked <span className="oe-mono" style={{ fontWeight: 600, color: 'var(--gold-700)' }}>$5.9B</span> of generative-AI work — not <em>building</em> AI, <em>installing</em> it. The same service, at solo scale, is a <span className="oe-mono" style={{ fontWeight: 600 }}>$2,000</span> project one operator can sell in a month.
      </Para>
      <div style={{ margin: '0 0 28px' }}><NCite source="CIO Dive · Constellation Research" date="Accenture FY2025" /></div>

      <Para>
        Here's the thesis. Every business now knows it's supposed to be using AI, and almost none of them know how. That gap between knowing and doing is a service business — and it's called implementation.
      </Para>

      <div style={{ margin: '36px 0' }}>
        <NSheet sheet={1} total={3} title="The market, both ends"
          subtitle="Start at the top because it proves demand; the floor is where you actually start." />
      </div>

      <Para>
        Accenture's GenAI bookings roughly doubled while overall new bookings stayed flat — the implementation work is the only thing growing. By late 2025 they stopped reporting it separately because it touched <span className="oe-mono" style={{ fontWeight: 600 }}>80%</span> of large deals.
      </Para>

      <div style={{ display: 'flex', gap: 40, margin: '28px 0' }}>
        <NStat prefix="$" value="5.9" unit="B" label="GenAI bookings, FY25" emphasis="gold" size="md" />
        <NStat value="80" unit="%" label="of large deals touched" size="md" />
        <NStat value="~2" unit="×" label="YoY growth" delta="flat overall" deltaDirection="flat" size="md" />
      </div>

      <Para>
        The floor is better documented because it's boring: freelancers doing AI automation at <span className="oe-mono" style={{ fontWeight: 600 }}>$5–6K/mo</span> on about <span className="oe-mono" style={{ fontWeight: 600 }}>$20</span> of tooling. Pricing converges across every source:
      </Para>

      <div style={{ margin: '0 0 12px' }}>
        <NTable
          columns={[
            { key: 'tier', label: 'Tier' },
            { key: 'first', label: 'First project', numeric: true },
            { key: 'retainer', label: 'Monthly retainer', numeric: true },
            { key: 'tooling', label: 'Tooling', numeric: true },
          ]}
          rows={[
            { tier: 'Freelancer', first: '$2,000', retainer: '$500', tooling: '$20' },
            { tier: 'Boutique', first: '$8,000', retainer: '$3,000', tooling: '$180' },
            { tier: 'Accenture', first: '$5.9B', retainer: '—', tooling: '—' },
          ]}
          source="Creator reports; ranges consistent across sources — estimate"
        />
      </div>
      <div style={{ margin: '10px 0 28px' }}><NBadge tone="gold">Marked estimate</NBadge></div>

      <div style={{ margin: '36px 0' }}>
        <NSheet sheet={2} total={3} title="The stack under $100/mo"
          subtitle="The brain, the runtime, the client-facing layer." />
      </div>

      <Para>
        The brain is Claude or ChatGPT at <span className="oe-mono" style={{ fontWeight: 600 }}>$20–40</span>. The runtime is n8n, Make, or Zapier — self-hosted n8n is close to free, which matters when you're quoting margins. The client-facing layer is Airtable or Notion: the dashboard they log into and feel ownership of.
      </Para>

      <div style={{
        borderTop: '1px solid var(--border)', borderBottom: '1px solid var(--border)',
        padding: '28px 0', margin: '40px 0', display: 'flex', flexDirection: 'column', gap: 14,
      }}>
        <div className="oe-label">Download the full blueprint</div>
        <p style={{ font: 'var(--type-body)', color: 'var(--text-muted)', margin: 0 }}>
          Operator Blueprint №004 — the who-pays map, the exact stack, a step-by-step plan to a first client, and the full source list.
        </p>
        <div><NButton variant="primary">Get Blueprint №004 (free)</NButton></div>
      </div>

      <p className="oe-caps" style={{ color: 'var(--text-faint)', marginTop: 40 }}>
        The Operator Economy · Build. Own. Operate. · Reply to this email and tell me what you'd build.
      </p>
    </article>
  );
}

window.NewsletterApp = NewsletterApp;
