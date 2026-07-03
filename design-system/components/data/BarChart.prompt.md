**BarChart** — a custom chart that reads as institutional research, never default Excel. Blue bars, mono value labels, one optional gold highlight bar, sourced footer.

```jsx
<BarChart
  prefix="$" unit="B"
  data={[
    { label: 'FY24', value: 3.0 },
    { label: 'FY25', value: 5.9, highlight: true },
  ]}
  source="Accenture Annual Report 2025"
/>
```

Mark one bar `highlight` for the gold key figure. Pass `format` for custom value labels.
