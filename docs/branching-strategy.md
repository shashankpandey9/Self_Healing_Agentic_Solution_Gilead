# Branching strategy

- **main** — protected, always-deployable. Updated only via PR from `develop`.
- **develop** — default integration branch. Collaborators clone the repo and branch off
  `develop` for new work; PRs target `develop`.
- **feature/&lt;name&gt;** — short-lived branch per agent or task, e.g. `feature/operator-agent`,
  `feature/dynamodb-infra`, `feature/step-functions-workflow`. Merged into `develop` via PR.

Release flow: `feature/*` → `develop` → (tested/validated) → `main`.
