# Infrastructure

boto3 provisioning scripts for the AWS resources the self-healing solution itself runs on
(as opposed to `terraform/`, which the Operator Agent applies to remediate *workloads*).

Each script is runnable standalone (`python -m infrastructure.<script>`) and idempotent.

| Script | Resource |
|---|---|
| `dynamodb_tables.py` | Incident memory table |
| `eventbridge_rules.py` | Rule that routes unresolved workload failures |
| `sqs_queue.py` | FIFO queue that serializes incident processing |
| `step_functions_state_machine.py` | Deploys `step_functions/self_healing_workflow.asl.json` |
| `lambda_functions.py` | Packages/deploys the handlers under `lambda_functions/` |
| `bedrock_knowledge_base.py` | Bedrock Knowledge Base backed by `knowledge_base/` in S3 |
| `ses_setup.py` | Verified sender identity for human-in-the-loop alerts |
| `iam_roles.py` | Execution roles for Lambda / Step Functions / Bedrock Agent |
