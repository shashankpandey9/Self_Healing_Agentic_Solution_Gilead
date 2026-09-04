# Architecture

This solution merges two inputs:

- The AWS-native workflow (detection → routing → orchestration → recall → act → learn).
- The multi-agent system design (Supervisor, Error Classifier, Operator, Ticketing and Log
  Retriever agents behind a Supervisor, using a central DynamoDB memory).

**MCP is not used.** In the original multi-agent diagram, agents reached tools through an
MCP client/server. In this implementation each agent instead will own a local `tools.py`
module that calls AWS APIs (boto3), the ticketing system, or GitHub Actions directly.

**Framework:** agents will be built with **LangGraph** (each agent as its own state graph
for internal reasoning/retries) and exposed as independent services over the **A2A
(Agent2Agent) protocol**, so the Supervisor and other agents call each other over a
standard agent-to-agent interface instead of in-process imports.

> This repository currently only contains the folder structure for the above — no
> implementation code yet. See [FOLDER_STRUCTURE.md](../FOLDER_STRUCTURE.md).

## Components

| Layer | AWS Service | Folder |
|---|---|---|
| Detection & observability | CloudWatch, DevOps Guru | `terraform/`, workload code |
| Event routing | EventBridge | `infrastructure/` |
| Concurrency control | SQS FIFO | `infrastructure/` |
| Workflow orchestration | Step Functions | `step_functions/`, `infrastructure/` |
| Recurrence lookup / memory | DynamoDB | `infrastructure/`, `agents/common/` |
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
