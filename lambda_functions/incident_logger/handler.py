import json
import logging

from botocore.exceptions import ClientError

from .dynamodb_service import DynamoDBIncidentService
from .parser import parse_incident_event

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Receives an EventBridge event, converts it to the incident schema and stores it in DynamoDB."""
    logger.info("Received incident event: %s", json.dumps(event))

    incident = parse_incident_event(event)
    service = DynamoDBIncidentService()

    try:
        service.create_incident(incident)
        logger.info("Incident created: %s", incident["incident_id"])
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Incident created", "incident_id": incident["incident_id"]}),
        }
    except ClientError as error:
        if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
            logger.warning("Incident already exists: %s", incident["incident_id"])
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {"message": "Incident already exists", "incident_id": incident["incident_id"]}
                ),
            }
        raise
