# Knowledge Base

Source content synced into the Bedrock Knowledge Base (via `infrastructure/bedrock_knowledge_base.py`)
that the Error Classifier Agent queries.

- `rca_documents/` — root-cause-analysis write-ups for previously seen failures.
- `business_rules/` — rules that constrain which remediations are allowed (e.g. approval
  thresholds, blackout windows).
- `application_docs/` — architecture/runbook documentation for the workloads being monitored
  (EMR, EKS, EC2, ALB).
