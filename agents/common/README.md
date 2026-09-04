# common

Shared code used by every agent. Not an agent itself.

Planned subfolders:

| Folder | Purpose |
|---|---|
| `agent/` | Base agent class wrapping a LangGraph state graph |
| `aws/` | Central boto3 client factory + shared DynamoDB incident-memory access |
| `model_provider/` | Factory for the LLM/Bedrock client used for agent reasoning |
| `util/` | Environment/config loading |
| `a2a/` | Helpers for serving an agent over A2A and calling other agents over A2A |
