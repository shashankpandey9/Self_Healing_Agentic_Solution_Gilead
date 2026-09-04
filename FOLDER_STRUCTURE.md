# Folder Structure Guide

This repository currently contains **only the folder structure** the team will develop
against — no implementation code or deployment automation yet (that comes later). This
document explains what each folder is for and where new code should go once work starts.

Framework decisions to follow when code is added:
- **LangGraph** for each agent's internal reasoning (one state graph per agent).
- **A2A (Agent2Agent) protocol** for agent-to-agent communication.
- **No MCP** — agents call their own capabilities directly instead of through an MCP client/server.

## Top-level layout

```
├── agents/                # Multi-agent system (Supervisor, Classifier, Operator, Ticketing, Log Retriever)
├── infrastructure/         # Provisioning for the solution's own AWS resources (DynamoDB, EventBridge, SQS, ...)
├── step_functions/         # Step Functions state machine (ASL) definitions
├── lambda_functions/       # Standalone Lambda handlers (incident logging, event routing)
├── knowledge_base/         # RCA documents, business rules, app docs used by the Bedrock KB
├── terraform/              # IaC modules the Operator Agent will apply to remediate workloads
├── tests/                  # Unit and integration tests
├── scripts/                # Local dev / deployment helper scripts (added later)
├── docs/                   # Architecture and process documentation
└── .github/workflows/      # CI/CD pipelines (added later)
```

## How to use each folder

### `agents/`
One subfolder per agent, plus `common/` for shared code. When implementing an agent, add:
- `state.py` — the LangGraph `TypedDict` state for that agent.
- `agent.py` — the agent's compiled `StateGraph`, exposed over A2A.
- `tools.py` — direct function-calling capabilities (no MCP).

Put anything reused across agents (base agent class, AWS client factory, config loading,
A2A client/server helpers, model provider factory) in `agents/common/`.

### `infrastructure/`
Provisioning for the solution's *own* AWS resources: the incident DynamoDB table, the
EventBridge rule, the SQS FIFO queue, the Step Functions state machine, the Bedrock
Knowledge Base, SES identity, and IAM roles. One file/module per resource.

### `step_functions/`
The Amazon States Language (ASL) JSON definition(s) for the self-healing workflow.

### `lambda_functions/`
Standalone Lambda handlers that aren't part of an agent's reasoning loop, e.g.
`incident_logger/` (writes incidents to DynamoDB) and `event_router/` (forwards events to
the SQS FIFO queue). One subfolder per function.

### `knowledge_base/`
Source content synced into the Bedrock Knowledge Base: `rca_documents/`,
`business_rules/`, `application_docs/`.

### `terraform/`
IaC modules the Operator Agent applies to remediate *workloads* (EMR, infra, connectivity
issues) — separate from `infrastructure/`, which provisions the solution itself.

### `tests/`
`unit/` for isolated agent/module tests, `integration/` for tests against real/mocked AWS
services.

### `scripts/`
Local environment setup and (later) deployment helper scripts.

### `docs/`
`architecture.md` (design) and `branching-strategy.md` (git workflow).

## Getting started

```bash
git clone <repo-url>
cd Self_Healing_Agentic_Solution_Gilead
git checkout develop
git checkout -b feature/<your-topic>
```

Add code to the folder matching your task, following the conventions above, and open a PR
into `develop` (see [CONTRIBUTING.md](CONTRIBUTING.md)).
