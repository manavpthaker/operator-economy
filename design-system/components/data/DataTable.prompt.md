**DataTable** — a ledger. Mono numerals in numeric columns, hairline rules, a sourced footer. Set `numeric` on money/count columns.

```jsx
<DataTable
  columns={[
    { key: 'tier', label: 'Tier' },
    { key: 'price', label: 'First project', numeric: true },
    { key: 'retainer', label: 'Monthly retainer', numeric: true },
  ]}
  rows={[
    { tier: 'Freelancer', price: '$2,000', retainer: '$500' },
    { tier: 'Boutique', price: '$8,000', retainer: '$3,000' },
  ]}
  source="Creator reports; ranges consistent — estimate"
/>
```
