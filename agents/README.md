# Agents

Each subfolder is a placeholder for one agent in the multi-agent self-healing system.
The team will implement these using **LangGraph** (per-agent state graph) and the
**A2A (Agent2Agent) protocol** for agent-to-agent communication. **MCP is not used** —
each agent will call its own capabilities directly instead of through an MCP client/server.

| Folder | Responsibility |
|---|---|
| `common/` | Shared code: base agent class, config loading, AWS/model clients, A2A client/server helpers |
| `supervisor_agent/` | Routes incidents, checks for known signatures, tracks workflow state |
| `log_retriever_agent/` | Retrieves CloudWatch/S3 logs for the failing workload |
| `error_classifier_agent/` | Classifies root cause via the Bedrock Knowledge Base |
| `operator_agent/` | Executes the remediation plan and validates the outcome |
| `ticketing_agent/` | Files tickets and sends human-in-the-loop alerts |

Expected convention once code is added (see the root [FOLDER_STRUCTURE.md](../FOLDER_STRUCTURE.md)):
each agent folder holds `state.py` (LangGraph state), `agent.py` (the agent's state graph)
and `tools.py` (direct function-calling capabilities, no MCP).
