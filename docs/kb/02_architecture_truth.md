# Architecture Truth

The public evidence shows a real multi-agent system, but not yet a fully hardened enterprise control plane. Nikhill Sood says he runs 11–14 agents, has a real-time command center, uses persistent memory, inter-agent communication, scheduling, and a dashboard that tracks status, blockers, pipeline metrics, and infrastructure health. [web:38][file:4]

He also publicly frames the system around ownership contracts, reliability contracts, evidence gates, blast-radius limits, rollback, and escalation ladders. That is meaningful architecture thinking; it implies he understands the control problem and has implemented at least some of the operational patterns. [file:4]

The likely stack is a mix of LangGraph for orchestration and n8n-style automation glue, with Azure as the hosting and integration substrate. He publicly described a 5-day SaaS build on Azure with 11 AI agents, and his posts explicitly reference self-learning systems built with n8n and DeepSeek R1. [web:30][web:38]

What still looks missing is the compounding layer: durable shared state across workflows, clean hierarchy between founder, orchestrator, and specialist agents, traceable handoff protocol, and first-class observability tied to business outcomes. In other words, he seems to have real orchestration concepts, but the enterprise-grade operating system is still the gap. [file:2][web:38]
