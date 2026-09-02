from datetime import datetime, timezone
from typing import Any, Dict
import uuid


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_detail(event: Dict[str, Any]) -> Dict[str, Any]:
    return event.get("detail", event)


def parse_incident_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert an EventBridge EMR/Glue failure event into
    the normalized incident schema used by DynamoDB.
    """

    detail = _get_detail(event)

    source_service = (
        detail.get("source_service") or detail.get("service") or _detect_service(event)
    )

    source_service = source_service.upper()

    if source_service not in {"EMR", "GLUE"}:
        raise ValueError(f"Unsupported source service: {source_service}")

    if source_service == "EMR":
        workload_id = (
            detail.get("cluster_id")
            or detail.get("jobFlowId")
            or detail.get("workload_id")
        )

        state = (
            detail.get("state")
            or detail.get("step_state")
            or detail.get("step_or_job_state")
            or "TERMINATED_WITH_ERRORS"
        )

        error_message = (
            detail.get("state_change_reason")
            or detail.get("error_message")
            or "EMR workload failed"
        )

    else:
        job_name = detail.get("job_name")
        job_run_id = detail.get("job_run_id")

        workload_id = detail.get("workload_id") or (
            f"{job_name}:{job_run_id}"
            if job_name and job_run_id
            else job_name or job_run_id
        )

        state = (
            detail.get("state")
            or detail.get("job_state")
            or detail.get("step_or_job_state")
            or "FAILED"
        )

        error_message = (
            detail.get("error_message")
            or detail.get("ErrorMessage")
            or "Glue job failed"
        )

    if not workload_id:
        raise ValueError("workload_id could not be determined")

    failure_time = (
        detail.get("failure_time")
        or detail.get("timestamp")
        or event.get("time")
        or _utc_now()
    )

    log_reference = (
        detail.get("log_reference")
        or detail.get("log_uri")
        or detail.get("log_path")
        or ""
    )

    incident_id = detail.get("incident_id") or (
        f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    now = _utc_now()

    return {
        "incident_id": incident_id,
        "source_service": source_service,
        "workload_id": workload_id,
        "step_or_job_state": state,
        "error_message": error_message,
        "failure_time": failure_time,
        "log_reference": log_reference,
        "state": "OPEN",
        "retry_count": int(detail.get("retry_count", 0)),
        "history": [
            {
                "timestamp": now,
                "action": "detected",
            }
        ],
        "created_at": now,
        "updated_at": now,
    }


def _detect_service(event: Dict[str, Any]) -> str:
    source = event.get("source", "").lower()

    if "emr" in source:
        return "EMR"

    if "glue" in source:
        return "GLUE"

    return ""
