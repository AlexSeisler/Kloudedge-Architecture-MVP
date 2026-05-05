# Diagram — Target State (ACS Control Plane)

Governance layer on top of execution: hierarchy, handoff contracts, **confirm-before-dispatch** through an **evidence gate**, **escalation** that runs **upward only**, **shared state** all layers read/write, and an **execution log** that mirrors runs for audit.

```mermaid
flowchart TD
  GM[GM]

  SA[System Architect]

  EG["Evidence gate<br/>client deliverable"]

  EA[Execution Agent]

  SS[(Shared state<br/>platform stickiness)]

  LOG["Execution log / observability<br/>audit trail"]

  GM -->|handoff contract| SA
  SA -->|handoff contract| GM

  SA -->|phase brief — dispatch| EA
  EA -->|structured handoff + artifacts| EG
  EG -->|confirm-before-dispatch| SA

  EA -.->|escalation| SA
  SA -.->|escalation| GM

  GM --- SS
  SA --- SS
  EA --- SS

  LOG -.->|mirrors| GM
  LOG -.->|mirrors| SA
  LOG -.->|mirrors| EA
  LOG -.->|mirrors| EG
```

**Business labels**

| Element | Meaning |
|--------|---------|
| Evidence gate | **Client deliverable** — verifiable outputs buyers can defend internally (what shipped, validated, escalated, locked). |
| Execution log | **Audit trail** — what ran, what passed gates, what escalated; substrate for enterprise trust. |
| Shared state | **Platform stickiness** — durable context and obligations compound instead of evaporating between phases. |
