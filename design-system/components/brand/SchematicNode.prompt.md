**SchematicNode** — one labeled node of the working schematic. **Rule: every node carries a real figure** (and the panel cites its source); placeholder nodes are banned.

```jsx
<SchematicNode step="Step 02 · The brain" name="Claude API" figure="$20" unit="/mo" status="Running" />
<SchematicNode step="Step 04 · Delivery" name="First client project" figure="$2,000" highlight />
```

`highlight` = gold, one per panel (the output). `status` is sage and means live/verified only. Compose inside `<Schematic>`.
