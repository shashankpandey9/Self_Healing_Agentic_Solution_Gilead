"""Error Classifier Agent - determines root cause and a remediation plan via the Bedrock Knowledge Base."""

from agents.common.agent.base_agent import AgentBase
from agents.error_classifier_agent.prompt import CLASSIFICATION_PROMPT
from agents.error_classifier_agent.tools import query_knowledge_base


class ErrorClassifierAgent(AgentBase):

    @property
    def name(self) -> str:
        return "error_classifier_agent"

    @property
    def description(self) -> str:
        return "Classifies incidents and proposes a remediation plan using the knowledge base."

    def invoke(self, state: dict) -> dict:
        result = query_knowledge_base(
            knowledge_base_id=state.get("knowledge_base_id", ""),
            query=CLASSIFICATION_PROMPT.format(
                error_message=state.get("error_message", ""),
                logs=state.get("cloudwatch_logs", []),
            ),
        )

        state["root_cause"] = result.get("root_cause")
        state["confidence"] = result.get("confidence", 0.0)
        state["remediation_plan"] = result.get("remediation_plan")
        state["next_agent"] = "operator_agent" if state["confidence"] >= 0.8 else "ticketing_agent"
        return state
