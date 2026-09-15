# Agent work packets

This folder is reserved for machine-validated work orders and isolated deliverables described in `../../../AGENT-WORKFLOWS.md`.

The implemented packet layout is:

```text
agents/
├── work-orders/
│   └── <work-order-id>.json
└── deliverables/
    └── <work-order-id>/
        ├── deliverable.json
        └── proposed files or report
```

Workers may write only to their assigned deliverable directory. The orchestrator alone merges canonical episode artifacts and advances gates.

Three hash-pinned read-only QA work orders and deliverable packets are present. Their `complete` status means the assigned packet passed its order; it never records an approval or changes production state.
