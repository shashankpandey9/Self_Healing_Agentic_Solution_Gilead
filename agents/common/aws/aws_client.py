import os

import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-west-2")


class AWSClientFactory:
    """Central place to create boto3 clients so agents/tools don't duplicate region config."""

    @staticmethod
    def dynamodb():
        return boto3.resource("dynamodb", region_name=AWS_REGION)

    @staticmethod
    def eventbridge():
        return boto3.client("events", region_name=AWS_REGION)

    @staticmethod
    def sqs():
        return boto3.client("sqs", region_name=AWS_REGION)

    @staticmethod
    def stepfunctions():
        return boto3.client("stepfunctions", region_name=AWS_REGION)

    @staticmethod
    def ssm():
        return boto3.client("ssm", region_name=AWS_REGION)

    @staticmethod
    def ses():
        return boto3.client("ses", region_name=AWS_REGION)

    @staticmethod
    def bedrock_agent_runtime():
        return boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

    @staticmethod
    def emr():
        return boto3.client("emr", region_name=AWS_REGION)

    @staticmethod
    def logs():
        return boto3.client("logs", region_name=AWS_REGION)

    @staticmethod
    def s3():
        return boto3.client("s3", region_name=AWS_REGION)
