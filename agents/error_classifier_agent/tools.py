"""Direct function-calling tools used by the Error Classifier Agent (no MCP layer)."""

from agents.common.aws.aws_client import AWSClientFactory


def query_knowledge_base(knowledge_base_id: str, query: str) -> dict:
    """Query the Bedrock Knowledge Base (RCA docs, business rules, application docs)."""
    client = AWSClientFactory.bedrock_agent_runtime()
    # TODO: call retrieve_and_generate and parse the response into
    # {"root_cause": ..., "confidence": ..., "remediation_plan": ...}
    return {"root_cause": None, "confidence": 0.0, "remediation_plan": None}
