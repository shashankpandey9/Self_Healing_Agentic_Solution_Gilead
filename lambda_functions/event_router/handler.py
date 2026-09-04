import json
import os

import boto3

QUEUE_URL = os.getenv("INCIDENT_QUEUE_URL", "")


def lambda_handler(event, context):
    """Forwards a CloudWatch/DevOps Guru anomaly event to the SQS FIFO queue for ordered processing."""
    sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "us-west-2"))

    detail = event.get("detail", event)
    message_group_id = detail.get("source_service", "default")

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(event),
        MessageGroupId=message_group_id,
    )

    return {"statusCode": 200}
