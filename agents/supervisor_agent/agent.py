"""Supervisor Agent - routes incidents to the correct specialist agent and tracks workflow state."""

from agents.common.agent.base_agent import AgentBase
from agents.supervisor_agent.tools import find_known_incident


class SupervisorAgent(AgentBase):

    @property
    def name(self) -> str:
        return "supervisor_agent"

    @property
    def description(self) -> str:
        return "Coordinates the multi-agent self-healing workflow."

    def invoke(self, state: dict) -> dict:
        known_incident = find_known_incident(
            error_type=state.get("error_type", ""),
            error_message=state.get("error_message", ""),
        )

        if known_incident:
            state["incident_exists"] = True
            state["previous_incident"] = known_incident
            state["remediation_plan"] = known_incident.get("remediation_plan")
            state["next_agent"] = "operator_agent"
            return state

        state["incident_exists"] = False
        state["next_agent"] = "log_retriever_agent"
        return state
