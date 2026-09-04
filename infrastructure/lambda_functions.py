"""Packages and deploys the handlers under `lambda_functions/` as AWS Lambda functions.

TODO: zip each handler folder and create/update the corresponding Lambda function.
"""

import os

REGION = os.getenv("AWS_REGION", "us-west-2")

FUNCTIONS = {
    "self-healing-incident-logger": "lambda_functions/incident_logger",
    "self-healing-event-router": "lambda_functions/event_router",
}


def deploy_all(role_arn: str):
    import boto3
    import zipfile
    import io

    client = boto3.client("lambda", region_name=REGION)

    for function_name, source_dir in FUNCTIONS.items():
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    path = os.path.join(root, file)
                    zf.write(path, os.path.relpath(path, source_dir))

        try:
            client.create_function(
                FunctionName=function_name,
                Runtime="python3.12",
                Role=role_arn,
                Handler="handler.lambda_handler",
                Code={"ZipFile": buffer.getvalue()},
            )
            print(f"Created Lambda function: {function_name}")
        except client.exceptions.ResourceConflictException:
            client.update_function_code(FunctionName=function_name, ZipFile=buffer.getvalue())
            print(f"Updated Lambda function: {function_name}")


if __name__ == "__main__":
    deploy_all(role_arn=os.environ["LAMBDA_EXECUTION_ROLE_ARN"])
