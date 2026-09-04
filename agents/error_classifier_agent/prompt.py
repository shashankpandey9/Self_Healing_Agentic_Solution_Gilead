CLASSIFICATION_PROMPT = """
You are classifying an infrastructure incident using the provided RCA documents,
business rules and application documentation.

Error message: {error_message}
Logs: {logs}

Return the root cause, a confidence score (0-1) and a step-by-step remediation plan.
"""
