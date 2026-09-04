"""Provisions the Bedrock Knowledge Base backed by the SOP/RCA documents in `knowledge_base/`.

TODO: create the S3 bucket/data source, vector index and Bedrock Knowledge Base, then sync.
"""

import os

REGION = os.getenv("AWS_REGION", "us-west-2")
KNOWLEDGE_BASE_BUCKET = os.getenv("KNOWLEDGE_BASE_BUCKET", "self-healing-knowledge-base")


def sync_knowledge_base(knowledge_base_id: str, data_source_id: str):
    import boto3

    client = boto3.client("bedrock-agent", region_name=REGION)
    response = client.start_ingestion_job(knowledgeBaseId=knowledge_base_id, dataSourceId=data_source_id)
    print(f"Started ingestion job for knowledge base: {knowledge_base_id}")
    return response


if __name__ == "__main__":
    sync_knowledge_base(
        knowledge_base_id=os.environ["BEDROCK_KNOWLEDGE_BASE_ID"],
        data_source_id=os.environ["BEDROCK_DATA_SOURCE_ID"],
    )
