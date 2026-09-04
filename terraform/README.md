# Terraform

IaC modules the Operator Agent applies to remediate *workloads* (as opposed to
`infrastructure/`, which provisions the self-healing solution's own AWS resources).

Covers the failure categories called out in the architecture:

- `modules/emr/` — dead node / no active node recovery.
- `modules/infrastructure/` — subnet issues, bootstrap failures, EC2 capacity.
- `modules/connectivity/` — HDFS-to-S3, Redshift table, compute-to-publish-table issues.

Each module should be plan/apply-able independently and invoked by
`agents/operator_agent/tools.py`.
