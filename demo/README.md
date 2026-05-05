# Kloudedge Control Plane simulator (Python)

Runnable, stdlib-only script that walks three scripted paths through the same hierarchy and infrastructure concepts shown in `docs/DIAGRAM_target_state.md`: Founder command layer, **Kloudedge Control Plane** (`Orchestrator` in code), domain agents, evidence gates, persistent memory, append-only evidence and audit trails, versioned configs, self-healing retries, and escalation.

## Run

From the repository root:

```bash
python demo/acs_demo.py
```

No virtual environment or `pip install` is required.

Log lines use ASCII punctuation so output stays readable on Windows terminals (`cp1252`) as well as UTF-8.

## What you will see

The script runs **three scenarios back-to-back**, each with its own fresh memory, evidence store, audit log, and version history:

1. **Happy path** – Founder sets a priority; the control plane dispatches **SalesAgent**, the evidence gate passes, outputs land in the evidence store; a **Sales → Marketing** inter-agent handoff (qualified lead) runs; **MarketingAgent** executes and passes the gate; the orchestrator confirms phases and reports completion to the Founder; adaptive feedback closes the loop.

2. **Self-healing path** – **DevOpsAgent** fails the gate once (no valid acceptance / artifacts); the orchestrator triggers an auto-retry with a **VersionRegistry**-logged config adjustment; the second run passes; escalation to the Founder is **not** used.

3. **Escalation path** – **DevOpsAgent** fails the gate twice after retry; the orchestrator raises an **escalation** to the Founder with a short evidence trail string; the audit log records the full sequence.

Each scenario ends with a replay block titled `--- AUDIT LOG ---` listing everything emitted during that run.

## Class map (code ↔ architecture)

| Class / function | Role in the real Kloudedge picture |
|------------------|-------------------------------------|
| `Founder` | Command layer: priorities in, completion and escalations out—does not operate agents directly. |
| `Orchestrator` | **Kloudedge Control Plane**: dispatch, gate coordination, evidence persistence decisions, self-healing retry loop, escalation routing. |
| `SalesAgent`, `MarketingAgent`, `DevOpsAgent` | Domain agents aligned with the diagram (sales / marketing / DevOps). |
| `HandoffReport` (typed dict) | Structured phase handoff—same shape every agent returns. |
| `evidence_gate()` | Discrete gate function (pass/fail + reason)—not inlined in orchestrator logic. |
| `PersistentMemory` | Shared context store agents read/write (diagram “persistent memory store” idea). |
| `EvidenceStore` | Append-only store for gate-approved outputs (client-facing proof path). |
| `AuditLog` | Append-only observability trail (terminal + replay footer). |
| `VersionRegistry` | Config snapshots per agent run; adjustments on retry; `rollback_last()` available for regression rollback demos. |

## Why this matters (beyond the script)

Regulated B2B buyers do not fund “clever chats”—they fund **repeatable systems** with named phases, verifiable outputs, and trails they can defend. This simulator is deliberately boring code: it shows that **governance** (gates, evidence, audit, versioning, escalation) can sit beside **execution** (agents) so the offer reads as infrastructure and product depth, not one-off automation—matching the narrative in `docs/MEMO_kloudedge_architecture.md` without tying the story to any vendor framework.
