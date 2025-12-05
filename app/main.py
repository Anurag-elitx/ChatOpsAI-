"""
FastAPI application entry point for the ChatOps platform.

Exposes the main /chat endpoint that orchestrates intent classification,
response generation, and external API calls. Also provides a basic
health-check route used by Kubernetes probes.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import APP_NAME, APP_VERSION, APP_ENV, HOST, PORT
from app.agents.workflow import run_agent
from app.celery_worker import process_document_for_rag
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

    # Use the LangChain Agentic Workflow
    try:
        agent_result = run_agent(user_message)
        bot_response = agent_result["output"]
    except Exception as e:
        bot_response = f"Error running agent: {str(e)}"

    # Record metrics for monitoring dashboards
    track_request(user_message, "agentic_chat")

    return {
        "intent": "agentic",
        "response": bot_response,
        "integration_data": {},
    }

@server.post("/api/v1/documents")
async def ingest_document(request: Request):
    """
    Ingest a document into the RAG pipeline.
    """
    body = await request.json()
    document_path = body.get("path")
    if not document_path:
        return JSONResponse(status_code=400, content={"error": "path is required"})
        
    # Trigger background job
    task = process_document_for_rag.delay(document_path)
    return {"status": "processing", "task_id": task.id}



# ── Local dev server ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:server",
        host=HOST,
        port=PORT,
        reload=True,
    )