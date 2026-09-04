# Self-Healing Agentic Solution (Gilead)

Multi-agent, AWS-native solution that automatically detects, classifies and remediates
workload failures (EMR, EKS, EC2, ALB) with a human-in-the-loop fallback when confidence
is low. See [docs/architecture.md](docs/architecture.md) for the full design.

> **Note:** This solution does **not** use MCP (Model Context Protocol). Each agent calls
> its capabilities directly through its own `tools.py` module.

## High level flow

1. **Detect** — CloudWatch / DevOps Guru raise an anomaly (OOM, pod crash, network issue).
2. **Route** — EventBridge routes the event; SQS FIFO enforces one-at-a-time processing.
3. **Orchestrate** — Step Functions drives the workflow; a Supervisor Agent coordinates it.
4. **Recall** — DynamoDB is checked for a known error signature.
   - Known → instant re-application of the stored fix.
   - Unknown → the Error Classifier Agent uses a Bedrock Knowledge Base (RCA docs,
     business rules, app docs) to propose a remediation plan.
5. **Act** — High confidence → Operator Agent executes the plan (Lambda / SSM / Terraform).
     Low confidence/risk → Ticketing Agent + SES notify a human; workflow pauses.
6. **Learn** — DynamoDB is updated with the incident, root cause, action taken and outcome.

## Repository layout

```
├── agents/                # Multi-agent system (Supervisor, Classifier, Operator, Ticketing, Log Retriever)
│   └── common/             # Shared base classes, config loader, AWS/model clients
├── infrastructure/         # boto3 provisioning scripts for the solution's own AWS resources
├── step_functions/         # Step Functions state machine (ASL) definitions
├── lambda_functions/       # Standalone Lambda handlers (incident logging, event routing)
├── knowledge_base/         # RCA documents, business rules, app docs used by the Bedrock KB
├── terraform/              # IaC modules the Operator Agent applies to remediate workloads
├── tests/                  # Unit and integration tests
├── scripts/                # Local dev / deployment helper scripts
├── docs/                   # Architecture and process documentation
└── .github/workflows/      # CI/CD pipelines
```

## Getting started

```bash
git clone <repo-url>
cd Self_Healing_Agentic_Solution_Gilead
git checkout develop
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

## Branching strategy

See [docs/branching-strategy.md](docs/branching-strategy.md). In short: `main` is the
protected, always-deployable branch; `develop` is the integration branch collaborators
branch off of and open PRs against; agent/feature work happens on `feature/<name>` branches.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
