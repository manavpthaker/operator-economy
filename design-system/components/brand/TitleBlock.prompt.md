**TitleBlock** — the drafting title block on every blueprint PDF, end-card, and chart. Signals a versioned, sourced *document*.

```jsx
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
```

Use `onInk` for the dark video end-card. Keep field values in mono (component sets this).
