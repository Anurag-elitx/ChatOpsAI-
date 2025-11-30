"""
Enterprise integration router.

Maps detected intents to the appropriate third-party API
(JIRA, Salesforce, Zendesk) and returns the API response.
"""

import httpx
import logging

from app.config import (
    JIRA_BASE_URL,
    SALESFORCE_BASE_URL,
    ZENDESK_BASE_URL,
    API_TIMEOUT_SECONDS,
)

_logger = logging.getLogger(__name__)

# Mapping from intent label → handler function
_INTENT_TO_HANDLER = {}  # populated after function definitions


async def route_to_integration(intent: str, message: str) -> dict:
    """
    Dispatch to the correct enterprise API based on intent.

    Returns an empty dict if the intent doesn't map to any integration.
    """
    handler = _INTENT_TO_HANDLER.get(intent.lower())
    if handler is None:
        return {}

    try:
        return await handler(message)
    except httpx.HTTPError as exc:
        _logger.error("Integration HTTP error for intent=%s: %s", intent, exc)
        return {"error": str(exc)}
    except Exception as exc:
        _logger.exception("Unexpected integration error for intent=%s", intent)
        return {"error": str(exc)}


# ── Individual integration handlers ──────────────────────────

async def create_jira_ticket(message: str) -> dict:
    """Create a bug ticket in JIRA from the user's message."""
    async with httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS) as client:
        resp = await client.post(
            f"{JIRA_BASE_URL}/rest/api/3/issue",
            json={"fields": {"summary": message, "issuetype": {"name": "Bug"}}},
        )
        resp.raise_for_status()
        return {"jira": resp.json()}


async def query_salesforce(message: str) -> dict:
    """Forward a sales-related query to Salesforce."""
    async with httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS) as client:
        resp = await client.post(
            f"{SALESFORCE_BASE_URL}/services/data/v58.0/query",
            json={"q": message},
        )
        resp.raise_for_status()
        return {"salesforce": resp.json()}


async def open_zendesk_ticket(message: str) -> dict:
    """Create a support ticket in Zendesk."""
    async with httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS) as client:
        resp = await client.post(
            f"{ZENDESK_BASE_URL}/api/v2/tickets.json",
            json={"ticket": {"subject": message[:80], "comment": {"body": message}}},
        )
        resp.raise_for_status()
        return {"zendesk": resp.json()}


# Register handlers
_INTENT_TO_HANDLER = {
    "bug": create_jira_ticket,
    "sales": query_salesforce,
    "support": open_zendesk_ticket,
}
