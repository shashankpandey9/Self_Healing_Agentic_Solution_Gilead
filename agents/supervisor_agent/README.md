# Supervisor Agent

Receives the incident, checks DynamoDB for a known error signature, and routes to the
right specialist agent (`log_retriever_agent` for new incidents, `operator_agent` for
known ones), tracking workflow state end-to-end.
