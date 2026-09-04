# Architecture

This solution merges two inputs:

- The AWS-native workflow (detection → routing → orchestration → recall → act → learn).
- The multi-agent system design (Supervisor, Error Classifier, Operator, Ticketing and Log
  Retriever agents behind a Supervisor, using a central DynamoDB memory).

**MCP is not used.** In the original multi-agent diagram, agents reached tools through an
MCP client/server. In this implementation each agent instead owns a local `tools.py` module
that calls AWS APIs (boto3), the ticketing system, or GitHub Actions directly.

## Components

| Layer | AWS Service | Folder |
|---|---|---|
| Detection & observability | CloudWatch, DevOps Guru | `terraform/`, workload code |
| Event routing | EventBridge | `infrastructure/eventbridge_rules.py` |
| Concurrency control | SQS FIFO | `infrastructure/sqs_queue.py` |
| Workflow orchestration | Step Functions | `step_functions/`, `infrastructure/step_functions_state_machine.py` |
| Recurrence lookup / memory | DynamoDB | `infrastructure/dynamodb_tables.py`, `agents/common/aws/dynamodb_service.py` |
| Reasoning / classification | Bedrock Agent + Knowledge Base | `agents/error_classifier_agent/`, `knowledge_base/` |
| Action execution | Lambda, SSM, Terraform | `agents/operator_agent/`, `lambda_functions/`, `terraform/` |
| Human-in-the-loop | SES | `agents/ticketing_agent/` |
| Ticketing | SPARC / internal ticketing API | `agents/ticketing_agent/` |
| Multi-agent coordination | — | `agents/supervisor_agent/` |
| Log retrieval | CloudWatch, S3 | `agents/log_retriever_agent/` |

## Agent responsibilities

- **Supervisor Agent** — receives the incident, checks DynamoDB for a known signature, and
  routes to the right specialist agent, tracking workflow state end-to-end.
- **Log Retriever Agent** — pulls CloudWatch/S3 logs for the failing workload.
- **Error Classifier Agent** — queries the Bedrock Knowledge Base (RCA docs, business rules,
  application docs) to determine root cause, confidence and a remediation plan.
- **Operator Agent** — executes the remediation plan (Lambda API calls, SSM Run Command,
  Terraform apply) and validates the outcome.
- **Ticketing Agent** — files/updates tickets and sends SES alerts when confidence is low or
  remediation fails, pausing the workflow for a human.

All agents write the final incident record (root cause, action taken, resolution status)
back to DynamoDB.
