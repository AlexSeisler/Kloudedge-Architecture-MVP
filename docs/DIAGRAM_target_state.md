# Diagram — Target State (Kloudedge Control Plane)

Governed stack: **Founder → Kloudedge Control Plane (Orchestrator) → domain agents → Infrastructure + Systems Layer**, with **inter-agent contracts**, cross-cutting **self-healing**, **adaptive loop**, **versioned configs**, **persistent memory**, **observability**, and the **engine / product / data substrates** that turn workflows into something buyers can deploy.

```mermaid
flowchart TD
  subgraph L0["Layer 0 — Founder / Command"]
    FD["Founder<br/>priorities · evidence summaries · escalation decisions<br/>does not operate agents directly"]
  end

  subgraph L1["Layer 1 — Kloudedge Control Plane"]
    CP["Orchestrator<br/>routing · handoff contracts · agent config registry"]
    PMEM[(Persistent memory<br/>platform stickiness)]
    VCTL["Version control<br/>rollback on regression"]
    CP --- PMEM
    CP --- VCTL
  end

  subgraph L2["Layer 2 — Domain agents"]
    SALES["Sales Agent<br/>outreach · pipeline · follow-up"]
    MKT["Marketing Agent<br/>content · distribution · campaigns"]
    DEV["DevOps Agent<br/>infra · deploy · monitoring"]
    MORE["Additional Agents<br/>extensible"]
  end

  subgraph L3["Layer 3 — Infrastructure + Systems Layer"]
    direction LR
    subgraph COL_A["Automation Substrate — the engine"]
      direction TB
      WF[Workflow engine<br/>triggers · schedulers · event hooks]
      API[API integration layer<br/>CRM · email · calendar · social · data]
      BUS[Webhook + event bus<br/>inter-system triggers · responses]
      WF --> API --> BUS
    end
    subgraph COL_B["Systems Powered — the product clients buy<br/>what the agents power"]
      direction TB
      SALESOS[Sales OS<br/>pipeline · outreach sequences · follow-up automation]
      MARKOS[Marketing OS<br/>content calendar · distribution · campaign analytics]
      DEVOS[DevOps OS<br/>deploy pipeline · infra monitoring · alert routing]
    end
    subgraph COL_C["Data + Memory Substrate — the compounding advantage"]
      direction TB
      PMSTORE[(Persistent memory store<br/>cross-agent shared context)]
      KB[(Knowledge base<br/>domain-specific · per vertical)]
      EVSTORE[(Evidence store<br/>compliance-ready · client-facing proof)]
      AUDLOG[(Audit log<br/>immutable operational record)]
    end
  end

  subgraph CC_SH["Cross-cutting — Self-healing"]
    DET[Failure detection]
    RET[Auto-retry]
    TRG[Escalation trigger]
    DET --> RET --> TRG
  end

  subgraph CC_AD["Adaptive loop — self-improving system"]
    EG["Evidence gate<br/>client deliverable"]
    FB[Feedback]
    CU[Config update]
    EG --> FB --> CU --> NR[Next run]
  end

  OBS["Observability<br/>execution log · pipeline health · escalation trail<br/>audit trail"]

  FD -->|priorities · policies| CP
  CP -->|evidence summary · escalation needing decision| FD

  CP -->|dispatch · routing| SALES
  CP -->|dispatch · routing| MKT
  CP -->|dispatch · routing| DEV
  CP -->|dispatch · routing| MORE

  SALES -->|qualified lead handoff| MKT
  MKT -->|campaign deploy trigger| DEV

  SALES -->|output| EG
  MKT -->|output| EG
  DEV -->|output| EG
  MORE -->|output| EG

  SALES -->|escalation · state update| CP
  MKT -->|escalation · state update| CP
  DEV -->|escalation · state update| CP
  MORE -->|escalation · state update| CP

  CU --> VCTL
  NR --> CP

  DET -.-> SALES
  DET -.-> MKT
  DET -.-> DEV
  DET -.-> MORE
  RET -.-> SALES
  RET -.-> MKT
  RET -.-> DEV
  RET -.-> MORE
  TRG --> CP

  PMEM -.-> SALES
  PMEM -.-> MKT
  PMEM -.-> DEV
  PMEM -.-> MORE

  SALES --> SALESOS
  SALESOS --> SALES
  MKT --> MARKOS
  MARKOS --> MKT
  DEV --> DEVOS
  DEVOS --> DEV

  SALES -->|event hooks| WF
  MKT -->|event hooks| WF
  DEV -->|event hooks| WF
  MORE -->|event hooks| WF

  SALES -->|read/write| PMSTORE
  PMSTORE -->|read/write| SALES
  MKT -->|read/write| PMSTORE
  PMSTORE -->|read/write| MKT
  DEV -->|read/write| PMSTORE
  PMSTORE -->|read/write| DEV
  MORE -->|read/write| PMSTORE
  PMSTORE -->|read/write| MORE

  SALES -->|read/write| KB
  KB -->|read/write| SALES
  MKT -->|read/write| KB
  KB -->|read/write| MKT
  DEV -->|read/write| KB
  KB -->|read/write| DEV
  MORE -->|read/write| KB
  KB -->|read/write| MORE

  EVSTORE --> EG
  AUDLOG --> OBS

  OBS -.-> CP
  OBS -.-> SALES
  OBS -.-> MKT
  OBS -.-> DEV
  OBS -.-> MORE
  OBS -.-> EG
```

**Business labels on key nodes**

| Node | Label |
|------|--------|
| Evidence gate | **client deliverable** |
| Execution log (inside Observability) | **audit trail** |
| Version control | **rollback on regression** |
| Persistent memory | **platform stickiness** |
| Adaptive loop | **self-improving system** |
| Automation Substrate | **the engine** |
| Systems Powered | **the product clients buy** / **what the agents power** |
| Data + Memory Substrate | **the compounding advantage** |
