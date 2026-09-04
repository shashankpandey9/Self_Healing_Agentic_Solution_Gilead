import uuid
from datetime import datetime, timezone


def parse_incident_event(event: dict) -> dict:
    """Normalize an EventBridge/Step Functions event into the standard incident schema."""
    detail = event.get("detail", event)

    return {
        "incident_id": detail.get("incident_id", str(uuid.uuid4())),
        "error_type": detail.get("error_type", "UNKNOWN"),
        "error_message": detail.get("error_message", ""),
        "source_service": detail.get("source_service", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
