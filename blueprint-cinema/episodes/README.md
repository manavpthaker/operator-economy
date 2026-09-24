# Blueprint Cinema episodes

Each episode uses a sortable canonical folder name:

```text
EP###-slug
```

Examples:

```text
EP006-direct-booking-recovery
EP007-example-slug
EP042-example-slug
```

The future episode identity record will store matching `episode_number`, `episode_code`, `slug`, and `folder_name` values. Episode numbers are explicit; they are never inferred from directory order.

These directories contain Blueprint Cinema visual-production state only. Research, scripts, VO, and word timings remain in `studio/originate/<slug>/` and are consumed through a hash-pinned input lock.

The documentation-canonical episode shape adds:

```text
direction/                 # bible, rhythm map, lookdev, treatments, shot board
hyperframes/               # canonical episode motion and directed-animatic project
assets/                    # manifest, candidates, selects, source, derivatives, proxies
edit/                      # edit and sound plans, handoff, Resolve records, reports
review/                    # artifact-bound findings and approvals
delivery/                  # ignored media plus tracked manifests and QC
```

See `../templates/episode/README.md` for the complete target scaffold. The current v1 initializer does not create or enforce every target artifact yet; do not confuse a hand-created scaffold with a completed gate.
