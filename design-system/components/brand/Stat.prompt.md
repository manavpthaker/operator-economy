**Stat** — a single published figure in mono numerals. Every number the channel shows uses this; the figure is the focal point, not decoration.

```jsx
<Stat prefix="$" value="5.9" unit="B" label="Accenture GenAI bookings" emphasis="gold" size="lg" />
<Stat value="31" unit="%" label="Gross margin" delta="2×" deltaDirection="up" />
<Stat prefix="$" value="2,000" label="Solo version" onInk size="xl" />  {/* thumbnail */}
```

`emphasis="gold"` marks the one key figure per view. `size` scales sm→xl. `deltaDirection` up=sage, down=brick.
