# Contributing

## Branches

- `main` — protected, always-deployable. Only updated via PR from `develop` (releases).
- `develop` — integration branch. All feature branches target this branch.
- `feature/<agent-or-topic>` — one branch per unit of work, e.g. `feature/error-classifier-agent`,
  `feature/step-functions-workflow`, `feature/dynamodb-infra`.

## Workflow

1. Branch from `develop`: `git checkout develop && git pull && git checkout -b feature/<name>`.
2. Keep changes scoped to the folder(s) relevant to your task (see the repository layout in
   [README.md](README.md)).
3. Add/update tests under `tests/unit` or `tests/integration`.
4. Open a PR into `develop`. CI (`.github/workflows/ci.yml`) must pass.
5. `develop` is periodically merged into `main` for releases.

## Code conventions

- Python for all agents, Lambda handlers and infrastructure scripts.
- Each agent lives under `agents/<agent_name>/` with `agent.py` (reasoning/orchestration) and
  `tools.py` (direct function-calling capabilities — no MCP layer).
- Shared code (AWS clients, config loading, model provider factory, base agent class) goes in
  `agents/common/`.
- boto3 clients are created through `agents.common.aws.aws_client.AWSClientFactory`, not
  instantiated ad hoc, so region/config stays consistent.
