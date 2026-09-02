from app.services.aws.aws_client import AWSClientFactory

from app.core.config import settings


class DynamoDBService:

    def __init__(self):

        db = AWSClientFactory.dynamodb()

        self.incident_table = db.Table(
            settings.dynamodb_incident_table
        )

    def get_incident(
        self,
        incident_signature: str
    ):

        response = (
            self.incident_table.get_item(
                Key={
                    "incident_signature":
                    incident_signature
                }
            )
        )

        return response.get("Item")

    def save_incident(
        self,
        incident
    ):

        self.incident_table.put_item(
            Item=incident
        )

    def update_incident(
        self,
        incident_signature,
        updates
    ):

        self.incident_table.update_item(
            Key={
                "incident_signature":
                incident_signature
            },
            AttributeUpdates=updates
        )
