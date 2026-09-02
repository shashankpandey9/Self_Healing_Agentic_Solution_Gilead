import os
from typing import Any, Dict

import boto3

TABLE_NAME = os.getenv(
    "INCIDENT_TABLE_NAME",
    "self-healing-incidents",
)

AWS_REGION = os.getenv(
    "AWS_REGION",
    "us-west-2",
)


class DynamoDBIncidentService:
    def __init__(self, table_name: str = TABLE_NAME):
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
        )

        self.table = dynamodb.Table(table_name)

    def create_incident(
        self,
        incident: Dict[str, Any],
    ) -> Dict[str, Any]:

        response = self.table.put_item(
            Item=incident,
            ConditionExpression="attribute_not_exists(incident_id)",
        )

        return response

    def update_incident(
        self,
        incident_id: str,
        updates: Dict[str, Any],
    ) -> Dict[str, Any]:

        expression_parts = []
        expression_values = {}
        expression_names = {}

        for index, (key, value) in enumerate(updates.items()):
            name_key = f"#field{index}"
            value_key = f":value{index}"

            expression_parts.append(f"{name_key} = {value_key}")

            expression_names[name_key] = key
            expression_values[value_key] = value

        response = self.table.update_item(
            Key={
                "incident_id": incident_id,
            },
            UpdateExpression="SET " + ", ".join(expression_parts),
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW",
        )

        return response
