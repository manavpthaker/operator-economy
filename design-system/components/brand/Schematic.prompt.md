**Schematic** — the navy working-schematic panel (drafting grid, sheet tag, RUNNING status, wired nodes, measurement bracket, sourced footer). The centerpiece of the brand's "the business you're going to build" motif.

```jsx
<Schematic sheet={1} total={5} title="The stack" bracket="≤ $100/mo"
  source="Sacra · Apr 2026" footer={<>Margin 94% <span style={{color:'var(--status-live)'}}>▲</span></>}>
  <SchematicNode step="Step 01 · Intake" name="Airtable client portal" figure="$0" unit="/mo" status="Live" />
  <SchematicNode step="Step 02 · The brain" name="Claude API" figure="$20" unit="/mo" status="Running" />
  <SchematicNode step="Step 04 · Delivery" name="First client project" figure="$2,000" highlight />
</Schematic>
```

Rules: every node = real figure; `source` is required in spirit — a schematic without sources is a violation; sage = status only; gold = the one output figure.
