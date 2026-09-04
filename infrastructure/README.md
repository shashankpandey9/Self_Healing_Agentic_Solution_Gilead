# Infrastructure

Placeholder for provisioning scripts for the AWS resources the self-healing solution
itself runs on (as opposed to `terraform/`, which the Operator Agent will apply to
remediate *workloads*).

Expected resources once implemented:

| Resource | Purpose |
|---|---|
| DynamoDB table | Incident memory |
| EventBridge rule | Routes unresolved workload failures |
| SQS FIFO queue | Serializes incident processing |
| Step Functions state machine | Runs the self-healing workflow |
| Lambda functions | Deploys the handlers under `lambda_functions/` |
| Bedrock Knowledge Base | Backed by `knowledge_base/` in S3 |
| SES identity | Sender for human-in-the-loop alerts |
| IAM roles | Execution roles for Lambda / Step Functions / Bedrock Agent |

Deployment automation for these resources will be added later.
