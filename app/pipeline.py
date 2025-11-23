"""
NLP processing pipeline.

Chains together intent classification, entity extraction,
semantic retrieval (RAG), and response generation into a
single callable function used by downstream consumers.
"""

from app.models.intent_classifier import classify_intent
from app.models.entity_extractor import extract_entities
from app.models.response_generator import generate_response
from app.models.vector_search import semantic_search
from app.utils.logger import logger


def execute_nlp_pipeline(user_message: str) -> dict:
    """
    Run the full NLP pipeline on a user message.

    Returns a dict containing the detected intent, extracted entities,
    and the generated bot response enriched with RAG context.
    """
    logger.debug(f"Pipeline input: {user_message!r}")

    detected_intent = classify_intent(user_message)
    entities = extract_entities(user_message)
    rag_context = semantic_search(user_message)
    bot_reply = generate_response(user_message, detected_intent, rag_context)

    logger.info(
        f"Pipeline complete — intent={detected_intent}, "
        f"entities={len(entities)} found"
    )

    return {
        "intent": detected_intent,
        "entities": entities,
        "response": bot_reply,
    }
