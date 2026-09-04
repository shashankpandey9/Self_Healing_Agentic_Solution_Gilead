# Agents

Each folder is an independent agent with two files:

- `agent.py` — reasoning/orchestration logic and the `invoke(state)` entry point.
- `tools.py` — direct function-calling capabilities the agent uses (no MCP layer).

Shared code lives in `agents/common/`:

- `agent/base_agent.py` — `AgentBase` interface all agents implement.
- `util/config_loader.py` — environment variable loading.
- `model_provider/factory.py` — creates the LLM/Bedrock client used for reasoning.
- `aws/aws_client.py` — central boto3 client factory.
- `aws/dynamodb_service.py` — shared incident memory read/write.

| Agent | Responsibility |
|---|---|
| `supervisor_agent` | Routes incidents, checks for known signatures, tracks workflow state |
| `log_retriever_agent` | Retrieves CloudWatch/S3 logs for the failing workload |
| `error_classifier_agent` | Classifies root cause via the Bedrock Knowledge Base |
| `operator_agent` | Executes the remediation plan and validates the outcome |
| `ticketing_agent` | Files tickets and sends human-in-the-loop alerts |
