"""Creates the IAM execution roles used by Lambda, Step Functions and the Bedrock Agent.

TODO: define least-privilege policies per role instead of the placeholder trust policies below.
"""

import json
import os

import boto3

REGION = os.getenv("AWS_REGION", "us-west-2")

TRUST_POLICIES = {
    "self-healing-lambda-role": "lambda.amazonaws.com",
    "self-healing-step-functions-role": "states.amazonaws.com",
    "self-healing-bedrock-agent-role": "bedrock.amazonaws.com",
}


def create_role(role_name: str, service_principal: str):
    iam = boto3.client("iam", region_name=REGION)

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {"Effect": "Allow", "Principal": {"Service": service_principal}, "Action": "sts:AssumeRole"}
        ],
    }

    try:
        response = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy))
        print(f"Created IAM role: {role_name}")
        return response
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"Role already exists: {role_name}")


if __name__ == "__main__":
    for name, principal in TRUST_POLICIES.items():
        create_role(name, principal)
