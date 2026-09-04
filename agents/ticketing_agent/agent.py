"""Ticketing Agent - files/updates tickets and notifies humans when confidence is low or remediation fails."""

from agents.common.agent.base_agent import AgentBase
from agents.ticketing_agent.tools import create_ticket, send_human_alert


class TicketingAgent(AgentBase):

    @property
    def name(self) -> str:
        return "ticketing_agent"

    @property
    def description(self) -> str:
        return "Creates/updates tickets and notifies humans when confidence is low or remediation fails."

    def invoke(self, state: dict) -> dict:
        state["ticket_id"] = create_ticket(state)
        send_human_alert(
            subject=f"Self-healing: human review needed for incident {state.get('incident_id')}",
            body=f"Root cause: {state.get('root_cause')}\nConfidence: {state.get('confidence')}",
        )
        state["workflow_status"] = "AWAITING_HUMAN_REVIEW"
        return state
