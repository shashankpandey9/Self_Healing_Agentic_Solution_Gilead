# Self-Healing Agentic Solution (Gilead)

Multi-agent, AWS-native solution that will automatically detect, classify and remediate
workload failures (EMR, EKS, EC2, ALB) with a human-in-the-loop fallback when confidence
is low. See [docs/architecture.md](docs/architecture.md) for the full design.

> This repository currently contains **only the folder structure** the team will develop
> against — no implementation code or deployment automation yet. See
> [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) for how to use each folder.

> **Note:** This solution will **not** use MCP (Model Context Protocol). Agents will call
> their capabilities directly. Agents will be built with **LangGraph** and communicate
> over the **A2A (Agent2Agent) protocol**.

## Getting started

```bash
git clone <repo-url>
cd Self_Healing_Agentic_Solution_Gilead
git checkout develop
git checkout -b feature/<your-topic>
```

Read [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) before adding code so new work lands in
the right place.

## Branching strategy

See [docs/branching-strategy.md](docs/branching-strategy.md). In short: `main` is the
protected, always-deployable branch; `develop` is the integration branch collaborators
branch off of and open PRs against; agent/feature work happens on `feature/<name>` branches.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
