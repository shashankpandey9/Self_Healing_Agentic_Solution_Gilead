import os


def load_env_variables() -> dict:
    """Load environment variables shared across agents."""
    return {
        "aws_region": os.getenv("AWS_REGION", "us-west-2"),
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "incident_table_name": os.getenv("INCIDENT_TABLE_NAME", "self-healing-incidents"),
        "bedrock_knowledge_base_id": os.getenv("BEDROCK_KNOWLEDGE_BASE_ID", ""),
        "bedrock_model_id": os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
    }
