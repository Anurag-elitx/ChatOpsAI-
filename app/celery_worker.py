import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "chatops_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def process_document_for_rag(document_path: str):
    """
    Background job to process a document, chunk it, and index it into ChromaDB.
    """
    from app.rag.indexing import index_document
    # This is a background task wrapper
    return index_document(document_path)

@celery_app.task
def run_agentic_workflow_bg(user_message: str):
    """
    Background task for long-running agent workflows.
    """
    from app.agents.workflow import run_agent
    return run_agent(user_message)
