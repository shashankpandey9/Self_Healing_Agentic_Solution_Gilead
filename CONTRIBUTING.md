# Contributing

## Branches

- `main` — protected, always-deployable. Only updated via PR from `develop` (releases).
- `develop` — integration branch. All feature branches target this branch.
- `feature/<agent-or-topic>` — one branch per unit of work, e.g. `feature/error-classifier-agent`,
  `feature/step-functions-workflow`, `feature/dynamodb-infra`.

## Workflow

1. Branch from `develop`: `git checkout develop && git pull && git checkout -b feature/<name>`.
2. Keep changes scoped to the folder(s) relevant to your task — see
   [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) for what belongs where.
3. Add/update tests under `tests/unit` or `tests/integration`.
4. Open a PR into `develop`.
5. `develop` is periodically merged into `main` for releases.

## Conventions (to follow once implementation starts)

- Python for all agents, Lambda handlers and infrastructure scripts.
- Agents are built with **LangGraph** and communicate over the **A2A (Agent2Agent)
  protocol** — no MCP layer.
- Each agent lives under `agents/<agent_name>/`; shared code goes in `agents/common/`.
