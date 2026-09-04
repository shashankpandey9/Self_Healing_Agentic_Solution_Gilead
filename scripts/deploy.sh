#!/usr/bin/env bash
set -euo pipefail

# Provisions/updates the solution's own AWS resources.
python -m infrastructure.iam_roles
python -m infrastructure.dynamodb_tables
python -m infrastructure.sqs_queue
python -m infrastructure.eventbridge_rules
python -m infrastructure.lambda_functions
python -m infrastructure.step_functions_state_machine
