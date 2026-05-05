#!/usr/bin/env python3
"""
Kloudedge Control Plane - runnable hierarchy simulator (stdlib only).

Demonstrates Founder -> Orchestrator -> domain agents with evidence gates,
persistent memory, evidence storage, versioned configs, self-healing retries,
and escalations. Output deliberately avoids framework shorthand per project naming rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypedDict


# --- Typed handoff (structured dict contract) --------------------------------


class HandoffReport(TypedDict):
    agent: str
    phase_id: str
    summary: str
    artifacts: list[str]
    acceptance_met: bool
    blockers: list[str]


def evidence_gate(report: HandoffReport) -> tuple[bool, str]:
    """Evidence gate - discrete pass/fail check before phase closure."""
    if not report.get("acceptance_met"):
        return False, "acceptance criteria not met"
    if not report.get("artifacts"):
        return False, "missing verifiable artifacts"
    if any(report.get("blockers") or []):
        return False, "open blockers recorded"
    return True, "gate cleared"


# --- Infrastructure substrates -----------------------------------------------


class PersistentMemory:
    """Cross-agent shared context (minimal persistent memory store)."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def write(self, key: str, value: Any) -> None:
        self._data[key] = value

    def read(self, key: str) -> Any:
        return self._data.get(key)


class AuditLog:
    """Append-only observability trail for every simulated event."""

    def __init__(self) -> None:
        self._lines: list[str] = []

    def emit(self, tag: str, message: str) -> None:
        prefix = f"[{tag}]".ljust(15)
        line = f"{prefix}{message}"
        print(line)
        self._lines.append(line)

    def dump_footer(self, title: str = "--- AUDIT LOG ---") -> None:
        print(title)
        for line in self._lines:
            print(line)


class EvidenceStore:
    """Append-only evidence outputs routed post gate PASS."""

    def __init__(self, audit: AuditLog) -> None:
        self._records: list[dict[str, Any]] = []
        self._audit = audit

    def append(self, report: HandoffReport, *, note: str = "") -> None:
        entry = {
            "agent": report["agent"],
            "phase_id": report["phase_id"],
            "summary": report["summary"],
            "artifacts": list(report["artifacts"]),
            "note": note,
        }
        self._records.append(entry)

    @property
    def entries(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._records)


class VersionRegistry:
    """Tracks immutable snapshots of agent configs; enables rollback."""

    def __init__(self, audit: AuditLog) -> None:
        self._history: dict[str, list[dict[str, Any]]] = {}
        self._audit = audit

    def record_run(self, agent: str, config: dict[str, Any]) -> int:
        self._history.setdefault(agent, []).append(dict(config))
        version = len(self._history[agent])
        self._audit.emit("VERSION", f"{agent} config snapshot recorded - v{version}")
        return version

    def record_adjustment(self, agent: str, adjustment: str, new_config: dict[str, Any]) -> int:
        self._audit.emit(
            "VERSION",
            f"{agent} config adjustment logged ({adjustment}) - versioning before retry",
        )
        return self.record_run(agent, new_config)

    def rollback_last(self, agent: str) -> dict[str, Any]:
        hist = self._history.setdefault(agent, [])
        if len(hist) < 2:
            raise ValueError("insufficient history for rollback")
        hist.pop()
        restored = dict(hist[-1])
        self._audit.emit("VERSION", f"{agent} rollback applied - restored prior snapshot")
        return restored


# --- Hierarchy ---------------------------------------------------------------


@dataclass
class Founder:
    audit: AuditLog

    def assign_priority(self, task_title: str) -> None:
        self.audit.emit("FOUNDER", f"Task received: {task_title}")

    def acknowledge_completion(self, note: str) -> None:
        self.audit.emit("FOUNDER", note)

    def receive_escalation(self, evidence_trail: str) -> None:
        self.audit.emit(
            "FOUNDER",
            f"Escalation requires decision - evidence trail: {evidence_trail}",
        )


class Orchestrator:
    """Kloudedge Control Plane - routing, confirmations, retries, escalations."""

    def __init__(
        self,
        founder: Founder,
        memory: PersistentMemory,
        evidence: EvidenceStore,
        versions: VersionRegistry,
        audit: AuditLog,
        *,
        max_self_heal_attempts: int = 1,
    ) -> None:
        self.founder = founder
        self.memory = memory
        self.evidence = evidence
        self.versions = versions
        self.audit = audit
        self.max_self_heal_attempts = max_self_heal_attempts

    def dispatch(self, agent_label: str, detail: str) -> None:
        self.audit.emit("ORCHESTRATOR", f"Dispatching to {agent_label} - {detail}")

    def gate_check(self, agent_label: str, report: HandoffReport) -> tuple[bool, str]:
        ok, reason = evidence_gate(report)
        status = "PASS" if ok else "FAIL"
        self.audit.emit("GATE", f"{agent_label} handoff - {status} ({reason})")
        return ok, reason

    def store_evidence(self, report: HandoffReport, note: str = "") -> None:
        self.evidence.append(report, note=note)
        self.audit.emit("EVIDENCE", "Output stored")

    def phase_confirmation_summary(self, phases: list[str]) -> None:
        joined = ", ".join(phases)
        self.audit.emit(
            "ORCHESTRATOR",
            f"All phases confirmed ({joined}). Reporting to Founder.",
        )

    def report_adaptive_feedback(self, agent_label: str, feedback: str) -> None:
        self.audit.emit("ADAPTIVE", f"Feedback absorbed - {agent_label}: {feedback}")

    def escalate_to_founder(self, trail: str) -> None:
        self.audit.emit("ESCALATION", "Self-healing exhausted - forwarding to Founder")
        self.founder.receive_escalation(trail)


class SalesAgent:
    name = "SalesAgent"

    def __init__(self, memory: PersistentMemory, audit: AuditLog) -> None:
        self.memory = memory
        self.audit = audit

    def execute(self, phase_id: str, task: str, *, acceptance_met: bool = True) -> HandoffReport:
        self.audit.emit("SALES", "Executing - writing to memory")
        self.memory.write(
            f"{self.name}:{phase_id}",
            {"task": task, "pipeline_segment": "enterprise"},
        )
        return HandoffReport(
            agent=self.name,
            phase_id=phase_id,
            summary=f"Qualified outreach wave for {task}",
            artifacts=[f"{phase_id}-call-sheet.json", f"{phase_id}-crm-notes.md"],
            acceptance_met=acceptance_met,
            blockers=[],
        )


class MarketingAgent:
    name = "MarketingAgent"

    def __init__(self, memory: PersistentMemory, audit: AuditLog) -> None:
        self.memory = memory
        self.audit = audit

    def execute(self, phase_id: str, campaign: str, *, acceptance_met: bool = True) -> HandoffReport:
        self.audit.emit("MARKETING", "Executing - writing to memory")
        ctx = self.memory.read("SalesAgent:launch-ready") or {}
        blended = {"campaign": campaign, "prior_sales_context": ctx}
        self.memory.write(f"{self.name}:{phase_id}", blended)
        return HandoffReport(
            agent=self.name,
            phase_id=phase_id,
            summary=f"Campaign assets assembled for {campaign}",
            artifacts=[f"{phase_id}-content-pack.zip", f"{phase_id}-distribution-plan.md"],
            acceptance_met=acceptance_met,
            blockers=[],
        )


class DevOpsAgent:
    name = "DevOpsAgent"

    def __init__(self, memory: PersistentMemory, audit: AuditLog) -> None:
        self.memory = memory
        self.audit = audit
        self.config = {"timeout_ms": 2000, "retry_budget": 1}

    def execute(self, phase_id: str, workload: str, *, acceptance_met: bool = True) -> HandoffReport:
        self.audit.emit("DEVOPS", "Executing - writing to memory")
        self.memory.write(
            f"{self.name}:{phase_id}",
            {"workload": workload, "config": dict(self.config)},
        )
        artifacts = []
        if acceptance_met:
            artifacts = [f"{phase_id}-deploy-manifest.yaml", f"{phase_id}-monitoring-hooks.json"]
        report = HandoffReport(
            agent=self.name,
            phase_id=phase_id,
            summary=f"Infrastructure delta prepared for {workload}",
            artifacts=artifacts,
            acceptance_met=acceptance_met,
            blockers=[] if acceptance_met else ["deployment probe threshold breached"],
        )
        return report

    def apply_self_heal_adjustment(self) -> None:
        self.config["timeout_ms"] = min(self.config["timeout_ms"] + 1500, 8000)
        self.config["retry_budget"] = max(self.config["retry_budget"], 1)


# --- Scenario runners --------------------------------------------------------


def _pad_banner(title: str) -> None:
    bar = "=" * len(title)
    print(bar)
    print(title)
    print(bar)


def scenario_happy_path() -> None:
    _pad_banner("PATH 1 - HAPPY PATH (Sales -> Marketing inter-agent contract)")
    audit = AuditLog()
    memory = PersistentMemory()
    evidence = EvidenceStore(audit)
    versions = VersionRegistry(audit)
    founder = Founder(audit)
    orch = Orchestrator(founder, memory, evidence, versions, audit)

    founder.assign_priority("Deploy Kloudedge Control Plane")

    sales = SalesAgent(memory, audit)
    marketing = MarketingAgent(memory, audit)

    orch.dispatch(sales.name, "Enterprise pipeline warm-up")
    versions.record_run(sales.name, {"plays": ["enterprise-intro", "exec-follow-up"]})
    sales_report = sales.execute("phase-sales-launch", "Enterprise pipeline warm-up", acceptance_met=True)
    ok, _ = orch.gate_check(sales.name, sales_report)
    if ok:
        orch.store_evidence(sales_report)

    orch.audit.emit("SALES->MKTG", "Inter-agent handoff: qualified lead")
    memory.write(
        "SalesAgent:launch-ready",
        {"qualified_accounts": ["Contoso MENA", "Fabrikam Gulf"], "warmth": "high"},
    )

    orch.dispatch(marketing.name, "Campaign build from qualified leads")
    versions.record_run(marketing.name, {"tone": "regulated-B2B", "channels": ["email", "linkedin"]})
    m_report = marketing.execute("phase-marketing-launch", "Regulated B2B nurture", acceptance_met=True)
    ok_m, _ = orch.gate_check(marketing.name, m_report)
    if ok_m:
        orch.store_evidence(m_report)

    orch.phase_confirmation_summary(["phase-sales-launch", "phase-marketing-launch"])
    founder.acknowledge_completion("Complete. Evidence on file.")
    orch.report_adaptive_feedback(
        marketing.name,
        "Insights from gate PASS fed forward - configs stable for next orchestration cycle",
    )

    audit.dump_footer()


def scenario_self_healing() -> None:
    _pad_banner("PATH 2 - SELF-HEALING (DevOps gate FAIL -> retry -> PASS)")
    audit = AuditLog()
    memory = PersistentMemory()
    evidence = EvidenceStore(audit)
    versions = VersionRegistry(audit)
    founder = Founder(audit)
    orch = Orchestrator(founder, memory, evidence, versions, audit, max_self_heal_attempts=1)

    founder.assign_priority("Harden deployment probes for Kloudedge stack")

    devops = DevOpsAgent(memory, audit)
    orch.dispatch(devops.name, "Canary deploy + probe sweep")

    attempts = 0
    passed = False
    while attempts <= orch.max_self_heal_attempts:
        acceptance = attempts > 0  # fail first attempt, pass on retry
        report = devops.execute(
            "phase-devops-canary",
            "Canary deploy + probe sweep",
            acceptance_met=acceptance,
        )
        ok, reason = orch.gate_check(devops.name, report)
        if ok:
            versions.record_run(devops.name, dict(devops.config))
            orch.store_evidence(report, note="post self-healing PASS")
            orch.report_adaptive_feedback(
                devops.name,
                "Config update applied after gate FAIL - proceeding to next run",
            )
            passed = True
            break

        attempts += 1
        if attempts <= orch.max_self_heal_attempts:
            audit.emit("SELF_HEAL", "Failure detected - auto-retry with orchestrator-guided adjustment")
            devops.apply_self_heal_adjustment()
            versions.record_adjustment(
                devops.name,
                "increased probe timeout after gate FAIL",
                dict(devops.config),
            )
            orch.report_adaptive_feedback(
                devops.name,
                "Feedback routed through adaptive loop - retry scheduled",
            )

    if passed:
        orch.phase_confirmation_summary(["phase-devops-canary"])
        founder.acknowledge_completion("Resolved via self-healing - escalation not required.")

    audit.dump_footer()


def scenario_escalation() -> None:
    _pad_banner("PATH 3 - ESCALATION (DevOps exhausts retries -> Founder)")
    audit = AuditLog()
    memory = PersistentMemory()
    evidence = EvidenceStore(audit)
    versions = VersionRegistry(audit)
    founder = Founder(audit)
    orch = Orchestrator(founder, memory, evidence, versions, audit, max_self_heal_attempts=1)

    founder.assign_priority("Restore production deployment lane")

    devops = DevOpsAgent(memory, audit)
    orch.dispatch(devops.name, "Hotfix rollout with strict probe gates")

    trail_parts: list[str] = []
    for attempt in range(2):
        report = devops.execute(
            "phase-devops-hotfix",
            "Hotfix rollout with strict probe gates",
            acceptance_met=False,  # persistently failing scenario
        )
        ok, reason = orch.gate_check(devops.name, report)
        trail_parts.append(f"attempt {attempt + 1}: FAIL ({reason})")
        if ok:
            break
        if attempt == 0:
            audit.emit("SELF_HEAL", "Failure detected - auto-retry with orchestrator-guided adjustment")
            devops.apply_self_heal_adjustment()
            versions.record_adjustment(
                devops.name,
                "expanded probe window - regression persists",
                dict(devops.config),
            )
        else:
            orch.escalate_to_founder("; ".join(trail_parts))

    audit.dump_footer()


def main() -> None:
    scenario_happy_path()
    print()
    scenario_self_healing()
    print()
    scenario_escalation()


if __name__ == "__main__":
    main()
