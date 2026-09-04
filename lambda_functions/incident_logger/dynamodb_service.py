import os

import boto3

TABLE_NAME = os.getenv("INCIDENT_TABLE_NAME", "self-healing-incidents")
REGION = os.getenv("AWS_REGION", "us-west-2")


class DynamoDBIncidentService:

    def __init__(self):
        self.table = boto3.resource("dynamodb", region_name=REGION).Table(TABLE_NAME)

    def create_incident(self, incident: dict) -> None:
        self.table.put_item(
            Item=incident,
            ConditionExpression="attribute_not_exists(incident_id)",
        )
