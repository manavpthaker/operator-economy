# Private review-page scaffold

`index.html` is self-contained and inactive. It has the current r4 colors, one heading, a full-film player, 16 presenter jump positions from the unchanged timeline, and optional comparison players. It uses native controls, inline playback, metadata preloading, responsive widths and 44 px minimum jump buttons. Starting one player pauses the others.

Fill the `review-config` JSON block only after the exact media exists:

```json
{
  "status": "Private review candidate",
  "fullFilm": { "src": "r5-look-transfer/EXACT-FULL-FILE.mp4" },
  "comparisons": [
    { "label": "Presenter comparison", "src": "r5-look-transfer/pilots/EXACT-COMPARISON.mp4" }
  ]
}
```

Retain the other configuration fields and exact frame-based jumps. URLs must be relative to the deployed page and remain on its origin. Default `fullFilm: null` and `comparisons: []` create **no media elements or requests**. Unconfigured media is omitted. A configured video that errors is removed rather than leaving a broken player. The full-film jumps appear only after its metadata loads.

The default status makes no owner-acceptance, lip-sync or performance-pass claim. Set final review wording to the actual QA state. The page contains no analytics, remote dependencies or external media requests. Its `noindex` tag is not access control: root must deploy only behind the existing private service.

This task did not copy the scaffold to live QA, configure any artifact URL, change the r4 page, start/modify a service, change Tailscale/public 443, or commit. Root owns final media configuration and deployment through the existing private 3071 tailnet route.
