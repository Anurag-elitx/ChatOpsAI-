"""
FastAPI application entry point for the ChatOps platform.

Exposes the main /chat endpoint that orchestrates intent classification,
response generation, and external API calls. Also provides a basic
health-check route used by Kubernetes probes.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import APP_NAME, APP_VERSION, APP_ENV, HOST, PORT
from app.models.intent_classifier import classify_intent
from app.models.response_generator import generate_response
from app.integrations.external_apis import route_to_integration
from app.monitoring import track_request
from app.utils.logger import logger

# ── FastAPI instance ──────────────────────────────────────────
server = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Enterprise ChatOps platform with RAG-powered responses",
)

logger.info(f"Starting {APP_NAME} v{APP_VERSION} in [{APP_ENV}] mode")


@server.get("/")
async def health_check():
    """Simple liveness probe for K8s / load balancers."""
    return {"status": "healthy", "app": APP_NAME, "version": APP_VERSION}


@server.get("/status")
async def detailed_status():
    """Returns environment and readiness info."""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "ready": True,
    }


@server.post("/chat")
async def chat_endpoint(request: Request):
    """
    Main conversation endpoint.

    Accepts a JSON body with a `message` field, classifies the user's
    intent, generates an LLM-backed response, and optionally forwards
    the request to an enterprise integration (JIRA, Salesforce, etc.).
    """
    body = await request.json()
    user_message: str = body.get("message", "")

    if not user_message.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "message field is required and cannot be empty"},
        )

    # Step 1: figure out what the user wants
    detected_intent = classify_intent(user_message)

    # Step 2: generate a natural-language answer
    bot_response = generate_response(user_message, detected_intent)

    # Step 3: call external tools if the intent warrants it
    integration_result = await route_to_integration(detected_intent, user_message)

    # Step 4: record metrics for monitoring dashboards
    track_request(user_message, detected_intent)

    return {
        "intent": detected_intent,
        "response": bot_response,
        "integration_data": integration_result,
    }


# ── Local dev server ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:server",
        host=HOST,
        port=PORT,
        reload=True,
    )