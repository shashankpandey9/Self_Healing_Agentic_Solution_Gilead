import os

import boto3

TABLE_NAME = os.getenv("INCIDENT_TABLE_NAME", "self-healing-incidents")
REGION = os.getenv("AWS_REGION", "us-west-2")


def create_incident_table():
    dynamodb = boto3.client("dynamodb", region_name=REGION)

    try:
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "incident_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "incident_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
            Tags=[
                {"Key": "Project", "Value": "Self-Healing-Agent"},
                {"Key": "Component", "Value": "IncidentMemory"},
            ],
        )
        print(f"Created DynamoDB table: {TABLE_NAME}")
        return response
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Table already exists: {TABLE_NAME}")


if __name__ == "__main__":
    create_incident_table()
