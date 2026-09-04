import json
import os

import boto3

REGION = os.getenv("AWS_REGION", "us-west-2")
STATE_MACHINE_NAME = os.getenv("STATE_MACHINE_NAME", "self-healing-workflow")
DEFINITION_PATH = os.path.join(
    os.path.dirname(__file__), "..", "step_functions", "self_healing_workflow.asl.json"
)


def deploy_state_machine(role_arn: str):
    with open(DEFINITION_PATH, encoding="utf-8") as f:
        definition = f.read()

    client = boto3.client("stepfunctions", region_name=REGION)

    try:
        response = client.create_state_machine(
            name=STATE_MACHINE_NAME,
            definition=definition,
            roleArn=role_arn,
            type="STANDARD",
        )
    except client.exceptions.StateMachineAlreadyExists:
        arn = f"arn:aws:states:{REGION}:{boto3.client('sts').get_caller_identity()['Account']}:stateMachine:{STATE_MACHINE_NAME}"
        response = client.update_state_machine(stateMachineArn=arn, definition=definition, roleArn=role_arn)

    print(f"Deployed state machine: {STATE_MACHINE_NAME}")
    return response


if __name__ == "__main__":
    deploy_state_machine(role_arn=os.environ["STEP_FUNCTIONS_ROLE_ARN"])
