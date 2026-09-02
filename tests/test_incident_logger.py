from unittest.mock import MagicMock, patch

from src.incident_logger.parser import parse_incident_event
from src.incident_logger.dynamodb_service import DynamoDBIncidentService
from src.incident_logger.handler import lambda_handler


def test_emr_incident():
    event = {
        "source": "self-healing.workloads",
        "detail-type": "Unresolved Workload Failure",
        "time": "2026-09-02T10:30:00Z",
        "detail": {
            "source_service": "EMR",
            "cluster_id": "j-123456789",
            "step_or_job_state": "TERMINATED_WITH_ERRORS",
            "state_change_reason": "Bootstrap Action Failed",
            "failure_time": "2026-09-02T10:30:00Z",
            "log_reference": "s3://example/emr/logs/",
            "retry_count": 3,
            "retry_exhausted": True,
        },
    }

    incident = parse_incident_event(event)

    assert incident["source_service"] == "EMR"
    assert incident["workload_id"] == "j-123456789"
    assert incident["state"] == "OPEN"
    assert incident["retry_count"] == 3
    assert incident["history"][0]["action"] == "detected"


def test_glue_incident():
    event = {
        "source": "self-healing.workloads",
        "detail-type": "Unresolved Workload Failure",
        "detail": {
            "source_service": "GLUE",
            "job_name": "customer-data-job",
            "job_run_id": "jr_123456",
            "state": "FAILED",
            "ErrorMessage": "Spark executor failed",
            "retry_count": 3,
            "retry_exhausted": True,
        },
    }

    incident = parse_incident_event(event)

    assert incident["source_service"] == "GLUE"
    assert (
        incident["workload_id"]
        == "customer-data-job:jr_123456"
    )
    assert incident["state"] == "OPEN"
    assert incident["retry_count"] == 3


@patch("src.incident_logger.dynamodb_service.boto3.resource")
def test_create_incident(mock_boto_resource):
    mock_dynamodb = MagicMock()
    mock_table = MagicMock()

    mock_dynamodb.Table.return_value = mock_table
    mock_boto_resource.return_value = mock_dynamodb

    service = DynamoDBIncidentService(
        table_name="test-incidents"
    )

    incident = {
        "incident_id": "INC-TEST-001",
        "source_service": "EMR",
        "workload_id": "j-123456789",
        "state": "OPEN",
        "retry_count": 3,
    }

    service.create_incident(incident)

    mock_table.put_item.assert_called_once()

    call_args = mock_table.put_item.call_args

    assert call_args.kwargs["Item"] == incident


@patch("src.incident_logger.handler.DynamoDBIncidentService")
def test_lambda_handler(mock_service_class):
    mock_service = MagicMock()
    mock_service_class.return_value = mock_service

    event = {
        "source": "self-healing.workloads",
        "detail-type": "Unresolved Workload Failure",
        "time": "2026-09-02T10:30:00Z",
        "detail": {
            "source_service": "EMR",
            "cluster_id": "j-123456789",
            "step_or_job_state": "TERMINATED_WITH_ERRORS",
            "state_change_reason": "Bootstrap Action Failed",
            "failure_time": "2026-09-02T10:30:00Z",
            "log_reference": "s3://example/emr/logs/",
            "retry_count": 3,
            "retry_exhausted": True,
        },
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200

    mock_service.create_incident.assert_called_once()

    incident = mock_service.create_incident.call_args.args[0]

    assert incident["source_service"] == "EMR"
    assert incident["workload_id"] == "j-123456789"
    assert incident["state"] == "OPEN"
    assert incident["retry_count"] == 3