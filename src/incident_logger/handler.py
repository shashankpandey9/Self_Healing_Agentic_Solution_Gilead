import json
import logging

from botocore.exceptions import ClientError

from .dynamodb_service import DynamoDBIncidentService
from .parser import parse_incident_event

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda entry point.

    Receives an EventBridge event, converts it into the
    standard incident schema and stores it in DynamoDB.
    """

    logger.info(
        "Received incident event: %s",
        json.dumps(event),
    )

    try:
        incident = parse_incident_event(event)

        logger.info(
            "Parsed incident: %s",
            json.dumps(incident),
        )

        service = DynamoDBIncidentService()

        try:
            service.create_incident(incident)

            logger.info(
                "Incident created successfully: %s",
                incident["incident_id"],
            )

            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "message": "Incident created",
                        "incident_id": incident["incident_id"],
                    }
                ),
            }

        except ClientError as error:

            if error.response["Error"]["Code"] == ("ConditionalCheckFailedException"):
                logger.warning(
                    "Incident already exists: %s",
                    incident["incident_id"],
                )

                return {
                    "statusCode": 200,
                    "body": json.dumps(
                        {
                            "message": "Incident already exists",
                            "incident_id": incident["incident_id"],
                        }
                    ),
                }

            raise

    except Exception as error:

        logger.exception("Failed to process incident event")

        raise error
