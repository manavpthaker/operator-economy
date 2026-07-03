/* WebsiteApp — theoperatoreconomy.com landing.
   Welsh-grade restraint: one promise, one capture, evidence up front.
   Composes DS primitives from the bundle namespace. */
const OE = window.TheOperatorEconomyDesignSystem_bf951d;
const { Button, Badge, Card, Input, CitationChip, Stat, TitleBlock, BarChart, DataTable } = OE;

function Header() {
  const [active, setActive] = React.useState('Episodes');
  const items = ['Episodes', 'Blueprints', 'Newsletter', 'About'];
  return (
    <header style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '20px 48px', borderBottom: '1px solid var(--border)',
      position: 'sticky', top: 0, background: 'rgba(245,240,230,0.86)',
      backdropFilter: 'blur(8px)', zIndex: 100,
    }}>
      <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1 }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: 'var(--text-muted)' }}>The</span>
        <span style={{ fontFamily: 'var(--font-serif)', fontWeight: 600, fontSize: 22, color: 'var(--ink-900)', letterSpacing: '-0.01em' }}>Operator Economy</span>
      </div>
      <nav style={{ display: 'flex', gap: 28, alignItems: 'center' }}>
        {items.map((it) => (
          <a key={it} href="#" onClick={(e) => { e.preventDefault(); setActive(it); }}
            style={{
              fontFamily: 'var(--font-sans)', fontSize: 14, fontWeight: 500,
              color: active === it ? 'var(--ink-900)' : 'var(--text-muted)',
              borderBottom: active === it ? '2px solid var(--drafting-blue)' : '2px solid transparent',
              paddingBottom: 4, textDecoration: 'none',
            }}>{it}</a>
        ))}
        <Button variant="primary" size="sm">Get the newsletter</Button>
      </nav>
    </header>
  );
}

function Hero() {
  return (
    <section style={{ padding: '84px 48px 64px', maxWidth: 1120, margin: '0 auto' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1.15fr 0.85fr', gap: 64, alignItems: 'center' }}>
        <div>
          <div className="oe-caps" style={{ marginBottom: 20 }}>Evidence-first · No hype · Real numbers</div>
          <h1 style={{ font: 'var(--type-display)', fontSize: 60, color: 'var(--ink-900)', margin: '0 0 24px', letterSpacing: '-0.015em', lineHeight: 1.04 }}>
            The businesses you could <span style={{ color: 'var(--drafting-blue)' }}>actually</span> build.
          </h1>
          <p style={{ font: 'var(--type-lead)', color: 'var(--text-body)', maxWidth: '46ch', margin: '0 0 32px' }}>
            AI collapsed the cost of building. Every week we take one real business, source the numbers, and show you exactly how hard it is to build your own version — documentary rigor, zero hustle.
          </p>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
            <Button variant="primary" size="lg">Watch the latest breakdown</Button>
            <Button variant="ghost" size="lg">Browse the blueprint library</Button>
          </div>
        </div>
        <TitleBlock
          docNumber="Operator Blueprint №004"
          title="AI Implementation as a Service"
          fields={[
            { label: 'Date', value: '2026-06-14' },
            { label: 'Revision', value: 'B' },
            { label: 'Sources', value: '11' },
            { label: 'Read', value: '9 min' },
          ]}
        />
      </div>
    </section>
  );
}

function EvidenceFeature() {
  return (
    <section style={{ background: 'var(--ink)', padding: '72px 48px' }}>
      <div style={{ maxWidth: 1120, margin: '0 auto', display: 'grid', gridTemplateColumns: '0.9fr 1.1fr', gap: 64, alignItems: 'center' }}>
        <div>
          <div className="oe-label" style={{ color: 'var(--sage-500)', marginBottom: 16 }}>This week's thesis</div>
          <h2 style={{ font: 'var(--type-h1)', fontSize: 40, color: 'var(--paper)', margin: '0 0 20px', letterSpacing: '-0.01em' }}>
            The gap between knowing and doing is a service business.
          </h2>
          <p style={{ font: 'var(--type-body)', color: 'var(--text-on-ink-muted)', maxWidth: '42ch', margin: '0 0 28px' }}>
            Accenture booked billions installing AI it didn't build. The exact same service exists at solo scale — and businesses at every size are buying.
          </p>
          <div style={{ display: 'flex', gap: 32, marginBottom: 24 }}>
            <Stat prefix="$" value="5.9" unit="B" label="Accenture GenAI bookings" emphasis="gold" size="lg" onInk />
            <Stat prefix="$" value="2,000" label="The solo version" size="lg" onInk />
          </div>
          <CitationChip source="CIO Dive · Constellation Research" date="FY2025" onInk />
        </div>
        <Card padding="lg" style={{ background: 'var(--paper-0)' }}>
          <div className="oe-label" style={{ marginBottom: 18 }}>Accenture generative-AI bookings</div>
          <BarChart
            prefix="$" unit="B"
            data={[{ label: 'FY24', value: 3.0 }, { label: 'FY25', value: 5.9, highlight: true }]}
            source="Accenture Annual Report 2025"
            height={190}
          />
        </Card>
      </div>
    </section>
  );
}

function BlueprintLibrary() {
  const items = [
    { n: '№004', title: 'AI Implementation as a Service', read: '9 min', tag: 'Services' },
    { n: '№003', title: 'The Vertical Newsletter That Prints', read: '7 min', tag: 'Media' },
    { n: '№002', title: 'Boring SaaS for One Industry', read: '11 min', tag: 'Software' },
  ];
  return (
    <section style={{ padding: '80px 48px', maxWidth: 1120, margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 32 }}>
        <div>
          <div className="oe-label" style={{ marginBottom: 10 }}>The blueprint library</div>
          <h2 style={{ font: 'var(--type-h2)', fontSize: 32, color: 'var(--ink-900)', margin: 0 }}>Documentation a VP would save and annotate.</h2>
        </div>
        <Button variant="secondary">View all 4 blueprints</Button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20 }}>
        {items.map((it) => (
          <Card key={it.n} sheet padding="lg" style={{ display: 'flex', flexDirection: 'column', gap: 16, minHeight: 200 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="oe-caps" style={{ color: 'var(--drafting-blue)', fontWeight: 600 }}>Blueprint {it.n}</span>
              <Badge tone="neutral">{it.tag}</Badge>
            </div>
            <h3 style={{ font: 'var(--type-h3)', fontSize: 21, color: 'var(--ink-900)', margin: 0, flex: 1 }}>{it.title}</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="oe-caps">{it.read} · PDF</span>
              <a href="#" style={{ fontFamily: 'var(--font-sans)', fontSize: 14, fontWeight: 600, color: 'var(--drafting-blue)' }}>Download →</a>
            </div>
          </Card>
        ))}
      </div>
    </section>
  );
}

function Capture() {
  const [email, setEmail] = React.useState('');
  const [done, setDone] = React.useState(false);
  return (
    <section style={{ padding: '0 48px 96px', maxWidth: 1120, margin: '0 auto' }}>
      <div style={{
        border: '1.5px solid var(--rule-strong)', borderRadius: 'var(--radius-md)',
        background: 'var(--paper-0)', padding: '56px 64px',
        display: 'grid', gridTemplateColumns: '1fr 0.8fr', gap: 56, alignItems: 'center',
      }}>
        <div>
          <div className="oe-label" style={{ marginBottom: 14 }}>The Operator Economy · Monday</div>
          <h2 style={{ font: 'var(--type-h2)', fontSize: 30, color: 'var(--ink-900)', margin: '0 0 12px' }}>One business, fully sourced, every Monday.</h2>
          <p style={{ font: 'var(--type-body)', color: 'var(--text-muted)', margin: 0, maxWidth: '44ch' }}>
            Read like a research note: doc number, real figures, exact stack, named failure modes. No hype, no income promises.
          </p>
        </div>
        <div>
          {done ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <Badge tone="positive" dot>You're on the list</Badge>
              <p style={{ font: 'var(--type-body)', color: 'var(--text-muted)', margin: '6px 0 0' }}>Blueprint №004 is on its way to your inbox.</p>
            </div>
          ) : (
            <form onSubmit={(e) => { e.preventDefault(); if (email.includes('@')) setDone(true); }} style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              <label className="oe-label">Work email</label>
              <Input type="email" placeholder="you@company.com" value={email} onChange={(e) => setEmail(e.target.value)} />
              <Button variant="primary" size="lg" fullWidth type="submit">Get the free blueprint</Button>
              <span className="oe-caps" style={{ color: 'var(--text-faint)' }}>4,100+ operators · unsubscribe anytime</span>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer style={{ background: 'var(--ink)', padding: '48px', color: 'var(--text-on-ink-muted)' }}>
      <div style={{ maxWidth: 1120, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 20 }}>
        <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.1 }}>
          <span style={{ fontFamily: 'var(--font-serif)', fontWeight: 600, fontSize: 20, color: 'var(--paper)' }}>The Operator Economy</span>
          <span className="oe-caps" style={{ color: 'var(--sage-500)', marginTop: 6 }}>Build. Own. Operate.</span>
        </div>
        <div style={{ display: 'flex', gap: 24 }}>
          {['YouTube', 'Newsletter', 'LinkedIn', 'Blueprints'].map((l) => (
            <a key={l} href="#" style={{ color: 'var(--text-on-ink-muted)', fontSize: 14, fontFamily: 'var(--font-sans)' }}>{l}</a>
          ))}
        </div>
        <span className="oe-caps" style={{ color: 'var(--text-on-ink-faint)' }}>@operatoreconomy · theoperatoreconomy.com</span>
      </div>
    </footer>
  );
}

function WebsiteApp() {
  return (
    <div>
      <Header />
      <Hero />
      <EvidenceFeature />
      <BlueprintLibrary />
      <Capture />
      <Footer />
    </div>
  );
}

window.WebsiteApp = WebsiteApp;
