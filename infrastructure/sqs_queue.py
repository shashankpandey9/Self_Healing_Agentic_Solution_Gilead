import os

import boto3

REGION = os.getenv("AWS_REGION", "us-west-2")
QUEUE_NAME = os.getenv("INCIDENT_QUEUE_NAME", "self-healing-incidents.fifo")


def create_queue():
    sqs = boto3.client("sqs", region_name=REGION)

    response = sqs.create_queue(
        QueueName=QUEUE_NAME,
        Attributes={
            "FifoQueue": "true",
            "ContentBasedDeduplication": "true",
            "VisibilityTimeout": "120",
        },
    )
    print(f"Created SQS FIFO queue: {QUEUE_NAME}")
    return response


if __name__ == "__main__":
    create_queue()
