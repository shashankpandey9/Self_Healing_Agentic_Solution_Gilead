import boto3

from app.core.config import settings


class AWSClientFactory:

    @staticmethod
    def emr():

        return boto3.client(
            "emr",
            region_name=settings.aws_region
        )

    @staticmethod
    def logs():

        return boto3.client(
            "logs",
            region_name=settings.aws_region
        )

    @staticmethod
    def dynamodb():

        return boto3.resource(
            "dynamodb",
            region_name=settings.aws_region
        )

    @staticmethod
    def s3():

        return boto3.client(
            "s3",
            region_name=settings.aws_region
        )

    @staticmethod
    def sns():

        return boto3.client(
            "sns",
            region_name=settings.aws_region
        )

    @staticmethod
    def eventbridge():

        return boto3.client(
            "events",
            region_name=settings.aws_region
        )