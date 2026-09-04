"""Factory for creating the LLM client used by agent reasoning (Amazon Bedrock)."""

import os

import boto3


class ModelFactory:

    @staticmethod
    def create_provider(model_id: str | None = None, region_name: str | None = None):
        return boto3.client(
            "bedrock-runtime",
            region_name=region_name or os.getenv("AWS_REGION", "us-west-2"),
        )
