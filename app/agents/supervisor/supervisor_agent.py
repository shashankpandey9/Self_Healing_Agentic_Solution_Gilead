import uuid
from repositories.incident_repository import IncidentRepository


class SupervisorAgent:

    def __init__(self):

        self.incident_repo = (
            IncidentRepository()
        )

    def invoke(self, state):

        state["conversation_id"] = str(uuid.uuid4())
        existing_incident = (
            self.incident_repo.find_incident(
                error_type=state.get(
                    "error_type",
                    ""
                ),
                error_message=state.get(
                    "error_message",
                    ""
                )
            )
        )

        if existing_incident:

            state["incident_exists"] = True
            state["previous_incident"] = existing_incident
            state["remediation_plan"] = (
                existing_incident[
                    "remediation_plan"
                ]
            )

            state["next_agent"] = "operator"
            state["workflow_status"] = "KNOWN_INCIDENT"

            return state

        state["incident_exists"] = False
        state["next_agent"] = "retrieval"
        state["workflow_status"] = "NEW_INCIDENT"

        return state