"""Direct function-calling tools used by the Operator Agent (no MCP layer)."""

from agents.common.aws.dynamodb_service import DynamoDBService


def execute_resolution(remediation_plan: dict) -> dict:
    """Apply the fix via AWS SSM Run Command, a Lambda API call, or a Terraform apply."""
    # TODO: dispatch on remediation_plan["action_type"] (ssm, lambda, terraform)
    return {"status": "PENDING"}


def validate_resolution(state: dict) -> bool:
    # TODO: re-check workload health (CloudWatch metric, EMR/EKS status) after remediation
    return False


def update_incident_memory(incident: dict) -> None:
    DynamoDBService().put_incident(incident)
