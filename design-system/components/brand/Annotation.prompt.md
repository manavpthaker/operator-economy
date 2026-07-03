**Annotation** — a measurement-style bracket + small-caps label calling out content, as if a schematic were being explained.

```jsx
<Annotation label="Retainer floor" side="right">
  <Stat prefix="$" value="500–5,000" unit="/mo" />
</Annotation>
<Annotation label="Where the margin lives" side="bottom" color="var(--gold-500)">
  <img src="chart.png" alt="" />
</Annotation>
```

`side`: left / right / top / bottom. Keep labels short (~2–4 words).
