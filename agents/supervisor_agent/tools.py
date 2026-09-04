"""Direct function-calling tools used by the Supervisor Agent (no MCP layer)."""

from agents.common.aws.dynamodb_service import DynamoDBService


def find_known_incident(error_type: str, error_message: str) -> dict | None:
    """Look up a previously resolved incident with a matching error signature."""
    return DynamoDBService().find_by_signature(error_type, error_message)
