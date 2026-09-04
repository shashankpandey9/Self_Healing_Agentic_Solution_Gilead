import os

from agents.common.aws.aws_client import AWSClientFactory


class DynamoDBService:
    """Read/write access to the shared incident memory table."""

    def __init__(self, table_name: str | None = None):
        self.table_name = table_name or os.getenv("INCIDENT_TABLE_NAME", "self-healing-incidents")
        self.table = AWSClientFactory.dynamodb().Table(self.table_name)

    def put_incident(self, incident: dict) -> None:
        self.table.put_item(Item=incident)

    def get_incident(self, incident_id: str) -> dict | None:
        response = self.table.get_item(Key={"incident_id": incident_id})
        return response.get("Item")

    def find_by_signature(self, error_type: str, error_message: str) -> dict | None:
        # TODO: replace scan with a GSI query on (error_type, error_message)
        response = self.table.scan()
        for item in response.get("Items", []):
            if item.get("error_type") == error_type and item.get("error_message") == error_message:
                return item
        return None
