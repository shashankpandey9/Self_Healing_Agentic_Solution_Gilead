# Lambda Functions

Standalone Lambda handlers invoked by Step Functions / EventBridge (separate from the
`agents/` package, which contains the reasoning agents themselves).

| Function | Purpose |
|---|---|
| `incident_logger` | Parses an incident event and writes/updates it in DynamoDB |
| `event_router` | Forwards a CloudWatch/DevOps Guru event to the SQS FIFO queue |
