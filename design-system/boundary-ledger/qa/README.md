# Boundary Ledger QA

Boundary Ledger has separate evidence gates for semantic integrity, static web behavior, browser motion references, and encoded media. Passing one gate does not imply that another passed.

## 1. Semantic system

Run from the repository root:

```bash
node design-system/boundary-ledger/qa/validate-system.mjs
```

The dependency-free validator checks the package version and hashes, core role and operation IDs, all color/motion/sound bindings, specimen timing and caption policy, actual-PCM trace provenance, reference-asset identity, entrypoint existence, and the retirement register.

It must fail if a binding invents a role or operation, an identity hash drifts, two commitment loci overlap, a caption duplicates an embedded phrase, a format is crop-based, or a retired consumer is allowed for new work.

## 2. Static web reference

Required viewport checks: `1280`, `933`, `390`, `373`, and `320` CSS pixels.

At every width verify:

- `document.documentElement.scrollWidth === document.documentElement.clientWidth` without overflow masking;
- the working-model image reports `1536 × 1024`, remains 3:2, and uses `object-fit: contain`;
- the complete hotel–OTA–guest relationship and oxide return path remain visible;
- the feature docket attaches by 16px and covers only the drawing's quiet top edge;
- mobile keeps 24px content gutters, an inset docket, and full-bleed working paper;
- keyboard targets are at least 44 CSS pixels in their relevant logical dimension;
- oxide focus is visible on paper and bright oxide focus is visible on mineral;
- source order remains coherent without layout CSS;
- reduced-motion mode removes smooth scrolling and animated transitions.

[`contrast.json`](./contrast.json) records the tested text and focus pairs. Recalculate it when any foreground or background token changes.

[`responsive-harness.html`](./responsive-harness.html) loads the real field manual in fixed-width, same-origin frames. It exists for inspection only and is not a public page pattern.

[`verification-2026-09-02.json`](./verification-2026-09-02.json) records the browser measurements for the locked 1.0.0 web reference. The cross-media promotion does not invalidate those measurements because it does not change the web palette, components, or locked illustration.

## 3. Browser motion and audio reference

The interactive specimen is a design reference, not a production runtime or encoded master. Check both treatments at `9:16`, `1:1`, and `16:9`:

- the same delivered audio continues when treatment or format changes;
- the trace is built from the precomputed actual-PCM envelope;
- semantic state changes follow spoken operations rather than amplitude peaks;
- the steel introduction is represented before the oxide return path;
- only one oxide commitment is active at a time;
- captions use `drop / rail / embed` and never duplicate the embedded thesis phrase;
- the model-led and text-led treatments reach a readable settled state;
- every aspect ratio is re-composed and has no horizontal overflow;
- the `390` and `320` CSS-pixel views remain usable;
- browser console logs contain no current initialization or media errors.

[`cross-media-verification-2026-09-02.json`](./cross-media-verification-2026-09-02.json) records this reference-level review and its explicit limitations.

## 4. Motion-ready asset gate

The approved hotel JPEG is a flattened still. It does not pass this gate. A production derivative must satisfy [`motion-ready-asset.schema.json`](../motion-ready-asset.schema.json) and the cross-file validator, including persistent object IDs, independent layer and mask identities, hashes, dimensions, route endpoints, evidence IDs, and a review record. Roughness must be authored; a polished path plus wobble is not equivalent.

## 5. Encoded-media gate

Only Blueprint Cinema, HyperFrames, and Resolve output can satisfy this gate. A browser specimen cannot.

Required evidence includes:

- deterministic root-audio timing and exact input hashes;
- entry, action, consequence, and settle snapshots;
- strict runtime checks and an assembled animation-map review;
- encoded duration, aspect ratio, dimensions, frame rate, codec, color tags, and audio-stream probes;
- phone-scale fine-line and caption-over-content inspection after compression;
- black-frame, flash, freeze, and unintended-silence checks;
- integrated loudness, true peak, phase/channel layout, sample rate, and intelligibility review;
- a normal-speed human review of the encoded master.

Until these pass, motion and sound bindings remain provisional and `encodedMediaChecked` stays `false`.
