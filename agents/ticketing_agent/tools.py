"""Direct function-calling tools used by the Ticketing Agent (no MCP layer)."""

import os

from agents.common.aws.aws_client import AWSClientFactory


def create_ticket(state: dict) -> str:
    """Create a ticket in the incident/ticket management system (e.g. SPARC)."""
    # TODO: call the ticketing system API
    return "TICKET-PENDING"


def send_human_alert(subject: str, body: str) -> None:
    """Send a human-in-the-loop notification email via SES."""
    from_address = os.getenv("ALERT_FROM_ADDRESS")
    to_address = os.getenv("ALERT_TO_ADDRESS")

    if not from_address or not to_address:
        return

    client = AWSClientFactory.ses()
    client.send_email(
        Source=from_address,
        Destination={"ToAddresses": [to_address]},
        Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
    )
