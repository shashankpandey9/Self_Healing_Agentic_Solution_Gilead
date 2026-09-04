from typing import TypedDict, Any, Dict, List

class IncidentState(TypedDict, total=False):
    incident_id: str
    cluster_id: str
    error_type: str
    error_message: str
    conversation_id: str
    incident_exists: bool
    previous_incident: dict
    remediation_plan: dict
    next_agent: str
    workflow_status: str