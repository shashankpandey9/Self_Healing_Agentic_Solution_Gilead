import os

import boto3

REGION = os.getenv("AWS_REGION", "us-west-2")


def verify_sender_identity(email_address: str):
    client = boto3.client("ses", region_name=REGION)
    client.verify_email_identity(EmailAddress=email_address)
    print(f"Verification email sent to: {email_address}")


if __name__ == "__main__":
    verify_sender_identity(os.environ["ALERT_FROM_ADDRESS"])
