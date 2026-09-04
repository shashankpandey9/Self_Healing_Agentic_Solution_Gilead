"""Direct function-calling tools used by the Log Retriever Agent (no MCP layer)."""

from agents.common.aws.aws_client import AWSClientFactory


def get_cloudwatch_logs(log_group: str, start_time: int, end_time: int) -> list:
    client = AWSClientFactory.logs()
    # TODO: implement filter_log_events with pagination
    return []


def get_s3_logs(bucket: str, prefix: str) -> list:
    client = AWSClientFactory.s3()
    # TODO: list_objects_v2 + get_object for matching keys
    return []
