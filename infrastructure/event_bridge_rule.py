import json

import boto3

REGION = "us-west-2"

RULE_NAME = "self-healing-unresolved-failures"


EVENT_PATTERN = {
    "source": ["self-healing.workloads"],
    "detail-type": ["Unresolved Workload Failure"],
    "detail": {"retry_exhausted": [True], "source_service": ["EMR", "GLUE"]},
}


def create_rule():

    events = boto3.client(
        "events",
        region_name=REGION,
    )

    response = events.put_rule(
        Name=RULE_NAME,
        EventPattern=json.dumps(EVENT_PATTERN),
        State="ENABLED",
        Description=(
            "Detect EMR and Glue failures "
            "that remain unresolved after "
            "configured retries."
        ),
    )

    print(f"Created EventBridge rule: {RULE_NAME}")

    return response


if __name__ == "__main__":
    create_rule()
